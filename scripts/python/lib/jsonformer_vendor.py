"""Vendored jsonformer (https://github.com/1rgs/jsonformer, MIT license,
v0.12.0) with the patches this project needs.

STATUS: explored and SET ASIDE 2026-08-23 — see `constrained.py` for the
decision record. Not used by any production notebook. Constrained JSON generation:
the harness emits the structural tokens (braces, brackets, quotes, keys)
itself and the model generates only the values, so output is syntactically
valid JSON by construction — the structural version of the 1.1/1.2 lesson
that a small model keeps syntax but not restraint.

Patches against upstream (each marked PATCH below):
1. `LogitsWarper` was removed from transformers; the number mask is a
   `LogitsProcessor` now.
2. The digit-token mask is built once per tokenizer and cached — upstream
   rebuilt it per instantiation by decoding the whole vocabulary
   (~150k decodes per call at our scale).
3. The mask moves to the logits' device (upstream assumed CPU).
4. `generate_boolean` compares the first sub-token of " true"/" false"
   encodings instead of assuming both are single vocabulary tokens.
5. Generation is explicitly greedy (`do_sample=False`); upstream passed a
   `temperature` that transformers ignores without `do_sample`, warning on
   every call. Greedy also makes the output a pure function of the prompt,
   which is the reproducibility this pipeline wants.
6. The whole generation runs under `torch.no_grad()`. Upstream calls raw
   `model.forward` for booleans and array-continuation, which builds the
   autograd graph over the full prompt — at our 3k-token prompts that
   accumulated ~40 GB of activations and OOMed an A40 on the first call.
7. The digit mask pads to the model's logit dimension, which can exceed
   `len(tokenizer)` (Qwen3.5: 248,320 logits vs 248,077 vocab entries).
9. `generate_number` slices its completion at the token level; upstream
   sliced the decoded string by `len(prompt)` characters, which swallows
   the digits whenever the prompt carries chat-template special tokens
   that `skip_special_tokens` removes from the decode. (An intermediate
   patch 8 restricting the mask to digit-only tokens was reverted: it
   misdiagnosed this bug and would have removed the whitespace tokens
   the number-stopping criterion relies on.)
"""

from typing import Any, Dict, List, Union

import json

import torch
from transformers import (LogitsProcessor, PreTrainedModel,
                          PreTrainedTokenizer, StoppingCriteria)


class StringStoppingCriteria(StoppingCriteria):
    def __init__(self, tokenizer: PreTrainedTokenizer, prompt_length: int):
        self.tokenizer = tokenizer
        self.prompt_length = prompt_length

    def __call__(self, input_ids: torch.LongTensor, _) -> bool:
        if len(input_ids[0]) <= self.prompt_length:
            return False
        last_token = self.tokenizer.decode(input_ids[0][-1],
                                           skip_special_tokens=True)
        return '"' in last_token


class NumberStoppingCriteria(StoppingCriteria):
    def __init__(self, tokenizer: PreTrainedTokenizer, prompt_length: int,
                 precision: int = 3):
        self.tokenizer = tokenizer
        self.precision = precision
        self.prompt_length = prompt_length

    def __call__(self, input_ids: torch.LongTensor,
                 scores: torch.FloatTensor) -> bool:
        decoded = self.tokenizer.decode(input_ids[0][self.prompt_length:],
                                        skip_special_tokens=True)
        if decoded.count(".") > 1:
            return True
        if (decoded.count(".") == 1
                and len(decoded.strip().split(".")[1]) > self.precision):
            return True
        if (len(decoded) > 1 and any(c.isdigit() for c in decoded)
                and decoded[-1] in [" ", "\n"]):
            return True
        return False


class OutputNumbersTokens(LogitsProcessor):          # PATCH 1: LogitsProcessor
    _mask_cache: dict = {}                           # PATCH 2: per-tokenizer

    def __init__(self, tokenizer: PreTrainedTokenizer):
        key = id(tokenizer)
        if key not in self._mask_cache:
            vocab_size = len(tokenizer)
            mask = torch.zeros(vocab_size, dtype=torch.bool)
            for _, token_id in tokenizer.get_vocab().items():
                token_str = tokenizer.decode(token_id).strip()
                # PATCH 11: digit-bearing tokens only. Upstream also
                # allowed pure-whitespace tokens as the number terminator;
                # the manual loop in generate_number terminates on the
                # model's unmasked preference instead, so whitespace
                # inside a number has no role left.
                if (token_str != ""
                        and all(c.isdigit() or c == "." for c in token_str)
                        and token_str.count(".") <= 1):
                    mask[token_id] = True
            self._mask_cache[key] = mask
        self.allowed_mask = self._mask_cache[key]
        self._padded: dict = {}

    def padded_mask(self, model, _ids=None) -> torch.Tensor:
        """The digit mask padded to the model's logit dimension (PATCH 7)
        and moved to its device, cached per dimension."""
        dim = model.get_output_embeddings().weight.shape[0]
        if dim not in self._padded:
            m = self.allowed_mask
            if m.numel() < dim:
                m = torch.cat([m, torch.zeros(dim - m.numel(),
                                              dtype=torch.bool)])
            self._padded[dim] = m.to(model.device)
        return self._padded[dim]

    def __call__(self, _, scores):
        mask = self.allowed_mask.to(scores.device)   # PATCH 3: device
        # PATCH 7: models pad the logit dimension beyond len(tokenizer)
        # (Qwen3.5: 248,320 logits vs 248,077 vocab entries); padded slots
        # are not real tokens and stay disallowed.
        if mask.numel() < scores.shape[-1]:
            pad = torch.zeros(scores.shape[-1] - mask.numel(),
                              dtype=torch.bool, device=scores.device)
            mask = torch.cat([mask, pad])
        scores = scores.masked_fill(~mask[None, :], -float("inf"))
        return scores


class Jsonformer:
    value: Dict[str, Any] = {}

    def __init__(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer,
                 json_schema: Dict[str, Any], prompt: str, *,
                 max_array_length: int = 10, max_number_tokens: int = 6,
                 max_string_token_length: int = 10):
        self.model = model
        self.tokenizer = tokenizer
        self.json_schema = json_schema
        self.prompt = prompt
        self.number_logit_processor = OutputNumbersTokens(tokenizer)
        self.generation_marker = "|GENERATION|"
        self.max_array_length = max_array_length
        self.max_number_tokens = max_number_tokens
        self.max_string_token_length = max_string_token_length

    def generate_number(self, iterations=0):
        # PATCH 11 (replaces the upstream generate()+stopping-criteria
        # design, and PATCH 9's slicing with it): a manual token loop that
        # ends the number when the model's UNMASKED preference is not a
        # digit token. Upstream relied on the model emitting whitespace to
        # stop; under greedy decoding with "," and "]" masked out, the
        # model that wants to end "47" is forced onto a third digit and
        # ids silently corrupt ("478").
        prompt = self.get_prompt()
        ids = self.tokenizer.encode(
            prompt, return_tensors="pt").to(self.model.device)
        mask = self.number_logit_processor.padded_mask(self.model, ids)
        digits: list[int] = []
        for _ in range(self.max_number_tokens):
            logits = self.model(ids).logits[0, -1]
            if digits and not bool(mask[logits.argmax()]):
                break
            masked = logits.masked_fill(~mask, -float("inf"))
            nxt = masked.argmax().view(1, 1)
            digits.append(int(nxt))
            ids = torch.cat([ids, nxt], dim=1)
        response = self.tokenizer.decode(digits,
                                         skip_special_tokens=True)
        response = response.strip().rstrip(".")
        try:
            return float(response)
        except ValueError:
            if iterations > 3:
                raise ValueError("Failed to generate a valid number")
            return self.generate_number(iterations=iterations + 1)

    def generate_boolean(self) -> bool:
        prompt = self.get_prompt()
        input_tensor = self.tokenizer.encode(prompt, return_tensors="pt")
        output = self.model.forward(input_tensor.to(self.model.device))
        logits = output.logits[0, -1]
        # PATCH 4+10: instruct models answer a JSON boolean in several
        # spellings — Qwen3.5 strongly prefers 1/0 (measured: '1' logit
        # 17.0 vs ' true' 14.3 at this position, with ' true' vs ' false'
        # within 0.1 of each other, i.e. noise). Compare the best-scoring
        # candidate on each side instead of one hardcoded token pair.
        def best(spellings):
            ids = {self.tokenizer.encode(s, add_special_tokens=False)[0]
                   for s in spellings
                   if self.tokenizer.encode(s, add_special_tokens=False)}
            return max(logits[i] for i in ids)
        return (best([" true", "true", "1", " 1", " yes"])
                > best([" false", "false", "0", " 0", " no"])).item()

    def generate_string(self) -> str:
        prompt = self.get_prompt() + '"'
        input_tokens = self.tokenizer.encode(
            prompt, return_tensors="pt").to(self.model.device)
        response = self.model.generate(
            input_tokens, max_new_tokens=self.max_string_token_length,
            num_return_sequences=1, do_sample=False,     # PATCH 5: greedy
            stopping_criteria=[
                StringStoppingCriteria(self.tokenizer, len(input_tokens[0]))],
            pad_token_id=self.tokenizer.eos_token_id)
        if (len(response[0]) >= len(input_tokens[0])
                and (response[0][: len(input_tokens[0])] == input_tokens).all()):
            response = response[0][len(input_tokens[0]):]
        if response.shape[0] == 1:
            response = response[0]
        response = self.tokenizer.decode(response, skip_special_tokens=True)
        if response.count('"') < 1:
            return response
        return response.split('"')[0].strip()

    def generate_object(self, properties: Dict[str, Any],
                        obj: Dict[str, Any]) -> Dict[str, Any]:
        for key, schema in properties.items():
            obj[key] = self.generate_value(schema, obj, key)
        return obj

    def generate_value(self, schema: Dict[str, Any],
                       obj: Union[Dict[str, Any], List[Any]],
                       key: Union[str, None] = None) -> Any:
        schema_type = schema["type"]
        if schema_type == "number":
            if key:
                obj[key] = self.generation_marker
            else:
                obj.append(self.generation_marker)
            return self.generate_number()
        elif schema_type == "boolean":
            if key:
                obj[key] = self.generation_marker
            else:
                obj.append(self.generation_marker)
            return self.generate_boolean()
        elif schema_type == "string":
            if key:
                obj[key] = self.generation_marker
            else:
                obj.append(self.generation_marker)
            return self.generate_string()
        elif schema_type == "array":
            new_array = []
            obj[key] = new_array
            return self.generate_array(schema["items"], new_array)
        elif schema_type == "object":
            new_obj = {}
            if key:
                obj[key] = new_obj
            else:
                obj.append(new_obj)
            return self.generate_object(schema["properties"], new_obj)
        else:
            raise ValueError(f"Unsupported schema type: {schema_type}")

    def generate_array(self, item_schema: Dict[str, Any],
                       obj: Dict[str, Any]) -> list:
        # NOTE (upstream behavior, kept): at least one element is always
        # generated — callers gate arrays behind a boolean when a schema
        # may legitimately be empty.
        for _ in range(self.max_array_length):
            element = self.generate_value(item_schema, obj)
            obj[-1] = element
            obj.append(self.generation_marker)
            input_prompt = self.get_prompt()
            obj.pop()
            input_tensor = self.tokenizer.encode(input_prompt,
                                                 return_tensors="pt")
            output = self.model.forward(input_tensor.to(self.model.device))
            logits = output.logits[0, -1]

            top_indices = logits.topk(30).indices
            sorted_token_ids = top_indices[
                logits[top_indices].argsort(descending=True)]
            found_comma = False
            found_close_bracket = False
            for token_id in sorted_token_ids:
                decoded_token = self.tokenizer.decode(token_id)
                if "," in decoded_token:
                    found_comma = True
                    break
                if "]" in decoded_token:
                    found_close_bracket = True
                    break
            if found_close_bracket or not found_comma:
                break
        return obj

    def get_prompt(self):
        template = ("{prompt}\nOutput result in the following JSON schema "
                    "format:\n{schema}\nResult: {progress}")
        progress = json.dumps(self.value)
        gen_marker_index = progress.find(f'"{self.generation_marker}"')
        if gen_marker_index != -1:
            progress = progress[:gen_marker_index]
        else:
            raise ValueError("Failed to find generation marker")
        return template.format(prompt=self.prompt,
                               schema=json.dumps(self.json_schema),
                               progress=progress)

    @torch.no_grad()                                 # PATCH 6: no autograd
    def __call__(self) -> Dict[str, Any]:
        self.value = {}
        return self.generate_object(self.json_schema["properties"],
                                    self.value)

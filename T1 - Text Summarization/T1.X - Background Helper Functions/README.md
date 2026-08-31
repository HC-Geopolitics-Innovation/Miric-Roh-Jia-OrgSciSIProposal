# Background Helper Functions for Text Summarization

This folder contains the core Python helper modules supporting the text chunking and map-reduce summarization tasks.

---

## Included Modules

- **[`chunking.py`](chunking.py)**:
  - **Purpose**: Implements turn-aware token chunking.
  - **Logic**: Groups whole speaking turns (uninterrupted participant contributions) into token-budgeted chunks. Prevents splitting speaker turns across window boundaries so that LLM map calls do not lose speaker context or attribution.

- **[`summarize.py`](summarize.py)**:
  - **Purpose**: Implements the 3-prompt Map-Reduce orchestration architecture.
  - **Logic**: Contains the prompt templates and LLM execution logic for:
    1. **Map Stage**: Summarizes individual turn-aware transcript chunks, extracting speaker-attributed statements.
    2. **Collapse Stage**: Condenses intermediate segment summaries if they exceed context window budgets.
    3. **Reduce Stage**: Synthesizes all segment summaries into a single, cohesive hearing summary.

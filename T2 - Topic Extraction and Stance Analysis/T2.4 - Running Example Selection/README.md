# Choosing the running-example topic for Section 6

Section 6 fixes one topic $k$ and uses legislators' direction on it in year $t$, $S_{kt}$, as the slope on firm exposure. The topic needs enough records, both support and concern, and a shift over time that a reader can name. This memo documents the two-step selection and puts the best cases up for decision. Everything is computed from the saved Stage-3 stance records (29,971 records on codebook v1.0, hearings held 1999–2025); no model was rerun.

## 1. Selection process and best cases for review

![Selection flowchart](output/T2.4.3%20-%20Summary%20Figures/fig_flowchart.png)

Step 1 is numeric and covers the 30 largest topics. Step 2 reads every record of the candidates that survive. The two steps answer different questions: Step 1 asks whether the model's support and concern labels move over time; Step 2 asks whether that movement is a change of *position* or only a change of *subject*.

**Best cases.** Net stance is (support − concern) / records from the model's labels. Net direction is (records favoring more − records favoring less) / records with a direction, from the Step 2 audit.

| Topic | Records | Step 1: net stance by administration | Step 2: net direction by administration | What moves | Fit for $S_{kt}$ |
|---|---:|---|---|---|---|
| 78 EPA air and water regulations | 560 | Bush −0.05, Obama −0.44, Trump −0.42, Biden +0.11 | Bush +0.73, **Obama −0.31**, Trump +0.63, Biden +0.08 | Direction reverses twice, with House control | **Best direction example**; widest firm relevance |
| 26 Renewable energy and storage | 571 | Bush +0.54, Obama +0.35, Trump +0.29, Biden −0.05 | Bush +0.98, Obama +0.55, Trump +0.78, **Biden +0.07** | Direction falls from unanimity to parity | Second direction example; 19% off-topic records |
| 68 Consumer data privacy legislation | 374 | −0.02 before 2018, +0.40 after | Clinton +0.95, Bush +0.84, Obama +0.63, Trump +0.80, Biden +0.84 | Angle only: harm-talk before 2018, federal-law-talk after | Angle example; continuity with the T3 worked example |
| 21 Nuclear energy R&D | 537 | +0.10 before 2017, +0.46 after | Bush +0.58, Obama +0.73, Trump +0.83, Biden +0.98 | Angle only: waste, then advanced reactors, then fusion | Angle example; few exposed firms |

**Recommendation.** If $S_{kt}$ is a policy direction, as Section 6 reads it, topic 78 is the choice: it is the only topic where legislators' direction changes sign, its two directions are equally common (237 records favoring more regulation, 236 favoring less), and any firm with emissions or discharge compliance is exposed. Topic 26 is the alternative with the same property and a cleaner story (unanimous under Bush, contested from 2011, at parity under Biden), but one record in five is off-topic. Topics 68 and 21 are consensus topics in these committees: legislators favor stronger privacy protection and more nuclear energy in every administration, and what the Step 1 shift picked up is a change in which aspect they talk about. They work only if $S_{kt}$ is redefined as attention to an angle, for example the share of privacy records that call for a federal law.

**Decision needed.** Which topic, and whether $S_{kt}$ measures direction (78 or 26) or attention to an angle (68 or 21).

## 2. Step 1: screening the 30 largest topics

### Criteria

| Criterion | Measure | Rule |
|---|---|---|
| 1. Volume | Records placed on the topic, hearings held 1999–2025 | Among the 30 largest topics (374 or more records), with at least three administrations of 30 or more records |
| 2. Balance | Support share = support / (support + concern) | Between 0.30 and 0.70 |
| 3. Clean shift | Net stance by administration (calendar-year blocks: Bush 2001–08, Obama 2009–16, Trump 2017–20, Biden 2021–24, Trump 2025) | Administrations differ (chi-square p < 0.01) and their net stances span at least 0.40 |
| Reading check | 40 sampled source sentences per passing topic, 10 support and 10 concern on each side of the best break year | One coherent subject; the shift is a change of position, not of subject; "concern" has a readable polarity |

Firm relevance was recorded as a fourth consideration but not used to rank: the number of S&P 500 firms with at least one 10-K whose text is close to the topic (the T3 similarity proxy). It flags topics with almost no firm text rather than ranking the rest.

### Results

![Volume and balance of the 30 largest topics](output/T2.4.1%20-%20Step%201%20-%20Topic%20Screening/fig_select_volume_balance.png)

Criteria 1 and 2 cut almost nothing: every top-30 topic has at least 374 records and at least 21 years with 5 or more records, and 28 of 30 sit inside the balance band (federal budget requests and online advertising are at 0.29). Criterion 3 is the binding one. Thirteen topics pass all three rules; the reading check then sorts them.

| ID | Topic | Records | Support share | Admin. range | Break year, Δ net | Firms | Reading verdict |
|---:|---|---:|---:|---:|---|---:|---|
| 78 | EPA air and water regulations | 560 | 0.32 | 0.55 | 2010, −0.34 | 498 | Coherent; concern from 2011 is House Republicans against EPA rules. **To Step 2** |
| 26 | Renewable energy technologies and storage | 571 | 0.68 | 0.59 | 2022, −0.53 | 291 | Coherent; the 2022 drop mixes subsidy critics with offshore-wind defenders. **To Step 2** |
| 68 | Consumer data privacy legislation | 374 | 0.59 | 0.44 | 2018, +0.42 | 285 | Coherent; bipartisan surge after Cambridge Analytica. **To Step 2** |
| 21 | Nuclear energy research and development | 537 | 0.63 | 0.43 | 2017, +0.36 | 66 | Coherent; post-2017 concern is pro-nuclear worry about cuts. **To Step 2** |
| 14 | Space debris and traffic management | 463 | 0.55 | 0.65 | 2017, +0.50 | 18 | Catch-all for human spaceflight; no firm relevance |
| 43 | Maritime security and port safety | 452 | 0.52 | 0.65 | 2018, +0.55 | 26 | Shift is a change of subject (port security to shipbuilding) |
| 44 | Fisheries management and conservation | 490 | 0.48 | 0.73 | 2017, +0.47 | 43 | Interpretable; no firm relevance |
| 147 | Next Generation Air Transportation System | 428 | 0.42 | 0.85 | 2020, +0.55 | 65 | Heterogeneous; sign of concern unclear |
| 121 | K-12 STEM education and workforce development | 421 | 0.62 | 0.71 | 2020, +0.50 | 8 | Only 9 concern records after 2020; no firm relevance |
| 13 | Space Shuttle retirement and NASA programs | 458 | 0.36 | 0.49 | 2014, +0.47 | 6 | NASA budgets; no firm relevance |
| 116 | Science competitiveness legislation | 599 | 0.69 | 0.42 | 2022, −0.27 | 501 | Support-heavy; break rests on 58 records |
| 54 | FCC telecommunications regulation authority | 663 | 0.52 | 0.78 | 2021, +0.22 | 352 | Support side is unrelated bills placed by the phrase "legislation" |
| 86 | Passenger fees and charges | 385 | 0.34 | 0.83 | 2012, +0.42 | 516 | Not one topic (E-rate, spectrum fees, fines, taxes) |

Four topics went to Step 2. A fifth, topic 65 consumer privacy and anti-spam legislation, was audited as well because it is the sibling of topic 68 and might have been merged with it; it turned out to be a catch-all (two thirds of its records are off-topic) and was dropped.

### Results for the best cases

![Step 1 net stance for the four finalists](output/T2.4.3%20-%20Summary%20Figures/fig_step1_finalists.png)

All four show administration means that differ by 0.4 or more, with yearly values that stay near their administration's mean. EPA regulations and renewable energy move with changes of House control and administration; privacy and nuclear energy each move once, at 2018 and 2017, and stay there under both parties.

## 3. Step 2: auditing every record of the candidates

### Criteria

Every record of the five candidate topics (2,589 records) was read against its cited sentences and given three codes. The coder was the assistant (Claude), in a single pass on 2026-10-22; no human has reviewed the codes yet.

| Code | Values | Question it answers |
|---|---|---|
| Verdict | ok, inverted, no stance, off-topic | Is the model's support or concern label right for this sentence, and is the record about this topic at all? |
| Angle | 7 to 9 aspects per topic (for EPA: a specific rule, overreach, science, the agency, health, state roles, liability) | Which aspect of the topic the sentence addresses, so that records can be aggregated by perspective |
| Direction | pro, anti, none | Does the speaker favor more or less of the policy object (stronger environmental regulation, more renewable support, stronger privacy protection, more nuclear energy)? This resolves the polarity of "concern": concern about a harm favors rules, concern about a rule opposes them |

A topic is a usable direction example when all three hold:

1. **Labels are accurate.** Agreement between the model's label and the verdict is at least 95% among records that carry a stance.
2. **Placement is clean.** At most about 20% of records are off-topic.
3. **Direction moves.** Administration means of net direction span at least 0.40 and at least one administration is near balance (below +0.30). A series that stays between +0.6 and +1.0 has no usable variation.

### Results

| Topic | Records | Label agreement | Off-topic | Favor more | Favor less | Net direction by administration (Bush, Obama, Trump, Biden) | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| 78 EPA regulations | 560 | 98.2% | 9% | 237 | 236 | +0.73, −0.31, +0.63, +0.08 | Direction example |
| 26 Renewable energy | 571 | 99.1% | 19% | 338 | 56 | +0.98, +0.55, +0.78, +0.07 | Direction example |
| 68 Consumer data privacy | 374 | 96.4% | 6% | 298 | 34 | +0.84, +0.63, +0.80, +0.84 | Angle example only |
| 21 Nuclear energy R&D | 537 | 99.3% | 12% | 375 | 48 | +0.58, +0.73, +0.83, +0.98 | Angle example only |
| 65 Privacy and anti-spam | 547 | 99.5% | 65% | 180 | 3 | all above +0.9 | Dropped: catch-all |

The model's labels are right 96 to 99 percent of the time, and the rare inversions are a speaker quoting or rebutting an opponent. Off-topic placement is the larger error: generic issue phrases ("energy efficiency", "legislation", "security") clear the placement threshold for several topics. Neither problem decides the choice. The direction test does: only EPA regulations and renewable energy have a direction series that moves.

### Results for the best cases

![Step 2 net direction for the four finalists](output/T2.4.3%20-%20Summary%20Figures/fig_step2_finalists.png)

- **78 EPA regulations.** Pro-regulation through the Bush years. From 2011 to 2016 the Republican House Science Committee's oversight hearings produce the anti-regulation wave (angles: overreach, science, state roles). From 2017 to 2021 the same committee's Democrats defend the agency against rollbacks; the model files these defenses as *concern* about cuts and repeals, which is why the Step 1 line stays negative while direction turns positive. After 2021 the topic is thin (under 20 records a year).
- **26 Renewable energy.** The Bush years are the hydrogen and fuel-cell era, 179 records favoring expansion against 2. Opposition begins in 2011 with Solyndra and "picking winners and losers", and reaches parity under Biden over grid reliability, EV mandates, subsidies and siting. Under Trump the pro records are mostly Democrats defending the efficiency and renewables office against budget cuts, again filed as concern by the model.
- **68 Consumer data privacy.** Legislators favor stronger protection in every administration (34 anti records in 27 years). Before 2018 the records describe harms; from 2018 on they are support for a federal privacy law from both parties. The Step 1 break at 2018 is a change from harm-talk to law-talk, not a change of lean.
- **21 Nuclear energy R&D.** Near-consensus for expansion (375 against 48). Attention moves from Yucca Mountain, cost and budget cuts under Bush and Obama to the advanced-reactor bills of 2017–2018 and fusion after 2021. Direction barely varies.

**Why the EPA direction runs against the president's party.** The series measures what legislators say in hearings, not what the administration does. Within every administration the direction is partisan: Democrats favor more regulation, Republicans less. What changes across administrations is who speaks and how much. Under Bush the few EPA records are Senate Democrats criticizing a Republican EPA; from 2011 the Republican House majority used the Science Committee for repeated EPA oversight hearings; under Trump the same committee's Democrats defended the agency. The direction series is therefore the congressional pushback against whoever runs the EPA, amplified by which party sets the hearing agenda. That is the right regressor if $S_{kt}$ is the legislative climate a firm faces; if it is meant as the direction policy is moving, its sign is inverted relative to the executive. Renewable energy shows the same structure in milder form.

| Administration | Democrats: more / less regulation | Republicans: more / less regulation |
|---|---:|---:|
| Bush | 28 / 2 | 9 / 4 |
| Obama | 86 / 3 | 19 / 197 |
| Trump (2017–2020) | 74 / 0 | 2 / 17 |
| Biden | 9 / 0 | 2 / 9 |

Records with a direction; party from the hearing membership table (missing for 10 of 560 records). Full table for the four finalists: `output/T2.4.3 - Summary Figures/direction_by_party.csv`.

## Caveats

- One coder, one pass, no adjudication. A human spot-check of a stratified sample and of the 29 inverted records would turn the audit into validation.
- Direction is defined per topic as favoring the policy object, so its sign means "more regulation" for EPA and privacy but "more deployment" for nuclear and renewables; the regression sign is interpreted per topic.
- Yearly cells are small (typically 10 to 25 records), so $S_{kt}$ at the year level is noisy. Administration or Congress blocks, or a minimum-record rule, should be considered for the regression.
- Removing off-topic records and reviewing the lowest-similarity placements would do more for the series than relabeling stances.

## Files

| Path | Contents |
|---|---|
| [T2.4.1 - Step 1 - Topic Screening.py](<T2.4.1 - Step 1 - Topic Screening.py>) | Screens the 30 largest topics; writes the metrics table, figures, and sampled sentences |
| [output/T2.4.1 - Step 1 - Topic Screening/](<output/T2.4.1 - Step 1 - Topic Screening/>) | Full 30-topic table, all Step 1 figures, sentence samples, and the [detailed Step 1 notes](<output/T2.4.1 - Step 1 - Topic Screening/README.md>) |
| [T2.4.2 - Step 2 - Stance Audit and Angle Coding.py](<T2.4.2 - Step 2 - Stance Audit and Angle Coding.py>) | Exports records for reading, joins the hand codes back, writes angle and direction tables and figures |
| [output/T2.4.2 - Step 2 - Stance Audit and Angle Coding/](<output/T2.4.2 - Step 2 - Stance Audit and Angle Coding/>) | Hand codes (`audit/codes_topic_<id>.csv`), per-year angle and direction tables, per-topic figures, and the [detailed Step 2 notes](<output/T2.4.2 - Step 2 - Stance Audit and Angle Coding/README.md>) with every angle table |
| [T2.4.3 - Summary Figures.py](<T2.4.3 - Summary Figures.py>) | The flowchart, the two finalist figures, and the direction-by-party table in this memo, from the Step 1 and Step 2 outputs |

Reproduce, from this folder:

```bash
PY=/project2/njia_1089/acroh/envs/llm_method/bin/python
$PY "T2.4.1 - Step 1 - Topic Screening.py" --data-root /project2/mmiric_1435/acroh/llm_method/data
$PY "T2.4.2 - Step 2 - Stance Audit and Angle Coding.py" aggregate --topics 68 78 21 26 65
$PY "T2.4.3 - Summary Figures.py" --data-root /project2/mmiric_1435/acroh/llm_method/data
```

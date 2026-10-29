**Table 2—Poisson Difference-in-Differences Estimates of Yearly Patent Counts on Topic Relevance × Post-2018**

| | (1) | (2) | (3) | (4) |
|:---|:---:|:---:|:---:|:---:|
| Dependent variable | Privacy patents | Privacy patents | All patents | All patents |
| Topic relevance × Post-2018 | −0.134 | −0.095 | −0.124 | −0.001 |
|  | (0.102) | (0.067) | (0.077) | (0.052) |
| Topic relevance (standard deviations) | 0.523*** |  | 0.211* |  |
|  | (0.183) |  | (0.123) |  |
| Log firm age, t − 1 | 0.256 | 0.048 | 0.292* | −0.035 |
|  | (0.320) | (0.181) | (0.172) | (0.073) |
| Log total assets, t − 1 | 0.376*** | 0.180 | 0.250*** | 0.193** |
|  | (0.093) | (0.114) | (0.061) | (0.085) |
| Log of one plus R&D expense, t − 1 | 0.514*** | 0.045 | 0.573*** | 0.226*** |
|  | (0.132) | (0.105) | (0.089) | (0.077) |
| R&D expense missing, t − 1 | 1.844** | −0.346 | 1.763*** | 1.027*** |
|  | (0.874) | (0.586) | (0.538) | (0.374) |
| Lagged controls | Yes | Yes | Yes | Yes |
| Firm fixed effects | No | Yes | No | Yes |
| NAICS two-digit-by-year fixed effects | Yes | Yes | Yes | Yes |
| Observations | 9,310 | 4,466 | 11,276 | 11,129 |
| Mean of dependent variable | 3.455 | 7.199 | 102.309 | 103.658 |
| Pseudo R² | 0.71 | 0.88 | 0.74 | 0.95 |
| Number of clusters (firms) | 652 | 258 | 683 | 655 |

*Notes*: The unit of observation is a firm-year: the T4.1.3 analysis sample (firms of the all-years T3 sample with at least one patent filed in 1999 to 2017), fiscal years 1999 to 2021 with a 10-K and the lagged controls observed. The dependent variable is the number of KPSS patents filed in the year that carry at least one CPC code of the project's privacy code list (T4.1.2) in columns 1 and 2, and all KPSS patents filed in the year in columns 3 and 4. Each column is a Poisson pseudo-maximum-likelihood regression (ppmlhdfe) with NAICS two-digit-by-year fixed effects absorbed, and firm fixed effects in columns 2 and 4; units whose count is zero throughout drop out. Topic relevance is the firm's score, the cosine similarity between a firm-level summary of its 10-K Item 1 sections and the policy summary of legislator statements on consumer data privacy legislation, one score per firm, standardized over the regression firm-years. Post-2018 equals one in fiscal years 2018 to 2021, after the Facebook–Cambridge Analytica revelations of March 2018; its main effect is absorbed by the NAICS-by-year fixed effects, and the score's main effect by the firm fixed effects where present. The interaction is the post-minus-pre change in the log expected count per standard deviation of relevance relative to less relevant firms in the same NAICS code and year. Controls are measured at fiscal year t − 1: firm age is years since the first CRSP listing; R&D means research and development, entered as the log of one plus the expense with missing R&D set to zero and flagged. Standard errors clustered by firm are in parentheses; * p < 0.10, ** p < 0.05, *** p < 0.01. Pseudo R² is the one ppmlhdfe reports.

*Source*: KPSS extended patent data (Kogan, Papanikolaou, Seru, and Stoffman, 2017, updated to 2025) with CPC codes; the privacy CPC code list in privacy_cpc/privacy_cpc_codes.xlsx; SEC EDGAR 10-K filings; congressional hearing statements from GovInfo; Compustat; CRSP-Compustat link; authors' calculations.

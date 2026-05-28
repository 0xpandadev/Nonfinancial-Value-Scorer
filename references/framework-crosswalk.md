# Framework Crosswalk

This crosswalk maps scoring tags to source frameworks. Use it to explain why each item belongs in the dashboard.

## Core Mapping

| Tag ID | Dashboard Label | METI Value Co-Creation | IFRS Integrated Reporting | SSBJ / ISSB | JPX / FSA / Other |
|---|---|---|---|---|---|
| VCS | Value Creation Story | Value creation story, values, long-term strategy, execution strategy, KPI, governance, dialogue | Value creation, preservation, erosion; strategy, governance, performance, prospects | Strategy; connected information | JPX growth path and investor explanation |
| MAT | Materiality / Key Issues | Important issues and value positioning | Material matters affecting value creation | Material sustainability-related risks and opportunities | FSA sustainability disclosure context |
| BMO | Business Model | Business model and value provision | Business model content element | Effects on business model and value chain | JPX business strategy / portfolio explanation |
| SIX | Six Capitals | Common language with related frameworks | Financial, manufactured, intellectual, human, social and relationship, natural capital | Value chain and business model inputs/outcomes | Human capital, IP, natural capital policy sources |
| STR | Strategy / Resource Allocation | Long-term strategy, execution strategy, implementation plan | Strategy and resource allocation | Strategy and decision-making effects | JPX capital allocation and growth investment |
| KPI | KPI / Outcomes | Results and key performance indicators | Performance and outcomes | Metrics and targets | Human capital indicators, climate metrics, IP causal-path indicators |
| GOV | Governance | Governance and dialogue | Governance structure supports value creation | Governance processes, controls, procedures | JPX board oversight, CG Code |
| DIA | Investor Dialogue | Practical and constructive dialogue / engagement | Stakeholder relationships | Investor-useful disclosure | Active fund manager declaration, JPX investor voice |
| QLT | Disclosure Quality | Common language, integrated organization | Conciseness, reliability, completeness, consistency, comparability | Qualitative characteristics, comparability | Usability for investors and peer comparison |
| RSK | Risks / Opportunities | SX risks and opportunities from social sustainability issues | Risks and opportunities | Sustainability-related risks and opportunities | TNFD, climate, human rights, economic security |

## Global Framework Mapping

| Tag ID | ISSB / SASB | GRI | ESRS | Topic Frameworks |
|---|---|---|---|---|
| VCS | ISSB strategy and connected financial effects | Supports impact-to-strategy context | Strategy and business model effects | IFRS Integrated Reporting is primary |
| MAT | Investor-focused material risks/opportunities; SASB industry topics | Impact materiality and stakeholder impacts | Double materiality | OECD/UNGP for salient human-rights risks |
| BMO | Business model and value-chain effects | Organizational context and impacts | Business model and value chain | IFRS Integrated Reporting is primary |
| SIX | Human/social/natural/intellectual capital via relevant disclosures | Strong impact evidence across people/environment | Social/environment topical standards | TNFD for natural capital; UNGP/OECD for human/social capital |
| STR | Strategy and decision-making effects | Management approach when linked to strategy | Strategy, policies, actions | SBTi for climate transition target credibility |
| KPI | Metrics and targets; SASB industry metrics | Topic-specific metrics | ESRS datapoints and targets | GHG Protocol, CDP, SBTi, TNFD |
| GOV | Governance processes, controls, oversight | Governance and management approach | Governance disclosures | OECD governance/RBC, UNGP accountability |
| RSK | Sustainability-related risks and opportunities | Actual/potential negative impacts | Impacts, risks, opportunities | TNFD, GHG Protocol, OECD, UNGP |
| QLT | Comparability, consistency, material information | Completeness and balance | Structured mandatory disclosure | CDP scoring, GHG methodology, assurance evidence |

## Interpretation Rules

- **METI gives the Japanese operating vocabulary**: value creation story, common language, SX, dialogue, long-term strategy, KPI.
- **IFRS Integrated Reporting gives the report architecture**: content elements, six capitals, connectivity, materiality, value creation/preservation/erosion.
- **SSBJ/ISSB gives the sustainability disclosure architecture**: governance, strategy, risk management, metrics and targets, materiality, value chain.
- **JPX gives market implementation pressure**: growth path, capital allocation, intangible assets, board-level oversight, investor explanation.
- **FSA gives mandatory-disclosure context**: sustainability information and diversity/human-capital disclosure in securities reports.

## Tag Definition Requirements

Every UI tag must include:

```yaml
tag_id:
label:
definition:
why_it_matters:
primary_frameworks:
supporting_frameworks:
scoring_question:
evidence_needed:
score_scale_ref:
weight:
ui_tooltip:
```

## Common Confusions

- "Value creation story" is explicit in METI's guidance language. IFRS Integrated Reporting supplies the underlying international structure for explaining value creation over time.
- "Materiality" differs by framework. For this skill, score whether the report explains matters that affect the company's ability to create value and/or could affect investor decisions.
- "Non-financial score" does not mean "non-economic." Many non-financial disclosures matter because they affect future cash flow, cost of capital, finance access, risk, trust, or strategic optionality.
- Do not require a company to name every framework. Score substance first, framework naming second.

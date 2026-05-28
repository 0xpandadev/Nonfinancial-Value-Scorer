---
name: nonfinancial-value-scorer
description: Score and visualize corporate non-financial value disclosures from integrated reports, sustainability reports, annual reports, and value-enhancement materials. Use when analyzing company non-financial value creation, corporate value improvement narratives, METI value co-creation guidance, IFRS integrated reporting, SSBJ/ISSB, human capital, intangible assets, TNFD, or when building evidence-linked scoring dashboards and peer comparisons from uploaded PDFs.
---

# Nonfinancial Value Scorer

## Purpose

Turn integrated reports, sustainability reports, annual reports, securities-report narrative sections, and related IR materials into an evidence-linked scoring board for non-financial value creation and corporate value-enhancement narratives.

The skill evaluates disclosure quality and strategic plausibility, not intrinsic corporate value. Always call the output a **non-financial value-creation disclosure score** unless the user explicitly defines a valuation model.

## Core Rule

Every score must be explainable from:

1. A named scoring tag.
2. A definition.
3. A source framework.
4. Evidence from the uploaded report, including page or section when available.
5. A score rule explaining why that number was assigned.
6. A confidence level.

Never output only a score. Scores without evidence are not usable.

## Reference Loading

Load only the files needed for the current task:

- For source hierarchy and official URLs: `references/source-register.md`
- For ticker/company lookup and report acquisition: `references/report-acquisition.md`
- For global non-Japanese standards and framework selection: `references/global-frameworks.md`
- For automatic framework selection by ticker, market, country, and report type: `references/framework-selection.md`
- For framework-to-score mapping: `references/framework-crosswalk.md`
- For scoring definitions and 100-point weights: `references/scoring-rubric.md`
- For consistency controls, calibration, and review checks: `references/calibration-protocol.md`
- For evidence objects and UI definition tags: `references/evidence-schema.md`
- For HTML dashboard and comparison UX: `references/dashboard-spec.md`
- For industry-specific KPI ideas: `references/industry-kpi-notes.md`

If the user asks to add new upstream documents, update `source-register.md` and the relevant crosswalk/rubric file. Do not dump full PDFs into the skill; distill them into definitions, tags, scoring rules, and source references.

## Workflow

1. **Resolve scope**
   - Identify report type: integrated report, sustainability report, annual securities report, IR deck, or mixed pack.
   - Identify companies, fiscal years, industry, and comparison set.
   - State whether the result is single-company scoring, peer comparison, or dashboard build.

2. **Acquire reports when needed**
   - If the user supplies files, use those files as the primary report pack.
   - If the user supplies a ticker, securities code, EDINET code, or company name plus years/report types, use `references/report-acquisition.md`.
   - Prefer official company IR/sustainability pages, exchange/regulator filings, and EDINET/FSA/JPX sources over third-party mirrors.
   - Save acquisition metadata: company, identifier, report type, fiscal year, title, URL, publisher, retrieval date, and confidence.
   - If multiple plausible PDFs exist, choose the official issuer/regulator source and record the reason. Ask only if ambiguity would change the score materially.

3. **Select scoring framework set**
   - Use `references/framework-selection.md` after company identification and before scoring.
   - Infer the framework set from country, listing market, report source, regulation, report language, and report type.
   - For Japanese listed companies, default to Japan core plus global cross-checks.
   - For US/global companies, default to IFRS Integrated Reporting, ISSB/SASB, GRI, and topic frameworks as relevant.
   - For EU companies or CSRD-style sustainability statements, include ESRS.
   - Record the selected framework set and reason in audit metadata.
   - Ask the user only if the ticker/company is ambiguous or if multiple regulatory regimes would materially change scoring.

4. **Extract evidence**
   - Parse text, tables, and page numbers from the provided PDF or document.
   - Preserve short excerpts only; do not over-quote.
   - Capture section titles, page numbers, evidence type, and confidence.
   - If OCR or page extraction is weak, label confidence as low and ask for a better source only if the task cannot proceed.

5. **Classify evidence**
   - Map excerpts to scoring tags from `scoring-rubric.md`.
   - Use `framework-crosswalk.md` and `global-frameworks.md` to connect each tag to METI, IFRS Integrated Reporting, ISSB/SASB, GRI, ESRS, SSBJ, JPX, FSA, human capital, intangible asset, GHG Protocol, CDP, SBTi, OECD/UNGP, or TNFD sources.
   - A single excerpt can support multiple tags, but avoid double-counting the same disclosure as separate substance.

6. **Score**
   - Use the 0-10 tag scale and 100-point weighted score from `scoring-rubric.md`.
   - Apply `references/calibration-protocol.md` before finalizing scores.
   - Use 0 when there is no relevant evidence.
   - Use 1-3 for generic claims, 4-6 for structured but incomplete disclosure, 7-8 for evidence-linked and strategically connected disclosure, and 9-10 for quantified, time-series, governed, comparable disclosure with clear tradeoffs or negative information.
   - Apply confidence haircuts when evidence is weak, stale, or not company-specific.
   - Record any score cap, override, or uncertainty as an audit note.

7. **Explain**
   - For each score, output: tag, score, definition, framework basis, evidence, reasoning, missing evidence, and confidence.
   - Include clear downgrade reasons.
   - Separate score facts from analyst inference.

8. **Compare**
   - For peer sets, normalize by industry and report year.
   - Lock the same rubric version, source set, fiscal-year policy, and evidence rules for every company in the run.
   - Compare both total score and tag-level score.
   - Show where one company has stronger disclosure substance, not just longer disclosure.

9. **Visualize**
   - Build or specify an HTML dashboard using `dashboard-spec.md`.
   - Recommended panels: summary score, scoring criteria and item definitions, radar chart, company x tag heatmap, evidence drawer, source definition drawer, peer gap view, CSV/JSON export.
   - Use `scripts/build_dashboard.py` when a structured scoring JSON exists.
   - For Japanese output, set `dashboard_locale: "ja"` on each company result or `scoring_audit.locale: "ja"`. Add localized fields such as `label_ja`, `definition_ja`, `reason_ja`, `missing_evidence_ja`, `section_ja`, `excerpt_ja`, `top_strengths_ja`, `top_gaps_ja`, and `comparability_warnings_ja`. The HTML board must keep source URLs clickable and show Japanese tag-click details.

## Output Standards

For a short answer, include:

- Overall score and confidence.
- Top 3 strengths.
- Top 3 gaps.
- Evidence-linked score table.
- How to improve the report.

For a dashboard or board, include:

- `scoring.json` with source-backed score objects.
- HTML dashboard, preferably self-contained.
- A visible scoring criteria panel containing every tag definition and the 1-10 scoring scale.
- Calibration/audit metadata showing rubric version, scorer, review status, and consistency warnings.
- Report acquisition metadata showing where each report came from and why it was included.
- A note that scores evaluate report evidence and disclosure quality, not investment merit.

## Guardrails

- Do not claim a company is objectively more valuable because it scores higher.
- Do not reward volume. Reward specificity, strategic connection, quantification, consistency, governance, and evidence.
- Do not punish a company for not using a specific framework name if the substance is present.
- Do not treat glossy diagrams as substance unless the diagram is supported by goals, KPIs, governance, or outcomes.
- Do not mix different fiscal years in peer comparison without a warning.
- Do not silently use unofficial report mirrors when official issuer, EDINET, FSA, or exchange sources are available.
- When uncertain, lower confidence instead of inventing precision.

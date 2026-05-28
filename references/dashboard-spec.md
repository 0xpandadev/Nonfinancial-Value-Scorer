# Dashboard Spec

Default output is a portable, self-contained HTML file when the user asks for visualization.

## Required Views

1. **Executive Summary**
   - Overall score.
   - Confidence.
   - Industry and fiscal year.
   - Top strengths and gaps.

2. **Scoring Criteria / Item Definitions**
   - Each scoring tag: VCS, MAT, BMO, SIX, STR, KPI, GOV, RSK, QLT.
   - Tag definition in the dashboard language.
   - Weight used in the 100-point score.
   - The generic 1-10 scoring scale, so a user can see why a score is 7 rather than 8 or 9.

3. **Radar Chart**
   - VCS, MAT, BMO, SIX, STR, KPI, GOV, RSK, QLT.
   - If multiple companies are present, allow overlay or company selector.

4. **Peer Heatmap**
   - Rows: companies.
   - Columns: scoring tags.
   - Cell: 0-10 score and confidence marker.

5. **Evidence Drawer**
   - Opens from any score.
   - Shows definition, source basis, scoring rule, evidence excerpts, pages, downgrade reasons.

6. **Gap Analysis**
   - Missing evidence by tag.
   - High-impact improvements.
   - Peer comparison gaps.

7. **Source Definition Panel**
   - Lists each framework used.
   - Shows source role: definition, implementation, investor practice, or example.
   - Shows clickable URL links to primary frameworks and company report sources.

8. **Calibration / Audit Panel**
   - Rubric version.
   - Source pack version.
   - Auto-selected framework set and reason.
   - Acquired report pack.
   - Report boundary policy.
   - Calibration status.
   - Reviewer / second-pass status.
   - Score caps and comparability warnings.

## UI Rules

- Never show a score without an evidence button.
- Show framework badges such as `METI`, `IFRS IR`, `SSBJ`, `JPX`, `FSA`, `TNFD`.
- For global companies, also show badges such as `ISSB`, `SASB`, `GRI`, `ESRS`, `GHG Protocol`, `CDP`, `SBTi`, `OECD`, and `UNGP`.
- Use neutral colors for confidence and score; avoid making low scores look like moral failure.
- Label the dashboard: "Disclosure and value-creation evidence score, not investment advice."
- Make comparison year and report type visible.
- Put definitions in tooltips or drawers so the main UI stays readable.
- Show calibration metadata so users know whether multiple companies were scored under the same rule set.
- Make source URLs clickable with `target="_blank"` and `rel="noopener noreferrer"` so users can jump directly to official PDFs/pages.
- If the board language is Japanese, the sidebar, headings, tag labels, tag-click details, evidence excerpts, missing-evidence text, and confidence labels should be Japanese.

## Visual Tone

Use a dark analytical dashboard tone inspired by technical monitoring tools:

- Dark surface, subtle grid background, glass panels, thin borders, cyan and indigo accents.
- Compact sidebar/topbar, mono labels, small uppercase metadata, dense but readable cards.
- Use the tone for analysis, not decoration: labels should be business-scoring concepts such as `VALUE_SIGNAL`, `EVIDENCE_NODES`, `GAP_LOAD`, `PEER_MATRIX`, and `EVIDENCE_STREAM`.
- Avoid marketing hero sections. The first viewport should immediately show scoring status, peer comparison, and evidence traceability.

## Suggested Layout

```text
Header: Company set / industry / years / report types
Summary band: Total score cards + confidence + warnings
Report acquisition pack
Main grid:
  left: radar chart
  right: top strengths / top gaps
Peer heatmap
Clickable source links: report PDFs + framework sources
Calibration/audit panel
Tag detail table
Evidence drawer
Source definition drawer
Export buttons: JSON / CSV / HTML
```

## Structured Input For Dashboard Script

Use the `Company Result Object` from `evidence-schema.md`. Multiple company objects may be stored in a single JSON array.

For Japanese dashboards, set one of:

```json
{
  "dashboard_locale": "ja",
  "scoring_audit": { "locale": "ja" }
}
```

When available, include localized companion fields:

```json
{
  "industry_ja": "輸送用機器 / 自動車",
  "top_strengths_ja": ["..."],
  "top_gaps_ja": ["..."],
  "comparability_warnings_ja": ["..."],
  "scores": [
    {
      "label_ja": "価値創造ストーリー",
      "definition_ja": "...",
      "reason_ja": "...",
      "missing_evidence_ja": ["..."]
    }
  ],
  "evidence": [
    {
      "section_ja": "...",
      "excerpt_ja": "..."
    }
  ]
}
```

## Script

Use `scripts/build_dashboard.py` to create a self-contained HTML board from scored JSON. The script includes the scoring criteria panel, clickable source links, localized Japanese UI when locale fields are present, the radar chart, heatmap, audit panel, evidence log, and tag-click detail drawer:

```bash
python scripts/build_dashboard.py scoring.json dashboard.html
```

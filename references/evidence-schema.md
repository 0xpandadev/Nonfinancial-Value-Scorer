# Evidence Schema

Use this schema for extracted report evidence and scored results.

## Report Source Object

```json
{
  "report_id": "R-001",
  "company": "Example Co.",
  "identifier": "7203 JP",
  "report_type": "integrated_report",
  "report_title": "Integrated Report 2024",
  "fiscal_year": 2024,
  "publication_year": 2024,
  "language": "ja",
  "publisher": "company|edinet|fsa|jpx|sec|other",
  "source_url": "https://...",
  "retrieved_at": "2026-05-28",
  "source_confidence": "high|medium|low",
  "selection_reason": "Official company PDF from IR library.",
  "local_path": "optional downloaded path"
}
```

## Evidence Object

```json
{
  "evidence_id": "E-001",
  "report_id": "R-001",
  "company": "Example Co.",
  "report_title": "Integrated Report 2026",
  "fiscal_year": 2026,
  "page": 42,
  "section": "Human Capital Strategy",
  "excerpt": "Short excerpt only.",
  "evidence_type": "text|table|figure|kpi|policy|target|governance|risk",
  "tags": ["SIX", "KPI", "GOV"],
  "source_quality": "high|medium|low",
  "extraction_confidence": "high|medium|low",
  "notes": "Any caveat about OCR, missing table context, or ambiguous wording."
}
```

## Score Object

```json
{
  "company": "Example Co.",
  "fiscal_year": 2026,
  "tag_id": "VCS",
  "label": "Value Creation Story",
  "weight": 18,
  "raw_score_0_10": 7,
  "weighted_points": 12.6,
  "definition": "The report explains how values, external environment, strengths, business model, strategy, KPI, governance, and dialogue connect to value creation.",
  "framework_basis": ["METI-VCC-2.0", "IFRS-IR"],
  "reason": "Company-specific strengths, business model, and long-term strategy are connected, but financial/non-financial causal links are only partial.",
  "evidence_ids": ["E-001", "E-009"],
  "positive_evidence": ["Value creation map links strengths to business model and long-term targets."],
  "missing_evidence": ["No explicit investor feedback loop; limited negative issue discussion."],
  "score_caps_applied": ["No governance/accountability evidence: cap 8"],
  "calibration_notes": ["Compared against high VCS anchor; kept at 7 because no negative issue discussion."],
  "confidence": "medium"
}
```

## Company Result Object

```json
{
  "company": "Example Co.",
  "dashboard_locale": "ja",
  "industry": "Chemicals",
  "industry_ja": "化学",
  "fiscal_year": 2026,
  "overall_score_0_100": 73.4,
  "confidence": "medium",
  "scoring_audit": {
    "rubric_version": "nonfinancial-value-scorer-2026-05",
    "source_pack_version": "core-sources-2026-05-28",
    "scoring_date": "2026-05-28",
    "framework_selection": {
      "mode": "auto",
      "company_identifier": "7203 JP",
      "detected_country": "Japan",
      "detected_market": "TSE Prime",
      "selected_framework_set": "japan_core",
      "primary_frameworks": ["METI-VCC-2.0", "IFRS-IR", "SSBJ", "JPX", "FSA"],
      "supporting_frameworks": ["ISSB", "SASB", "GRI", "GHG-PROTOCOL"],
      "selection_reason": "Japanese listed company; use Japanese disclosure context plus global comparability cross-checks.",
      "selection_confidence": "high"
    },
    "calibration_status": "checked",
    "locale": "ja",
    "report_boundary_policy": "latest integrated report plus sustainability report",
    "report_boundary_policy_ja": "最新の統合レポートとサステナビリティレポートを対象",
    "reviewer": "second-pass reviewer or model name",
    "audit_notes": ["Horizontal tag calibration completed."],
    "audit_notes_ja": ["タグ横比較の較正を実施。"]
  },
  "report_sources": [],
  "scores": [],
  "evidence": [],
  "top_strengths": [],
  "top_strengths_ja": [],
  "top_gaps": [],
  "top_gaps_ja": [],
  "comparability_warnings": [],
  "comparability_warnings_ja": []
}
```

## Optional Localized Fields

When building a Japanese HTML board, keep the canonical English keys and add `_ja` companion fields. The dashboard script uses these fields when `dashboard_locale` or `scoring_audit.locale` starts with `ja`.

```json
{
  "report_type_ja": "統合レポート",
  "report_title_ja": "統合レポート2025",
  "selection_reason_ja": "公式IRページのPDFを使用。",
  "section_ja": "人的資本",
  "excerpt_ja": "短い日本語要約または引用。",
  "label_ja": "人的・知的・自然資本",
  "definition_ja": "採点項目の日本語定義。",
  "reason_ja": "なぜこの点数かの日本語説明。",
  "missing_evidence_ja": ["上位点に必要だが不足している根拠。"]
}
```

## UI Definition Tag

Every dashboard card should expose a definition tag.

```json
{
  "tag_id": "VCS",
  "label": "Value Creation Story",
  "definition": "...",
  "why_it_matters": "This is the central logic that connects non-financial information to future value creation.",
  "primary_frameworks": ["METI-VCC-2.0", "IFRS-IR"],
  "supporting_frameworks": ["JPX-CAPITAL-COST", "SSBJ-GENERAL"],
  "score_scale_ref": "Global 0-10 scale plus VCS tag rubric",
  "weight": 18,
  "ui_tooltip": "Shows whether the report connects purpose, external environment, business model, strategy, KPI, and governance into a coherent value-creation explanation."
}
```

## Required Dashboard Traceability

For every visible score, the UI must let the user inspect:

- Definition.
- Source basis.
- Score rule.
- Evidence excerpt.
- Page or section.
- Positive reason.
- Missing evidence or downgrade reason.
- Confidence.

If any of these fields are absent, the UI should show `definition missing`, `source missing`, or `evidence missing` rather than silently hiding the gap.

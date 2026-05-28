# Calibration Protocol

Use this protocol to keep scores stable across companies, analysts, and repeated runs.

## Non-Negotiable Consistency Rules

1. Use the same rubric version for every company in a comparison set.
2. Score each tag from evidence first, then apply weights. Do not start from the desired total score.
3. Do not reward page volume. Reward evidence quality, specificity, linkage, quantification, governance, and comparability.
4. Apply the same fiscal-year and report-boundary policy to every company.
5. Apply score caps consistently. If one company is capped for missing KPI, the same cap applies to all peers.
6. Record every manual override, confidence haircut, or judgment call.
7. Re-score anchor examples before scoring a new peer set if the rubric was changed.

## Run Metadata

Each scoring run should record:

```json
{
  "rubric_version": "nonfinancial-value-scorer-2026-05",
  "source_pack_version": "core-sources-2026-05-28",
  "scoring_date": "YYYY-MM-DD",
  "scorer": "model-or-analyst-name",
  "reviewer": "optional second reviewer",
  "peer_set_policy": "same industry, same fiscal year where possible",
  "report_boundary_policy": "integrated report plus sustainability report, latest available",
  "calibration_status": "draft|checked|reviewed|locked",
  "audit_notes": []
}
```

## Anchor Examples

Before scoring real companies, keep 3-5 anchor examples per tag:

- **Low anchor**: generic statement, no metric, no company-specific mechanism. Usually 1-3.
- **Mid anchor**: structured disclosure with initiatives and partial KPI. Usually 4-6.
- **High anchor**: quantified, time-series, strategically connected, governed, and balanced. Usually 7-9.
- **Exceptional anchor**: decision-grade, peer-comparable, includes missed targets or tradeoffs. Usually 10.

When scores drift, compare the candidate evidence to these anchors rather than relying on intuition.

## Score Cap Rules

Apply these caps unless a stronger, documented reason exists:

| Condition | Cap |
|---|---:|
| Boilerplate disclosure only | 3 |
| No company-specific mechanism | 4 |
| No KPI for a KPI-heavy tag | 5 |
| No strategy or business-model connection | 6 |
| No time-series, baseline, or target | 7 |
| No governance/accountability evidence | 8 |
| Different fiscal year from peer set | No cap, but comparability warning required |
| Evidence extracted from weak OCR | No cap, but confidence must be low or medium |

## Review Workflow

1. **First pass scoring**
   - Extract evidence and assign provisional tag scores.
   - Record caps and missing evidence.

2. **Horizontal calibration**
   - Review one tag across all companies before moving to the next tag.
   - Example: score VCS for all companies, then MAT for all companies.
   - This reduces company-order bias.

3. **Distribution check**
   - Inspect whether scores cluster too high or too low.
   - If all companies score 8+, confirm there is real decision-grade evidence, not just polished wording.
   - If all companies score below 4, confirm the report set is not missing sustainability or annual-report documents.

4. **Contradiction check**
   - Search for evidence that contradicts the positive story: missed targets, risk factors, litigation, workforce issues, emissions growth, governance concerns.
   - Do not lower scores solely for bad outcomes; lower scores when the report hides, disconnects, or fails to explain them.

5. **Second reviewer / model check**
   - A second pass should challenge every score >= 8 and <= 3.
   - Require explicit evidence for every score above 8.
   - Require clear missing-evidence logic for every score below 3.

6. **Lock**
   - Once reviewed, mark the run `locked`.
   - If the rubric changes later, do not compare new scores against locked historical scores without a version warning.

## Inter-Rater Drift Checks

Use these checks when multiple analysts or models score the same reports:

- Tag-level difference of 0-1 point: acceptable.
- Difference of 2 points: review evidence and cap rules.
- Difference of 3+ points: require adjudication and written rationale.
- Overall score difference of 5 points or more: review weighting and missing-evidence treatment.
- Overall score difference of 10 points or more: rerun extraction or review report boundary.

## Audit Output

Every final dashboard should expose:

- Rubric version.
- Source pack version.
- Scoring date.
- Calibration status.
- Report boundary.
- Any caps applied.
- Any peer comparability warnings.
- Reviewer or second-pass status.

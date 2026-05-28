# Report Acquisition

Use this protocol when the user gives a ticker, securities code, EDINET code, company name, fiscal-year range, and/or desired report type instead of uploading files.

## Supported Inputs

Examples:

- `7203, 2022-2025, integrated report and sustainability report`
- `Toyota, FY2021-FY2024, annual securities report plus sustainability data book`
- `AAPL, 2021-2024, sustainability report`
- `E02144, latest 3 years, annual securities report narrative sections`

Accepted identifiers:

- Japanese securities code, usually 4 digits.
- EDINET code, usually `E` plus digits.
- Ticker plus exchange or country, such as `AAPL US`, `7203 JP`, `6758.T`.
- Company legal name or English trade name.

If country/exchange is unclear and the ticker is ambiguous, ask a short clarification. If the identifier is a Japanese 4-digit securities code, assume Japan unless the user says otherwise.

## Report Type Aliases

Map user language to these internal report types:

| User Wording | Internal Type | Priority |
|---|---|---:|
| integrated report, 統合報告書, annual integrated report | `integrated_report` | 1 |
| sustainability report, サステナビリティレポート | `sustainability_report` | 1 |
| sustainability data book, ESG data book | `sustainability_databook` | 2 |
| annual report, annual review | `annual_report` | 2 |
| annual securities report, 有価証券報告書, Yuho | `annual_securities_report` | 1 for Japan |
| corporate governance report, CG report | `corporate_governance_report` | 3 |
| IR deck, medium-term plan, 中期経営計画 | `ir_deck` | 3 |

For non-financial scoring, prefer `integrated_report`, `sustainability_report`, and `annual_securities_report`. Use data books and CG reports as supporting evidence.

## Acquisition Priority

1. Official company IR, sustainability, or investor-relations document library.
2. Regulator or exchange source, such as EDINET/FSA/JPX where applicable.
3. Company-hosted PDF linked from an official press release or report archive.
4. Trusted archive only when official sources are unavailable, with low acquisition confidence.

Never use third-party summaries as primary evidence for scoring. They may be used only to locate the official report.

## Japanese Listed Companies

When a Japanese securities code or EDINET code is supplied:

1. Resolve the company name, EDINET code, securities code, industry, and fiscal year-end.
2. For annual securities reports, use EDINET/FSA data or an EDINET-capable connector when available.
3. For integrated reports and sustainability reports, search the official company IR/sustainability archive first.
4. If both Japanese and English reports exist, prefer the language requested by the user. If no language was requested, prefer Japanese for Japanese companies and record language in metadata.
5. When the report year label and fiscal year differ, store both. Example: `Integrated Report 2024` may cover FY2023.

## Global Companies

When a global ticker is supplied:

1. Resolve ticker, exchange, legal issuer, and investor-relations domain.
2. Search official report archives using report type aliases.
3. Prefer issuer-hosted PDF or HTML annual/sustainability report pages.
4. For SEC issuers, annual report/10-K may support governance, risk, business model, and human-capital evidence, but sustainability reports should come from official sustainability/ESG pages where available.
5. Record currency, reporting standard, and report language if visible.

## Search Query Templates

Use official-source-biased queries:

```text
{company} {securities_code_or_ticker} integrated report PDF {year} official
{company} sustainability report PDF {year} official
site:{company_domain} integrated report {year} PDF
site:{company_domain} sustainability report {year} PDF
{company} IR library integrated report {year}
{company} ESG data book {year}
{company} annual securities report {year} EDINET
```

For Japanese companies, also try:

```text
{company_japanese_name} 統合報告書 {year} PDF
{company_japanese_name} サステナビリティレポート {year} PDF
{company_japanese_name} ESGデータブック {year} PDF
{company_japanese_name} 有価証券報告書 {year}
```

## Acquisition Metadata

For every acquired report, create a report source object:

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
  "retrieved_at": "YYYY-MM-DD",
  "source_confidence": "high|medium|low",
  "selection_reason": "Official company PDF from IR library.",
  "local_path": "optional downloaded path"
}
```

## Coverage Rules

- If the user requests a year range, try to collect every requested year for every company.
- If a report is unavailable, record it as missing instead of filling the year with a different report type.
- If companies have different report types, include a comparability warning.
- If one company has integrated reports and another has only sustainability reports, score both, but mark report-boundary risk.
- Do not mix report languages if translation differences could change interpretation without warning.

## Acquisition Confidence

Use `high` when:

- The report is hosted by the issuer, EDINET/FSA/JPX, SEC, or another official regulator/exchange.
- Title, company, fiscal year, and report type are clear.

Use `medium` when:

- The URL is official but year/report boundary is ambiguous.
- The report is HTML-only and pages are hard to preserve.

Use `low` when:

- The source is an archive or mirror.
- OCR is poor.
- The report might not match the requested fiscal year.

## Output Requirement

Before scoring, briefly list the acquired report pack:

| Company | Identifier | Fiscal Year | Report Type | Source | Confidence |
|---|---|---:|---|---|---|

Then proceed to extraction and scoring. In the final dashboard, include the same acquisition metadata in the audit trail.

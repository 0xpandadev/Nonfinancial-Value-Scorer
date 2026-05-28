# Framework Selection

Use this file to choose the scoring framework set automatically from a ticker, securities code, EDINET code, company name, market, country, and report type.

## Principle

Default to auto-selection. Do not ask the user to choose frameworks unless the company identity or regulatory context is ambiguous.

Every scoring run should record:

```json
{
  "framework_selection": {
    "mode": "auto",
    "company_identifier": "7203 JP",
    "detected_country": "Japan",
    "detected_market": "TSE Prime",
    "selected_framework_set": "japan_core",
    "primary_frameworks": ["METI-VCC-2.0", "IFRS-IR", "SSBJ", "JPX", "FSA"],
    "supporting_frameworks": ["ISSB", "SASB", "GRI", "GHG-PROTOCOL", "TNFD"],
    "selection_reason": "Japanese listed company with integrated/sustainability reports; use Japanese disclosure context plus global comparability cross-checks.",
    "selection_confidence": "high"
  }
}
```

## Detection Rules

| Input Pattern | Assume | Framework Set |
|---|---|---|
| 4-digit Japanese securities code, `7203`, `6758`, `8035` | Japan listed company | `japan_core` |
| EDINET code, `E02144` | Japan listed company / issuer | `japan_core` |
| Ticker ending `.T` or `JP` | Japan listed company | `japan_core` |
| US ticker or exchange, `AAPL`, `MSFT US`, `NYSE`, `NASDAQ` | US/global issuer | `global_investor_core` |
| EU country, EU exchange, CSRD/ESRS report language | EU issuer | `eu_csrd_core` |
| UK issuer or LSE ticker | UK/global issuer | `global_investor_core`, add TCFD-style climate context if report uses it |
| Company publishes `Sustainability Statement`, `ESRS`, `CSRD` | EU-style sustainability statement | `eu_csrd_core` |
| Company publishes `GRI content index` but no investor-oriented report | Impact-heavy report | `impact_core_plus_investor_check` |
| Nature-heavy sector or TNFD report | Nature exposure | Add `nature_topic_pack` |
| Climate transition-heavy sector | Climate exposure | Add `climate_topic_pack` |
| Human-rights or supply-chain-heavy sector | Human rights / RBC exposure | Add `human_rights_topic_pack` |

## Framework Sets

### `japan_core`

Use when the company is Japanese-listed or reports primarily under Japanese disclosure context.

Primary:

- METI Value Co-Creation Guidance 2.0.
- IFRS Integrated Reporting Framework.
- SSBJ/ISSB sustainability disclosure architecture.
- JPX capital-cost / growth-path / governance expectations.
- FSA sustainability and human-capital disclosure context.

Supporting:

- SASB for industry-specific metric comparability.
- GRI for impact completeness.
- GHG Protocol / SBTi / CDP for climate.
- TNFD for nature.
- OECD / UNGP for supply chain and human rights.

### `global_investor_core`

Use for US, UK, and global companies unless another regulatory context is stronger.

Primary:

- IFRS Integrated Reporting Framework for value creation architecture.
- ISSB IFRS S1/S2 for investor-useful sustainability-related financial disclosure.
- SASB for industry-specific topics and metrics.

Supporting:

- GRI for impact completeness.
- GHG Protocol / SBTi / CDP for climate.
- TNFD for nature.
- OECD / UNGP for human rights and responsible business conduct.
- Local annual report or 10-K / annual filing evidence for governance, risk, human capital, and business model.

### `eu_csrd_core`

Use for EU companies, CSRD/ESRS sustainability statements, or reports explicitly prepared under ESRS.

Primary:

- ESRS for double materiality, IROs, policies, actions, targets, and metrics.
- ISSB/SASB for investor comparability when the user wants enterprise-value comparison.
- IFRS Integrated Reporting for value-creation narrative.

Supporting:

- GRI, because ESRS and GRI often map in impact reporting.
- GHG Protocol / SBTi / CDP for climate.
- TNFD for nature.
- OECD / UNGP for due diligence and human rights.

### `impact_core_plus_investor_check`

Use when the report is GRI-heavy or stakeholder-impact oriented.

Primary:

- GRI.
- OECD / UNGP for due diligence topics.
- Topic frameworks based on material topics.

Investor check:

- IFRS Integrated Reporting.
- ISSB/SASB, to test whether impact disclosure connects to enterprise value.

## Topic Packs

### `climate_topic_pack`

Add when climate, transition plan, emissions, or energy intensity is material.

- GHG Protocol.
- SBTi.
- CDP.
- ISSB IFRS S2 / SSBJ climate standard.

### `nature_topic_pack`

Add when biodiversity, water, land use, agriculture, mining, food, chemicals, real estate, forestry, apparel, or supply-chain nature exposure is material.

- TNFD.
- GRI topic standards where applicable.
- CDP water/forests where applicable.

### `human_rights_topic_pack`

Add when labor, supply chain, sourcing, factories, conflict minerals, privacy, safety, or communities are material.

- OECD Guidelines / due diligence guidance.
- UNGP.
- GRI topic standards where applicable.

## Confidence Rules

High confidence:

- Identifier maps clearly to one market/regime.
- Report source is official.
- Report states its framework basis.

Medium confidence:

- Company is multinational and reports under several regimes.
- Report uses mixed standards.
- Ticker lacks exchange suffix but company identity is likely.

Low confidence:

- Ticker is ambiguous.
- Report source is unofficial.
- Company domicile and primary listing differ and reporting basis is unclear.

## Ask The User Only When

- The ticker maps to multiple companies.
- The user wants a specific lens, such as "investor value only" or "impact materiality only."
- The company is dual-listed and report regime materially changes scoring.
- Required report years cannot be found from official sources.

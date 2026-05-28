# Nonfinancial Value Scorer

Evidence-linked scoring and visualization for corporate non-financial value creation disclosures.

This repository contains a Codex skill, scoring rubric, reference framework map, report-acquisition workflow, example scoring data, and a self-contained HTML dashboard generator. It is designed for integrated reports, sustainability reports, annual reports, securities-report narrative sections, and value-enhancement materials.

> The score evaluates disclosure evidence and value-creation explanation quality. It is not an investment rating, credit rating, ESG rating, or intrinsic valuation.

## Quick Links

- Skill entrypoint: [`SKILL.md`](SKILL.md)
- Dashboard generator: [`scripts/build_dashboard.py`](scripts/build_dashboard.py)
- Scoring rubric: [`references/scoring-rubric.md`](references/scoring-rubric.md)
- Framework selection: [`references/framework-selection.md`](references/framework-selection.md)
- Source register: [`references/source-register.md`](references/source-register.md)
- Evidence schema: [`references/evidence-schema.md`](references/evidence-schema.md)
- Fictional GUI sample: [`docs/fictional-dashboard.html`](docs/fictional-dashboard.html)
- Fictional scoring JSON: [`docs/fictional-scoring.json`](docs/fictional-scoring.json)
- GitHub Pages overview: [`docs/index.html`](docs/index.html)

## 日本語

### これは何か

`Nonfinancial Value Scorer` は、統合報告書、サステナビリティレポート、有価証券報告書の記述情報、IR資料などから、企業の非財務価値創造開示を根拠付きでスコアリングし、HTMLダッシュボードとして可視化するためのCodexスキルです。

評価対象は「会社そのものの価値」ではありません。人的資本、知的資本、自然資本、サプライチェーン、人権、気候リスク、ガバナンス、KPI、資本配分などが、将来の価値創造とどれだけ論理的につながって説明されているかを評価します。

### なぜ必要か

PBR、ROIC、PER、利益率だけでは、人的資本、知財、顧客関係、自然資本、サプライチェーンの強さ、人権、気候リスク、ガバナンスの質は比較しにくいです。一方で、統合報告書やサステナビリティレポートは会社ごとに表現が違い、読む人によって採点がぶれやすい。

このスキルは、各スコアに必ず「定義、参照フレームワーク、根拠、採点理由、不足根拠、信頼度」を持たせることで、非財務開示を監査可能なスコアボードに変換します。

### 使う基準

会社名、ティッカー、証券コード、EDINETコード、国、上場市場、レポート種別から、使うフレームワークセットを自動選択します。

日本企業では主に以下を使います。

- 経済産業省 価値協創ガイダンス 2.0
- IFRS Foundation Integrated Reporting Framework
- SSBJ / ISSB サステナビリティ開示基準
- JPX 資本コスト、株価を意識した経営、コーポレートガバナンス文脈
- 金融庁 サステナビリティ開示、人的資本、有価証券報告書開示文脈

海外企業では、必要に応じて以下を組み合わせます。

- IFRS Integrated Reporting Framework
- ISSB / IFRS S1, S2
- SASB Standards
- GRI Standards
- ESRS / CSRD
- GHG Protocol
- CDP
- SBTi
- TNFD
- OECD Responsible Business Conduct
- UN Guiding Principles on Business and Human Rights

### 採点項目

100点満点です。各タグは0から10点で採点し、重みを掛けて合計します。

| Tag | 日本語 | Weight | 見るもの |
| --- | --- | ---: | --- |
| VCS | 価値創造ストーリー | 18 | 理念、外部環境、強み、ビジネスモデル、戦略、KPI、ガバナンスが中長期価値につながるか |
| MAT | マテリアリティ / 重要課題 | 12 | 重要課題の特定、優先順位、根拠、見直し、企業価値との関係 |
| BMO | ビジネスモデル | 10 | 投入資本、事業活動、アウトプット、アウトカム、顧客、バリューチェーン |
| SIX | 6つの資本 / 非財務資本 | 12 | 人的、知的、社会関係、自然資本などの形成、活用、毀損 |
| STR | 戦略 / 資源配分 | 12 | 重要課題に対する投資、撤退、R&D、M&A、人材、設備、DXの配分 |
| KPI | KPI / 成果 | 14 | 目標、実績、時系列、非財務ドライバーと事業成果の接続 |
| GOV | ガバナンス / 説明責任 | 10 | 取締役会、経営陣、委員会、報酬、監督、責任主体 |
| RSK | リスク / 機会 | 6 | 気候、自然、人権、サプライチェーン、技術、規制などの将来価値への影響 |
| QLT | 開示品質 | 6 | 具体性、比較可能性、根拠、ポジティブ情報とネガティブ情報のバランス |

## English

### What This Is

`Nonfinancial Value Scorer` is a skill and toolkit for scoring how well companies explain non-financial value creation in integrated reports, sustainability reports, annual reports, and related IR materials.

It does not score whether a company is a good investment. It scores whether the disclosure gives enough evidence for investors and stakeholders to understand the link between non-financial drivers and future value creation.

### Scoring Tags

| Tag | Label | Weight | What It Tests |
| --- | --- | ---: | --- |
| VCS | Value Creation Story | 18 | Whether purpose, context, strengths, business model, strategy, KPIs, governance, and dialogue form a value-creation logic |
| MAT | Materiality / Key Issues | 12 | Whether material issues are selected, prioritized, justified, refreshed, and linked to enterprise value |
| BMO | Business Model | 10 | Whether inputs, activities, outputs, outcomes, customers, and value chain are connected |
| SIX | Six Capitals / Non-Financial Capital | 12 | Whether human, intellectual, social/relationship, natural, and other capitals are formed, used, strengthened, or eroded |
| STR | Strategy / Resource Allocation | 12 | Whether resources and investments follow material issues and business-model logic |
| KPI | KPI / Outcomes | 14 | Whether targets, actuals, time series, and value-driver links are disclosed |
| GOV | Governance / Accountability | 10 | Whether the board and management oversee non-financial value, risks, incentives, and accountability |
| RSK | Risks / Opportunities | 6 | Whether climate, nature, human rights, supply chain, technology, and regulation are connected to future value |
| QLT | Disclosure Quality | 6 | Whether disclosure is concrete, comparable, evidence-based, and balanced |

### 1-10 Scale

| Score | Meaning | Rule of Thumb |
| ---: | --- | --- |
| 10 | Benchmark | Quantified, time-series, comparable, governed, balanced, and externally evidenced |
| 9 | Advanced | Strong disclosure with only minor traceability or validation gaps |
| 8 | Strong | Clear story, KPIs, and evidence; some tradeoff or comparability gaps remain |
| 7 | Good | Most elements exist, but cross-linkage is uneven |
| 6 | Adequate | Topic is evidenced, but targets or outcomes are not decision-grade |
| 5 | Partial | Basic disclosure exists but value linkage is weak |
| 4 | Thin | Fragmented examples; scope or accountability unclear |
| 3 | Weak | Mentioned but not assessable |
| 2 | Minimal | Generic policies or slogans only |
| 1 | Absent | No meaningful evidence found |

### Workflow

1. Resolve company, ticker, report type, fiscal years, and peer set.
2. Acquire official reports from issuer, regulator, or exchange sources.
3. Select the framework set automatically.
4. Extract short evidence excerpts with pages and sections.
5. Classify evidence into tags.
6. Score each tag on a 0-10 scale.
7. Record downgrade reasons, missing evidence, score caps, and confidence.
8. Lock the same rubric and source pack across peer comparisons.
9. Generate a self-contained HTML dashboard.

## 中文

### 这是什么

`Nonfinancial Value Scorer` 是一个用于分析企业非财务价值创造披露的Codex技能。它可以读取综合报告、可持续发展报告、年度报告、证券报告叙述部分和IR材料，把文本披露转换成有证据、有定义、有评分理由的可视化评分面板。

它不是投资评级、信用评级、ESG评级，也不是公司内在价值估算。它评估的是企业是否把非财务资本、战略、KPI、风险、治理和未来价值创造之间的关系讲清楚。

### 评分项目

| Tag | 中文 | 权重 | 评估重点 |
| --- | --- | ---: | --- |
| VCS | 价值创造叙事 | 18 | 宗旨、外部环境、优势、商业模式、战略、KPI和治理是否形成价值创造逻辑 |
| MAT | 重要性议题 | 12 | 议题选择、优先级、依据、更新机制和企业价值相关性 |
| BMO | 商业模式 | 10 | 投入、活动、产出、结果、客户和价值链是否连接 |
| SIX | 非财务资本 | 12 | 人力、知识、社会关系、自然资本等如何形成、使用、强化或受损 |
| STR | 战略与资源配置 | 12 | 投资、人力、研发、并购、设备、DX和退出逻辑是否清楚 |
| KPI | KPI与成果 | 14 | 目标、实际结果、时间序列以及与价值驱动因素的关系 |
| GOV | 治理与问责 | 10 | 董事会、管理层、委员会、激励和责任主体是否明确 |
| RSK | 风险与机会 | 6 | 气候、自然、人权、供应链、技术、监管等是否连接到未来价值 |
| QLT | 披露质量 | 6 | 具体性、可比性、证据、正负信息平衡和可追溯性 |

## How To Run

Generate the fictional dashboard:

```bash
python scripts/build_dashboard.py examples/sample-scoring.json examples/sample-dashboard.html
```

For Japanese output, set `dashboard_locale: "ja"` or `scoring_audit.locale: "ja"` in the scoring JSON and include localized fields such as `reason_ja`, `definition_ja`, `excerpt_ja`, `top_strengths_ja`, and `top_gaps_ja`.

## Repository Structure

```text
.
|-- SKILL.md
|-- agents/
|-- references/
|-- scripts/
|   `-- build_dashboard.py
|-- examples/
|   |-- sample-scoring.json
|   `-- sample-dashboard.html
`-- docs/
    |-- index.html
    |-- fictional-dashboard.html
    `-- fictional-scoring.json
```

## License

See [`LICENSE`](LICENSE).

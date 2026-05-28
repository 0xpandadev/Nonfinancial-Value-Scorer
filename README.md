# Nonfinancial Value Scorer

Evidence-linked scoring and visualization for corporate non-financial value creation disclosures.

This repository contains a Codex skill, scoring rubric, reference framework map, report-acquisition workflow, and a self-contained HTML dashboard generator. It is designed for integrated reports, sustainability reports, annual reports, securities-report narrative sections, and value-enhancement materials.

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
- GitHub Pages style overview: [`docs/index.html`](docs/index.html)

---

## 日本語

### これは何か

`Nonfinancial Value Scorer` は、企業の統合報告書、サステナビリティレポート、有価証券報告書の記述情報、IR資料などから、非財務価値創造の説明力をスコアリングし、根拠付きのダッシュボードにするためのスキルです。

評価対象は「会社そのものの価値」ではなく、「企業が非財務資本、戦略、ガバナンス、リスク、KPIをどれだけ投資家・ステークホルダーが検証できる形で説明しているか」です。

### なぜ必要か

PBR、ROIC、PER、利益率だけでは、人的資本、知的資本、顧客関係、自然資本、サプライチェーン、人権、気候リスク、ガバナンスなど、将来価値に効く非財務要素を十分に比較できません。

一方で、統合報告書やサステナビリティレポートは文章量が多く、会社ごとに表現も異なります。そのまま読むだけでは、次の問題が起きます。

- どの会社が本当に価値創造ストーリーを説明できているのか分かりにくい。
- マテリアリティやKPIが、企業価値とつながっているのか判断しにくい。
- 同じ業種の複数社を、同じ基準で横比較しにくい。
- 「きれいな開示」と「投資判断に使える開示」が混ざりやすい。
- スコアの根拠が曖昧だと、毎回採点がぶれる。

このスキルは、各スコアに必ず定義、フレームワーク、根拠、採点理由、不足根拠、信頼度を持たせることで、スコアリングを監査可能にします。

### 何の基準を使うか

会社、国、上場市場、レポート種別から、使用するフレームワークセットを自動選択します。

日本企業の場合は、次を中核にします。

- 経済産業省: 価値協創ガイダンス / ESG・非財務情報開示関連資料
- IFRS Foundation: Integrated Reporting Framework
- SSBJ / ISSB: サステナビリティ開示基準
- JPX: 資本コストや株価を意識した経営
- 金融庁: サステナビリティ開示、有価証券報告書開示

海外企業の場合は、地域やレポート形式に応じて次を組み合わせます。

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

総合点は100点満点です。各タグは0-10点で採点し、重みを掛けます。

| Tag | 日本語 | Weight | 見るもの |
| --- | --- | ---: | --- |
| VCS | 価値創造ストーリー | 18 | 理念、外部環境、強み、ビジネスモデル、戦略、KPI、ガバナンスが短中長期価値につながるか |
| MAT | マテリアリティ | 12 | 重要課題の特定、優先順位、根拠、更新プロセス |
| BMO | ビジネスモデル | 10 | 投入資本、活動、アウトプット、アウトカム、顧客・価値連鎖 |
| SIX | 非財務資本 | 12 | 人的、知的、社会関係、自然資本などの形成・活用・毀損 |
| STR | 戦略・資源配分 | 12 | 重要課題に対する資源配分、投資判断、実行ロードマップ |
| KPI | KPI・成果 | 12 | 目標、実績、時系列、企業価値ドライバーとの接続 |
| GOV | ガバナンス | 10 | 取締役会・経営陣の監督、責任、報酬、委員会 |
| RSK | リスク・機会 | 8 | 気候、自然、人権、供給網、技術、規制などの将来価値への影響 |
| QLT | 開示品質 | 6 | 具体性、比較可能性、根拠、ポジティブ/ネガティブのバランス |

### 1-10点の考え方

| Score | 判定 | 基準 |
| ---: | --- | --- |
| 10 | ベンチマーク級 | 定量、時系列、比較可能、戦略接続、ガバナンス責任、ネガティブ情報、外部根拠まで揃う |
| 9 | 先進的 | ほぼ完備。根拠追跡、バランス、外部検証のどこかに軽微な不足 |
| 8 | 強い | 明確なストーリー、KPI、根拠がある。一部トレードオフや比較可能性に不足 |
| 7 | 良好 | 必要要素は概ね揃うが、戦略・資本・KPI・ガバナンスの接続にばらつき |
| 6 | 十分 | テーマと根拠はあるが、投資家が使える目標・成果説明が弱い |
| 5 | 部分的 | 基本開示はあるが、価値創造や将来業績との接続が弱い |
| 4 | 薄い | 断片的な記述や事例のみ。範囲、責任、根拠が不明確 |
| 3 | 弱い | 言及はあるが、評価に必要な具体性が足りない |
| 2 | 最小限 | 一般的な方針文やスローガン程度 |
| 1 | 未開示 | 意味のある根拠が見つからない |

### どう回すか

1. 会社名、ティッカー、証券コード、EDINETコード、年度、レポート種別を指定する。
2. 公式IRページ、EDINET、FSA、JPX、SECなどからレポートを取得する。
3. 国・市場・レポート種別からフレームワークセットを選ぶ。
4. レポートからページ番号、章、短い根拠抜粋を抽出する。
5. 根拠を9つのタグに分類する。
6. 0-10点で採点し、100点満点に換算する。
7. 不足根拠、ダウングレード理由、信頼度を記録する。
8. 複数社比較では、同じルーブリック、同じソースセット、同じ年度方針で横比較する。
9. HTMLダッシュボードを生成し、タグをクリックすると定義・根拠・採点理由を確認できるようにする。

### 使い方

```bash
python scripts/build_dashboard.py examples/sample-scoring.json examples/sample-dashboard.html
```

日本語ボードを作る場合は、JSONに `dashboard_locale: "ja"` または `scoring_audit.locale: "ja"` を入れ、`reason_ja`、`definition_ja`、`excerpt_ja` などの日本語フィールドを追加します。

---

## English

### What This Is

`Nonfinancial Value Scorer` is a skill and toolkit for scoring how well companies explain non-financial value creation in integrated reports, sustainability reports, annual reports, and related IR materials.

It does not score whether a company is a good investment. It scores whether the disclosure gives enough evidence for investors and stakeholders to understand the link between non-financial drivers and future value creation.

### Why It Exists

Financial metrics such as PBR, ROIC, PER, and margins do not fully capture human capital, intellectual assets, customer relationships, natural capital, supply-chain resilience, human rights, climate risk, governance, and other non-financial drivers.

Companies disclose these topics differently. Without a locked rubric, the scoring can drift from one company to another. This repository turns narrative disclosure into a structured, evidence-linked scoring board.

### Framework Basis

The skill automatically selects a framework set based on country, market, identifier, report language, and report type.

Japan core:

- METI Value Co-Creation Guidance and ESG disclosure materials
- IFRS Integrated Reporting Framework
- SSBJ / ISSB sustainability disclosure standards
- JPX capital-cost and corporate-value improvement context
- FSA sustainability and securities-report disclosure context

Global and regional additions:

- IFRS Integrated Reporting
- ISSB / IFRS S1 and S2
- SASB Standards
- GRI Standards
- ESRS / CSRD
- GHG Protocol
- CDP
- SBTi
- TNFD
- OECD RBC
- UN Guiding Principles on Business and Human Rights

### Scoring Tags

| Tag | Label | Weight | What It Tests |
| --- | --- | ---: | --- |
| VCS | Value Creation Story | 18 | Whether purpose, context, strengths, business model, strategy, KPIs, governance, and dialogue form a value-creation logic |
| MAT | Materiality | 12 | Whether material issues are selected, prioritized, justified, and refreshed |
| BMO | Business Model | 10 | Whether inputs, activities, outputs, outcomes, customers, and value chain are connected |
| SIX | Non-Financial Capital | 12 | Whether human, intellectual, social/relationship, natural, and other capitals are formed, used, and protected |
| STR | Strategy Allocation | 12 | Whether resources and investments follow material issues and business-model logic |
| KPI | KPI Outcomes | 12 | Whether targets, actuals, time series, and value-driver links are disclosed |
| GOV | Governance | 10 | Whether the board and management oversee non-financial value, risks, incentives, and accountability |
| RSK | Risk Opportunity | 8 | Whether climate, nature, human rights, supply chain, technology, and regulation are connected to future value |
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

---

## 中文

### 这是什么

`Nonfinancial Value Scorer` 是一个用于分析企业非财务价值创造披露的评分与可视化工具。它可以读取综合报告、可持续发展报告、年度报告、证券报告中的叙述性内容以及IR材料，把非财务信息转换成有证据链的评分面板。

它评估的不是公司是否值得投资，而是公司是否把非财务资本、战略、治理、风险、KPI与未来价值创造之间的关系解释清楚。

### 为什么需要

PBR、ROIC、PER、利润率等财务指标无法充分解释人力资本、知识资本、客户关系、自然资本、供应链、人权、气候风险和治理质量等长期价值驱动因素。

同时，不同公司披露方式差异很大。如果没有统一的定义、证据标准和校准机制，评分很容易漂移。本项目的目标是让每个分数都能追溯到定义、框架、证据、评分理由、缺失证据和置信度。

### 使用的框架

系统会根据公司所在国家、上市市场、识别代码、报告语言和报告类型自动选择框架组合。

日本公司通常使用：

- METI 价值协创指南及ESG/非财务披露资料
- IFRS 综合报告框架
- SSBJ / ISSB 可持续披露标准
- JPX 资本成本与企业价值提升要求
- FSA 可持续披露与证券报告披露要求

全球公司会根据情况加入：

- ISSB / IFRS S1, S2
- SASB
- GRI
- ESRS / CSRD
- GHG Protocol
- CDP
- SBTi
- TNFD
- OECD RBC
- UNGP

### 评分项目

| Tag | 中文 | 权重 | 评价内容 |
| --- | --- | ---: | --- |
| VCS | 价值创造故事 | 18 | 理念、外部环境、优势、商业模式、战略、KPI、治理是否形成价值创造逻辑 |
| MAT | 重要性议题 | 12 | 议题识别、优先级、依据、更新机制 |
| BMO | 商业模式 | 10 | 投入资本、业务活动、产出、结果、客户和价值链 |
| SIX | 非财务资本 | 12 | 人力、知识、社会关系、自然资本等的形成、使用和损耗 |
| STR | 战略与资源配置 | 12 | 资源投入和战略执行是否基于重要议题和商业模式 |
| KPI | KPI与成果 | 12 | 目标、实际结果、时间序列以及与企业价值驱动因素的连接 |
| GOV | 治理 | 10 | 董事会和管理层的监督、责任、薪酬和委员会机制 |
| RSK | 风险与机会 | 8 | 气候、自然、人权、供应链、技术、监管等对未来价值的影响 |
| QLT | 披露质量 | 6 | 具体性、可比性、证据、正负面信息的平衡 |

### 如何运行

```bash
python scripts/build_dashboard.py examples/sample-scoring.json examples/sample-dashboard.html
```

生成的HTML面板会显示总分、雷达图、公司 x 标签热力图、证据日志、来源链接、校准信息和标签点击后的详细解释。

---

## Repository Structure

```text
.
├── SKILL.md
├── agents/
├── references/
├── scripts/
│   └── build_dashboard.py
├── examples/
│   ├── sample-scoring.json
│   └── sample-dashboard.html
└── docs/
    ├── index.html
    ├── fictional-dashboard.html
    └── fictional-scoring.json
```

## License

See [`LICENSE`](LICENSE).

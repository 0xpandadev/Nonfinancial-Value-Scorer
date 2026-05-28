#!/usr/bin/env python3
"""Build a self-contained HTML dashboard from value-story scoring JSON."""

from __future__ import annotations

import html
import json
import math
import sys
from pathlib import Path


TAGS = ["VCS", "MAT", "BMO", "SIX", "STR", "KPI", "GOV", "RSK", "QLT"]
TAG_LABELS = {
    "VCS": "Value Story",
    "MAT": "Materiality",
    "BMO": "Business Model",
    "SIX": "Non-Financial Capital",
    "STR": "Strategy Allocation",
    "KPI": "KPI Outcomes",
    "GOV": "Governance",
    "RSK": "Risk Opportunity",
    "QLT": "Disclosure Quality",
}
TAG_DEFINITIONS = {
    "VCS": "How clearly the report connects purpose, external environment, strengths, business model, strategy, KPIs, governance, and dialogue to short-, medium-, and long-term value creation.",
    "MAT": "Whether the company identifies value-relevant and stakeholder-relevant material issues, explains prioritization, and shows the basis for selecting them.",
    "BMO": "Whether inputs, business activities, outputs, outcomes, customers, and the value chain are connected into an investable business model explanation.",
    "SIX": "Whether human, intellectual, social/relationship, natural, and other non-financial capitals are explained from formation, use, and impairment perspectives.",
    "STR": "Whether the report explains where resources are allocated and how strategy is executed based on material issues and the business model.",
    "KPI": "Whether indicators, targets, actual results, and time series make strategy and non-financial value creation verifiable.",
    "GOV": "Whether the board and management oversee and manage value creation, risks, and non-financial capitals.",
    "RSK": "Whether risks and opportunities such as climate, nature, human rights, supply chain, technology, and regulation are linked to future value.",
    "QLT": "Whether disclosure is concrete, comparable, evidence-based, and balanced between positive and negative information.",
}
TAG_LABELS_JA = {
    "VCS": "価値創造ストーリー",
    "MAT": "マテリアリティ",
    "BMO": "ビジネスモデル",
    "SIX": "非財務資本",
    "STR": "戦略・資源配分",
    "KPI": "KPI・成果",
    "GOV": "ガバナンス",
    "RSK": "リスク・機会",
    "QLT": "開示品質",
}
TAG_DEFINITIONS_JA = {
    "VCS": "企業理念、外部環境、強み、ビジネスモデル、戦略、KPI、ガバナンス、対話が、短中長期の価値創造にどうつながるか。",
    "MAT": "企業価値やステークホルダーにとって重要な課題を特定し、優先順位と根拠を説明しているか。",
    "BMO": "投入資本、事業活動、アウトプット、アウトカム、顧客・価値連鎖をつなげて説明しているか。",
    "SIX": "人的・知的・社会関係・自然資本などの非財務資本を、形成・活用・毀損の観点から説明しているか。",
    "STR": "重要課題やビジネスモデルに基づき、どこへ資源を配分し、どう実行するかを説明しているか。",
    "KPI": "戦略と非財務価値創造を検証できる指標、目標、実績、時系列を示しているか。",
    "GOV": "取締役会・経営陣が価値創造、リスク、非財務資本を監督・管理しているか。",
    "RSK": "気候、自然、人権、供給網、技術、規制などのリスクと機会を将来価値に結びつけて説明しているか。",
    "QLT": "開示が具体的で、比較可能で、根拠があり、ポジティブ/ネガティブのバランスがあるか。",
}
UI = {
    "ja": {
        "brand": "非財務<span>価値</span>",
        "side_subtitle": "DISCLOSURE_NODE // JP",
        "overview": "概要",
        "radar": "レーダー",
        "heatmap": "比較表",
        "evidence": "根拠",
        "sources": "ソース",
        "criteria": "基準",
        "scoring_tags": "採点タグ",
        "analyst_mode": "分析モード",
        "evidence_locked": "根拠固定",
        "value_signal": "総合スコア",
        "evidence_nodes": "根拠ノード",
        "gap_load": "改善論点",
        "low_tag_alerts": "低スコアタグ",
        "refs": "件",
        "items": "件",
        "tags": "タグ",
        "company_signal": "企業シグナル",
        "confidence": "信頼度",
        "score_note": "根拠付き非財務開示スコア",
        "strengths": "強み",
        "gaps": "ギャップ",
        "audit_title": "採点基準・監査",
        "framework_auto": "フレーム自動選択",
        "report_pack": "取得資料",
        "check_notes": "チェックメモ",
        "warnings": "比較上の注意",
        "radar_title": "フレームワーク別シグナル",
        "heatmap_title": "年度 x タグ 比較ヒートマップ",
        "tag_score": "0-10 タグスコア",
        "trace_log": "根拠ログ",
        "source_title": "資料・採点フレームワーク",
        "acquired_reports": "取得したレポート",
        "frameworks": "採点フレームワーク",
        "click_through": "クリック遷移",
        "criteria_title": "採点基準・項目定義",
        "tag_definitions": "項目定義",
        "score_scale": "1-10 採点基準",
        "weight": "重み",
        "detail_title": "定義・根拠ドロワー",
        "definition": "定義",
        "framework": "根拠フレーム",
        "reason": "採点理由",
        "missing": "不足根拠",
        "weighted": "加重点",
        "topbar": "非財務 <span>価値</span> スコアリングボード",
        "companies": "対象",
        "trace_ready": "根拠確認可",
        "no_evidence": "根拠オブジェクトがありません。",
        "no_reports": "取得資料メタデータがありません。",
        "no_sources": "ソースURLがありません。",
        "no_selection": "フレームワーク選択メタデータがありません。",
        "no_notes": "監査メモがありません。",
        "no_warnings": "比較上の注意はありません。",
        "not_supplied": "未設定",
        "draft": "下書き",
        "medium": "中",
        "high": "高",
        "low": "低",
    },
    "en": {},
}
SCORE_SCALE = [
    (
        10,
        "Benchmark",
        "Comparable, quantified, time-series disclosure with clear strategy linkage, governance ownership, negative/positive balance, and external evidence or assurance.",
        "比較可能な定量・時系列開示があり、戦略との接続、ガバナンス責任、ポジティブ/ネガティブのバランス、外部根拠または保証まで揃う。",
    ),
    (
        9,
        "Advanced",
        "Strong disclosure with only minor gaps in traceability, balance, or external validation.",
        "かなり強い開示。根拠追跡、バランス、外部検証のどこかに軽微な不足がある程度。",
    ),
    (
        8,
        "Strong",
        "Clear narrative, relevant KPIs, and credible evidence; some tradeoffs, downside, or comparability detail remains limited.",
        "明確なストーリー、関連KPI、信頼できる根拠がある。ただしトレードオフ、悪化情報、比較可能性に一部不足が残る。",
    ),
    (
        7,
        "Good",
        "Most required elements are present, but linkage across strategy, capital, KPI, and governance is uneven.",
        "必要要素は概ね揃うが、戦略・資本・KPI・ガバナンスの接続にばらつきがある。",
    ),
    (
        6,
        "Adequate",
        "Topic is disclosed with some evidence, but the investor-useful logic, targets, or outcomes are not fully developed.",
        "テーマと根拠は示されるが、投資家が使える論理、目標、成果の説明が十分ではない。",
    ),
    (
        5,
        "Partial",
        "Basic disclosure exists, but it is mostly descriptive and weakly tied to value creation or future performance.",
        "基本的な開示はあるが、説明中心で、価値創造や将来業績との結びつきが弱い。",
    ),
    (
        4,
        "Thin",
        "Fragmented statements or isolated examples exist; evidence, scope, or accountability is unclear.",
        "断片的な記述や個別事例はあるが、根拠、範囲、責任主体が不明確。",
    ),
    (
        3,
        "Weak",
        "The item is mentioned, but without enough detail to support an assessment.",
        "項目への言及はあるが、評価に必要な具体性が足りない。",
    ),
    (
        2,
        "Minimal",
        "Only generic policy language or slogans are present.",
        "一般的な方針文やスローガン程度にとどまる。",
    ),
    (
        1,
        "Absent",
        "No meaningful report evidence was found for the scoring item.",
        "採点項目について意味のあるレポート根拠が見つからない。",
    ),
]
RADAR_COLORS = ["#00dbe9", "#6b7cff", "#7df4ff", "#ff6b6b"]
CORE_SOURCE_LINKS = [
    {
        "label": "METI Value Co-Creation Guidance",
        "source_id": "METI-VCC-2.0",
        "role": "Japanese value-creation common language",
        "url": "https://www.meti.go.jp/policy/economy/keiei_innovation/kigyoukaikei/ESGguidance.html",
    },
    {
        "label": "IFRS Integrated Reporting Framework",
        "source_id": "IFRS-IR",
        "role": "Integrated reporting architecture",
        "url": "https://www.ifrs.org/content/dam/ifrs/integrated-reporting/framework-and-translations/integratedreporting-framework-061024.pdf",
    },
    {
        "label": "SSBJ Sustainability Standards",
        "source_id": "SSBJ",
        "role": "Japan sustainability disclosure standards",
        "url": "https://www.ssb-j.jp/jp/ssbj_standards.html",
    },
    {
        "label": "ISSB / IFRS Sustainability Standards",
        "source_id": "ISSB",
        "role": "Global sustainability disclosure architecture",
        "url": "https://www.ifrs.org/sustainability/knowledge-hub/introduction-to-issb-and-ifrs-sustainability-disclosure-standards/",
    },
    {
        "label": "SASB Standards",
        "source_id": "SASB",
        "role": "Industry-specific sustainability topics and metrics",
        "url": "https://www.ifrs.org/issued-standards/sasb-standards/",
    },
    {
        "label": "GRI Standards",
        "source_id": "GRI",
        "role": "Impact reporting across economy, environment and people",
        "url": "https://www.globalreporting.org/standards",
    },
    {
        "label": "European Sustainability Reporting Standards",
        "source_id": "ESRS",
        "role": "EU CSRD double-materiality reporting",
        "url": "https://finance.ec.europa.eu/news/commission-adopts-european-sustainability-reporting-standards-2023-07-31_en",
    },
    {
        "label": "GHG Protocol Standards",
        "source_id": "GHG",
        "role": "Corporate greenhouse-gas accounting",
        "url": "https://ghgprotocol.org/standards",
    },
    {
        "label": "CDP Question Bank",
        "source_id": "CDP",
        "role": "Environmental questionnaire and scoring benchmark",
        "url": "https://www.cdp.net/en/disclose/question-bank",
    },
    {
        "label": "SBTi Corporate Net-Zero Standard",
        "source_id": "SBTI",
        "role": "Science-based climate target credibility",
        "url": "https://sciencebasedtargets.org/net-zero",
    },
    {
        "label": "JPX Capital Cost Management",
        "source_id": "JPX-CAPITAL-COST",
        "role": "Market implementation and investor explanation",
        "url": "https://www.jpx.co.jp/equities/follow-up/02.html",
    },
    {
        "label": "FSA Sustainability Disclosure",
        "source_id": "FSA-SUSTAINABILITY",
        "role": "Japanese mandatory-disclosure context",
        "url": "https://www.fsa.go.jp/policy/kaiji/sustainability-kaiji.html",
    },
    {
        "label": "TNFD Recommendations",
        "source_id": "TNFD",
        "role": "Nature-related risks, dependencies, impacts",
        "url": "https://tnfd.global/publication/recommendations-of-the-taskforce-on-nature-related-financial-disclosures/",
    },
    {
        "label": "OECD Responsible Business Conduct",
        "source_id": "OECD",
        "role": "Risk-based due diligence and responsible business conduct",
        "url": "https://www.oecd.org/corporate/mne/oecdguidelinesformultinationalenterprises.htm",
    },
    {
        "label": "UN Guiding Principles on Business and Human Rights",
        "source_id": "UNGP",
        "role": "Human-rights due diligence and remedy",
        "url": "https://www.ohchr.org/Documents/Issues/Business/Intro_Guiding_PrinciplesBusinessHR.pdf",
    },
]


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def is_ja(results) -> bool:
    for company in results:
        audit = company.get("scoring_audit") or {}
        if str(company.get("dashboard_locale", "")).lower().startswith("ja"):
            return True
        if str(audit.get("locale", "")).lower().startswith("ja"):
            return True
    return False


def tr(key: str, ja: bool) -> str:
    if ja:
        return UI["ja"].get(key, key)
    fallback = {
        "brand": "Value<span>Story</span>",
        "side_subtitle": "DISCLOSURE_NODE // 01",
        "overview": "OVERVIEW",
        "radar": "RADAR",
        "heatmap": "HEATMAP",
        "evidence": "EVIDENCE",
        "sources": "SOURCES",
        "criteria": "CRITERIA",
        "scoring_tags": "SCORING_TAGS",
        "analyst_mode": "ANALYST_MODE",
        "evidence_locked": "EVIDENCE_LOCKED",
        "criteria_title": "Scoring Criteria and Item Definitions",
        "tag_definitions": "Tag Definitions",
        "score_scale": "1-10 Scoring Scale",
        "weight": "Weight",
        "score_note": "Evidence-linked disclosure score",
        "not_supplied": "not supplied",
        "draft": "draft",
    }
    return fallback.get(key, key)


def localized(obj, key: str, ja: bool):
    if ja:
        value = obj.get(f"{key}_ja")
        if value not in (None, ""):
            return value
    return obj.get(key)


def localized_list(obj, key: str, ja: bool):
    if ja and obj.get(f"{key}_ja"):
        return obj.get(f"{key}_ja") or []
    return obj.get(key) or []


def confidence_label(value, ja: bool) -> str:
    text = "" if value is None else str(value)
    if not ja:
        return text
    return {"high": "高", "medium": "中", "low": "低"}.get(text.lower(), text)


def tag_label(tag: str, ja: bool) -> str:
    return (TAG_LABELS_JA if ja else TAG_LABELS).get(tag, tag)


def score_label(score, ja: bool) -> str:
    tag = score.get("tag_id", "")
    if ja:
        return score.get("label_ja") or tag_label(tag, ja)
    return score.get("label") or tag_label(tag, ja)


def score_definition(score, ja: bool) -> str:
    tag = score.get("tag_id", "")
    if ja:
        return score.get("definition_ja") or TAG_DEFINITIONS_JA.get(tag) or score.get("definition")
    definition = score.get("definition")
    if definition and not str(definition).startswith("See nonfinancial-value-scorer"):
        return definition
    return TAG_DEFINITIONS.get(tag) or definition


def load_results(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("Input JSON must be an object or array of objects")


def score_map(company):
    return {score.get("tag_id"): score for score in company.get("scores", [])}


def score_class(score):
    if score is None:
        return "missing"
    if score >= 8:
        return "high"
    if score >= 5:
        return "mid"
    return "low"


def score_value(item):
    raw = item.get("raw_score_0_10") if item else None
    return raw if isinstance(raw, (int, float)) else None


def pct(value, maximum=100):
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0
    return max(0, min(100, number / maximum * 100))


def all_scores(results):
    values = []
    for company in results:
        for score in company.get("scores", []):
            raw = score_value(score)
            if raw is not None:
                values.append(raw)
    return values


def evidence_count(results):
    return sum(len(company.get("evidence", [])) for company in results)


def gap_count(results):
    return sum(len(company.get("top_gaps", [])) for company in results)


def average_overall(results):
    values = []
    for company in results:
        try:
            values.append(float(company.get("overall_score_0_100")))
        except (TypeError, ValueError):
            pass
    return round(sum(values) / len(values), 1) if values else 0


def tag_average(results, tag):
    values = []
    for company in results:
        raw = score_value(score_map(company).get(tag))
        if raw is not None:
            values.append(raw)
    return round(sum(values) / len(values), 1) if values else None


def render_shell_nav(ja=False):
    nav = [
        (tr("overview", ja), "overview", "active"),
        (tr("criteria", ja), "criteria", ""),
        (tr("radar", ja), "radar", ""),
        (tr("heatmap", ja), "heatmap", ""),
        (tr("evidence", ja), "evidence", ""),
        (tr("sources", ja), "sources", ""),
    ]
    tags = "".join(f"<span>{tag}</span>" for tag in TAGS)
    items = "".join(
        f'<a class="nav-item {state}" href="#{esc(anchor)}"><span class="nav-dot"></span>{esc(label)}</a>'
        for label, anchor, state in nav
    )
    return f"""
    <aside class="sidebar">
      <div class="brand">
        <div class="pulse"></div>
        <div>
          <h1>{tr("brand", ja)}</h1>
          <p>{esc(tr("side_subtitle", ja))}</p>
        </div>
      </div>
      <nav>{items}</nav>
      <div class="tag-stack">
        <p>{esc(tr("scoring_tags", ja))}</p>
        <div>{tags}</div>
      </div>
      <div class="operator">
        <div class="avatar">VS</div>
        <div>
          <b>{esc(tr("analyst_mode", ja))}</b>
          <span>{esc(tr("evidence_locked", ja))}</span>
        </div>
      </div>
    </aside>
    """


def render_metric_cards(results):
    ja = is_ja(results)
    avg = average_overall(results)
    scores = all_scores(results)
    weak = len([x for x in scores if x < 5])
    metrics = [
        (tr("value_signal", ja), avg, "/100", "#00dbe9", avg),
        (tr("evidence_nodes", ja), evidence_count(results), tr("refs", ja), "#6b7cff", min(evidence_count(results) * 12, 100)),
        (tr("gap_load", ja), gap_count(results), tr("items", ja), "#ff6b6b", min(gap_count(results) * 14, 100)),
        (tr("low_tag_alerts", ja), weak, tr("tags", ja), "#c2c6d6", min(weak * 18, 100)),
    ]
    cards = []
    for label, value, unit, color, bar in metrics:
        cards.append(
            f"""
            <section class="glass metric">
              <div class="scanline"></div>
              <div class="metric-head">
                <span>{esc(label)}</span>
                <i style="background:{color}"></i>
              </div>
              <div class="metric-value">{esc(value)}<small>{esc(unit)}</small></div>
              <div class="microbar"><em style="width:{pct(bar)}%; background:{color}"></em></div>
            </section>
            """
        )
    return f"<div class='metric-grid'>{''.join(cards)}</div>"


def render_company_cards(results):
    ja = is_ja(results)
    cards = []
    for company in results:
        warnings = localized_list(company, "comparability_warnings", ja)
        strengths = localized_list(company, "top_strengths", ja)
        gaps = localized_list(company, "top_gaps", ja)
        score = company.get("overall_score_0_100")
        cards.append(
            f"""
            <section class="glass company-card">
              <div class="section-head">
                <div>
                  <span class="kicker">{esc(tr("company_signal", ja))}</span>
                  <h2>{esc(company.get('company'))}</h2>
                </div>
                <span class="status {esc(str(company.get('confidence', '')).lower())}">{esc(tr("confidence", ja))}: {esc(confidence_label(company.get('confidence'), ja))}</span>
              </div>
              <div class="score-row">
                <div class="score-main">{esc(score)}<small>/100</small></div>
                <div class="ring" style="--score:{pct(score)}%"><span>{esc(company.get('fiscal_year'))}</span></div>
              </div>
              <p class="meta">{esc(localized(company, 'industry', ja) or company.get('industry'))} / {esc(tr("score_note", ja))}</p>
              <div class="split-list">
                <div>
                  <b>{esc(tr("strengths", ja))}</b>
                  <ul>{''.join(f'<li>{esc(x)}</li>' for x in strengths[:3])}</ul>
                </div>
                <div>
                  <b>{esc(tr("gaps", ja))}</b>
                  <ul>{''.join(f'<li>{esc(x)}</li>' for x in gaps[:3])}</ul>
                </div>
              </div>
              {('<div class="warning">' + '<br>'.join(esc(w) for w in warnings) + '</div>') if warnings else ''}
            </section>
            """
        )
    return "".join(cards)


def render_scoring_criteria(results):
    ja = is_ja(results)
    first_scores = score_map(results[0]) if results else {}
    tag_cards = []
    for tag in TAGS:
        score = first_scores.get(tag) or {"tag_id": tag}
        weight = score.get("weight")
        weight_text = f"{weight}%" if isinstance(weight, (int, float)) else "-"
        definition = TAG_DEFINITIONS_JA.get(tag) if ja else TAG_DEFINITIONS.get(tag)
        tag_cards.append(
            f"""
            <article class="criteria-tag">
              <div><span>{esc(tag)}</span><b>{esc(tag_label(tag, ja))}</b></div>
              <p>{esc(definition)}</p>
              <em>{esc(tr("weight", ja))}: {esc(weight_text)}</em>
            </article>
            """
        )
    scale_rows = []
    for point, label, en_text, ja_text in SCORE_SCALE:
        scale_rows.append(
            f"""
            <li>
              <strong>{point}</strong>
              <div>
                <b>{esc(label if not ja else score_scale_label_ja(point))}</b>
                <p>{esc(ja_text if ja else en_text)}</p>
              </div>
            </li>
            """
        )
    return f"""
    <section class="glass criteria-panel" id="criteria">
      <div class="section-head">
        <div>
          <span class="kicker">RUBRIC_REFERENCE</span>
          <h2>{esc(tr("criteria_title", ja))}</h2>
        </div>
        <span class="status">{esc(tr("score_scale", ja))}</span>
      </div>
      <div class="criteria-layout">
        <div>
          <h3>{esc(tr("tag_definitions", ja))}</h3>
          <div class="criteria-tags">{''.join(tag_cards)}</div>
        </div>
        <div>
          <h3>{esc(tr("score_scale", ja))}</h3>
          <ol class="score-scale">{''.join(scale_rows)}</ol>
        </div>
      </div>
    </section>
    """


def score_scale_label_ja(point: int) -> str:
    labels = {
        10: "ベンチマーク級",
        9: "先進的",
        8: "強い",
        7: "良好",
        6: "十分",
        5: "部分的",
        4: "薄い",
        3: "弱い",
        2: "最小限",
        1: "未開示",
    }
    return labels.get(point, str(point))


def render_audit_panel(results):
    ja = is_ja(results)
    audits = [company.get("scoring_audit") or {} for company in results]
    first = audits[0] if audits else {}
    first_selection = first.get("framework_selection") or {}
    rubric_versions = sorted({str(a.get("rubric_version")) for a in audits if a.get("rubric_version")})
    source_versions = sorted({str(a.get("source_pack_version")) for a in audits if a.get("source_pack_version")})
    statuses = sorted({str(a.get("calibration_status")) for a in audits if a.get("calibration_status")})
    policies = sorted({str(localized(a, "report_boundary_policy", ja) if ja else a.get("report_boundary_policy")) for a in audits if a.get("report_boundary_policy")})
    reviewers = sorted({str(a.get("reviewer")) for a in audits if a.get("reviewer")})
    cap_total = 0
    notes = []
    warnings = []
    report_sources = []
    for company in results:
        warnings.extend(localized_list(company, "comparability_warnings", ja))
        report_sources.extend(company.get("report_sources") or [])
        audit = company.get("scoring_audit") or {}
        notes.extend(localized_list(audit, "audit_notes", ja))
        for score in company.get("scores", []):
            cap_total += len(score.get("score_caps_applied") or [])
            notes.extend(score.get("calibration_notes") or [])
    if len(rubric_versions) > 1:
        warnings.append("複数のルーブリック版が検出されました。" if ja else "Multiple rubric versions detected.")
    if len(source_versions) > 1:
        warnings.append("複数のソースパック版が検出されました。" if ja else "Multiple source pack versions detected.")
    rows = [
        ("RUBRIC_VERSION", ", ".join(rubric_versions) or first.get("rubric_version") or tr("not_supplied", ja)),
        ("SOURCE_PACK", ", ".join(source_versions) or first.get("source_pack_version") or tr("not_supplied", ja)),
        ("CALIBRATION", ", ".join(statuses) or first.get("calibration_status") or tr("draft", ja)),
        ("FRAMEWORK_SET", first_selection.get("selected_framework_set") or tr("not_supplied", ja)),
        ("REPORT_BOUNDARY", " / ".join(policies) or first.get("report_boundary_policy") or tr("not_supplied", ja)),
        ("REVIEWER", ", ".join(reviewers) or first.get("reviewer") or tr("not_supplied", ja)),
        ("CAPS_APPLIED", cap_total),
        ("REPORT_SOURCES", len(report_sources)),
    ]
    row_html = "".join(
        f"<div class='audit-row'><span>{esc(label)}</span><b>{esc(value)}</b></div>"
        for label, value in rows
    )
    note_html = "".join(f"<li>{esc(note)}</li>" for note in notes[:6])
    warning_html = "".join(f"<li>{esc(warning)}</li>" for warning in warnings[:6])
    selection_html = ""
    if first_selection:
        selection_html = (
            f"<li><b>{esc(first_selection.get('selected_framework_set'))}</b> / "
            f"{esc(first_selection.get('detected_country'))} / "
            f"{esc(first_selection.get('selection_confidence'))}</li>"
            f"<li>{esc(localized(first_selection, 'selection_reason', ja))}</li>"
        )
    report_html = "".join(
        f"<li><b>{esc(localized(source, 'report_type', ja) or source.get('report_type'))}</b> <a href=\"{esc(source.get('source_url'))}\" target=\"_blank\" rel=\"noopener noreferrer\">{esc(localized(source, 'report_title', ja) or source.get('report_title'))}</a> / FY{esc(source.get('fiscal_year'))} / {esc(source.get('publisher'))} / {esc(confidence_label(source.get('source_confidence'), ja))}</li>"
        for source in report_sources[:8]
    )
    return f"""
    <section class="glass audit-panel">
      <div class="section-head">
        <div>
          <span class="kicker">CALIBRATION_LOCK</span>
          <h2>{esc(tr("audit_title", ja))}</h2>
        </div>
        <span class="status">{esc(rows[2][1])}</span>
      </div>
      <div class="audit-grid">{row_html}</div>
      <div class="audit-columns">
        <div>
          <b>{esc(tr("framework_auto", ja))}</b>
          <ul>{selection_html if selection_html else f'<li>{esc(tr("no_selection", ja))}</li>'}</ul>
        </div>
        <div>
          <b>{esc(tr("report_pack", ja))}</b>
          <ul>{report_html if report_html else f'<li>{esc(tr("no_reports", ja))}</li>'}</ul>
        </div>
        <div>
          <b>{esc(tr("check_notes", ja))}</b>
          <ul>{note_html if note_html else f'<li>{esc(tr("no_notes", ja))}</li>'}</ul>
        </div>
        <div>
          <b>{esc(tr("warnings", ja))}</b>
          <ul>{warning_html if warning_html else f'<li>{esc(tr("no_warnings", ja))}</li>'}</ul>
        </div>
      </div>
    </section>
    """


def render_source_links_panel(results):
    ja = is_ja(results)
    report_sources = []
    for company in results:
        report_sources.extend(company.get("report_sources") or [])
    report_links = "".join(
        f"""
        <a class="source-link" href="{esc(source.get('source_url'))}" target="_blank" rel="noopener noreferrer">
          <span>{esc(localized(source, 'report_type', ja) or source.get('report_type'))}</span>
          <b>{esc(localized(source, 'report_title', ja) or source.get('report_title'))}</b>
          <em>{esc(source.get('company'))} / FY{esc(source.get('fiscal_year'))} / {esc(confidence_label(source.get('source_confidence'), ja))}</em>
        </a>
        """
        for source in report_sources
        if source.get("source_url")
    )
    framework_links = "".join(
        f"""
        <a class="source-link framework" href="{esc(source['url'])}" target="_blank" rel="noopener noreferrer">
          <span>{esc(source['source_id'])}</span>
          <b>{esc(source['label'])}</b>
          <em>{esc(source['role'])}</em>
        </a>
        """
        for source in CORE_SOURCE_LINKS
    )
    return f"""
    <section class="glass source-panel" id="sources">
      <div class="section-head">
        <div>
          <span class="kicker">SOURCE_LINKS</span>
          <h2>{esc(tr("source_title", ja))}</h2>
        </div>
        <span class="status">{esc(tr("click_through", ja))}</span>
      </div>
      <div class="source-grid">
        <div>
          <h3>{esc(tr("acquired_reports", ja))}</h3>
          <div class="source-list">{report_links if report_links else f'<p>{esc(tr("no_sources", ja))}</p>'}</div>
        </div>
        <div>
          <h3>{esc(tr("frameworks", ja))}</h3>
          <div class="source-list">{framework_links}</div>
        </div>
      </div>
    </section>
    """


def radar_points(company, radius=132, center=160):
    smap = score_map(company)
    points = []
    for index, tag in enumerate(TAGS):
        angle = -math.pi / 2 + index * (2 * math.pi / len(TAGS))
        raw = score_value(smap.get(tag)) or 0
        distance = radius * raw / 10
        x = center + math.cos(angle) * distance
        y = center + math.sin(angle) * distance
        points.append(f"{x:.1f},{y:.1f}")
    return " ".join(points)


def radar_axes(radius=132, center=160, ja=False):
    lines = []
    labels = []
    for index, tag in enumerate(TAGS):
        angle = -math.pi / 2 + index * (2 * math.pi / len(TAGS))
        x = center + math.cos(angle) * radius
        y = center + math.sin(angle) * radius
        lx = center + math.cos(angle) * (radius + 22)
        ly = center + math.sin(angle) * (radius + 22)
        lines.append(f'<line x1="{center}" y1="{center}" x2="{x:.1f}" y2="{y:.1f}" />')
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}">{esc(tag_label(tag, ja))}</text>')
    return "".join(lines), "".join(labels)


def render_radar(results):
    ja = is_ja(results)
    axes, labels = radar_axes(ja=ja)
    polygons = []
    legend = []
    for index, company in enumerate(results[:4]):
        color = RADAR_COLORS[index % len(RADAR_COLORS)]
        polygons.append(
            f'<polygon points="{radar_points(company)}" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-width="1.6" />'
        )
        legend.append(f'<span><i style="background:{color}"></i>{esc(company.get("company"))}</span>')
    tag_bars = []
    for tag in TAGS:
        avg = tag_average(results, tag)
        cls = score_class(avg)
        tag_bars.append(
            f"""
            <div class="tag-bar {cls}">
              <div><b>{tag}</b><span>{esc(tag_label(tag, ja))}</span></div>
              <em><i style="width:{pct(avg, 10)}%"></i></em>
              <strong>{esc(avg if avg is not None else "-")}</strong>
            </div>
            """
        )
    return f"""
    <section class="glass radar-panel" id="radar">
      <div class="section-head">
        <div>
          <span class="kicker">VALUE_CREATION_RADAR</span>
          <h2>{esc(tr("radar_title", ja))}</h2>
        </div>
        <div class="legend">{''.join(legend)}</div>
      </div>
      <div class="radar-layout">
        <svg class="radar" viewBox="0 0 320 320" role="img" aria-label="Tag radar chart">
          <g class="rings">
            <circle cx="160" cy="160" r="132"></circle>
            <circle cx="160" cy="160" r="99"></circle>
            <circle cx="160" cy="160" r="66"></circle>
            <circle cx="160" cy="160" r="33"></circle>
          </g>
          <g class="axes">{axes}</g>
          <g class="polygons">{''.join(polygons)}</g>
          <g class="labels">{labels}</g>
        </svg>
        <div class="tag-bars">{''.join(tag_bars)}</div>
      </div>
    </section>
    """


def render_heatmap(results):
    ja = is_ja(results)
    header = "".join(f"<th>{esc(tag)}</th>" for tag in TAGS)
    rows = []
    for company in results:
        smap = score_map(company)
        cells = []
        for tag in TAGS:
            item = smap.get(tag, {})
            raw = score_value(item)
            cls = score_class(raw)
            reason = esc(localized(item, "reason", ja) or "No score")
            confidence = esc(confidence_label(item.get("confidence", ""), ja))
            cells.append(
                f'<td class="{cls}" title="{reason}"><button data-company="{esc(company.get("company"))}" data-tag="{tag}"><b>{esc(raw if raw is not None else "-")}</b><small>{confidence}</small></button></td>'
            )
        rows.append(f"<tr><th>{esc(company.get('company'))}</th>{''.join(cells)}</tr>")
    return f"""
    <section class="glass heatmap-panel" id="heatmap">
      <div class="section-head">
        <div>
          <span class="kicker">PEER_MATRIX</span>
          <h2>{esc(tr("heatmap_title", ja))}</h2>
        </div>
        <span class="status">{esc(tr("tag_score", ja))}</span>
      </div>
      <div class="table-scroll">
        <table class="heatmap"><thead><tr><th>{esc("企業" if ja else "Company")}</th>{header}</tr></thead><tbody>{''.join(rows)}</tbody></table>
      </div>
    </section>
    """


def render_evidence_log(results):
    ja = is_ja(results)
    items = []
    for company in results:
        for evidence in company.get("evidence", []):
            tags = ", ".join(evidence.get("tag_ids") or evidence.get("tags") or [])
            items.append(
                f"""
                <li>
                  <span>[{esc(evidence.get('evidence_id'))}]</span>
                  <b>{esc(company.get('company'))}</b>
                  <em>p.{esc(evidence.get('page'))} / {esc(localized(evidence, 'section', ja))} / {esc(tags)}</em>
                  <p>{esc(localized(evidence, 'excerpt', ja))}</p>
                </li>
                """
            )
    return f"""
    <section class="glass evidence-log" id="evidence">
      <div class="section-head">
        <div>
          <span class="kicker">EVIDENCE_STREAM</span>
          <h2>{esc(tr("trace_log", ja))}</h2>
        </div>
        <span class="live-dot"></span>
      </div>
      <ol>{''.join(items) if items else f'<li><p>{esc(tr("no_evidence", ja))}</p></li>'}</ol>
    </section>
    """


def render_details(results):
    ja = is_ja(results)
    panels = []
    for company in results:
        evidence_by_id = {e.get("evidence_id"): e for e in company.get("evidence", [])}
        for score in company.get("scores", []):
            tag = score.get("tag_id")
            evidences = [evidence_by_id.get(eid, {"evidence_id": eid}) for eid in score.get("evidence_ids", [])]
            evidence_html = "".join(
                f"""
                <li>
                  <strong>{esc(e.get('evidence_id'))}</strong>
                  <span>p.{esc(e.get('page'))} {esc(localized(e, 'section', ja))}</span>
                  <blockquote>{esc(localized(e, 'excerpt', ja))}</blockquote>
                </li>
                """
                for e in evidences
            )
            panels.append(
                f"""
                <article class="detail" id="detail-{esc(company.get('company'))}-{esc(tag)}" data-company="{esc(company.get('company'))}" data-tag="{esc(tag)}">
                  <div class="detail-head">
                    <span>{esc(tag)}</span>
                    <h3>{esc(company.get('company'))}: {esc(score_label(score, ja))}</h3>
                    <b>{esc(score.get('raw_score_0_10'))}/10</b>
                  </div>
                  <p><b>{esc(tr("definition", ja))}:</b> {esc(score_definition(score, ja))}</p>
                  <p><b>{esc(tr("framework", ja))}:</b> {esc(', '.join(score.get('framework_basis', [])))}</p>
                  <p><b>{esc(tr("reason", ja))}:</b> {esc(localized(score, 'reason', ja))}</p>
                  <p><b>{esc(tr("missing", ja))}:</b> {esc('; '.join(localized_list(score, 'missing_evidence', ja)))}</p>
                  <p><b>{esc(tr("confidence", ja))}:</b> {esc(confidence_label(score.get('confidence'), ja))} / <b>{esc(tr("weighted", ja))}:</b> {esc(score.get('weighted_points'))}</p>
                  <ul>{evidence_html}</ul>
                </article>
                """
            )
    return f"""
    <section class="glass detail-panel" id="overview">
      <div class="section-head">
        <div>
          <span class="kicker">SCORE_DETAILS</span>
          <h2>{esc(tr("detail_title", ja))}</h2>
        </div>
      </div>
      {''.join(panels)}
    </section>
    """


def build_html(results):
    ja = is_ja(results)
    data_json = esc(json.dumps(results, ensure_ascii=False))
    company_count = len(results)
    year_span = ", ".join(str(c.get("fiscal_year")) for c in results if c.get("fiscal_year"))
    return f"""<!doctype html>
<html lang="{esc('ja' if ja else 'en')}" class="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc('非財務価値スコアリングダッシュボード' if ja else 'Nonfinancial Value Scoring Dashboard')}</title>
<style>
  :root {{
    --surface:#0c0e12; --surface-lowest:#080a0d; --surface-low:#111318; --surface-panel:rgba(21,24,30,.58);
    --surface-high:#1c1e24; --line:rgba(132,148,149,.18); --line-strong:rgba(0,219,233,.24);
    --text:#e2e2e8; --muted:#a0b0b1; --dim:rgba(160,176,177,.56); --cyan:#00dbe9; --cyan-soft:#7df4ff;
    --indigo:#6b7cff; --danger:#ff6b6b; --amber:#d3a44b;
  }}
  * {{ box-sizing:border-box; }}
  html {{ background:var(--surface); }}
  body {{
    margin:0; min-height:100vh; overflow:hidden; color:var(--text);
    font:14px/1.5 "Hanken Grotesk", "Segoe UI", system-ui, sans-serif;
    background:
      linear-gradient(to right, rgba(132,148,149,.035) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(132,148,149,.035) 1px, transparent 1px),
      var(--surface);
    background-size:30px 30px;
  }}
  a {{ color:inherit; text-decoration:none; }}
  .shell {{ display:flex; min-height:100vh; }}
  .sidebar {{
    width:244px; flex:0 0 244px; background:var(--surface-lowest); border-right:1px solid rgba(59,73,75,.32);
    padding:24px 14px; display:flex; flex-direction:column; gap:28px;
  }}
  .brand {{ display:flex; gap:10px; align-items:flex-start; padding:0 10px; }}
  .pulse {{ width:8px; height:8px; margin-top:8px; border-radius:999px; background:var(--cyan); box-shadow:0 0 14px var(--cyan); animation:pulse 1.8s infinite; }}
  .brand h1 {{ margin:0; font-size:21px; line-height:1.1; letter-spacing:0; }}
  .brand h1 span {{ color:var(--cyan); }}
  .brand p, .tag-stack p, .kicker, .nav-item, .status, .metric-head span {{
    margin:0; font-family:"JetBrains Mono", ui-monospace, monospace; font-size:10px; font-weight:700; letter-spacing:.12em;
    text-transform:uppercase; color:var(--dim);
  }}
  nav {{ display:grid; gap:4px; }}
  .nav-item {{ display:flex; align-items:center; gap:12px; padding:11px 14px; border-radius:6px; transition:.18s ease; }}
  .nav-item:hover, .nav-item.active {{ color:var(--cyan); background:rgba(0,219,233,.08); }}
  .nav-item.active {{ border-right:2px solid var(--cyan); }}
  .nav-dot {{ width:7px; height:7px; border:1px solid currentColor; border-radius:999px; }}
  .tag-stack {{ margin-top:auto; padding:14px 10px; border-top:1px solid var(--line); }}
  .tag-stack div {{ display:flex; flex-wrap:wrap; gap:6px; margin-top:10px; }}
  .tag-stack span {{ font:10px "JetBrains Mono", ui-monospace, monospace; color:var(--cyan); border:1px solid rgba(0,219,233,.18); background:rgba(0,219,233,.05); padding:4px 6px; border-radius:4px; }}
  .operator {{ display:flex; gap:10px; align-items:center; padding:10px; background:rgba(17,19,24,.9); border:1px solid var(--line); border-radius:8px; }}
  .avatar {{ width:30px; height:30px; border-radius:6px; display:grid; place-items:center; color:var(--cyan); border:1px solid rgba(0,219,233,.28); background:linear-gradient(135deg, rgba(0,219,233,.12), rgba(107,124,255,.12)); font:700 10px "JetBrains Mono", monospace; }}
  .operator b, .operator span {{ display:block; font:10px "JetBrains Mono", ui-monospace, monospace; }}
  .operator span {{ color:var(--indigo); margin-top:2px; }}
  .main {{ flex:1; min-width:0; height:100vh; overflow:auto; }}
  .topbar {{
    position:sticky; top:0; z-index:5; height:56px; display:flex; align-items:center; justify-content:space-between; gap:18px;
    padding:0 24px; background:rgba(12,14,18,.82); backdrop-filter:blur(16px); border-bottom:1px solid rgba(59,73,75,.35);
  }}
  .topbar h2 {{ margin:0; font-size:13px; font-family:"JetBrains Mono", ui-monospace, monospace; letter-spacing:.2em; text-transform:uppercase; }}
  .topbar h2 span {{ color:var(--cyan); }}
  .top-meta {{ display:flex; gap:10px; align-items:center; color:var(--muted); font:10px "JetBrains Mono", ui-monospace, monospace; text-transform:uppercase; }}
  .top-meta i {{ width:6px; height:6px; border-radius:999px; background:var(--cyan); box-shadow:0 0 10px var(--cyan); }}
  .content {{ padding:18px 24px 32px; display:grid; gap:14px; }}
  .glass {{
    position:relative; overflow:hidden; background:var(--surface-panel); border:1px solid rgba(0,219,233,.10);
    border-radius:8px; box-shadow:0 4px 24px rgba(0,0,0,.28); backdrop-filter:blur(20px);
  }}
  .glass:hover {{ border-color:rgba(0,219,233,.24); background:rgba(21,24,30,.68); }}
  .scanline {{ position:absolute; left:0; right:0; height:1px; background:linear-gradient(to right, transparent, rgba(0,219,233,.18), transparent); animation:scan 6s linear infinite; pointer-events:none; }}
  .metric-grid {{ display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:12px; }}
  .metric {{ padding:16px; min-height:124px; }}
  .metric-head {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }}
  .metric-head i {{ width:9px; height:9px; border-radius:999px; box-shadow:0 0 12px currentColor; }}
  .metric-value {{ font:700 30px/1.1 "JetBrains Mono", ui-monospace, monospace; color:var(--text); letter-spacing:0; }}
  .metric-value small {{ margin-left:6px; font-size:10px; color:var(--dim); font-weight:500; }}
  .microbar {{ height:2px; margin-top:17px; background:rgba(132,148,149,.18); }}
  .microbar em {{ display:block; height:100%; box-shadow:0 0 9px currentColor; }}
  .company-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:12px; }}
  .company-card, .radar-panel, .heatmap-panel, .evidence-log, .detail-panel, .audit-panel, .source-panel, .criteria-panel {{ padding:18px; }}
  .section-head {{ display:flex; justify-content:space-between; gap:16px; align-items:flex-start; margin-bottom:16px; }}
  h2, h3 {{ margin:0; letter-spacing:0; }}
  h2 {{ font-size:20px; line-height:1.18; }}
  .status {{ display:inline-flex; align-items:center; border:1px solid rgba(0,219,233,.22); color:var(--cyan); background:rgba(0,219,233,.06); border-radius:4px; padding:5px 7px; white-space:nowrap; }}
  .status.low {{ border-color:rgba(255,107,107,.24); color:var(--danger); background:rgba(255,107,107,.06); }}
  .score-row {{ display:flex; justify-content:space-between; align-items:center; gap:18px; margin:10px 0; }}
  .score-main {{ font:700 48px/1 "JetBrains Mono", ui-monospace, monospace; color:var(--cyan); text-shadow:0 0 18px rgba(0,219,233,.18); }}
  .score-main small {{ font-size:13px; color:var(--dim); margin-left:4px; }}
  .ring {{ width:72px; height:72px; border-radius:999px; display:grid; place-items:center; background:conic-gradient(var(--cyan) var(--score), rgba(132,148,149,.14) 0); box-shadow:0 0 18px rgba(0,219,233,.08); }}
  .ring span {{ width:58px; height:58px; display:grid; place-items:center; border-radius:999px; background:var(--surface-low); font:700 11px "JetBrains Mono", monospace; color:var(--muted); }}
  .meta {{ color:var(--muted); margin:0 0 14px; font-size:12px; }}
  .split-list {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
  .split-list b {{ display:block; color:var(--cyan); font:700 10px "JetBrains Mono", monospace; letter-spacing:.12em; margin-bottom:6px; }}
  ul {{ margin:0; padding-left:16px; color:var(--muted); }}
  li {{ margin:0 0 6px; }}
  .warning {{ margin-top:12px; padding:9px 10px; color:#ffd8a8; border:1px solid rgba(211,164,75,.28); background:rgba(211,164,75,.07); border-radius:4px; font-size:12px; }}
  .audit-grid {{ display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:8px; }}
  .audit-row {{ min-height:58px; padding:10px; border:1px solid rgba(132,148,149,.15); background:rgba(8,10,13,.36); border-radius:5px; }}
  .audit-row span, .audit-columns b {{ display:block; color:var(--dim); font:700 9px "JetBrains Mono", ui-monospace, monospace; letter-spacing:.12em; text-transform:uppercase; margin-bottom:5px; }}
  .audit-row b {{ color:var(--text); font:700 11px "JetBrains Mono", ui-monospace, monospace; word-break:break-word; }}
  .audit-columns {{ display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:12px; margin-top:12px; }}
  .audit-columns div {{ border-top:1px solid rgba(132,148,149,.14); padding-top:10px; }}
  .audit-columns ul {{ color:var(--muted); font-size:12px; }}
  .audit-columns a, .source-list a {{ color:var(--cyan-soft); }}
  .criteria-layout {{ display:grid; grid-template-columns:minmax(0, 1.25fr) minmax(320px, .85fr); gap:14px; }}
  .criteria-layout h3 {{ color:var(--text); font:700 11px "JetBrains Mono", ui-monospace, monospace; letter-spacing:.12em; text-transform:uppercase; margin-bottom:10px; }}
  .criteria-tags {{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:8px; }}
  .criteria-tag {{ padding:10px; min-height:132px; border:1px solid rgba(132,148,149,.15); background:rgba(8,10,13,.38); border-radius:5px; }}
  .criteria-tag div {{ display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:6px; }}
  .criteria-tag span {{ color:var(--cyan); font:700 10px "JetBrains Mono", ui-monospace, monospace; }}
  .criteria-tag b {{ color:var(--text); font-size:13px; text-align:right; }}
  .criteria-tag p {{ margin:0; color:var(--muted); font-size:12px; }}
  .criteria-tag em {{ display:block; margin-top:8px; color:var(--indigo); font:10px "JetBrains Mono", ui-monospace, monospace; font-style:normal; }}
  .score-scale {{ list-style:none; padding:0; margin:0; display:grid; gap:7px; }}
  .score-scale li {{ display:grid; grid-template-columns:36px 1fr; gap:9px; padding:8px; border:1px solid rgba(132,148,149,.15); background:rgba(8,10,13,.34); border-radius:5px; }}
  .score-scale strong {{ display:grid; place-items:center; width:28px; height:28px; color:var(--cyan); border:1px solid rgba(0,219,233,.28); border-radius:4px; font:700 12px "JetBrains Mono", monospace; }}
  .score-scale b {{ display:block; color:var(--text); font-size:12px; }}
  .score-scale p {{ margin:2px 0 0; color:var(--muted); font-size:11px; }}
  .source-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
  .source-grid h3 {{ color:var(--text); font:700 11px "JetBrains Mono", ui-monospace, monospace; letter-spacing:.12em; text-transform:uppercase; margin-bottom:10px; }}
  .source-list {{ display:grid; gap:8px; }}
  .source-list p {{ color:var(--muted); margin:0; }}
  .source-link {{ display:block; padding:10px; border:1px solid rgba(132,148,149,.15); background:rgba(8,10,13,.38); border-radius:5px; transition:.16s ease; }}
  .source-link:hover {{ border-color:rgba(0,219,233,.34); background:rgba(0,219,233,.06); }}
  .source-link span {{ display:block; color:var(--cyan); font:700 9px "JetBrains Mono", ui-monospace, monospace; letter-spacing:.12em; text-transform:uppercase; margin-bottom:4px; }}
  .source-link b {{ display:block; color:var(--text); font-size:13px; }}
  .source-link em {{ display:block; color:var(--muted); font-size:11px; font-style:normal; margin-top:3px; }}
  .source-link.framework span {{ color:var(--indigo); }}
  .analytics-grid {{ display:grid; grid-template-columns:minmax(0, 1.6fr) minmax(320px, .9fr); gap:12px; }}
  .radar-layout {{ display:grid; grid-template-columns:360px minmax(260px,1fr); gap:18px; align-items:center; }}
  .radar {{ width:100%; max-width:360px; height:auto; }}
  .rings circle, .axes line {{ fill:none; stroke:rgba(160,176,177,.14); stroke-width:1; }}
  .labels text {{ fill:var(--muted); font:700 10px "JetBrains Mono", monospace; text-anchor:middle; dominant-baseline:middle; }}
  .legend {{ display:flex; flex-wrap:wrap; justify-content:flex-end; gap:10px; }}
  .legend span {{ display:flex; gap:6px; align-items:center; color:var(--muted); font:10px "JetBrains Mono", monospace; }}
  .legend i {{ width:8px; height:8px; border-radius:999px; }}
  .tag-bars {{ display:grid; gap:9px; }}
  .tag-bar {{ display:grid; grid-template-columns:170px 1fr 36px; align-items:center; gap:10px; }}
  .tag-bar b {{ color:var(--text); font:700 10px "JetBrains Mono", monospace; }}
  .tag-bar span {{ display:block; color:var(--dim); font-size:11px; }}
  .tag-bar em {{ height:2px; background:rgba(132,148,149,.18); }}
  .tag-bar i {{ display:block; height:100%; }}
  .tag-bar.high i {{ background:var(--cyan); box-shadow:0 0 8px rgba(0,219,233,.45); }}
  .tag-bar.mid i {{ background:var(--indigo); box-shadow:0 0 8px rgba(107,124,255,.35); }}
  .tag-bar.low i {{ background:var(--danger); box-shadow:0 0 8px rgba(255,107,107,.25); }}
  .tag-bar strong {{ font:700 11px "JetBrains Mono", monospace; color:var(--text); text-align:right; }}
  .table-scroll {{ overflow:auto; }}
  table {{ width:100%; min-width:760px; border-collapse:collapse; }}
  th, td {{ border-bottom:1px solid rgba(132,148,149,.14); padding:9px; text-align:left; }}
  th {{ color:var(--dim); font:700 10px "JetBrains Mono", monospace; letter-spacing:.12em; text-transform:uppercase; }}
  td button {{ width:100%; min-width:54px; border:1px solid rgba(255,255,255,.05); border-radius:5px; padding:7px 6px; color:var(--text); cursor:pointer; background:rgba(132,148,149,.13); }}
  td.high button {{ background:rgba(0,219,233,.14); border-color:rgba(0,219,233,.25); color:var(--cyan-soft); }}
  td.mid button {{ background:rgba(107,124,255,.14); border-color:rgba(107,124,255,.25); color:#dce2ff; }}
  td.low button {{ background:rgba(255,107,107,.12); border-color:rgba(255,107,107,.22); color:#ffd8d8; }}
  td small {{ display:block; font:9px "JetBrains Mono", monospace; color:var(--dim); text-transform:uppercase; }}
  .evidence-log ol {{ list-style:none; padding:0; margin:0; display:grid; gap:9px; max-height:376px; overflow:auto; }}
  .evidence-log li {{ border-left:1px solid rgba(0,219,233,.35); padding:8px 10px; background:rgba(0,219,233,.04); }}
  .evidence-log span {{ color:var(--cyan); font:10px "JetBrains Mono", monospace; }}
  .evidence-log b {{ margin-left:8px; font-size:12px; }}
  .evidence-log em {{ display:block; margin-top:3px; color:var(--indigo); font:10px "JetBrains Mono", monospace; font-style:normal; }}
  .evidence-log p {{ margin:5px 0 0; color:var(--muted); font-size:12px; }}
  .live-dot {{ width:7px; height:7px; border-radius:999px; background:var(--cyan); box-shadow:0 0 12px var(--cyan); animation:pulse 1.8s infinite; }}
  .detail-panel {{ display:grid; gap:12px; }}
  .detail {{ border-top:1px solid rgba(132,148,149,.16); padding-top:14px; }}
  .detail:first-of-type {{ border-top:0; padding-top:0; }}
  .detail.target {{ outline:1px solid rgba(0,219,233,.35); background:rgba(0,219,233,.04); border-radius:6px; padding:14px; }}
  .detail-head {{ display:grid; grid-template-columns:46px 1fr 54px; gap:10px; align-items:center; margin-bottom:8px; }}
  .detail-head span {{ color:var(--cyan); font:700 11px "JetBrains Mono", monospace; }}
  .detail-head h3 {{ font-size:15px; }}
  .detail-head b {{ color:var(--cyan-soft); font:700 12px "JetBrains Mono", monospace; text-align:right; }}
  .detail p {{ margin:5px 0; color:var(--muted); font-size:12px; }}
  .detail p b {{ color:var(--text); }}
  .detail ul {{ margin-top:9px; padding:0; list-style:none; }}
  .detail li {{ padding:8px 10px; border:1px solid rgba(132,148,149,.14); border-radius:5px; background:rgba(8,10,13,.42); }}
  .detail li strong {{ color:var(--cyan); font:700 10px "JetBrains Mono", monospace; }}
  .detail li span {{ color:var(--dim); font-size:11px; margin-left:6px; }}
  blockquote {{ margin:6px 0 0; padding-left:10px; border-left:2px solid rgba(0,219,233,.26); color:var(--muted); }}
  @keyframes scan {{ from {{ top:-5%; }} to {{ top:105%; }} }}
  @keyframes pulse {{ 0%, 100% {{ opacity:1; }} 50% {{ opacity:.35; }} }}
  @media (max-width: 980px) {{
    body {{ overflow:auto; }}
    .shell {{ display:block; }}
    .sidebar {{ display:none; }}
    .main {{ height:auto; overflow:visible; }}
    .metric-grid, .analytics-grid, .radar-layout {{ grid-template-columns:1fr; }}
    .topbar {{ padding:0 16px; }}
    .content {{ padding:14px 14px 80px; }}
    .split-list {{ grid-template-columns:1fr; }}
    .audit-grid, .audit-columns, .source-grid, .criteria-layout, .criteria-tags {{ grid-template-columns:1fr; }}
  }}
  @media (max-width: 620px) {{
    .metric-grid, .company-grid {{ grid-template-columns:1fr; }}
    .top-meta {{ display:none; }}
    .score-main {{ font-size:40px; }}
    .company-card, .radar-panel, .heatmap-panel, .evidence-log, .detail-panel, .criteria-panel {{ padding:14px; }}
  }}
</style>
</head>
<body>
<div class="shell">
  {render_shell_nav(ja)}
  <main class="main">
    <header class="topbar">
      <h2>{tr("topbar", ja)}</h2>
      <div class="top-meta"><span>{company_count} {esc(tr("companies", ja))}</span><span>FY {esc(year_span or 'N/A')}</span><i></i><span>{esc(tr("trace_ready", ja))}</span></div>
    </header>
    <div class="content">
      {render_metric_cards(results)}
      <div class="company-grid">{render_company_cards(results)}</div>
      {render_scoring_criteria(results)}
      {render_audit_panel(results)}
      <div class="analytics-grid">
        {render_radar(results)}
        {render_evidence_log(results)}
      </div>
      {render_heatmap(results)}
      {render_source_links_panel(results)}
      {render_details(results)}
    </div>
  </main>
</div>
<script type="application/json" id="scoring-data">{data_json}</script>
<script>
  const detailPanels = [...document.querySelectorAll('.detail')];
  document.querySelectorAll('.heatmap button').forEach((button) => {{
    button.addEventListener('click', () => {{
      detailPanels.forEach((panel) => panel.classList.remove('target'));
      const target = detailPanels.find((panel) => panel.dataset.company === button.dataset.company && panel.dataset.tag === button.dataset.tag);
      if (target) {{
        target.classList.add('target');
        target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}
    }});
  }});
</script>
</body>
</html>
"""


def main(argv):
    if len(argv) != 3:
        print("Usage: build_dashboard.py scoring.json dashboard.html", file=sys.stderr)
        return 2
    results = load_results(Path(argv[1]))
    html_text = "\n".join(line.rstrip() for line in build_html(results).splitlines()) + "\n"
    Path(argv[2]).write_text(html_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

import streamlit as st


def render_navbar(keys_configured: bool):
    status_html = (
        '<span class="nav-status nav-online"><span class="dot" style="background:#10B981;"></span>Live Web Grounding Active</span>'
        if keys_configured
        else '<span class="nav-status nav-offline"><span class="dot" style="background:#EF4444;"></span>API Keys Missing</span>'
    )
    st.markdown(
        f"""
        <div class="navbar">
            <div class="nav-brand">
                <span class="nav-logo-mark"></span>
                <span>FactLens</span>
                <span class="nav-tagline">&middot; Live Claim &amp; Source Audit</span>
            </div>
            <div>{status_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-pill">Interactive Document Fact-Checking Workspace</div>
            <div class="hero-heading">Verify Every Statistic, Date, and Claim Before You Publish.</div>
            <p class="hero-lead">
                FactLens parses PDF reports, pitch decks, and research whitepapers, isolates every verifiable factual assertion, and cross-examines it against live web sources to catch outdated metrics and AI hallucinations.
            </p>
            <div class="hero-pillars">
                <div class="pillar-box">
                    <div class="pillar-step">Step 01 &middot; Extraction</div>
                    <div class="pillar-title">Isolate Factual Claims</div>
                    <div class="pillar-desc">Automatically detects statistics, financial valuations, timelines, and technical benchmarks across every page of your document.</div>
                </div>
                <div class="pillar-box">
                    <div class="pillar-step">Step 02 &middot; Live Grounding</div>
                    <div class="pillar-title">Cross-Examine on the Web</div>
                    <div class="pillar-desc">Queries live search indexes in real time to verify extracted claims against authoritative primary sources and current data.</div>
                </div>
                <div class="pillar-box">
                    <div class="pillar-step">Step 03 &middot; Audit Dashboard</div>
                    <div class="pillar-title">Surface Ground Truth</div>
                    <div class="pillar-desc">Flags false or outdated figures side-by-side with corrected facts, confidence scores, and exportable audit reports.</div>
                </div>
            </div>
            <a href="#upload-workspace" class="scroll-cue">Scroll Down to Upload &amp; Audit Document &darr;</a>
        </div>
        <div id="upload-workspace"></div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(eyebrow: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="web-section-header">
            <div class="web-section-eyebrow">{eyebrow}</div>
            <div class="web-section-title">{title}</div>
            <div class="web-section-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_grid(total: int, verified: int, inaccurate: int, false: int, trust_score: int):
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card kpi-trust">
                <div class="kpi-label" style="color:#A5B4FC;">Document Trust Score</div>
                <div class="kpi-value" style="color:#818CF8;">{trust_score}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label" style="color:#A1A1AA;">Claims Audited</div>
                <div class="kpi-value" style="color:#FFFFFF;">{total}</div>
            </div>
            <div class="kpi-card kpi-verified">
                <div class="kpi-label" style="color:#34D399;">Verified Accurate</div>
                <div class="kpi-value" style="color:#10B981;">{verified}</div>
            </div>
            <div class="kpi-card kpi-inaccurate">
                <div class="kpi-label" style="color:#FBBF24;">Inaccurate / Outdated</div>
                <div class="kpi-value" style="color:#F59E0B;">{inaccurate}</div>
            </div>
            <div class="kpi-card kpi-false">
                <div class="kpi-label" style="color:#F87171;">False / Fabricated</div>
                <div class="kpi-value" style="color:#EF4444;">{false}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_claim_card(r: dict):
    status = r["status"]
    if status == "Verified":
        badge_html = '<span class="badge badge-verified"><span class="dot"></span>Verified</span>'
        card_border = "#10B981"
    elif status == "Inaccurate":
        badge_html = '<span class="badge badge-inaccurate"><span class="dot"></span>Inaccurate / Outdated</span>'
        card_border = "#F59E0B"
    else:
        badge_html = '<span class="badge badge-false"><span class="dot"></span>False / Fabricated</span>'
        card_border = "#EF4444"

    st.markdown(
        f"""
        <div class="claim-card" style="border-left: 4px solid {card_border};">
            <div class="claim-header">
                {badge_html}
                <span class="meta-pill">Claim #{r['id']}</span>
                <span class="meta-pill">Page {r['page']}</span>
                <span class="meta-pill">{r['category']}</span>
                <span class="meta-pill">{r['confidence']}% Confidence</span>
            </div>
            <div class="compare-grid">
                <div class="compare-box-claim">
                    <div class="box-label" style="color:#A1A1AA;">Extracted Document Claim</div>
                    <div class="box-text-claim">“{r['claim']}”</div>
                </div>
                <div class="compare-box-truth">
                    <div class="box-label" style="color:#818CF8;">Live Web Ground Truth</div>
                    <div class="box-text-truth">{r['real_fact']}</div>
                </div>
            </div>
            <p class="analysis-text"><strong>Audit Analysis:</strong> {r['explanation']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander(f"Inspect Live Web Sources & Search Query — Claim #{r['id']}"):
        st.caption(f"Search Query Executed: `{r['search_query']}`")
        if r["all_sources"]:
            for src in r["all_sources"]:
                st.markdown(f"- [{src['title']}]({src['url']})")
        else:
            st.write("No corroborating web sources returned for this query.")
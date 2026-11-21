import inspect
import json
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from components import (
    render_claim_card,
    render_hero,
    render_kpi_grid,
    render_navbar,
    render_section_header,
)
from fact_checker import extract_claims, extract_text_from_pdf, verify_claims_batch
from styles import inject_custom_css

load_dotenv()

st.set_page_config(
    page_title="FactLens | Live Claim & Source Audit",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_custom_css()

# Newer Streamlit versions use width="stretch"; older ones use
# use_container_width=True. This works on both.
if "width" in inspect.signature(st.download_button).parameters:
    STRETCH = {"width": "stretch"}
else:
    STRETCH = {"use_container_width": True}


def get_secret(key_name: str) -> str:
    env_val = os.getenv(key_name, "").strip()
    if env_val:
        return env_val
    try:
        return str(st.secrets.get(key_name, "")).strip()
    except Exception:
        return ""


def friendly_error(error: Exception) -> str:
    """Turn raw API errors into a short, readable message."""

    message = str(error)

    if any(c in message for c in ("503", "UNAVAILABLE", "high demand")):
        return "The AI service is busy right now. Please wait about 30 seconds and try again."
    if any(c in message for c in ("429", "RESOURCE_EXHAUSTED", "quota")):
        return "The API request limit was reached. Please wait a minute and try again."
    if any(c in message for c in ("API key", "API_KEY", "401", "403")):
        return "An API key was rejected. Please check GEMINI_API_KEY and TAVILY_API_KEY."
    if any(c in message.lower() for c in ("timed out", "timeout", "504", "deadline")):
        return "The AI took too long to respond. Please try again."
    return "Something went wrong while auditing the document."


gemini_key = get_secret("GEMINI_API_KEY")
tavily_key = get_secret("TAVILY_API_KEY")
keys_configured = bool(gemini_key and tavily_key)

# =========================================================
# SECTION 1: TOP NAVBAR & WEBSITE HERO SECTION
# =========================================================
render_navbar(keys_configured)
render_hero()

# =========================================================
# SECTION 2: DOCUMENT UPLOAD & AUDIT TRIGGER
# =========================================================
render_section_header(
    eyebrow="Document Ingestion",
    title="Upload a PDF Document to Audit",
    subtitle="Upload any multi-page report, presentation deck, or whitepaper to begin automated claim extraction and web verification.",
)

uploaded_file = st.file_uploader(
    "Upload PDF Document",
    type=["pdf"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    st.markdown(
        f"""
        <div class="file-strip">
            <span class="file-strip-name">{uploaded_file.name}</span>
            <span class="file-strip-meta">{round(uploaded_file.size / 1024, 1)} KB &middot; Ready for Verification</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    run_audit = st.button("Run Fact-Check Audit", type="primary", **STRETCH)
else:
    run_audit = False

if uploaded_file is not None and run_audit:
    if not keys_configured:
        st.error("API credentials missing. Please configure `GEMINI_API_KEY` and `TAVILY_API_KEY` in `.env` or Streamlit Secrets.")
        st.stop()

    pdf_bytes = uploaded_file.read()
    error_message, error_details = None, None

    with st.status("Running FactLens verification pipeline...", expanded=True) as status:
        try:
            st.write("Parsing PDF pages and extracting structured text...")
            raw_text = extract_text_from_pdf(pdf_bytes)

            if not raw_text.strip():
                status.update(label="Text extraction failed", state="error")
                st.error("No readable text found. Please upload a text-based PDF.")
                st.stop()

            st.write("Extracting verifiable statistics, financial figures, dates, and technical claims...")
            claims = extract_claims(raw_text, gemini_key)

            if not claims:
                status.update(label="No factual claims detected", state="complete")
                st.warning("No concrete factual claims or statistics were found in this document.")
                st.stop()

            st.write(f"Cross-examining {len(claims)} claims against live web search indexes...")
            progress_bar = st.progress(0)
            status_text = st.empty()

            def update_progress(pct: float, msg: str):
                progress_bar.progress(min(pct, 1.0))
                status_text.write(msg)

            results = verify_claims_batch(claims, gemini_key, tavily_key, progress_callback=update_progress)

            st.session_state["audit_results"] = results
            st.session_state["audited_filename"] = uploaded_file.name
            status.update(label=f"Verification complete — {len(results)} claims audited", state="complete", expanded=False)

        except Exception as error:
            error_message, error_details = friendly_error(error), str(error)
            status.update(label="Audit failed", state="error", expanded=True)

    if error_message:
        st.error(error_message)
        with st.expander("Technical details"):
            st.code(error_details)

# =========================================================
# SECTION 3: INTERACTIVE AUDIT DASHBOARD
# =========================================================
if "audit_results" in st.session_state and st.session_state["audit_results"]:
    results = st.session_state["audit_results"]
    total = len(results)
    verified_cnt = sum(1 for r in results if r["status"] == "Verified")
    inaccurate_cnt = sum(1 for r in results if r["status"] == "Inaccurate")
    false_cnt = sum(1 for r in results if r["status"] == "False")
    trust_score = round((verified_cnt / total) * 100) if total else 0

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    render_section_header(
        eyebrow="Verification Dashboard",
        title="Audit Results & Ground Truth Analysis",
        subtitle=f"Audited Document: {st.session_state.get('audited_filename', 'Document')}",
    )

    render_kpi_grid(
        total=total,
        verified=verified_cnt,
        inaccurate=inaccurate_cnt,
        false=false_cnt,
        trust_score=trust_score,
    )

    df_export = pd.DataFrame(
        [
            {
                "ID": r["id"],
                "Page": r["page"],
                "Verdict": r["status"],
                "Category": r["category"],
                "Confidence": f"{r['confidence']}%",
                "Extracted PDF Claim": r["claim"],
                "Live Web Ground Truth": r["real_fact"],
                "Primary Source": r["source_url"],
            }
            for r in results
        ]
    )

    with st.expander("Executive Summary Table (All Extracted Claims)", expanded=True):
        st.dataframe(df_export, hide_index=True, **STRETCH)

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    col_filter, col_csv, col_json = st.columns([3.2, 0.7, 0.7], vertical_alignment="bottom")
    with col_filter:
        status_filter = st.multiselect(
            "Filter Detailed Cards by Verdict",
            options=["False", "Inaccurate", "Verified"],
            default=["False", "Inaccurate", "Verified"],
        )
    with col_csv:
        st.download_button(
            "Export CSV",
            data=df_export.to_csv(index=False).encode("utf-8"),
            file_name="factlens_audit_report.csv",
            mime="text/csv",
            **STRETCH,
        )
    with col_json:
        st.download_button(
            "Export JSON",
            data=json.dumps(results, indent=2).encode("utf-8"),
            file_name="factlens_audit_report.json",
            mime="application/json",
            **STRETCH,
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    filtered_results = [r for r in results if r["status"] in status_filter]
    if not filtered_results:
        st.info("No claims match the selected filter.")

    for r in filtered_results:
        render_claim_card(r)
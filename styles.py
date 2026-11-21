import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        *, *::before, *::after {
            box-sizing: border-box;
        }

        html {
            font-size: 16px !important;
            scroll-behavior: smooth;
        }

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        html, body, .stApp {
            overflow-x: hidden;
        }

        /* Pitch-Black Canvas */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background-color: #050507 !important;
            color: #FAFAFA;
        }

        /* Hide Streamlit Header, Deploy Toolbar, Menu & Sidebar */
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        #MainMenu,
        footer,
        section[data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }

        /* =========================================================
           PAGE WIDTH: one centered column for EVERY section.
           The padding lives on the inner block (not the outer
           container), so content can never touch the screen edge.
           ========================================================= */
        .stApp .block-container,
        .stApp [data-testid="stMainBlockContainer"] {
            width: 100% !important;
            max-width: 100% !important;
            padding: 1.25rem 0 7rem 0 !important;
        }

        .stApp [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
            width: 100% !important;
            max-width: 1180px !important;
            margin: 0 auto !important;
            padding: 0 2rem !important;
        }

        /* Top Navbar */
        .navbar {
            width: 100%;
            height: 66px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1.5rem;
            background-color: #0B0B10;
            border: 1px solid #1E1E28;
            border-radius: 14px;
            margin-bottom: 1.5rem;
        }
        .nav-brand {
            font-size: 20px !important;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .nav-tagline {
            font-size: 14px !important;
            font-weight: 500;
            color: #8E8E9E;
        }
        .nav-logo-mark {
            width: 12px;
            height: 12px;
            border-radius: 3px;
            background: linear-gradient(135deg, #6366F1, #A855F7);
            display: inline-block;
            flex-shrink: 0;
        }
        .nav-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 13px !important;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 999px;
            white-space: nowrap;
        }
        .nav-online {
            background-color: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.35);
            color: #34D399;
        }
        .nav-offline {
            background-color: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.35);
            color: #F87171;
        }

        /* =========================================================
           FIRST PAGE: HERO CONTAINER
           ========================================================= */
        .hero-section {
            width: 100%;
            min-height: min(calc(100vh - 115px), 900px);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 3.5rem 2.5rem;
            background: radial-gradient(ellipse at top center, rgba(99, 102, 241, 0.18) 0%, #0A0A0F 72%);
            border: 1px solid #1E1E28;
            border-radius: 18px;
            margin-bottom: 2rem;
        }
        .hero-pill {
            display: inline-block;
            background: rgba(99, 102, 241, 0.16);
            border: 1px solid rgba(99, 102, 241, 0.38);
            color: #A5B4FC;
            font-size: 13px !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 7px 18px;
            border-radius: 999px;
            margin-bottom: 1.5rem;
        }
        .hero-heading {
            font-size: 50px !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            letter-spacing: -0.03em;
            line-height: 1.15 !important;
            margin: 0 auto 1.25rem auto !important;
            max-width: 860px;
        }
        .hero-lead {
            font-size: 19px !important;
            color: #B4B4BE !important;
            line-height: 1.7 !important;
            margin: 0 auto 3rem auto !important;
            max-width: 760px;
        }

        /* Step cards: taller, with larger text */
        .hero-pillars {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1.5rem;
            width: 100%;
            max-width: 1100px;
            margin: 0 auto 2.5rem auto;
            text-align: left;
            align-items: stretch;
        }
        .pillar-box {
            background-color: #0E0E15;
            border: 1px solid #262636;
            border-radius: 18px;
            padding: 2.6rem 2.2rem !important;
            min-height: 360px !important;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .pillar-step {
            font-size: 14px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: #818CF8 !important;
            margin-bottom: 16px !important;
        }
        .pillar-title {
            font-size: 27px !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            line-height: 1.3 !important;
            margin-bottom: 16px !important;
        }
        .pillar-desc {
            font-size: 17.5px !important;
            color: #C4C4CE !important;
            line-height: 1.75 !important;
            margin: 0 !important;
        }

        /* Scroll Prompt Pill */
        .scroll-cue {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 15px !important;
            font-weight: 600 !important;
            color: #C7D2FE !important;
            background-color: rgba(99, 102, 241, 0.14);
            border: 1px solid rgba(99, 102, 241, 0.35);
            padding: 12px 26px;
            border-radius: 999px;
            text-decoration: none !important;
        }
        .scroll-cue:hover {
            background-color: rgba(99, 102, 241, 0.24);
            border-color: #818CF8;
        }

        /* =========================================================
           SECOND PAGE: UPLOAD WORKSPACE
           ========================================================= */
        #upload-workspace {
            scroll-margin-top: 1.5rem;
            height: 1px;
        }

        .workspace-card {
            background-color: #0A0A0F;
            border: 1px solid #1E1E28;
            border-radius: 18px;
            padding: 2rem 2rem 0.5rem 2rem;
            margin-bottom: 1.25rem;
        }

        .web-section-header {
            width: 100%;
            margin: 1rem 0 1.5rem 0;
        }
        .web-section-eyebrow {
            font-size: 13px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: #818CF8 !important;
            margin-bottom: 8px;
        }
        .web-section-title {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            letter-spacing: -0.02em;
            line-height: 1.25;
            margin: 0;
        }
        .web-section-sub {
            font-size: 17px !important;
            color: #B4B4BE !important;
            line-height: 1.6;
            margin-top: 8px;
            max-width: 760px;
        }

        /* File uploader: stays inside the page column, never clipped */
        [data-testid="stFileUploader"] {
            width: 100% !important;
            max-width: 100% !important;
            background: linear-gradient(180deg, #0E0E16 0%, #09090D 100%) !important;
            border: 1.5px dashed #333347 !important;
            border-radius: 16px !important;
            padding: 2.5rem 1.5rem !important;
            margin-bottom: 1.25rem !important;
            overflow: hidden !important;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #6366F1 !important;
        }
        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploaderDropzone"] {
            width: 100% !important;
            max-width: 100% !important;
            background-color: transparent !important;
            border: none !important;
            padding: 0.5rem 0 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            gap: 0.9rem !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] span {
            font-size: 17px !important;
            font-weight: 600 !important;
            color: #F4F4F5 !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] small {
            font-size: 14.5px !important;
            color: #9A9AAA !important;
            margin-top: 4px !important;
        }
        /* Only the main Browse/Upload button is filled indigo */
        [data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] {
            background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 28px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3) !important;
        }
        /* The small remove (x) and add (+) buttons next to an uploaded file stay quiet */
        [data-testid="stFileUploader"] button[data-testid="stBaseButton-minimal"],
        [data-testid="stFileUploader"] button[data-testid="stBaseButton-borderlessIcon"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 4px 8px !important;
            color: #C7D2FE !important;
        }
        [data-testid="stFileUploaderFile"] {
            width: 100% !important;
            max-width: 620px !important;
            margin: 0.75rem auto 0 auto !important;
            background-color: #13131C !important;
            border: 1px solid #2A2A3B !important;
            border-radius: 10px !important;
            padding: 0.65rem 1rem !important;
        }
        [data-testid="stFileUploaderFileName"] {
            max-width: 100% !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            white-space: nowrap !important;
            color: #F4F4F5 !important;
        }

        /* Unified File Action Strip */
        .file-strip {
            width: 100%;
            background-color: #0E0E14;
            border: 1px solid #262633;
            border-left: 4px solid #6366F1;
            border-radius: 12px;
            padding: 0.9rem 1.35rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        .file-strip-name {
            font-size: 16px !important;
            font-weight: 600 !important;
            color: #FFFFFF !important;
            overflow-wrap: anywhere;
        }
        .file-strip-meta {
            font-size: 14px !important;
            font-weight: 600 !important;
            color: #A5B4FC !important;
        }

        /* Primary CTA Button */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            height: 54px !important;
            min-height: 54px !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.28) !important;
        }

        /* =========================================================
           DARK STYLING FOR STREAMLIT'S OWN WIDGETS
           ========================================================= */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label,
        label {
            color: #D4D4D8;
        }
        /* Button labels keep the button's own color */
        .stButton button p,
        .stDownloadButton button p,
        [data-testid="stFileUploader"] button p {
            color: inherit !important;
        }
        [data-testid="stExpander"] {
            background-color: #0B0B0F !important;
            border: 1px solid #1E1E28 !important;
            border-radius: 12px !important;
        }
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p {
            color: #F4F4F5 !important;
            font-weight: 600 !important;
        }
        [data-testid="stStatus"],
        [data-testid="stStatusContainer"] {
            background-color: #0B0B0F !important;
            border: 1px solid #1E1E28 !important;
            border-radius: 12px !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #0E0E14 !important;
            border-color: #262633 !important;
            color: #F4F4F5 !important;
        }
        [data-testid="stDataFrame"] {
            border: 1px solid #1E1E28;
            border-radius: 12px;
            overflow: hidden;
        }
        [data-testid="stAlert"] {
            border-radius: 12px !important;
        }

        /* Equal-Height KPI Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 1rem;
            align-items: stretch;
            margin-top: 1rem;
            margin-bottom: 1.75rem;
        }
        .kpi-card {
            background-color: #0B0B0F;
            border-radius: 12px;
            padding: 1.25rem 1.35rem;
            border: 1px solid #1E1E26;
            min-height: 112px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .kpi-trust { border-color: rgba(99, 102, 241, 0.45); background: linear-gradient(180deg, #111122 0%, #0B0B0F 100%); }
        .kpi-verified { border-color: rgba(16, 185, 129, 0.4); background: linear-gradient(180deg, #0B1915 0%, #0B0B0F 100%); }
        .kpi-inaccurate { border-color: rgba(245, 158, 11, 0.4); background: linear-gradient(180deg, #1A150B 0%, #0B0B0F 100%); }
        .kpi-false { border-color: rgba(239, 68, 68, 0.4); background: linear-gradient(180deg, #1C0D11 0%, #0B0B0F 100%); }

        .kpi-label {
            font-size: 12px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .kpi-value {
            font-size: 32px !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em;
            margin-top: 6px;
        }

        /* Side-by-Side Comparison Claim Card */
        .claim-card {
            background-color: #0B0B0F;
            border: 1px solid #1E1E26;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 0.85rem;
        }
        .claim-header {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-bottom: 1rem;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 12px !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
        }
        .badge-verified { background-color: rgba(16, 185, 129, 0.14); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.35); }
        .badge-verified .dot { background-color: #10B981; }
        .badge-inaccurate { background-color: rgba(245, 158, 11, 0.14); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.35); }
        .badge-inaccurate .dot { background-color: #F59E0B; }
        .badge-false { background-color: rgba(239, 68, 68, 0.14); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.35); }
        .badge-false .dot { background-color: #EF4444; }

        .meta-pill {
            background-color: #15151D;
            color: #D4D4D8;
            border: 1px solid #262633;
            padding: 4px 11px;
            border-radius: 6px;
            font-size: 13px !important;
            font-weight: 500;
        }

        /* Two-Column Claim vs Ground Truth Grid */
        .compare-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
            align-items: stretch;
            margin-bottom: 1rem;
        }
        .compare-box-claim {
            background-color: #121218;
            border: 1px solid #252530;
            border-radius: 10px;
            padding: 1.1rem 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .compare-box-truth {
            background-color: #101221;
            border: 1px solid #282B4A;
            border-left: 3.5px solid #6366F1;
            border-radius: 10px;
            padding: 1.1rem 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .box-label {
            font-size: 12px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
        }
        .box-text-claim {
            font-size: 15.5px !important;
            font-weight: 600 !important;
            color: #FFFFFF !important;
            line-height: 1.55;
            overflow-wrap: anywhere;
        }
        .box-text-truth {
            font-size: 15px !important;
            font-weight: 500 !important;
            color: #E0E7FF !important;
            line-height: 1.55;
            overflow-wrap: anywhere;
        }
        .analysis-text {
            font-size: 14.5px !important;
            color: #A1A1AA !important;
            line-height: 1.6;
            margin: 0;
        }
        .analysis-text strong {
            color: #E4E4E7;
        }

        /* Export Buttons */
        div.stDownloadButton > button {
            background-color: #0E0E14 !important;
            color: #F4F4F5 !important;
            border: 1px solid #262633 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            height: 44px !important;
            min-height: 44px !important;
        }

        /* =========================================================
           RESPONSIVE
           ========================================================= */
        @media (min-width: 901px) {
            .pillar-title { min-height: 70px; }
        }
        @media (max-width: 1024px) {
            .kpi-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
            .hero-heading { font-size: 42px !important; }
        }
        @media (max-width: 900px) {
            .hero-pillars { grid-template-columns: 1fr; }
            .pillar-box { min-height: auto !important; }
        }
        @media (max-width: 768px) {
            .stApp [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
                padding: 0 1rem !important;
            }
            .hero-section { min-height: auto; padding: 2rem 1.25rem; }
            .hero-heading { font-size: 32px !important; }
            .hero-lead { font-size: 17px !important; }
            .nav-tagline { display: none; }
            .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .compare-grid { grid-template-columns: 1fr; }
            .web-section-title { font-size: 26px !important; }
        }
        @media (max-width: 480px) {
            .kpi-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
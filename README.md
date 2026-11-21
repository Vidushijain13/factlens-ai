# 🛡️ FactLens AI — Automated PDF Fact-Check Agent

An automated **Fact-Checking Web App** built with **Streamlit**, **Google Gemini (`gemini-2.5-flash`)**, and **Tavily Live Web Search**. Designed as a "Truth Layer" to audit marketing collateral, reports, and decks for outdated statistics, exaggerated figures, and hallucinated claims.

## ✨ Key Features
- **Automated Claim Extraction:** Parses uploaded PDFs page-by-page and isolates verifiable statistics, dates, financial metrics, and technical benchmarks.
- **Real-Time Web Cross-Referencing:** Runs live web searches against authoritative sources for every extracted claim.
- **3-Tier Verdict Engine:** Classifies every claim as **Verified**, **Inaccurate**, or **False**, accompanied by the corrected real-world facts and clickable source citations.
- **Executive Audit Dashboard:** Displays overall document Trust Score, filterable claim cards, and one-click CSV/JSON report downloads.

## 🚀 Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/truthlayer-fact-checker.git
   cd truthlayer-fact-checker
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

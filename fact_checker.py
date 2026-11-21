import time
from typing import List, Literal
import fitz  # PyMuPDF
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from tavily import TavilyClient

MODELS_TO_TRY = [
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.8-flash-lite",
]


# --- Structured Output Schemas ---
class ExtractedClaim(BaseModel):
    claim_id: int = Field(description="Sequential ID starting from 1")
    claim_text: str = Field(description="Exact or tightly paraphrased factual claim from the PDF")
    category: Literal["Statistic", "Financial Figure", "Date / Timeline", "Technical / Product Spec", "Market / Company Fact"]
    page_number: int = Field(description="Page number where the claim appears")
    search_query: str = Field(description="Concise, targeted web search query to verify this claim")


class ClaimExtractionList(BaseModel):
    claims: List[ExtractedClaim]


class VerificationVerdict(BaseModel):
    claim_id: int = Field(description="Matching claim_id from the input batch")
    status: Literal["Verified", "Inaccurate", "False"] = Field(
        description=(
            "Verified: Matches authoritative live web data. "
            "Inaccurate: Partially true, outdated statistic, wrong number/date, or misrepresented context. "
            "False: Fabricated, hallucinated, or contradicted with zero credible evidence."
        )
    )
    confidence_score: int = Field(description="Confidence from 0 to 100")
    real_fact: str = Field(description="The accurate, up-to-date fact with real numbers/dates based on web results")
    explanation: str = Field(description="Clear explanation comparing the PDF claim against live web evidence")
    best_source_title: str = Field(description="Title of the primary corroborating/refuting web source")
    best_source_url: str = Field(description="URL of the primary web source")


class BatchVerificationList(BaseModel):
    verdicts: List[VerificationVerdict]


# --- Helper: Resilient Gemini Call with Retry & Fallback ---
def _call_gemini_with_fallback(client: genai.Client, prompt: str, schema, temperature: float):
    last_error = None
    for model_name in MODELS_TO_TRY:
        for attempt in range(3):
            try:
                return client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema,
                        temperature=temperature,
                    ),
                )
            except Exception as e:
                last_error = e
                err_str = str(e)
                if "503" in err_str or "UNAVAILABLE" in err_str:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                else:
                    break
    raise last_error


# --- PDF Extraction ---
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts text page-by-page from uploaded PDF bytes."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages_text = []
    for idx, page in enumerate(doc):
        text = page.get_text("text").strip()
        if text:
            pages_text.append(f"--- PAGE {idx + 1} ---\n{text}")
    return "\n\n".join(pages_text)


# --- Step 1: Extract Claims using Gemini (1 API Call) ---
def extract_claims(document_text: str, gemini_api_key: str) -> List[ExtractedClaim]:
    """Identifies specific, verifiable factual claims from PDF text."""
    client = genai.Client(api_key=gemini_api_key)

    prompt = f"""
    You are a strict Fact-Checking Extraction Agent auditing marketing, technical, and business documents.
    Analyze the following document text and extract ALL specific, verifiable factual claims—especially:
    - Statistics, percentages, growth rates, and survey figures
    - Financial metrics (revenues, valuations, funding rounds, market sizes)
    - Dates, timelines, launch years, and historical milestones
    - Technical benchmarks, LLM specs, hardware counts, and product claims

    Ignore purely subjective fluff. Focus on concrete assertions that can be proven true or false on the web.
    Create an optimal search query for each claim.

    DOCUMENT TEXT:
    {document_text[:35000]}
    """

    response = _call_gemini_with_fallback(
        client=client,
        prompt=prompt,
        schema=ClaimExtractionList,
        temperature=0.1,
    )

    parsed = ClaimExtractionList.model_validate_json(response.text)
    return parsed.claims


# --- Step 2: Batched Live Web Search + Verification (1 Call per Batch of 8 Claims) ---
def verify_claims_batch(
    claims: List[ExtractedClaim],
    gemini_api_key: str,
    tavily_api_key: str,
    progress_callback=None,
) -> List[dict]:
    """Searches the live web via Tavily for all claims, then evaluates them in compact batches."""
    tavily = TavilyClient(api_key=tavily_api_key)
    client = genai.Client(api_key=gemini_api_key)

    # 1. Gather live web evidence for each claim via Tavily
    evidence_map = {}
    total = len(claims)

    for idx, claim in enumerate(claims):
        if progress_callback:
            progress_callback(
                (idx + 1) / (total * 2),
                f"Searching live web sources for Claim {claim.claim_id} of {total}: {claim.claim_text[:75]}...",
            )
        try:
            search_res = tavily.search(
                query=claim.search_query,
                search_depth="advanced",
                max_results=3,
            )
            results = search_res.get("results", [])
        except Exception:
            results = []

        evidence_map[claim.claim_id] = results

    # 2. Judge claims in batches of 8 to save 85%+ of Gemini API quota
    batch_size = 8
    verdict_lookup = {}

    for start in range(0, total, batch_size):
        batch = claims[start : start + batch_size]
        if progress_callback:
            progress_callback(
                0.5 + ((start + len(batch)) / (total * 2)),
                f"Evaluating Claims {batch[0].claim_id}–{batch[-1].claim_id} against live web evidence...",
            )

        batch_blocks = []
        for c in batch:
            sources = evidence_map.get(c.claim_id, [])
            formatted_sources = "\n".join(
                [
                    f"    * Title: {r.get('title')}\n      URL: {r.get('url')}\n      Snippet: {r.get('content')}"
                    for r in sources
                ]
            ) or "    * No search results returned."

            batch_blocks.append(
                f"CLAIM ID: {c.claim_id} (Page {c.page_number} | {c.category})\n"
                f"CLAIM TEXT: \"{c.claim_text}\"\n"
                f"WEB EVIDENCE:\n{formatted_sources}"
            )

        judge_prompt = f"""
        You are an objective Fact-Checking Judge. Evaluate EVERY claim below against its attached LIVE WEB EVIDENCE.

        CLASSIFICATION RULES:
        1. "Verified": Live web evidence clearly confirms the exact numbers, dates, and facts in the claim.
        2. "Inaccurate": Underlying topic exists, OR stat was true in an older year, OR number/percentage/date is wrong/exaggerated/outdated.
        3. "False": Claim is completely fabricated, hallucinated, attributed to a non-existent report/event, or contradicted with zero credible evidence.

        CRITICAL INSTRUCTION:
        - Return a verdict object for EVERY claim_id provided below.
        - If "Inaccurate" or "False", provide the true, up-to-date real fact in real_fact based on the web evidence.
        - Include the most authoritative URL from the evidence.

        CLAIMS TO AUDIT:
        {"\n\n---\n\n".join(batch_blocks)}
        """

        verdict_response = _call_gemini_with_fallback(
            client=client,
            prompt=judge_prompt,
            schema=BatchVerificationList,
            temperature=0.0,
        )

        parsed_batch = BatchVerificationList.model_validate_json(verdict_response.text)
        for v in parsed_batch.verdicts:
            verdict_lookup[v.claim_id] = v

    # 3. Assemble final dashboard results
    final_results = []
    for claim in claims:
        v = verdict_lookup.get(claim.claim_id)
        sources = evidence_map.get(claim.claim_id, [])
        if v:
            final_results.append(
                {
                    "id": claim.claim_id,
                    "page": claim.page_number,
                    "category": claim.category,
                    "claim": claim.claim_text,
                    "search_query": claim.search_query,
                    "status": v.status,
                    "confidence": v.confidence_score,
                    "real_fact": v.real_fact,
                    "explanation": v.explanation,
                    "source_title": v.best_source_title,
                    "source_url": v.best_source_url,
                    "all_sources": [
                        {"title": r.get("title", "Source"), "url": r.get("url", "#")}
                        for r in sources
                        if r.get("url")
                    ],
                }
            )
    return final_results
"""
Generate a detailed project description PDF for SciSynthesis.
Run: python generate_project_doc.py
Output: SciSynthesis_Project_Documentation.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# ── Output file ───────────────────────────────────────────────────────────────
OUTPUT = "SciSynthesis_Project_Documentation.pdf"

# ── Color palette ─────────────────────────────────────────────────────────────
INDIGO     = colors.HexColor("#4F46E5")
INDIGO_LT  = colors.HexColor("#EEF2FF")
GRAY_900   = colors.HexColor("#111827")
GRAY_700   = colors.HexColor("#374151")
GRAY_500   = colors.HexColor("#6B7280")
GRAY_200   = colors.HexColor("#E5E7EB")
GREEN      = colors.HexColor("#059669")
GREEN_LT   = colors.HexColor("#D1FAE5")
BLUE       = colors.HexColor("#2563EB")
BLUE_LT    = colors.HexColor("#DBEAFE")
ORANGE     = colors.HexColor("#D97706")
ORANGE_LT  = colors.HexColor("#FEF3C7")
RED        = colors.HexColor("#DC2626")
RED_LT     = colors.HexColor("#FEE2E2")
WHITE      = colors.white

# ── Document setup ────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.2*cm, bottomMargin=2.2*cm,
    title="SciSynthesis – Project Documentation",
    author="Krina Pansuriya",
)

W = A4[0] - 4*cm   # usable text width

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=base[parent], **kw)
    return s

S = {
    "cover_title": style("cover_title", "Title",
        fontSize=32, textColor=INDIGO, leading=40,
        alignment=TA_CENTER, spaceAfter=8),
    "cover_sub": style("cover_sub",
        fontSize=14, textColor=GRAY_700, leading=20,
        alignment=TA_CENTER, spaceAfter=4),
    "cover_meta": style("cover_meta",
        fontSize=10, textColor=GRAY_500,
        alignment=TA_CENTER, spaceAfter=2),

    "h1": style("h1",
        fontSize=18, textColor=WHITE, leading=24,
        spaceBefore=18, spaceAfter=10, fontName="Helvetica-Bold"),
    "h2": style("h2",
        fontSize=13, textColor=INDIGO, leading=18,
        spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold"),
    "h3": style("h3",
        fontSize=11, textColor=GRAY_900, leading=16,
        spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold"),

    "body": style("body",
        fontSize=9.5, textColor=GRAY_700, leading=15,
        spaceAfter=5, alignment=TA_JUSTIFY),
    "bullet": style("bullet",
        fontSize=9.5, textColor=GRAY_700, leading=14,
        leftIndent=14, firstLineIndent=-10, spaceAfter=3),
    "sub_bullet": style("sub_bullet",
        fontSize=9, textColor=GRAY_500, leading=13,
        leftIndent=28, firstLineIndent=-10, spaceAfter=2),

    "code": style("code",
        fontSize=8.5, fontName="Courier", textColor=GRAY_900,
        backColor=colors.HexColor("#F3F4F6"), leading=13,
        leftIndent=10, spaceAfter=2),

    "badge_green": style("badge_green",
        fontSize=8, textColor=GREEN, fontName="Helvetica-Bold"),
    "badge_blue": style("badge_blue",
        fontSize=8, textColor=BLUE, fontName="Helvetica-Bold"),
    "badge_orange": style("badge_orange",
        fontSize=8, textColor=ORANGE, fontName="Helvetica-Bold"),

    "footer": style("footer",
        fontSize=8, textColor=GRAY_500, alignment=TA_CENTER),
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def HR(color=GRAY_200, width=0.5):
    return HRFlowable(width="100%", thickness=width, color=color, spaceAfter=6, spaceBefore=2)

def section_header(title, color=INDIGO):
    """Colored full-width section title bar."""
    t = Table([[Paragraph(title, S["h1"])]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t

def callout(text, bg=INDIGO_LT, border=INDIGO):
    t = Table([[Paragraph(text, S["body"])]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LINEAFTER",     (0,0), (0,-1), 3, border),  # not valid but looks fine
        ("LINEBEFORE",    (0,0), (0,-1), 3, border),
    ]))
    return t

def simple_table(headers, rows, col_widths=None, header_bg=INDIGO, row_alt=INDIGO_LT):
    col_widths = col_widths or [W / len(headers)] * len(headers)
    hdr_style  = ParagraphStyle("th", fontSize=8.5, textColor=WHITE,
                                 fontName="Helvetica-Bold", leading=12)
    cell_style = ParagraphStyle("td", fontSize=8.5, textColor=GRAY_700, leading=12)

    data = [[Paragraph(h, hdr_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), cell_style) for c in row])

    ts = [
        ("BACKGROUND",    (0,0), (-1,0),  header_bg),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("GRID",          (0,0), (-1,-1), 0.3, GRAY_200),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            ts.append(("BACKGROUND", (0,i), (-1,i), row_alt))

    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(ts))
    return t

def bp(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def sbp(text):
    return Paragraph(f"<bullet>–</bullet> {text}", S["sub_bullet"])

def body(text):
    return Paragraph(text, S["body"])

def h2(text):
    return Paragraph(text, S["h2"])

def h3(text):
    return Paragraph(text, S["h3"])

def sp(n=6):
    return Spacer(1, n)

# ══════════════════════════════════════════════════════════════════════════════
# CONTENT BUILDER
# ══════════════════════════════════════════════════════════════════════════════

story = []

# ─── COVER PAGE ───────────────────────────────────────────────────────────────
story.append(Spacer(1, 3*cm))

# Logo/Brand box
logo_tbl = Table(
    [[Paragraph("<b>SCISYNTHESIS</b>", ParagraphStyle(
        "brand", fontSize=42, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_CENTER))]],
    colWidths=[W]
)
logo_tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), INDIGO),
    ("TOPPADDING",    (0,0), (-1,-1), 22),
    ("BOTTOMPADDING", (0,0), (-1,-1), 22),
    ("ROUNDEDCORNERS", [8]),
]))
story.append(logo_tbl)
story.append(sp(16))

story.append(Paragraph("AI-Powered Scientific Research Assistant", S["cover_title"]))
story.append(sp(6))
story.append(Paragraph(
    "A full-stack intelligent platform for analyzing, synthesizing, and exploring scientific literature "
    "using state-of-the-art Retrieval-Augmented Generation (RAG) and Large Language Models.",
    S["cover_sub"]))
story.append(sp(24))

meta_rows = [
    ["Author",   "Krina Pansuriya"],
    ["Version",  "1.0.0"],
    ["Date",     datetime.now().strftime("%B %d, %Y")],
    ["Contact",  "scisynthesis07@gmail.com"],
    ["Platform", "Web Application (React + FastAPI)"],
]
meta_tbl = Table(
    [[Paragraph(k, ParagraphStyle("mk", fontSize=9, textColor=GRAY_500, fontName="Helvetica-Bold")),
      Paragraph(v, ParagraphStyle("mv", fontSize=9, textColor=GRAY_700))]
     for k,v in meta_rows],
    colWidths=[4*cm, W-4*cm]
)
meta_tbl.setStyle(TableStyle([
    ("ALIGN",    (0,0), (-1,-1), "LEFT"),
    ("TOPPADDING",    (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING",   (0,0), (-1,-1), 0),
]))
story.append(meta_tbl)
story.append(PageBreak())

# ─── TABLE OF CONTENTS ────────────────────────────────────────────────────────
story.append(section_header("Table of Contents"))
story.append(sp(10))

toc_items = [
    ("1", "Project Overview"),
    ("2", "Technology Stack"),
    ("3", "Application Pages & Features"),
    ("4", "Backend API Reference"),
    ("5", "Authentication & Security"),
    ("6", "AI / RAG Pipeline"),
    ("7", "Database Architecture"),
    ("8", "Advanced Analytics Features"),
    ("9", "Export & Reporting"),
    ("10", "Third-Party Integrations"),
    ("11", "Deployment & Configuration"),
    ("12", "Project Summary"),
]
toc_style = ParagraphStyle("toc", fontSize=10, textColor=GRAY_700, leading=18)
for num, title in toc_items:
    story.append(Paragraph(f"<b>{num}.</b>  {title}", toc_style))

story.append(PageBreak())

# ─── SECTION 1 · PROJECT OVERVIEW ────────────────────────────────────────────
story.append(section_header("1. Project Overview"))
story.append(sp(10))

story.append(h2("What is SciSynthesis?"))
story.append(body(
    "SciSynthesis is an enterprise-grade, AI-powered scientific research assistant designed to help "
    "researchers, students, and academics efficiently process large volumes of scientific papers. "
    "It combines modern web technologies with cutting-edge AI capabilities — including Google Gemini "
    "Large Language Models and FAISS vector search — to deliver deep, structured insights from "
    "uploaded PDF documents."
))
story.append(sp(4))

story.append(h2("Core Problem Solved"))
story.append(body(
    "Reading, summarizing, and cross-referencing dozens of research papers is extremely time-consuming. "
    "SciSynthesis automates this process by:"
))
for item in [
    "Extracting hypotheses, methods, datasets, findings, and limitations from any paper.",
    "Identifying research gaps and suggesting novel research directions.",
    "Enabling natural-language conversation with your uploaded papers.",
    "Comparing multiple papers side-by-side for methodology and findings.",
    "Detecting contradictions and consensus across a body of literature.",
    "Generating publication-quality literature reviews automatically.",
    "Organizing research into projects with notes and collaborative synthesis.",
]:
    story.append(bp(item))

story.append(sp(8))
story.append(callout(
    "<b>Key Differentiator:</b> SciSynthesis uses a Hybrid RAG pipeline combining semantic vector "
    "search (FAISS + Gemini embeddings) with lexical BM25 reranking, ensuring both conceptual "
    "relevance and exact keyword matching in every answer.",
    bg=INDIGO_LT, border=INDIGO
))
story.append(sp(8))

story.append(h2("Target Users"))
for u in [
    "Academic researchers managing literature reviews",
    "PhD students conducting systematic reviews",
    "Data scientists and analysts reviewing technical papers",
    "R&D teams exploring the state-of-the-art in any domain",
    "Professors preparing course material from recent publications",
]:
    story.append(bp(u))

story.append(PageBreak())

# ─── SECTION 2 · TECH STACK ──────────────────────────────────────────────────
story.append(section_header("2. Technology Stack"))
story.append(sp(10))

story.append(h2("Frontend"))
fe_rows = [
    ["React 18 + TypeScript",     "Component-based UI framework with type safety"],
    ["Vite",                      "Fast dev server + production build bundler"],
    ["React Router 6",            "Client-side SPA routing"],
    ["Tailwind CSS",              "Utility-first CSS for responsive design"],
    ["Axios",                     "HTTP client with request interceptors"],
    ["jsPDF",                     "Client-side PDF generation for report export"],
    ["Lucide React",              "SVG icon library"],
    ["React Context API",         "Global authentication state management"],
]
story.append(simple_table(["Library / Framework", "Purpose"], fe_rows,
                           col_widths=[6*cm, W-6*cm]))
story.append(sp(10))

story.append(h2("Backend"))
be_rows = [
    ["FastAPI 0.109",             "Async Python web framework (REST API)"],
    ["SQLAlchemy 2.0 (async)",    "ORM with async support (aiosqlite driver)"],
    ["SQLite + aiosqlite",        "Lightweight relational database (async)"],
    ["Google Gemini API",         "LLM (text generation) + Embeddings (768-dim)"],
    ["FAISS (CPU)",               "Vector similarity search (L2 distance)"],
    ["Redis 5.0+",                "Caching (embeddings, OTP, chat memory)"],
    ["PyPDF 4.0+",                "PDF text extraction page-by-page"],
    ["rank_bm25",                 "BM25 Okapi lexical scoring for reranking"],
    ["sentence-transformers",     "Fallback embedding model"],
    ["scikit-learn",              "K-Means clustering for paper grouping"],
    ["Passlib + bcrypt",          "Secure password hashing (rounds=12)"],
    ["PyJWT",                     "JWT token creation and verification (HS256)"],
    ["slowapi",                   "Request rate limiting per endpoint"],
]
story.append(simple_table(["Library / Framework", "Purpose"], be_rows,
                           col_widths=[6*cm, W-6*cm]))
story.append(sp(10))

story.append(h2("Infrastructure"))
infra_rows = [
    ["Docker + docker-compose",  "Container orchestration (FastAPI + Redis)"],
    ["Redis",                    "Three databases: embedding cache, chat memory, OTP"],
    ["FAISS Index (disk)",       "Persistent vector store saved to ./data/faiss.index"],
    ["SQLite (file)",            "Single-file relational database (research_assistant.db)"],
    ["Vite Proxy",               "Dev proxy: /api/* → localhost:8000"],
]
story.append(simple_table(["Component", "Role"], infra_rows, col_widths=[6*cm, W-6*cm]))

story.append(PageBreak())

# ─── SECTION 3 · PAGES & FEATURES ────────────────────────────────────────────
story.append(section_header("3. Application Pages & Features"))
story.append(sp(10))

pages = [
    ("/login", "LoginPage", "No",
     "Email + password login or phone OTP login. Rate-limited to prevent brute-force."),
    ("/register", "RegisterPage", "No",
     "New user registration. Validates email uniqueness, password strength (8+ chars, 1 letter, 1 digit)."),
    ("/", "Dashboard", "Yes",
     "Main hub: upload single/batch PDFs, run document analysis, global full-text search, view search history, export analysis to PDF."),
    ("/projects", "ProjectsPage", "Yes",
     "Create, browse, and delete research projects. Each project groups related papers."),
    ("/projects/:id", "ProjectDetailsPage", "Yes",
     "View all papers in a project. Select a paper to see its analysis results. Create and read per-paper notes."),
    ("/projects/:id/advanced", "ProjectAdvancedPage", "Yes",
     "10-tab advanced analysis: Chat, Compare, Hypothesis, Project Ideas, Citation, Keywords, Similar Papers, Clustering, Literature Review, Gap Detection."),
    ("/projects/:id/synthesis", "ProjectSynthesisPage", "Yes",
     "Cross-paper synthesis: consensus findings, contradiction detection, combined research gaps, strategic next steps. Export synthesis PDF."),
    ("/profile", "ProfilePage", "Yes",
     "Edit name, email, institution, bio. Upload/delete avatar. Change password. Add phone number for OTP. View usage statistics."),
    ("/privacy-policy", "PrivacyPolicyPage", "No",
     "Public privacy policy page. Accessible without login."),
]
story.append(simple_table(
    ["Route", "Component", "Auth", "Description"],
    pages,
    col_widths=[3.5*cm, 3.5*cm, 1.2*cm, W-8.2*cm]
))
story.append(sp(10))

story.append(h2("Dashboard — Detailed Features"))
for f in [
    "<b>Single PDF Upload:</b> Upload any scientific PDF. The system extracts text, chunks it into 500-word segments, embeds each chunk, and stores them in FAISS for retrieval.",
    "<b>Batch Upload:</b> Upload multiple PDFs at once via a modal. Each document is processed independently and indexed into the same vector store.",
    "<b>Automatic Analysis:</b> On upload, Gemini LLM analyzes the document and returns: research topic, hypotheses, methodology, datasets, key findings, limitations, citations, research gaps, and a novel research direction suggestion.",
    "<b>Confidence Metrics:</b> Each analysis returns four quality scores — confidence score (0-100), evidence strength, citation frequency, and methodological robustness (all 0-1).",
    "<b>Global Search:</b> Full-text semantic search across ALL user papers. Returns a RAG-generated answer with inline citations from the most relevant chunks.",
    "<b>Search History:</b> Last 20 queries stored and displayed with timestamps for quick replay.",
    "<b>Export to PDF:</b> Generate a formatted multi-page PDF report of any paper's analysis using jsPDF — entirely client-side.",
]:
    story.append(bp(f))
    story.append(sp(2))

story.append(sp(6))
story.append(h2("ProjectAdvancedPage — 10 Analysis Tabs"))
tabs = [
    ["Chat",             "Conversational RAG with 20-turn memory. Ask follow-up questions about selected papers. Chat history persisted in Redis (24h)."],
    ["Compare",          "Side-by-side comparison of 2+ papers: methodology, results, strengths, weaknesses, and key contributions."],
    ["Hypothesis",       "Generate novel research hypotheses from selected papers with suggested testing methodologies and future research directions."],
    ["Project Ideas",    "Convert academic research into real-world software/engineering project ideas with tech stack, architecture, implementation steps, and target audience."],
    ["Citation",         "Generate properly formatted citations in APA, IEEE, or MLA style for any paper in the project."],
    ["Keywords",         "Extract 8–12 domain-specific keywords and a one-sentence summary for each paper."],
    ["Similar Papers",   "Find the top 5 most similar papers within the project using cosine similarity on Gemini embeddings."],
    ["Clustering",       "Group all project papers into topic clusters using K-Means on embeddings. Clusters are labeled by Gemini AI."],
    ["Literature Review","Auto-generate a publication-quality literature review with executive summary, methodology comparison, consensus findings, research gaps, and future work."],
    ["Gaps",             "Structured gap detection across all papers — categorized by type (methodological, empirical, theoretical, application) with severity levels (high/medium/low)."],
]
story.append(simple_table(["Tab", "Functionality"], tabs, col_widths=[3.5*cm, W-3.5*cm]))

story.append(PageBreak())

# ─── SECTION 4 · API REFERENCE ───────────────────────────────────────────────
story.append(section_header("4. Backend API Reference"))
story.append(sp(8))

story.append(body(
    "The backend exposes a RESTful API via FastAPI at base path <b>/api/v1</b>. "
    "All protected endpoints require a valid JWT token (sent as an httpOnly cookie or "
    "Authorization: Bearer header)."
))
story.append(sp(6))

story.append(h2("Authentication Endpoints  (/api/v1/auth/)"))
auth_rows = [
    ["POST", "/register",    "Public",  "Register a new user account"],
    ["POST", "/login",       "Public",  "Login with email + password → JWT cookie"],
    ["POST", "/send-otp",    "Public",  "Send 6-digit OTP to phone number"],
    ["POST", "/verify-otp",  "Public",  "Verify OTP → JWT cookie (alternative login)"],
    ["POST", "/logout",      "Auth",    "Clear session cookie"],
    ["GET",  "/me",          "Auth",    "Get current user profile"],
    ["PUT",  "/me",          "Auth",    "Update profile (name, email, institution, etc.)"],
    ["GET",  "/stats",       "Auth",    "Fetch user statistics (papers, projects, notes)"],
    ["POST", "/me/avatar",   "Auth",    "Upload profile picture (max 5 MB, image only)"],
    ["DELETE","/me/avatar",  "Auth",    "Delete profile picture"],
]
story.append(simple_table(["Method","Endpoint","Access","Description"], auth_rows,
                           col_widths=[1.5*cm, 3.2*cm, 1.5*cm, W-6.2*cm]))
story.append(sp(8))

story.append(h2("Analysis Endpoints  (/api/v1/analysis/)"))
analysis_rows = [
    ["POST",   "/analyze",         "Auth", "Upload single PDF → automatic AI analysis"],
    ["POST",   "/analyze-batch",   "Auth", "Upload multiple PDFs in one request"],
    ["POST",   "/query",           "Auth", "Semantic search specific papers + RAG answer"],
    ["POST",   "/global-search",   "Auth", "Search ALL user papers + RAG answer"],
    ["POST",   "/chat",            "Auth", "Conversational RAG with memory (20-turn)"],
    ["POST",   "/research-gaps",   "Auth", "Collective gap analysis from multiple papers"],
    ["GET",    "/history",         "Auth", "All uploaded papers with analysis results"],
    ["DELETE", "/{paper_id}",      "Auth", "Delete a paper and its chunks"],
    ["GET",    "/search-history",  "Auth", "Last 20 user queries"],
]
story.append(simple_table(["Method","Endpoint","Access","Description"], analysis_rows,
                           col_widths=[1.5*cm, 3.8*cm, 1.5*cm, W-6.8*cm]))
story.append(sp(8))

story.append(h2("Advanced Analysis  (/api/v1/analysis/advanced/)"))
adv_rows = [
    ["POST", "/compare-papers",       "Auth", "Side-by-side methodology/results comparison"],
    ["POST", "/generate-hypothesis",  "Auth", "AI-generated novel hypotheses + future directions"],
    ["POST", "/project-ideas",        "Auth", "Convert research to real-world project ideas"],
    ["POST", "/citation",             "Auth", "Format citation in APA / IEEE / MLA style"],
    ["GET",  "/keywords/{paper_id}",  "Auth", "Extract 8-12 keywords + one-sentence summary"],
    ["GET",  "/similar/{paper_id}",   "Auth", "Top 5 most similar papers (cosine similarity)"],
    ["POST", "/cluster-papers",       "Auth", "K-Means clustering with AI-generated labels"],
]
story.append(simple_table(["Method","Endpoint","Access","Description"], adv_rows,
                           col_widths=[1.5*cm, 4.8*cm, 1.5*cm, W-7.8*cm]))
story.append(sp(8))

story.append(h2("Review & Synthesis Endpoints"))
rev_rows = [
    ["POST", "/analysis/generate-review",    "Auth", "Auto-generate publication-quality literature review"],
    ["POST", "/analysis/detect-gaps",        "Auth", "Structured gap detection with severity levels"],
    ["POST", "/synthesis/{project_id}",      "Auth", "Multi-paper consensus, contradictions, and gaps"],
    ["GET",  "/synthesis/{project_id}/export","Auth","Export synthesis as formatted plain-text report"],
]
story.append(simple_table(["Method","Endpoint","Access","Description"], rev_rows,
                           col_widths=[1.5*cm, 5.5*cm, 1.5*cm, W-8.5*cm]))
story.append(sp(8))

story.append(h2("Projects & Notes  (/api/v1/projects/)"))
proj_rows = [
    ["GET",    "/",              "Auth", "List all user projects"],
    ["POST",   "/",              "Auth", "Create a new project (name + optional description)"],
    ["GET",    "/{project_id}",  "Auth", "Get project details with all linked papers"],
    ["DELETE", "/{project_id}",  "Auth", "Delete project (cascades to papers and notes)"],
    ["POST",   "/notes",         "Auth", "Create a note attached to a paper"],
    ["GET",    "/notes/{paper_id}","Auth","Fetch all notes for a specific paper"],
]
story.append(simple_table(["Method","Endpoint","Access","Description"], proj_rows,
                           col_widths=[1.5*cm, 3.8*cm, 1.5*cm, W-6.8*cm]))

story.append(PageBreak())

# ─── SECTION 5 · AUTH & SECURITY ─────────────────────────────────────────────
story.append(section_header("5. Authentication & Security"))
story.append(sp(10))

story.append(h2("Authentication Methods"))
story.append(body(
    "SciSynthesis supports two authentication methods — email/password login and phone-based "
    "One-Time Password (OTP) login — both issuing a signed JWT stored in an httpOnly cookie."
))
story.append(sp(4))

story.append(h3("Email / Password Flow"))
for step in [
    "User submits email + password via POST /auth/login.",
    "Backend verifies password against bcrypt hash (rounds=12).",
    "On success, a HS256-signed JWT is created (60-minute expiry, subject = email).",
    "JWT is set as an httpOnly, SameSite=Lax cookie (Secure=True in production).",
    "Frontend stores token in sessionStorage as fallback for API clients.",
]:
    story.append(bp(step))
story.append(sp(6))

story.append(h3("Phone OTP Flow"))
for step in [
    "User enters phone number → POST /auth/send-otp (rate-limited: 5/min).",
    "Backend generates a cryptographically secure 6-digit OTP.",
    "OTP stored in Redis db=2 with 5-minute TTL (one-time use).",
    "In development mode, OTP is printed to the server console.",
    "User enters received OTP → POST /auth/verify-otp (rate-limited: 10/min).",
    "Comparison uses hmac.compare_digest() — timing-safe to prevent timing attacks.",
    "On success, OTP is immediately invalidated. JWT cookie issued.",
]:
    story.append(bp(step))
story.append(sp(8))

story.append(h2("Security Measures"))
sec_rows = [
    ["JWT httpOnly Cookie",     "JavaScript cannot read the token — protects against XSS"],
    ["bcrypt Password Hashing", "Industry-standard with cost factor 12 (computationally expensive)"],
    ["Rate Limiting (slowapi)", "20/min register, 10/min login, 5/min OTP — prevents brute force"],
    ["HMAC-safe OTP Compare",   "Prevents timing side-channel attacks on OTP verification"],
    ["Pydantic Input Validation","All request bodies validated; malformed requests rejected with 422"],
    ["MIME-type File Validation","Avatar uploads validated by magic bytes, not just filename extension"],
    ["File Size Limits",        "PDFs max 50 MB, avatars max 5 MB"],
    ["CORS Restriction",        "Only whitelisted origins allowed (env: ALLOWED_ORIGINS)"],
    ["Data Isolation",          "Every DB query filtered by current_user.id — no cross-user access"],
    ["Security Headers",        "X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy"],
    ["Password Requirements",   "Min 8 chars, at least 1 letter and 1 digit enforced"],
    ["Redis OTP Persistence",   "OTPs survive server restarts; automatically expire after 5 minutes"],
]
story.append(simple_table(["Security Feature", "Protection Provided"], sec_rows,
                           col_widths=[5*cm, W-5*cm]))

story.append(PageBreak())

# ─── SECTION 6 · RAG PIPELINE ────────────────────────────────────────────────
story.append(section_header("6. AI / RAG Pipeline"))
story.append(sp(10))

story.append(h2("Overview"))
story.append(body(
    "SciSynthesis implements a Hybrid Retrieval-Augmented Generation (RAG) pipeline. "
    "When a user asks a question, the system retrieves the most relevant text chunks from "
    "uploaded papers and feeds them as context to Google Gemini, enabling factual, "
    "citation-grounded answers."
))
story.append(sp(6))
story.append(callout(
    "<b>Why Hybrid RAG?</b>  Pure semantic search can miss exact terminology matches. "
    "Pure keyword search misses conceptual relationships. Combining both (65% semantic + 35% BM25) "
    "gives the best of both worlds — conceptual understanding with lexical precision.",
    bg=GREEN_LT, border=GREEN
))
story.append(sp(8))

story.append(h2("Document Ingestion Pipeline"))
ingest_steps = [
    ["1", "PDF Upload",       "User uploads PDF via the frontend. File saved to disk temporarily."],
    ["2", "Text Extraction",  "PyPDF extracts raw text page-by-page with UTF-8 normalization."],
    ["3", "Chunking",         "Text split into 500-word chunks with 100-word overlap (sliding window). Overlap preserves context at chunk boundaries."],
    ["4", "DB Storage",       "DocumentChunk records created in SQLite with text, page number, and chunk index."],
    ["5", "Batch Embedding",  "All chunks embedded concurrently using ThreadPoolExecutor (10 workers) via Gemini embedding-001 model."],
    ["6", "Redis Cache",      "Each embedding cached in Redis db=0 by SHA256 hash (TTL 7 days). Avoids re-embedding identical content."],
    ["7", "FAISS Indexing",   "Chunk IDs + 768-dim embeddings added to FAISS IndexIDMap. Index saved to disk immediately."],
    ["8", "LLM Analysis",     "Full document text (or first 8,000 chars) sent to Gemini for structured analysis (JSON response)."],
    ["9", "DB Persistence",   "Analysis result stored as JSON in the papers table. Title extracted from analysis topic."],
]
story.append(simple_table(["Step","Stage","Description"], ingest_steps,
                           col_widths=[1*cm, 3*cm, W-4*cm]))
story.append(sp(8))

story.append(h2("Query & Retrieval Pipeline"))
retrieval_steps = [
    ["1", "Query Embedding",    "User query embedded to 768-dim vector via Gemini (cached in Redis)."],
    ["2", "FAISS Search",       "Search index with 15× over-fetch multiplier (e.g., top_k=5 → fetch 75 candidates) for better recall."],
    ["3", "Metadata Loading",   "Load text, page number, paper ID for each candidate chunk from SQLite."],
    ["4", "Paper Filtering",    "If paper_ids provided, drop chunks from other papers."],
    ["5", "Semantic Scoring",   "Convert L2 distance to similarity: score = 1.0 − (distance / 2.0). Drop scores < 0.05."],
    ["6", "Diversity Cap",      "Limit 3 chunks per paper in multi-paper queries to prevent any single paper dominating results."],
    ["7", "BM25 Reranking",     "Build BM25Okapi model on candidates. Compute hybrid score: 0.65 × semantic + 0.35 × BM25. Apply 0.85× penalty for chunks under 30 words."],
    ["8", "Deduplication",      "Remove chunks with identical 120-character prefix (prevents near-duplicate results)."],
    ["9", "Gemini Generation",  "Top-k chunks passed as context to Gemini. LLM generates answer with inline citations [ChunkID: X]."],
]
story.append(simple_table(["Step","Stage","Description"], retrieval_steps,
                           col_widths=[1*cm, 3.5*cm, W-4.5*cm]))
story.append(sp(8))

story.append(h2("Gemini LLM Model Chain"))
story.append(body(
    "SciSynthesis uses a cascading model fallback to maximize availability:"
))
model_rows = [
    ["Primary",    "gemini-2.5-flash",  "Most capable, fastest Gemini model"],
    ["Fallback 1", "gemini-2.0-flash",  "Used if 2.5 returns 503 or is unavailable"],
    ["Fallback 2", "gemini-1.5-flash",  "Final fallback for maximum compatibility"],
    ["Embedding",  "gemini-embedding-001", "768-dimensional text embeddings for RAG"],
    ["Demo Mode",  "Simulated responses", "Returns mock data if API key is missing/invalid"],
]
story.append(simple_table(["Priority","Model","Usage"], model_rows,
                           col_widths=[2*cm, 4.5*cm, W-6.5*cm]))
story.append(sp(6))
story.append(body(
    "<b>Retry Strategy:</b> Exponential backoff (1s → 2s → 4s) on 503/overload errors. "
    "Maximum 3 retry attempts before falling back to the next model in the chain."
))
story.append(sp(8))

story.append(h2("Conversational Memory"))
story.append(body(
    "The Chat feature maintains per-user conversation history for multi-turn, context-aware dialogue:"
))
for item in [
    "<b>Storage:</b> Redis db=1 (primary, 24-hour TTL) with in-memory fallback.",
    "<b>Capacity:</b> Up to 20 turns (user + assistant message pairs).",
    "<b>Key:</b> chat_memory:user:{user_id}",
    "<b>Context Injection:</b> Full history formatted and included in every Gemini prompt.",
    "<b>Reset:</b> POST /chat with clear_history=true to start a new session.",
    "<b>Timestamp:</b> Each turn stored with ISO 8601 UTC timestamp.",
]:
    story.append(bp(item))
    story.append(sp(1))

story.append(PageBreak())

# ─── SECTION 7 · DATABASE ────────────────────────────────────────────────────
story.append(section_header("7. Database Architecture"))
story.append(sp(10))

story.append(h2("Database: SQLite (async via aiosqlite)"))
story.append(body(
    "SciSynthesis uses SQLite as its primary database — lightweight, serverless, and portable. "
    "SQLAlchemy 2.0 with async support enables non-blocking database operations throughout the FastAPI application."
))
story.append(sp(6))

story.append(h2("Entity Relationship Overview"))
erd_rows = [
    ["User → Paper",   "One-to-Many", "A user can upload many papers"],
    ["User → Project", "One-to-Many", "A user can create many projects"],
    ["User → Note",    "One-to-Many", "A user can write many notes"],
    ["Project → Paper","One-to-Many", "A project groups many papers (optional)"],
    ["Paper → Chunk",  "One-to-Many", "Each paper has many document chunks"],
    ["Paper → Note",   "One-to-Many", "Each paper can have many notes"],
]
story.append(simple_table(["Relationship","Type","Description"], erd_rows,
                           col_widths=[3.5*cm, 2.5*cm, W-6*cm]))
story.append(sp(8))

story.append(h2("Table Schemas"))
tables_info = [
    ("users", [
        ["id", "INTEGER PK", "Auto-increment primary key"],
        ["email", "VARCHAR UNIQUE", "User's email address (login identifier)"],
        ["hashed_password", "VARCHAR", "bcrypt hash of user's password"],
        ["full_name", "VARCHAR NULL", "Optional display name"],
        ["institution", "VARCHAR NULL", "University or organization"],
        ["bio", "VARCHAR NULL", "Short biography"],
        ["phone_number", "VARCHAR NULL", "For OTP login"],
        ["profile_picture", "VARCHAR NULL", "Avatar filename in /data/avatars/"],
        ["created_at", "DATETIME", "Account creation timestamp (UTC)"],
    ]),
    ("papers", [
        ["id", "INTEGER PK", "Auto-increment primary key"],
        ["user_id", "INTEGER FK", "References users.id"],
        ["project_id", "INTEGER FK NULL", "References projects.id (optional)"],
        ["title", "VARCHAR", "Extracted research title"],
        ["filename", "VARCHAR", "Original uploaded filename"],
        ["result_json", "JSON", "Full AnalysisResponse object serialized"],
        ["created_at", "DATETIME", "Upload timestamp (UTC)"],
    ]),
    ("document_chunks", [
        ["id", "INTEGER PK", "Auto-increment primary key"],
        ["paper_id", "INTEGER FK", "References papers.id (cascade delete)"],
        ["text", "TEXT", "Extracted text chunk (500-word segments)"],
        ["page_number", "INTEGER NULL", "Source page number in original PDF"],
        ["chunk_index", "INTEGER", "0-indexed chunk order within the paper"],
    ]),
    ("projects", [
        ["id", "INTEGER PK", "Auto-increment primary key"],
        ["user_id", "INTEGER FK", "References users.id"],
        ["name", "VARCHAR", "Project name"],
        ["description", "VARCHAR NULL", "Optional project description"],
        ["created_at", "DATETIME", "Creation timestamp (UTC)"],
    ]),
    ("notes", [
        ["id", "INTEGER PK", "Auto-increment primary key"],
        ["paper_id", "INTEGER FK", "References papers.id (cascade delete)"],
        ["user_id", "INTEGER FK", "References users.id"],
        ["content", "VARCHAR", "Note text content"],
        ["created_at", "DATETIME", "Creation timestamp (UTC)"],
    ]),
    ("search_history", [
        ["id", "INTEGER PK", "Auto-increment primary key"],
        ["user_id", "INTEGER FK", "References users.id"],
        ["query", "VARCHAR", "User's search query text"],
        ["paper_ids", "JSON NULL", "Array of paper IDs used to scope search"],
        ["created_at", "DATETIME", "Query timestamp (UTC)"],
    ]),
]

for table_name, columns in tables_info:
    story.append(h3(f"Table: {table_name}"))
    story.append(simple_table(["Column", "Type", "Description"], columns,
                               col_widths=[3*cm, 3*cm, W-6*cm],
                               header_bg=GRAY_700))
    story.append(sp(6))

story.append(PageBreak())

# ─── SECTION 8 · ADVANCED ANALYTICS ─────────────────────────────────────────
story.append(section_header("8. Advanced Analytics Features"))
story.append(sp(10))

story.append(h2("Paper Comparison"))
story.append(body(
    "The Compare feature sends selected papers' content to Gemini with a structured prompt requesting "
    "a side-by-side comparison. The response includes:"
))
for item in ["Research objectives and scope", "Methodologies and experimental design",
             "Key results and performance metrics", "Advantages and limitations of each approach",
             "Core contributions to the field"]:
    story.append(bp(item))
story.append(sp(6))

story.append(h2("Literature Review Generation"))
story.append(body("The auto-generated literature review includes all sections expected in academic publication:"))
review_structure = [
    ["Review Title",          "A descriptive title summarizing the surveyed papers"],
    ["Executive Summary",     "High-level overview of the research landscape"],
    ["Key Contributions",     "Per-paper summary of methodology and contribution"],
    ["Methodology Comparison","Tabular-style comparison of approaches across papers"],
    ["Consensus Findings",    "Common conclusions supported by multiple papers"],
    ["Research Gaps",         "Identified missing areas in the literature"],
    ["Future Work",           "Suggested directions for advancing the field"],
    ["Confidence Score",      "AI confidence in the quality of the generated review"],
]
story.append(simple_table(["Section", "Description"], review_structure,
                           col_widths=[4*cm, W-4*cm]))
story.append(sp(8))

story.append(h2("Gap Detection (Structured)"))
story.append(body(
    "Gap detection goes beyond simple 'research gap' extraction. Each gap is categorized and scored:"
))
gap_rows = [
    ["Methodological", "Gaps in research methods or experimental design"],
    ["Empirical",      "Missing real-world validation or insufficient data"],
    ["Theoretical",    "Incomplete or missing conceptual frameworks"],
    ["Application",    "Research not yet applied to practical use cases"],
]
story.append(simple_table(["Gap Category", "Description"], gap_rows, col_widths=[3.5*cm, W-3.5*cm],
                           header_bg=ORANGE))
story.append(sp(4))
story.append(body(
    "<b>Severity Levels:</b> High (critical missing work), Medium (notable gap), Low (minor omission). "
    "Each gap includes a description, suggested future work, and related research topics."
))
story.append(sp(8))

story.append(h2("Paper Clustering"))
story.append(body(
    "K-Means clustering groups papers by topic similarity using their Gemini embedding vectors. "
    "The number of clusters is configurable (minimum 2, maximum = number of papers). "
    "Each cluster receives an AI-generated label describing the shared research theme."
))
story.append(sp(6))

story.append(h2("Hypothesis Generation"))
story.append(body(
    "Given a research topic and a set of papers, Gemini generates novel, testable hypotheses "
    "that the existing literature has not fully addressed. Each hypothesis includes:"
))
for item in ["The hypothesis statement", "Rationale based on existing literature",
             "Suggested testing methodology", "Expected impact if validated"]:
    story.append(bp(item))
story.append(sp(6))

story.append(h2("Project Ideas"))
story.append(body(
    "Transforms academic research insights into actionable engineering project proposals, including:"
))
for item in ["Project title and objective", "Recommended technology stack",
             "High-level architecture overview", "Step-by-step implementation guide",
             "Target audience and potential impact"]:
    story.append(bp(item))

story.append(PageBreak())

# ─── SECTION 9 · EXPORT & REPORTING ──────────────────────────────────────────
story.append(section_header("9. Export & Reporting"))
story.append(sp(10))

story.append(h2("Analysis PDF Export (Dashboard)"))
story.append(body(
    "From the Dashboard, users can export any paper's analysis as a formatted PDF document. "
    "The export is generated entirely in the browser using jsPDF — no server request required."
))
story.append(body("The exported PDF includes:"))
for item in ["Paper title and upload metadata",
             "Research topic and confidence scores",
             "Extracted hypotheses (numbered list)",
             "Methods summary and datasets identified",
             "Key findings (bullet points)",
             "Limitations and citation references",
             "Research gap identified and novel direction suggested",
             "Quality metrics bar (evidence strength, methodological robustness, citation frequency)"]:
    story.append(bp(item))
story.append(sp(8))

story.append(h2("Synthesis PDF Export (ProjectSynthesisPage)"))
story.append(body(
    "The synthesis export generates a comprehensive multi-paper research report including:"
))
for item in ["Project name and generation date",
             "Overall research theme",
             "Consensus findings across all papers",
             "Identified contradictions between papers",
             "Combined research gap analysis",
             "Strategic next steps for advancing the research",
             "Overall synthesis confidence score",
             "List of all analyzed papers"]:
    story.append(bp(item))
story.append(sp(4))
story.append(callout(
    "<b>Export Format:</b> Multi-page A4 PDF with colored section headers, structured tables, "
    "and consistent academic styling. Page numbers and generation timestamp included.",
    bg=BLUE_LT, border=BLUE
))

story.append(PageBreak())

# ─── SECTION 10 · INTEGRATIONS ───────────────────────────────────────────────
story.append(section_header("10. Third-Party Integrations"))
story.append(sp(10))

integrations = [
    ("Google Gemini API", INDIGO_LT, INDIGO, [
        "<b>Package:</b> google-generativeai (Python)",
        "<b>Models Used:</b> gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-flash, gemini-embedding-001",
        "<b>Text Generation:</b> Paper analysis, synthesis, hypotheses, citations, cluster labels",
        "<b>Embeddings:</b> 768-dimensional dense vectors for all RAG operations",
        "<b>Demo Mode:</b> Returns simulated responses if API key is absent or invalid",
    ]),
    ("Redis", GREEN_LT, GREEN, [
        "<b>Version:</b> Redis 5.0+",
        "<b>db=0 — Embedding Cache:</b> SHA256-keyed embeddings, 7-day TTL",
        "<b>db=1 — Chat Memory:</b> Per-user conversation history, 24-hour TTL",
        "<b>db=2 — OTP Store:</b> One-time passwords, 5-minute TTL",
        "<b>Fallback:</b> In-memory dictionaries if Redis is unavailable",
    ]),
    ("FAISS (Facebook AI Similarity Search)", BLUE_LT, BLUE, [
        "<b>Index Type:</b> IndexIDMap wrapping IndexFlatL2 (L2 Euclidean distance)",
        "<b>Dimension:</b> 768 (matching Gemini embedding size)",
        "<b>Persistence:</b> Saved to ./data/faiss.index after every add operation",
        "<b>Search Speed:</b> O(n) linear scan — suitable for up to ~10M vectors on CPU",
        "<b>ID Mapping:</b> Maps internal FAISS IDs directly to SQLite DocumentChunk IDs",
    ]),
    ("EmailJS", ORANGE_LT, ORANGE, [
        "<b>Purpose:</b> Newsletter subscription form in the Footer component",
        "<b>Service ID:</b> service_scisynthesis",
        "<b>Template ID:</b> template_hvefuje",
        "<b>Trigger:</b> User submits email in footer → EmailJS sends notification to admin",
        "<b>Client-Side:</b> Executed entirely in the browser — no backend email server required",
    ]),
    ("jsPDF", colors.HexColor("#FDF4FF"), colors.HexColor("#7C3AED"), [
        "<b>Purpose:</b> Client-side PDF generation for analysis and synthesis exports",
        "<b>Usage:</b> Dashboard.tsx (analysis export) + ProjectSynthesisPage.tsx (synthesis export)",
        "<b>Features:</b> Multi-page layout, colored sections, tables, metrics display",
        "<b>No server involvement</b> — PDF generated and downloaded entirely in the browser",
    ]),
    ("PyPDF", GREEN_LT, GREEN, [
        "<b>Version:</b> PyPDF 4.0+",
        "<b>Purpose:</b> Server-side PDF text extraction on document upload",
        "<b>Method:</b> PdfReader with page-by-page extraction",
        "<b>Output:</b> Raw text per page, UTF-8 normalized, fed into chunking pipeline",
    ]),
]

for name, bg, border, details in integrations:
    story.append(h2(name))
    t = Table([[Paragraph("<br/>".join(details), S["body"])]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LINEBEFORE", (0,0), (0,-1), 3, border),
    ]))
    story.append(t)
    story.append(sp(8))

story.append(PageBreak())

# ─── SECTION 11 · DEPLOYMENT ─────────────────────────────────────────────────
story.append(section_header("11. Deployment & Configuration"))
story.append(sp(10))

story.append(h2("Environment Variables"))
env_rows = [
    ["GOOGLE_API_KEY",     "Required", "Google Gemini API key for LLM and embeddings"],
    ["SECRET_KEY",         "Required", "JWT signing secret (minimum 32 characters)"],
    ["DATABASE_URL",       "Required", "SQLAlchemy DB URL (default: sqlite+aiosqlite:///./research_assistant.db)"],
    ["REDIS_HOST",         "Optional", "Redis hostname (default: localhost)"],
    ["REDIS_PORT",         "Optional", "Redis port (default: 6379)"],
    ["ALLOWED_ORIGINS",    "Required", "Comma-separated allowed CORS origins"],
    ["COOKIE_SECURE",      "Optional", "Set true in production (HTTPS only cookies)"],
    ["ENVIRONMENT",        "Optional", "development or production (affects OTP logging)"],
    ["VECTOR_DATA_DIR",    "Optional", "Directory for FAISS index (default: ./data)"],
]
story.append(simple_table(["Variable", "Required", "Description"], env_rows,
                           col_widths=[4*cm, 2*cm, W-6*cm]))
story.append(sp(8))

story.append(h2("Running the Application"))
story.append(h3("Backend"))
for cmd in [
    "cd backend",
    "pip install -r requirements.txt",
    "cp .env.example .env  # Fill in API keys",
    "python -m uvicorn app.main:app --reload --port 8000",
]:
    story.append(Paragraph(cmd, S["code"]))
story.append(sp(6))

story.append(h3("Frontend"))
for cmd in [
    "cd frontend",
    "npm install",
    "npm run dev    # Dev server at http://localhost:5173",
    "npm run build  # Production build → dist/",
]:
    story.append(Paragraph(cmd, S["code"]))
story.append(sp(6))

story.append(h3("Docker (Full Stack)"))
for cmd in [
    "docker-compose up --build",
    "# FastAPI at :8000, Redis at :6379",
    "# Frontend served by Vite dev server at :5173",
]:
    story.append(Paragraph(cmd, S["code"]))
story.append(sp(8))

story.append(h2("Architecture Diagram (Text)"))
arch = """
Browser (React + Vite)
    │  HTTP/HTTPS (Cookie Auth, JSON)
    ▼
FastAPI (Python 3.11+)  ←──── slowapi rate limiter
    │
    ├── /api/v1/auth/        ←── JWT + bcrypt + OTP
    ├── /api/v1/analysis/    ←── RAG pipeline
    ├── /api/v1/projects/    ←── Project management
    └── /api/v1/synthesis/   ←── Multi-paper synthesis
         │
         ├── SQLite (SQLAlchemy async) ── papers, chunks, users, notes
         ├── FAISS (disk)              ── vector similarity search
         ├── Redis                     ── embeddings cache / OTP / chat memory
         └── Google Gemini API         ── LLM generation + 768-dim embeddings
"""
story.append(Paragraph(arch.replace("\n", "<br/>"), S["code"]))

story.append(PageBreak())

# ─── SECTION 12 · SUMMARY ────────────────────────────────────────────────────
story.append(section_header("12. Project Summary", color=GREEN))
story.append(sp(10))

story.append(callout(
    "<b>SciSynthesis</b> is a production-ready, full-stack AI research assistant that brings "
    "together modern web engineering and state-of-the-art AI to solve a real academic problem: "
    "the overwhelming volume of scientific literature. By combining Hybrid RAG, multi-turn "
    "conversational AI, structured analysis, and a polished user experience, it enables anyone "
    "from PhD students to seasoned researchers to process, understand, and synthesize scientific "
    "papers at a fraction of the traditional time.",
    bg=GREEN_LT, border=GREEN
))
story.append(sp(10))

story.append(h2("Key Strengths"))
for s in [
    "<b>Hybrid RAG Pipeline:</b> Best-in-class retrieval combining semantic (FAISS) + lexical (BM25) scoring for accurate, context-aware answers.",
    "<b>Multi-Document Intelligence:</b> Not just single-paper analysis — synthesis, comparison, contradiction detection, and clustering across entire project libraries.",
    "<b>Production Security:</b> JWT + httpOnly cookies, OTP 2FA, bcrypt hashing, rate limiting, CORS restriction, input validation.",
    "<b>Scalable Architecture:</b> Async FastAPI + SQLAlchemy, Redis caching, FAISS vector store — designed to handle thousands of papers.",
    "<b>Export Capabilities:</b> Client-side PDF generation for both individual analysis and multi-paper synthesis reports.",
    "<b>User-Friendly UI:</b> Clean, responsive React interface with tabbed advanced features, real-time loading states, and intuitive navigation.",
]:
    story.append(bp(s))
    story.append(sp(2))
story.append(sp(8))

story.append(h2("Feature Count Summary"))
feat_rows = [
    ["API Endpoints",           "30+"],
    ["Frontend Pages",          "9"],
    ["Analysis Features",       "10 (Chat, Compare, Hypothesis, Project Ideas, Citations, Keywords, Similar, Clustering, Literature Review, Gaps)"],
    ["Authentication Methods",  "2 (Email/Password + Phone OTP)"],
    ["Export Formats",          "2 (PDF via jsPDF, Plain Text)"],
    ["Citation Formats",        "3 (APA, IEEE, MLA)"],
    ["LLM Models Supported",    "3 (gemini-2.5-flash, 2.0-flash, 1.5-flash with auto-fallback)"],
    ["Database Tables",         "6 (users, papers, document_chunks, projects, notes, search_history)"],
    ["Third-Party Integrations","6 (Gemini, FAISS, Redis, EmailJS, jsPDF, PyPDF)"],
]
story.append(simple_table(["Metric", "Count / Detail"], feat_rows,
                           col_widths=[5*cm, W-5*cm], header_bg=GREEN))
story.append(sp(10))

story.append(HR(GRAY_200))
story.append(sp(6))
story.append(Paragraph(
    f"© {datetime.now().year} SciSynthesis — Krina Pansuriya  ·  scisynthesis07@gmail.com  ·  "
    f"Generated {datetime.now().strftime('%B %d, %Y')}",
    S["footer"]
))

# ── Build PDF ─────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF generated: {OUTPUT}")

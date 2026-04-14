"""
Generate all project diagrams for SciSynthesis.
Outputs 9 PNG files in the project root.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Ellipse, FancyArrowPatch, Arc
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
import numpy as np
from datetime import datetime, timedelta

# ── Shared palette ─────────────────────────────────────────────────────────────
INDIGO   = '#4F46E5'
INDIGO_L = '#EEF2FF'
BLUE     = '#2563EB'
BLUE_L   = '#DBEAFE'
GREEN    = '#059669'
GREEN_L  = '#D1FAE5'
ORANGE   = '#D97706'
ORANGE_L = '#FEF3C7'
PINK     = '#DB2777'
PINK_L   = '#FCE7F3'
PURPLE   = '#7C3AED'
PURPLE_L = '#EDE9FE'
RED      = '#DC2626'
RED_L    = '#FEE2E2'
GRAY9    = '#0F172A'
GRAY7    = '#334155'
GRAY5    = '#64748B'
GRAY2    = '#E2E8F0'
WHITE    = '#FFFFFF'
BG       = '#F8F9FF'

def save(fig, name):
    fig.savefig(name, dpi=160, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved: {name}")

def title_bar(ax, fig, text, sub=''):
    fig.patch.set_facecolor(BG)
    ax.text(0.5, 1.01, text, transform=ax.transAxes,
            ha='center', va='bottom', fontsize=16, fontweight='bold', color=GRAY9)
    if sub:
        ax.text(0.5, 0.995, sub, transform=ax.transAxes,
                ha='center', va='bottom', fontsize=9, color=GRAY5)

# ══════════════════════════════════════════════════════════════════════════════
# 1. TIMELINE CHART
# ══════════════════════════════════════════════════════════════════════════════
def make_timeline():
    fig, ax = plt.subplots(figsize=(22, 11))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    start = datetime(2026, 3, 1)
    end   = datetime(2026, 5, 8)
    total_days = (end - start).days

    phases = [
        # (Label, start_offset_days, duration_days, color, milestone)
        ("Project Planning & Requirements Analysis",  0,  7,  '#6366F1', "Mar 1"),
        ("System Architecture & Database Design",     7,  7,  '#8B5CF6', "Mar 8"),
        ("Backend Core: FastAPI + Auth Setup",        14, 9,  '#2563EB', "Mar 15"),
        ("Database Models & API Endpoints",           23, 7,  '#0EA5E9', "Mar 24"),
        ("AI/RAG Pipeline (FAISS + Gemini Embed)",    28, 9,  '#059669', "Mar 29"),
        ("Document Ingestion & Chunking Engine",      35, 6,  '#10B981', "Apr 5"),
        ("Frontend: React + Auth + Dashboard",        37, 8,  '#F59E0B', "Apr 7"),
        ("Advanced Analysis Features (10 Tabs)",      44, 9,  '#D97706', "Apr 14"),
        ("Synthesis Engine & Multi-Paper Analysis",   51, 7,  '#DB2777', "Apr 21"),
        ("Chat Memory + BM25 Reranker Integration",   56, 5,  '#EC4899', "Apr 26"),
        ("Export (PDF), Profile, Privacy Policy",     60, 5,  '#7C3AED', "Apr 30"),
        ("Testing, Bug Fixes & Performance Tuning",   64, 4,  '#DC2626', "May 4"),
        ("Documentation & Final Deployment",          67, 1,  '#374151', "May 8"),
    ]

    milestones = [
        (0,   "▶ Project Start",      '#6366F1'),
        (14,  "✓ Auth Ready",         '#2563EB'),
        (28,  "✓ RAG Live",           '#059669'),
        (44,  "✓ 10 AI Tabs Done",    '#D97706'),
        (60,  "✓ Export & UI Polish", '#7C3AED'),
        (67,  "✓ Final Deployment",   '#374151'),
    ]

    bar_h = 0.6
    n = len(phases)

    for i, (label, s, d, color, ms_label) in enumerate(phases):
        y = n - i - 1
        x_start = s / total_days * 20
        x_w     = d / total_days * 20

        # Shadow
        shadow = FancyBboxPatch((x_start + 0.05, y - bar_h/2 - 0.04), x_w, bar_h,
                                 boxstyle="round,pad=0.05",
                                 facecolor='#00000015', edgecolor='none')
        ax.add_patch(shadow)

        # Bar
        bar = FancyBboxPatch((x_start, y - bar_h/2), x_w, bar_h,
                              boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='white',
                              linewidth=1.2, alpha=0.92)
        ax.add_patch(bar)

        # Label inside bar if wide enough
        if x_w > 0.8:
            ax.text(x_start + x_w/2, y, label,
                    ha='center', va='center', fontsize=7.2,
                    color='white', fontweight='bold')

        # Phase label on left
        ax.text(-0.3, y, f"{i+1:02d}. {label}",
                ha='right', va='center', fontsize=7.5,
                color=color, fontweight='bold')

        # Date label on right
        ax.text(20.3, y, ms_label,
                ha='left', va='center', fontsize=7,
                color=GRAY5)

    # Milestone diamonds
    for day_off, label, color in milestones:
        x = day_off / total_days * 20
        ax.plot(x, n + 0.2, 'D', ms=9, color=color, zorder=8)
        ax.text(x, n + 0.55, label, ha='center', va='bottom', fontsize=7,
                color=color, fontweight='bold', rotation=25)

    # Month grid lines
    month_starts = [
        (datetime(2026, 3, 1),  "March 2026"),
        (datetime(2026, 4, 1),  "April 2026"),
        (datetime(2026, 5, 1),  "May 2026"),
    ]
    for dt, mlabel in month_starts:
        x = (dt - start).days / total_days * 20
        ax.axvline(x, color=GRAY2, lw=1.2, ls='--', zorder=0)
        ax.text(x + 0.1, -1.0, mlabel, fontsize=9,
                color=GRAY5, fontweight='bold')

    # Week grid
    d = start
    while d <= end:
        x = (d - start).days / total_days * 20
        ax.axvline(x, color='#E2E8F0', lw=0.4, zorder=0)
        d += timedelta(days=7)

    ax.set_xlim(-8.5, 21.5)
    ax.set_ylim(-1.5, n + 1.5)
    ax.axis('off')

    ax.text(6, n + 1.8,
            'SciSynthesis — Project Timeline',
            ha='center', va='bottom', fontsize=18,
            fontweight='bold', color=GRAY9)
    ax.text(6, n + 1.35,
            'Development Schedule: March 1, 2026 – May 8, 2026',
            ha='center', va='bottom', fontsize=10, color=GRAY5)

    # Legend
    legend_items = [
        mpatches.Patch(facecolor='#6366F1', label='Planning'),
        mpatches.Patch(facecolor='#2563EB', label='Backend'),
        mpatches.Patch(facecolor='#059669', label='AI/RAG'),
        mpatches.Patch(facecolor='#F59E0B', label='Frontend'),
        mpatches.Patch(facecolor='#DB2777', label='Integration'),
        mpatches.Patch(facecolor='#DC2626', label='Testing'),
        mpatches.Patch(facecolor='#374151', label='Deployment'),
        Line2D([0],[0], marker='D', color='w', markerfacecolor=GRAY5, markersize=8, label='Milestone'),
    ]
    ax.legend(handles=legend_items, loc='lower right',
              fontsize=8, framealpha=0.9, ncol=4,
              bbox_to_anchor=(1.0, -0.08))

    ax.text(10, -1.35,
            '© 2026 SciSynthesis — Krina Pansuriya',
            ha='center', fontsize=7.5, color='#94A3B8')

    save(fig, 'Diagram_1_Timeline.png')


# ══════════════════════════════════════════════════════════════════════════════
# 2. USE CASE DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════
def make_usecase():
    fig, ax = plt.subplots(figsize=(26, 18))
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 18)
    ax.axis('off')

    def sys_box(x, y, w, h, lbl, bg, bd, fs=9):
        ax.add_patch(FancyBboxPatch((x,y), w, h, boxstyle="round,pad=0.15",
                                     facecolor=bg, edgecolor=bd, linewidth=2.2))
        ax.text(x+w/2, y+h-0.25, lbl, ha='center', va='top',
                fontsize=fs, fontweight='bold', color=bd)

    def uc(x, y, w, h, txt, bd=INDIGO):
        ax.add_patch(Ellipse((x,y), w, h, facecolor=WHITE, edgecolor=bd, linewidth=1.6, zorder=4))
        lines = []
        words = txt.split()
        cur = []
        for ww in words:
            cur.append(ww)
            if len(' '.join(cur)) > 14:
                lines.append(' '.join(cur[:-1]))
                cur = [ww]
        lines.append(' '.join(cur))
        lines = [l for l in lines if l]
        for i, l in enumerate(lines):
            ax.text(x, y - (i-(len(lines)-1)/2)*0.175, l,
                    ha='center', va='center', fontsize=7.2,
                    color=GRAY9, fontweight='semibold', zorder=5)

    def stick(x, y, lbl, col=INDIGO):
        ax.add_patch(plt.Circle((x, y+0.5), 0.2, color=col, zorder=6))
        ax.plot([x,x],[y+0.3,y-0.15], color=col, lw=2.5, zorder=6)
        ax.plot([x-0.28,x+0.28],[y+0.08,y+0.08], color=col, lw=2.5, zorder=6)
        ax.plot([x,x-0.22],[y-0.15,y-0.55], color=col, lw=2.5, zorder=6)
        ax.plot([x,x+0.22],[y-0.15,y-0.55], color=col, lw=2.5, zorder=6)
        ax.text(x, y-0.75, lbl, ha='center', va='top', fontsize=8, fontweight='bold', color=col)

    def ln(x1,y1,x2,y2,col='#94A3B8', lw=0.9, ls='-'):
        ax.plot([x1,x2],[y1,y2], color=col, lw=lw, ls=ls, zorder=2)

    # System boundary
    sys_box(2.2, 0.4, 21.4, 17.0, 'SciSynthesis Platform', INDIGO_L, INDIGO, 13)

    # Sub-systems
    sys_box(2.6, 14.2, 6.2, 2.9, 'Authentication', BLUE_L, BLUE)
    sys_box(9.3, 14.2, 5.8, 2.9, 'Document Management', GREEN_L, GREEN)
    sys_box(15.5, 14.2, 7.7, 2.9, 'Project Management', PINK_L, PINK)
    sys_box(2.6, 0.7, 11.8, 13.2, 'Advanced Analysis & AI Features', ORANGE_L, ORANGE, 10)
    sys_box(15.5, 0.7, 7.7, 13.2, 'Synthesis & Reporting', PURPLE_L, PURPLE, 10)

    # Auth UCs
    for x,y,t in [(3.8,16.6,'Register Account'),(6.2,16.6,'Email/Password Login'),
                   (3.8,15.3,'Phone OTP Login'),(6.2,15.3,'Update Profile & Avatar')]:
        uc(x,y,2.2,0.6,t,BLUE)
    # Doc UCs
    for x,y,t in [(10.3,16.6,'Upload PDF'),(12.6,16.6,'Batch Upload PDFs'),
                   (10.3,15.3,'Delete Paper'),(12.6,15.3,'View History')]:
        uc(x,y,2.0,0.6,t,GREEN)
    # Project UCs
    for x,y,t in [(16.5,16.6,'Create Project'),(18.7,16.6,'View Projects'),
                   (20.9,16.6,'Delete Project'),(16.5,15.3,'Add Notes'),
                   (18.7,15.3,'View Notes'),(20.9,15.3,'Change Password')]:
        uc(x,y,1.9,0.6,t,PINK)
    # Advanced UCs
    for x,y,t in [
        (3.9,13.0,'Analyze Paper'),(7.0,13.0,'Search Papers'),(10.2,13.0,'Global Search'),
        (3.9,11.5,'Chat with Papers'),(7.0,11.5,'Research Gaps'),(10.2,11.5,'Compare Papers'),
        (3.9,10.0,'Generate Hypothesis'),(7.0,10.0,'Project Ideas'),(10.2,10.0,'Generate Citation'),
        (3.9, 8.5,'Extract Keywords'),(7.0, 8.5,'Find Similar Papers'),(10.2, 8.5,'Cluster Papers'),
        (3.9, 7.0,'Literature Review'),(7.0, 7.0,'Detect Gaps'),(10.2, 7.0,'View Search History'),
        (3.9, 5.5,'Embed Chunks'),(7.0, 5.5,'BM25 Reranking'),(10.2, 5.5,'Semantic Retrieval'),
        (3.9, 4.0,'Rate Limiting'),(7.0, 4.0,'Security Headers'),(10.2, 4.0,'CORS Validation'),
    ]:
        uc(x,y,2.2,0.65,t,ORANGE)
    # Synthesis UCs
    for x,y,t in [
        (17.2,13.0,'Synthesize Papers'),(20.8,13.0,'Detect Contradictions'),
        (17.2,11.5,'Consensus Findings'),(20.8,11.5,'Strategic Next Steps'),
        (17.2,10.0,'Export Analysis PDF'),(20.8,10.0,'Export Synthesis PDF'),
        (17.2, 8.5,'Subscribe Newsletter'),(20.8, 8.5,'View Privacy Policy'),
        (17.2, 7.0,'OTP Authentication'),(20.8, 7.0,'Embedding Cache'),
        (17.2, 5.5,'Chat Memory'),(20.8, 5.5,'Vector Similarity'),
        (17.2, 4.0,'JWT Auth Cookie'),(20.8, 4.0,'API Health Check'),
    ]:
        uc(x,y,2.8,0.65,t,PURPLE)

    # Actors
    stick(1.2, 10.5, 'Researcher\n(User)', INDIGO)
    stick(1.2, 4.5,  'Admin\n(User)', '#7C3AED')

    # External systems
    for x,y,lbl,col in [
        (25.0,15.5,'Google\nGemini AI',GREEN),
        (25.0,13.5,'Redis\nCache',BLUE),
        (25.0,11.5,'FAISS\nVector DB',PURPLE),
        (25.0, 9.5,'EmailJS',ORANGE),
        (25.0, 7.5,'PyPDF\nExtractor',RED),
    ]:
        ax.add_patch(FancyBboxPatch((x-0.7,y-0.35),1.4,0.7,
                                    boxstyle="round,pad=0.07",
                                    facecolor=WHITE, edgecolor=col, linewidth=2, zorder=6))
        ax.text(x,y, lbl, ha='center', va='center', fontsize=7, fontweight='bold', color=col, zorder=7)

    # Association lines - researcher to use cases
    rx, ry = 1.2, 10.5
    for ux,uy in [(3.8,16.6),(6.2,16.6),(3.8,15.3),(6.2,15.3),
                   (10.3,16.6),(12.6,16.6),(10.3,15.3),
                   (16.5,16.6),(18.7,16.6),(16.5,15.3),(18.7,15.3),
                   (3.9,13.0),(7.0,13.0),(10.2,13.0),
                   (3.9,11.5),(7.0,11.5),(10.2,11.5),
                   (3.9,10.0),(7.0,10.0),(10.2,10.0),
                   (3.9,8.5),(7.0,8.5),(10.2,8.5),
                   (3.9,7.0),(7.0,7.0),
                   (17.2,13.0),(20.8,13.0),(17.2,11.5),(17.2,10.0),(20.8,10.0),
                   (17.2,8.5)]:
        ln(rx+0.32, ry, ux-1.1, uy, '#CBD5E1', 0.7)

    # Admin lines
    for ux,uy in [(3.9,4.0),(7.0,4.0),(10.2,4.0),(17.2,4.0),(20.8,4.0),(17.2,5.5)]:
        ln(1.2+0.32, 4.5, ux-1.1, uy, '#C4B5FD', 0.7)

    # External system lines
    for ux,uy in [(10.2,13.0),(17.2,13.0),(3.9,10.0),(3.9,7.0),(10.2,11.5)]:
        ln(24.3, 15.5, ux+1.1, uy, '#86EFAC', 0.7)
    for ux,uy in [(20.8,7.0),(17.2,5.5),(17.2,7.0)]:
        ln(24.3, 13.5, ux+1.4, uy, '#7DD3FC', 0.7)
    for ux,uy in [(20.8,5.5),(10.2,5.5),(7.0,8.5)]:
        ln(24.3, 11.5, ux+1.4, uy, '#C4B5FD', 0.7)
    ln(24.3, 9.5, 20.8+1.4, 8.5, '#FCD34D', 0.7)
    for ux,uy in [(3.9,5.5),(10.3,16.6)]:
        ln(24.3, 7.5, ux+1.1, uy, '#FCA5A5', 0.7)

    ax.text(13, 17.75, 'SciSynthesis — Use Case Diagram',
            ha='center', va='center', fontsize=17, fontweight='bold', color=GRAY9)
    ax.text(13, 17.3, 'AI-Powered Scientific Research Assistant · UML 2.x',
            ha='center', va='center', fontsize=9, color=GRAY5)
    ax.text(13, 0.15, '© 2026 SciSynthesis — Krina Pansuriya',
            ha='center', fontsize=7.5, color='#94A3B8')

    save(fig, 'Diagram_2_Use_Case.png')


# ══════════════════════════════════════════════════════════════════════════════
# 3. SEQUENCE DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════
def make_sequence():
    fig, ax = plt.subplots(figsize=(24, 18))
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 18)
    ax.axis('off')

    actors = [
        (1.5,  'User\n(Browser)',    INDIGO),
        (4.5,  'React\nFrontend',    BLUE),
        (7.5,  'FastAPI\nBackend',   GREEN),
        (10.5, 'Auth\nMiddleware',   ORANGE),
        (13.5, 'RAG\nPipeline',      PURPLE),
        (16.5, 'Gemini\nAI API',     RED),
        (19.5, 'FAISS\nVector DB',   '#0891B2'),
        (22.5, 'SQLite\nDatabase',   GRAY7),
    ]

    top_y = 17.2
    bot_y = 0.5

    # Lifeline boxes and lines
    for x, lbl, col in actors:
        ax.add_patch(FancyBboxPatch((x-0.75, top_y-0.45), 1.5, 0.85,
                                    boxstyle="round,pad=0.08",
                                    facecolor=col, edgecolor='white', linewidth=1.5, zorder=5))
        for line in lbl.split('\n'):
            idx = lbl.split('\n').index(line)
            ax.text(x, top_y - 0.02 + (0.18 if len(lbl.split('\n'))>1 else 0) - idx*0.22,
                    line, ha='center', va='center', fontsize=7.5,
                    fontweight='bold', color=WHITE, zorder=6)
        ax.plot([x,x],[bot_y, top_y-0.45], color=col, lw=1, ls='--', alpha=0.5, zorder=1)

    def msg(y, x1, x2, txt, col=GRAY7, ret=False, note=''):
        direction = 1 if x2 > x1 else -1
        ls = '--' if ret else '-'
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.5,
                                   linestyle=ls, mutation_scale=14), zorder=4)
        mx = (x1+x2)/2
        ax.text(mx, y+0.12, txt, ha='center', va='bottom',
                fontsize=7.2, color=col, fontweight='semibold', zorder=5)
        if note:
            ax.text(mx, y-0.14, note, ha='center', va='top',
                    fontsize=6.2, color=GRAY5, style='italic', zorder=5)

    def activation(x, y_start, y_end, col):
        ax.add_patch(FancyBboxPatch((x-0.1, y_end), 0.2, y_start-y_end,
                                    boxstyle="square,pad=0",
                                    facecolor=col, edgecolor='white',
                                    linewidth=0.5, alpha=0.5, zorder=3))

    def section(y, label, col):
        ax.add_patch(FancyBboxPatch((0.1, y-0.18), 23.8, 0.3,
                                    boxstyle="round,pad=0.04",
                                    facecolor=col+'22', edgecolor=col, linewidth=1, zorder=2))
        ax.text(0.3, y, label, va='center', fontsize=7.5,
                fontweight='bold', color=col, zorder=5)

    # ── Sequence 1: Login ──
    section(16.5, '① User Login Flow', BLUE)
    msg(16.0, 1.5, 4.5, 'POST /login {email, password}', BLUE)
    activation(4.5, 16.0, 15.5, BLUE)
    msg(15.8, 4.5, 7.5, 'Forward credentials', GREEN)
    activation(7.5, 15.8, 15.3, GREEN)
    msg(15.6, 7.5, 10.5, 'Verify JWT / authenticate', ORANGE)
    activation(10.5, 15.6, 15.2, ORANGE)
    msg(15.4, 10.5, 22.5, 'SELECT user WHERE email=?', GRAY7)
    msg(15.2, 22.5, 10.5, 'User record', GRAY7, ret=True)
    msg(15.0, 10.5, 7.5, 'bcrypt.verify(password)', ORANGE, ret=True)
    msg(14.8, 7.5, 4.5, 'JWT token + Set httpOnly cookie', GREEN, ret=True)
    msg(14.6, 4.5, 1.5, '200 OK — Redirect to Dashboard', BLUE, ret=True)

    # ── Sequence 2: Upload & Analyze ──
    section(14.0, '② PDF Upload & Auto-Analysis Flow', GREEN)
    msg(13.5, 1.5, 4.5, 'POST /analyze (PDF file + project_id)', GREEN)
    activation(4.5, 13.5, 8.5, GREEN)
    msg(13.3, 4.5, 7.5, 'Multipart form upload', GREEN)
    activation(7.5, 13.3, 8.5, GREEN)
    msg(13.1, 7.5, 22.5, 'INSERT paper record', GRAY7)
    msg(12.9, 22.5, 7.5, 'paper_id = 42', GRAY7, ret=True)
    msg(12.7, 7.5, 13.5, 'ingest_document(paper_id, content)', PURPLE)
    activation(13.5, 12.7, 8.8, PURPLE)
    msg(12.5, 13.5, 16.5, 'embed_content(chunks[])', RED)
    activation(16.5, 12.5, 12.0, RED)
    msg(12.3, 16.5, 13.5, '768-dim vectors[]', RED, ret=True)
    msg(12.1, 13.5, 19.5, 'add(chunk_ids, embeddings)', '#0891B2')
    msg(11.9, 19.5, 13.5, 'FAISS index updated', '#0891B2', ret=True)
    msg(11.7, 13.5, 22.5, 'INSERT document_chunks', GRAY7)
    msg(11.5, 7.5, 16.5, 'generate_content(full_text, prompt)', RED)
    activation(16.5, 11.5, 10.8, RED)
    msg(11.1, 16.5, 7.5, 'AnalysisResponse (JSON)', RED, ret=True)
    msg(10.9, 7.5, 22.5, 'UPDATE paper.result_json', GRAY7)
    msg(10.7, 7.5, 4.5, 'AnalysisResponse', GREEN, ret=True)
    msg(10.5, 4.5, 1.5, 'Render analysis results', BLUE, ret=True)

    # ── Sequence 3: RAG Chat ──
    section(10.0, '③ Conversational RAG Chat Flow', PURPLE)
    msg(9.5, 1.5, 4.5, 'POST /chat {query, paper_ids}', PURPLE)
    msg(9.3, 4.5, 7.5, 'Forward query', PURPLE)
    activation(7.5, 9.3, 5.5, PURPLE)
    msg(9.1, 7.5, 13.5, 'retrieve_chunks(query, paper_ids)', PURPLE)
    activation(13.5, 9.1, 5.8, PURPLE)
    msg(8.9, 13.5, 16.5, 'embed_content(query)', RED)
    msg(8.7, 16.5, 13.5, 'query_vector[768]', RED, ret=True)
    msg(8.5, 13.5, 19.5, 'search(query_vec, top_k×15)', '#0891B2')
    msg(8.3, 19.5, 13.5, 'candidate chunk_ids + distances', '#0891B2', ret=True)
    msg(8.1, 13.5, 22.5, 'SELECT chunks WHERE id IN (...)', GRAY7)
    msg(7.9, 22.5, 13.5, 'chunk texts + metadata', GRAY7, ret=True)
    msg(7.7, 13.5, 7.5, 'rerank(BM25+semantic) → top_k', PURPLE, ret=True)
    msg(7.5, 7.5, 13.5, 'build_context(history + chunks)', PURPLE)
    msg(7.3, 13.5, 16.5, 'generate_content(context+query)', RED)
    msg(7.1, 16.5, 13.5, 'answer with citations', RED, ret=True)
    msg(6.9, 13.5, 7.5, 'ChatResponse', PURPLE, ret=True)
    msg(6.7, 7.5, 4.5, '{answer, citations, confidence}', PURPLE, ret=True)
    msg(6.5, 4.5, 1.5, 'Render chat message', BLUE, ret=True)

    # ── Sequence 4: Synthesis ──
    section(6.1, '④ Multi-Paper Synthesis Flow', ORANGE)
    msg(5.7, 1.5, 4.5, 'POST /synthesis/{project_id}', ORANGE)
    msg(5.5, 4.5, 7.5, 'Trigger synthesis', ORANGE)
    activation(7.5, 5.5, 1.5, ORANGE)
    msg(5.3, 7.5, 22.5, 'SELECT papers WHERE project_id=?', GRAY7)
    msg(5.1, 22.5, 7.5, 'papers[] with result_json', GRAY7, ret=True)
    msg(4.9, 7.5, 16.5, 'generate_content(all papers data)', RED)
    activation(16.5, 4.9, 4.0, RED)
    msg(4.7, 16.5, 7.5, 'SynthesisResponse (JSON)', RED, ret=True)
    msg(4.5, 7.5, 4.5, 'consensus + gaps + contradictions', ORANGE, ret=True)
    msg(4.3, 4.5, 1.5, 'Render synthesis report', BLUE, ret=True)
    msg(4.0, 1.5, 4.5, 'Click Export PDF', ORANGE)
    msg(3.8, 4.5, 1.5, 'jsPDF.save() — browser download', ORANGE, ret=True)

    ax.text(12, 17.8, 'SciSynthesis — Sequence Diagram',
            ha='center', fontsize=17, fontweight='bold', color=GRAY9)
    ax.text(12, 17.45, 'Key Interaction Flows: Login · Upload/Analyze · RAG Chat · Synthesis',
            ha='center', fontsize=9, color=GRAY5)
    ax.text(12, 0.15, '© 2026 SciSynthesis — Krina Pansuriya',
            ha='center', fontsize=7.5, color='#94A3B8')

    save(fig, 'Diagram_3_Sequence.png')


# ══════════════════════════════════════════════════════════════════════════════
# 4. ACTIVITY DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════
def make_activity():
    fig, ax = plt.subplots(figsize=(20, 26))
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 26)
    ax.axis('off')

    def node(x, y, w, h, txt, bg=INDIGO_L, bd=INDIGO, fs=8.5, bold=True):
        ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                                    boxstyle="round,pad=0.12",
                                    facecolor=bg, edgecolor=bd, linewidth=1.8, zorder=4))
        lines = txt.split('\n')
        for i, l in enumerate(lines):
            ax.text(x, y+(len(lines)-1-2*i)*0.16, l, ha='center', va='center',
                    fontsize=fs, fontweight='bold' if bold else 'normal',
                    color=bd if bg!=bd else WHITE, zorder=5)

    def diamond(x, y, w, h, txt, col=ORANGE):
        xs = [x, x+w/2, x, x-w/2, x]
        ys = [y+h/2, y, y-h/2, y, y+h/2]
        ax.fill(xs, ys, facecolor=ORANGE_L, edgecolor=col, linewidth=2, zorder=4)
        ax.text(x, y, txt, ha='center', va='center', fontsize=7.5,
                fontweight='bold', color=col, zorder=5)

    def start_end(x, y, r=0.22, filled=True):
        c = plt.Circle((x,y), r, color=GRAY9 if filled else WHITE,
                        ec=GRAY9, lw=2.5, zorder=5)
        ax.add_patch(c)
        if not filled:
            c2 = plt.Circle((x,y), r*0.6, color=GRAY9, zorder=6)
            ax.add_patch(c2)

    def arr(x1,y1,x2,y2,col=GRAY7, lbl=''):
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.5, mutation_scale=14), zorder=3)
        if lbl:
            ax.text((x1+x2)/2+0.15,(y1+y2)/2, lbl, fontsize=7, color=col, style='italic')

    def swim(x, w, label, col):
        ax.add_patch(FancyBboxPatch((x, 0.3), w, 25.4, boxstyle="round,pad=0.05",
                                    facecolor=col+'15', edgecolor=col, linewidth=1.5, alpha=0.7, zorder=0))
        ax.text(x+w/2, 25.5, label, ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=col)

    # Swim lanes
    swim(0.2, 6.6, 'User', INDIGO)
    swim(7.0, 6.6, 'Backend / FastAPI', GREEN)
    swim(13.8, 6.2, 'AI / RAG Pipeline', ORANGE)

    # ── Flow ──
    start_end(3.5, 24.8)
    arr(3.5,24.6, 3.5,24.1)
    node(3.5, 23.7, 4.0, 0.65, 'Open SciSynthesis\nApp', INDIGO_L, INDIGO)
    arr(3.5,23.35, 3.5,22.8)

    diamond(3.5, 22.4, 3.0, 0.75, 'Logged In?', ORANGE)
    arr(3.5,22.0, 3.5,21.45, ORANGE, 'No')
    node(3.5, 21.1, 4.0, 0.65, 'Login / Register', BLUE_L, BLUE)
    arr(3.5,20.77, 3.5,20.2)
    node(3.5, 19.85, 4.0, 0.65, 'Authenticate\n(JWT Cookie Set)', BLUE_L, BLUE)
    arr(3.5,19.52, 3.5,18.95, ORANGE, 'Yes')
    node(3.5, 18.6, 4.0, 0.65, 'Go to Dashboard', INDIGO_L, INDIGO)

    # Fork
    ax.plot([3.5,3.5],[18.28,17.8], color=GRAY7, lw=1.5)
    ax.plot([2.0,12.0],[17.8,17.8], color=GRAY7, lw=2.5)
    for xf in [2.0, 7.0, 12.0]:
        arr(xf,17.8, xf,17.25, GRAY7)

    # Branch 1 – Upload
    node(2.0, 16.9, 3.6, 0.65, 'Select & Upload\nPDF File', INDIGO_L, INDIGO)
    arr(2.0,16.57, 8.5,16.0)
    node(8.5, 15.65, 4.5, 0.65, 'Extract Text\n(PyPDF page-by-page)', GREEN_L, GREEN)
    arr(8.5,15.32, 8.5,14.75)
    node(8.5, 14.4, 4.5, 0.65, 'Chunk Text\n(500 words, 100 overlap)', GREEN_L, GREEN)
    arr(8.5,14.07, 15.5,13.5)
    node(15.5, 13.15, 5.2, 0.65, 'Generate Embeddings\n(Gemini embedding-001)', ORANGE_L, ORANGE)
    arr(15.5,12.82, 15.5,12.25)
    node(15.5, 11.9, 5.2, 0.65, 'Cache in Redis\n(SHA256, 7-day TTL)', ORANGE_L, ORANGE)
    arr(15.5,11.57, 15.5,11.0)
    node(15.5, 10.65, 5.2, 0.65, 'Index in FAISS\n(IndexIDMap, L2)', ORANGE_L, ORANGE)
    arr(15.5,10.32, 8.5,9.75)
    node(8.5, 9.4, 4.5, 0.65, 'Store Chunks\nin SQLite', GREEN_L, GREEN)
    arr(8.5,9.07, 8.5,8.5)
    node(8.5, 8.15, 4.5, 0.65, 'Analyze with Gemini LLM\n(hypothesis, gaps, findings)', GREEN_L, GREEN)
    arr(8.5,7.82, 8.5,7.25)
    node(8.5, 6.9, 4.5, 0.65, 'Save result_json\nto papers table', GREEN_L, GREEN)
    arr(8.5,6.57, 2.0,6.0)
    node(2.0, 5.65, 3.6, 0.65, 'Display Analysis\nResults to User', INDIGO_L, INDIGO)

    # Branch 2 – Search/Chat
    node(7.0, 16.9, 3.6, 0.65, 'Type Search\nQuery / Chat', INDIGO_L, INDIGO)
    arr(7.0,16.57, 8.5,16.0)

    # Branch 3 – Synthesis
    node(12.0, 16.9, 3.6, 0.65, 'Click Synthesize\nProject', INDIGO_L, INDIGO)
    arr(12.0,16.57, 8.5,16.0)

    # Decision after display
    arr(2.0,5.32, 2.0,4.75)
    diamond(2.0, 4.35, 3.2, 0.75, 'More Actions?', ORANGE)
    arr(0.5,4.35, 0.5,3.5, ORANGE, 'Yes')
    ax.annotate('', xy=(2.0,16.9-0.32), xytext=(0.5,3.5),
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2, linestyle='dashed'))
    arr(2.0,3.97, 2.0,3.3, ORANGE, 'No')
    node(2.0, 2.95, 3.6, 0.65, 'Logout / End\nSession', INDIGO_L, INDIGO)
    arr(2.0,2.62, 2.0,2.05)
    start_end(2.0, 1.75, 0.22, False)

    ax.text(10, 25.75, 'SciSynthesis — Activity Diagram',
            ha='center', fontsize=17, fontweight='bold', color=GRAY9)
    ax.text(10, 25.38, 'Document Upload, Analysis & RAG Pipeline Workflow',
            ha='center', fontsize=9, color=GRAY5)
    ax.text(10, 0.15, '© 2026 SciSynthesis — Krina Pansuriya',
            ha='center', fontsize=7.5, color='#94A3B8')

    save(fig, 'Diagram_4_Activity.png')


# ══════════════════════════════════════════════════════════════════════════════
# 5. CLASS DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════
def make_class():
    fig, ax = plt.subplots(figsize=(26, 20))
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 20)
    ax.axis('off')

    def cls(x, y, name, attrs, methods, col=INDIGO, w=5.5):
        row_h = 0.38
        n_attrs = len(attrs)
        n_meths = len(methods)
        total_h = 0.7 + n_attrs*row_h + 0.12 + n_meths*row_h + 0.15

        # Header
        ax.add_patch(FancyBboxPatch((x, y), w, 0.65,
                                    boxstyle="round,pad=0.0",
                                    facecolor=col, edgecolor=col, linewidth=0))
        ax.text(x+w/2, y+0.32, f'«class»', ha='center', va='center',
                fontsize=6.5, color=WHITE+'aa', style='italic')
        ax.add_patch(FancyBboxPatch((x, y+0.38), w, 0.27,
                                    boxstyle="square,pad=0",
                                    facecolor=col, edgecolor=col))
        ax.text(x+w/2, y+0.52, name, ha='center', va='center',
                fontsize=9, fontweight='bold', color=WHITE)

        # Body
        body_h = total_h - 0.65
        ax.add_patch(FancyBboxPatch((x, y-body_h+0.0), w, body_h,
                                    boxstyle="square,pad=0",
                                    facecolor=WHITE, edgecolor=col, linewidth=1.8))

        # Attrs
        cy = y - 0.08
        for a in attrs:
            cy -= row_h
            icon = '+ ' if a.startswith('+') else '- ' if a.startswith('-') else '# '
            txt  = a.lstrip('+-# ')
            ax.text(x+0.15, cy+row_h/2, icon, va='center', fontsize=7,
                    color=GREEN if icon=='+ ' else RED if icon=='- ' else ORANGE)
            ax.text(x+0.42, cy+row_h/2, txt, va='center', fontsize=7, color=GRAY7)

        # Divider
        cy -= 0.1
        ax.plot([x+0.1, x+w-0.1], [cy+row_h/2, cy+row_h/2], color=GRAY2, lw=1)

        # Methods
        for m in methods:
            cy -= row_h
            ax.text(x+0.15, cy+row_h/2, '+ ', va='center', fontsize=7, color=BLUE)
            ax.text(x+0.42, cy+row_h/2, m, va='center', fontsize=7,
                    color=BLUE, style='italic')

        return x+w/2, y+0.52, x, y-body_h, x+w, y+0.65  # cx, cy_top, ...

    def rel(x1,y1,x2,y2, kind='assoc', lbl='', mult1='', mult2=''):
        if kind == 'inherit':
            ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                        arrowprops=dict(arrowstyle='-|>', color=INDIGO, lw=1.5,
                                        mutation_scale=14))
        elif kind == 'compose':
            ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                        arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5,
                                        mutation_scale=12))
            ax.plot(x1,y1,'D', ms=7, color=GREEN, zorder=5)
        else:
            ax.plot([x1,x2],[y1,y2], color=GRAY5, lw=1.2, ls='--')
        if lbl:
            ax.text((x1+x2)/2,(y1+y2)/2+0.12, lbl, ha='center',
                    fontsize=6.5, color=GRAY5, style='italic')
        if mult1:
            ax.text(x1+0.15*(x2-x1),y1+0.15*(y2-y1)+0.1, mult1, fontsize=6.5, color=GRAY5)
        if mult2:
            ax.text(x2-0.15*(x2-x1),y2+0.1*(y2-y1 if y2!=y1 else 1)+0.1, mult2, fontsize=6.5, color=GRAY5)

    # Classes
    cls(0.3, 14.5, 'User',
        ['- id: Integer PK',
         '+ email: String UNIQUE',
         '- hashed_password: String',
         '+ full_name: String?',
         '+ institution: String?',
         '+ bio: String?',
         '+ phone_number: String?',
         '+ profile_picture: String?',
         '+ created_at: DateTime'],
        ['+ get_papers()',
         '+ get_projects()',
         '+ verify_password()',
         '+ create_access_token()'],
        INDIGO, 5.8)

    cls(7.0, 14.5, 'Paper',
        ['- id: Integer PK',
         '+ user_id: Integer FK',
         '+ project_id: Integer FK?',
         '+ title: String',
         '+ filename: String',
         '+ result_json: JSON',
         '+ created_at: DateTime'],
        ['+ get_chunks()',
         '+ get_notes()',
         '+ delete_with_chunks()',
         '+ export_analysis()'],
        GREEN, 5.5)

    cls(13.2, 14.5, 'DocumentChunk',
        ['- id: Integer PK',
         '+ paper_id: Integer FK',
         '+ text: Text',
         '+ page_number: Integer?',
         '+ chunk_index: Integer'],
        ['+ get_embedding()',
         '+ to_faiss_vector()'],
        ORANGE, 5.3)

    cls(19.2, 14.5, 'Project',
        ['- id: Integer PK',
         '+ user_id: Integer FK',
         '+ name: String',
         '+ description: String?',
         '+ created_at: DateTime'],
        ['+ get_papers()',
         '+ synthesize()',
         '+ delete_cascade()'],
        PURPLE, 5.5)

    cls(0.3, 8.8, 'Note',
        ['- id: Integer PK',
         '+ paper_id: Integer FK',
         '+ user_id: Integer FK',
         '+ content: String',
         '+ created_at: DateTime'],
        ['+ create()',
         '+ list_by_paper()'],
        PINK, 5.3)

    cls(7.0, 8.8, 'SearchHistory',
        ['- id: Integer PK',
         '+ user_id: Integer FK',
         '+ query: String',
         '+ paper_ids: JSON?',
         '+ created_at: DateTime'],
        ['+ save_query()',
         '+ get_recent(limit=20)'],
        BLUE, 5.5)

    cls(13.2, 8.8, 'VectorStore',
        ['- index: FAISS IndexIDMap',
         '- dimension: Int = 768',
         '- index_path: String'],
        ['+ add(ids, embeddings)',
         '+ search(query_vec, k)',
         '+ save_to_disk()',
         '+ load_from_disk()'],
        '#0891B2', 5.3)

    cls(19.2, 8.8, 'ChatMemory',
        ['- storage: Redis | Dict',
         '- max_turns: Int = 20',
         '- ttl: Int = 86400'],
        ['+ add_turn(user_id, role, txt)',
         '+ get_history(user_id)',
         '+ clear_history(user_id)',
         '+ build_context_block()'],
        RED, 5.5)

    cls(0.3, 3.5, 'AnalysisResponse',
        ['+ research_topic: str',
         '+ extracted_hypotheses: list',
         '+ methods_summary: str',
         '+ key_findings: list',
         '+ limitations: list',
         '+ research_gap_identified: str',
         '+ confidence_score: float',
         '+ evidence_strength: float'],
        ['+ to_json()',
         '+ from_json()'],
        GRAY7, 5.8)

    cls(7.0, 3.5, 'SynthesisResponse',
        ['+ overall_theme: str',
         '+ consensus_findings: list',
         '+ major_contradictions: list',
         '+ combined_research_gap: str',
         '+ strategic_next_steps: list',
         '+ confidence_score: float'],
        ['+ to_json()',
         '+ export_pdf()'],
        '#0F766E', 5.5)

    cls(13.2, 3.5, 'RAGRetriever',
        ['- candidate_multiplier: 15',
         '- min_relevance: 0.05',
         '- max_per_paper: 3'],
        ['+ retrieve_chunks(query, db)',
         '+ embed_query(text)',
         '+ filter_by_paper_ids()',
         '+ apply_diversity_cap()'],
        '#7C3AED', 5.3)

    cls(19.2, 3.5, 'BM25Reranker',
        ['- semantic_weight: 0.65',
         '- lexical_weight: 0.35',
         '- short_thresh: 30',
         '- dedup_prefix: 120'],
        ['+ rerank_chunks(query, chunks)',
         '+ normalize_bm25()',
         '+ apply_penalty()',
         '+ deduplicate()'],
        '#B45309', 5.5)

    # Relationships
    rel(3.2,14.5, 9.7,17.3, 'compose', 'owns', '1', '*')
    rel(3.2,14.5, 21.9,17.3, 'compose', 'creates', '1', '*')
    rel(3.2,14.5, 9.7,11.5, 'compose', 'writes', '1', '*')
    rel(3.2,14.5, 10.2,11.5, 'logs', '1', '*')
    rel(9.7,14.5, 15.9,17.3, 'compose', 'has chunks', '1', '*')
    rel(9.7,14.5, 3.2,11.5, 'compose', 'has notes', '1', '*')
    rel(21.9,14.5, 9.7,17.3, 'assoc', 'groups', '1', '*')
    rel(3.2,3.5, 9.7,14.5, 'assoc', 'result of', '1', '1')
    rel(15.9,8.8, 21.9,8.8, 'assoc', 'uses')
    rel(15.9,8.8, 15.9,14.5, 'compose', 'stores vectors')
    rel(15.9,5.5, 22.0,5.5, 'assoc', 'uses')

    ax.text(13, 19.7, 'SciSynthesis — Class Diagram',
            ha='center', fontsize=17, fontweight='bold', color=GRAY9)
    ax.text(13, 19.3, 'Domain Model · Database Models · Services · Schemas',
            ha='center', fontsize=9, color=GRAY5)

    # Legend
    for i, (sym, lbl) in enumerate([('─▷', 'Inheritance'), ('◆─', 'Composition'),
                                     ('- -', 'Association'), ('+ attr', 'Public'),
                                     ('- attr', 'Private')]):
        ax.text(1.0 + i*4.5, 0.5, f'{sym}  {lbl}', fontsize=8, color=GRAY7)

    ax.text(13, 0.15, '© 2026 SciSynthesis — Krina Pansuriya',
            ha='center', fontsize=7.5, color='#94A3B8')
    save(fig, 'Diagram_5_Class.png')


# ══════════════════════════════════════════════════════════════════════════════
# 6. DFD LEVEL 0 — CONTEXT DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════
def make_dfd0():
    fig, ax = plt.subplots(figsize=(18, 12))
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')

    def ext(x, y, w, h, lbl, col):
        ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                                    boxstyle="round,pad=0.12",
                                    facecolor=col+'22', edgecolor=col, linewidth=2.5))
        for i, l in enumerate(lbl.split('\n')):
            ax.text(x, y+(len(lbl.split('\n'))-1-2*i)*0.2, l,
                    ha='center', va='center', fontsize=9,
                    fontweight='bold', color=col)

    def system(x, y, r, lbl):
        c = plt.Circle((x,y), r, facecolor=INDIGO, edgecolor=WHITE,
                        linewidth=3, zorder=4)
        ax.add_patch(c)
        lines = lbl.split('\n')
        for i, l in enumerate(lines):
            ax.text(x, y+(len(lines)-1-2*i)*0.22, l,
                    ha='center', va='center', fontsize=10,
                    fontweight='bold', color=WHITE, zorder=5)

    def flow(x1,y1,x2,y2, lbl, col=GRAY5, both=False):
        if both:
            ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                        arrowprops=dict(arrowstyle='<->', color=col, lw=2, mutation_scale=16), zorder=3)
        else:
            ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                        arrowprops=dict(arrowstyle='->', color=col, lw=2, mutation_scale=16), zorder=3)
        mx,my = (x1+x2)/2, (y1+y2)/2
        ax.add_patch(FancyBboxPatch((mx-1.2, my-0.18), 2.4, 0.36,
                                    boxstyle="round,pad=0.06",
                                    facecolor=WHITE, edgecolor=col+'66', linewidth=1, zorder=4))
        for i, l in enumerate(lbl.split('\n')):
            ax.text(mx, my+(len(lbl.split('\n'))-1-2*i)*0.13, l,
                    ha='center', va='center', fontsize=7,
                    fontweight='semibold', color=col, zorder=5)

    # System center
    system(9, 6, 2.5, 'SciSynthesis\nPlatform\n(Process 0)')

    # External entities
    ext(2.5, 10.0, 3.2, 1.1, 'Researcher\n(User)', INDIGO)
    ext(15.5, 10.0, 3.2, 1.1, 'Google\nGemini AI', GREEN)
    ext(2.5, 2.0,  3.2, 1.1, 'Redis\nCache Server', BLUE)
    ext(15.5, 2.0,  3.2, 1.1, 'FAISS\nVector DB', PURPLE)
    ext(9.0, 10.8,  3.2, 0.9, 'EmailJS\nService', ORANGE)
    ext(9.0, 1.2,   3.2, 0.9, 'SQLite\nDatabase', GRAY7)

    # Data flows
    flow(3.8,9.6, 7.1,7.1, 'PDF upload\nqueries / chat', INDIGO)
    flow(7.2,6.5, 3.8,9.2, 'Analysis results\nChat answers', INDIGO, both=False)
    flow(10.8,7.1, 14.2,9.6, 'Text prompts\nembedding requests', GREEN)
    flow(14.1,9.2, 10.9,6.5, 'LLM responses\n768-dim vectors', GREEN, False)
    flow(3.8,2.4, 7.0,4.9, 'Cache read/write\nOTP store', BLUE)
    flow(7.1,5.3, 3.9,2.5, 'Cached embeddings\nOTP codes', BLUE, False)
    flow(10.9,4.9, 14.2,2.4, 'Vector add/search', PURPLE)
    flow(14.1,2.5, 10.8,5.1, 'Chunk IDs + distances', PURPLE, False)
    flow(9.0,10.2, 9.0,8.5, 'Newsletter\nsubscription', ORANGE)
    flow(9.0,3.5, 9.0,8.0, 'SQL CRUD\noperations', GRAY7)
    flow(9.0,7.5, 9.0,2.1, 'Query results\nrecords', GRAY7, False)

    ax.text(9, 11.7, 'SciSynthesis — DFD Level 0 (Context Diagram)',
            ha='center', fontsize=15, fontweight='bold', color=GRAY9)
    ax.text(9, 11.3, 'System as a single process — all external entities and primary data flows',
            ha='center', fontsize=9, color=GRAY5)
    ax.text(9, 0.2, '© 2026 SciSynthesis — Krina Pansuriya',
            ha='center', fontsize=7.5, color='#94A3B8')

    save(fig, 'Diagram_6_DFD_Level0.png')


# ══════════════════════════════════════════════════════════════════════════════
# 7. DFD LEVEL 1
# ══════════════════════════════════════════════════════════════════════════════
def make_dfd1():
    fig, ax = plt.subplots(figsize=(24, 18))
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 18)
    ax.axis('off')

    def proc(x, y, r, num, lbl, col=INDIGO):
        ax.add_patch(plt.Circle((x,y), r, facecolor=col, edgecolor=WHITE, lw=2.5, zorder=4))
        ax.text(x, y+0.22, f'P{num}', ha='center', va='center',
                fontsize=7, fontweight='bold', color=WHITE+'88', zorder=5)
        for i, l in enumerate(lbl.split('\n')):
            ax.text(x, y - 0.05 - i*0.28, l, ha='center', va='center',
                    fontsize=8, fontweight='bold', color=WHITE, zorder=5)

    def ext(x, y, w, h, lbl, col):
        ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                                    boxstyle="round,pad=0.1",
                                    facecolor=col+'22', edgecolor=col, linewidth=2.2))
        ax.text(x, y, lbl, ha='center', va='center', fontsize=8.5,
                fontweight='bold', color=col)

    def store(x, y, w, h, lbl, col=GRAY7):
        ax.add_patch(FancyBboxPatch((x-w/2, y-h/4), w, h/2,
                                    boxstyle="square,pad=0",
                                    facecolor=WHITE, edgecolor=col, linewidth=2))
        ax.plot([x-w/2, x+w/2],[y+h/4, y+h/4], color=col, lw=2)
        ax.text(x, y, lbl, ha='center', va='center', fontsize=8, color=col, fontweight='bold')

    def fl(x1,y1,x2,y2, lbl, col=GRAY5, lw=1.5):
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                    arrowprops=dict(arrowstyle='->', color=col, lw=lw, mutation_scale=12), zorder=3)
        mx,my = (x1+x2)/2,(y1+y2)/2
        ax.text(mx,my+0.12, lbl, ha='center', fontsize=6.5, color=col,
                fontweight='semibold',
                bbox=dict(boxstyle='round,pad=0.1', facecolor=WHITE, edgecolor='none', alpha=0.8))

    # External entities
    ext(2.0, 15.0, 2.8, 0.9, 'Researcher', INDIGO)
    ext(2.0, 3.0, 2.8, 0.9, 'Researcher', INDIGO)
    ext(22.0, 15.5, 2.8, 0.9, 'Gemini AI', GREEN)
    ext(22.0, 9.0, 2.8, 0.9, 'Redis', BLUE)
    ext(22.0, 3.5, 2.8, 0.9, 'FAISS', PURPLE)
    ext(22.0, 12.0, 2.8, 0.9, 'EmailJS', ORANGE)

    # Data stores
    store(12.0, 1.2, 4.0, 0.8, 'D1: SQLite DB', GRAY7)
    store(12.0, 0.3, 4.0, 0.8, 'D2: FAISS Index', PURPLE)

    # Processes
    proc(6.0, 15.0, 1.1, 1, 'Authentication\n& Session', BLUE)
    proc(12.0, 15.0, 1.1, 2, 'Document\nIngestion', GREEN)
    proc(18.0, 15.0, 1.1, 3, 'AI Analysis\nEngine', RED)
    proc(6.0, 9.0, 1.1, 4, 'RAG\nRetrieval', ORANGE)
    proc(12.0, 9.0, 1.1, 5, 'Project\nManagement', PINK)
    proc(18.0, 9.0, 1.1, 6, 'Synthesis\nEngine', PURPLE)
    proc(6.0, 3.0, 1.1, 7, 'Advanced\nAnalytics', '#0891B2')
    proc(12.0, 3.0, 1.1, 8, 'Chat &\nMemory', '#B45309')
    proc(18.0, 3.0, 1.1, 9, 'Export &\nReporting', '#374151')

    # Flows - User → Auth
    fl(2.0+1.4,15.0, 6.0-1.1,15.0, 'credentials', INDIGO)
    fl(6.0-1.1,15.3, 2.0+1.4,15.3, 'JWT cookie', INDIGO)
    # Auth → Doc Ingestion
    fl(6.0+1.1,15.0, 12.0-1.1,15.0, 'auth context', BLUE)
    # Doc → AI Analysis
    fl(12.0+1.1,15.0, 18.0-1.1,15.0, 'raw text + meta', GREEN)
    # AI → Gemini
    fl(18.0+1.1,15.2, 22.0-1.4,15.5, 'prompts', RED)
    fl(22.0-1.4,15.2, 18.0+1.1,14.9, 'LLM response', GREEN)
    # Doc → DB
    fl(12.0,15.0-1.1, 12.0,1.6, 'chunks + paper', GRAY7)
    # AI → DB
    fl(18.0,15.0-1.1, 12.0+2.0,1.6, 'result_json', GRAY7)
    # RAG Retrieval
    fl(2.0+1.4,3.2, 6.0-1.1,3.2, 'user query', ORANGE)
    fl(6.0+1.1,9.1, 12.0-1.1,9.1, 'chunks request', ORANGE)
    fl(6.0,9.0-1.1, 12.0,1.6, 'chunk fetch', GRAY7)
    fl(6.0-1.1,8.8, 2.0+1.4,2.8, 'RAG answer', ORANGE)
    # Redis flows
    fl(6.0+1.1,8.8, 22.0-1.4,9.0, 'embed cache r/w', BLUE)
    fl(22.0-1.4,9.3, 6.0+1.1,9.3, 'cached vectors', BLUE)
    # FAISS
    fl(6.0+1.1,8.7, 22.0-1.4,3.7, 'vector search', PURPLE)
    fl(22.0-1.4,3.3, 6.0+1.1,8.5, 'chunk IDs', PURPLE)
    # Synthesis
    fl(12.0+1.1,9.0, 18.0-1.1,9.0, 'papers data', PINK)
    fl(18.0,9.0-1.1, 18.0,3.0+1.1, 'synthesis result', PURPLE)
    fl(18.0+1.1,9.2, 22.0-1.4,12.0, 'newsletter email', ORANGE)
    # Export
    fl(18.0,3.0-1.1, 18.0,1.6, 'report data', GRAY7)
    fl(18.0-1.1,3.0, 2.0+1.4,3.0, 'PDF / report', '#374151')
    # Chat memory
    fl(12.0,3.0-1.1, 12.0,0.7, 'chat history', '#B45309')
    fl(12.0+1.1,3.0, 18.0-1.1,3.0, 'export request', '#374151')
    # Project mgmt
    fl(5.5,9.0-1.1, 5.5,3.0+1.1, 'project context', PINK)
    fl(12.0,9.0-1.1, 12.0,3.0+1.1, 'project data', PINK)

    ax.text(12, 17.5, 'SciSynthesis — DFD Level 1',
            ha='center', fontsize=16, fontweight='bold', color=GRAY9)
    ax.text(12, 17.1, 'Main System Processes: Authentication, Ingestion, AI Analysis, RAG, Synthesis, Export',
            ha='center', fontsize=9, color=GRAY5)
    ax.text(12, 0.05, '© 2026 SciSynthesis — Krina Pansuriya',
            ha='center', fontsize=7.5, color='#94A3B8')

    save(fig, 'Diagram_7_DFD_Level1.png')


# ══════════════════════════════════════════════════════════════════════════════
# 8. DFD LEVEL 2 — Document Ingestion & RAG Retrieval decomposed
# ══════════════════════════════════════════════════════════════════════════════
def make_dfd2():
    fig, ax = plt.subplots(figsize=(26, 18))
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 18)
    ax.axis('off')

    def proc(x, y, r, num, lbl, col):
        ax.add_patch(plt.Circle((x,y), r, facecolor=col, edgecolor=WHITE, lw=2.5, zorder=4))
        ax.text(x, y+r*0.55, f'P{num}', ha='center', va='center',
                fontsize=6.5, color=WHITE+'99', zorder=5)
        for i, l in enumerate(lbl.split('\n')):
            ax.text(x, y-i*0.26+0.05, l, ha='center', va='center',
                    fontsize=7.5, fontweight='bold', color=WHITE, zorder=5)

    def ext(x, y, w, h, lbl, col):
        ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                                    boxstyle="round,pad=0.1",
                                    facecolor=col+'20', edgecolor=col, linewidth=2.2))
        ax.text(x, y, lbl, ha='center', va='center', fontsize=8,
                fontweight='bold', color=col)

    def store(x, y, w, lbl, col=GRAY7):
        ax.add_patch(FancyBboxPatch((x-w/2, y-0.22), w, 0.44,
                                    boxstyle="square,pad=0",
                                    facecolor=WHITE, edgecolor=col, linewidth=2))
        ax.plot([x-w/2,x+w/2],[y+0.22,y+0.22], color=col, lw=2)
        ax.text(x, y-0.02, lbl, ha='center', va='center', fontsize=8,
                color=col, fontweight='bold')

    def fl(x1,y1,x2,y2, lbl, col=GRAY5):
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.6, mutation_scale=12), zorder=3)
        mx,my = (x1+x2)/2,(y1+y2)/2
        ax.text(mx,my+0.13, lbl, ha='center', fontsize=6.5, color=col, fontweight='semibold',
                bbox=dict(boxstyle='round,pad=0.1', facecolor=WHITE, edgecolor='none', alpha=0.85))

    def section_lbl(x, y, txt, col):
        ax.add_patch(FancyBboxPatch((x-0.3, y-0.2), len(txt)*0.13+0.6, 0.42,
                                    boxstyle="round,pad=0.07",
                                    facecolor=col, edgecolor='none'))
        ax.text(x+len(txt)*0.065, y, txt, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=WHITE)

    # ── Left side: P2 Decomposed — Document Ingestion ──
    section_lbl(6.5, 17.5, 'P2: Document Ingestion (Decomposed)', GREEN)
    ax.add_patch(FancyBboxPatch((0.2, 3.5), 12.5, 13.6,
                                boxstyle="round,pad=0.1",
                                facecolor=GREEN_L+'80', edgecolor=GREEN, linewidth=1.5))

    ext(1.5, 16.0, 2.2, 0.7, 'User\n(Browser)', INDIGO)
    ext(1.5, 5.0,  2.2, 0.7, 'Paper Record\nDB', GRAY7)
    store(6.5, 4.2, 4.5, 'D1: document_chunks', GREEN)
    store(6.5, 3.7, 4.5, 'D2: FAISS Index', PURPLE)

    proc(4.0, 15.0, 0.9, '2.1', 'PDF Text\nExtraction', '#16A34A')
    proc(7.5, 15.0, 0.9, '2.2', 'Text\nChunking', '#15803D')
    proc(10.5, 15.0, 0.9, '2.3', 'Metadata\nExtraction', '#166534')
    proc(4.0, 11.5, 0.9, '2.4', 'Embedding\nGeneration', '#0891B2')
    proc(7.5, 11.5, 0.9, '2.5', 'Redis Cache\nCheck', '#0369A1')
    proc(10.5, 11.5, 0.9, '2.6', 'FAISS\nIndexing', PURPLE)
    proc(4.0, 8.0, 0.9, '2.7', 'DB Chunk\nStorage', GRAY7)
    proc(7.5, 8.0, 0.9, '2.8', 'LLM Analysis\n(Gemini)', RED)
    proc(10.5, 8.0, 0.9, '2.9', 'Result\nPersistence', '#374151')

    fl(1.5+1.1,16.0, 4.0-0.9,15.0, 'PDF bytes', GREEN)
    fl(4.0+0.9,15.0, 7.5-0.9,15.0, 'page text[]', GREEN)
    fl(7.5+0.9,15.0, 10.5-0.9,15.0, '500w chunks', GREEN)
    fl(10.5,15.0-0.9, 10.5,11.5+0.9, 'chunk+meta', '#166534')
    fl(7.5,15.0-0.9, 4.0,11.5+0.9, 'chunk text', '#15803D')
    fl(4.0,11.5-0.9, 7.5-0.9,11.5, 'text batch', '#0891B2')
    fl(7.5,11.5-0.9, 7.5,8.0+0.9, 'cache miss → embed', BLUE)
    fl(7.5+0.9,11.5, 10.5-0.9,11.5, 'vectors[]', '#0369A1')
    fl(10.5,11.5-0.9, 10.5,8.0+0.9, 'IDs+vecs', PURPLE)
    fl(4.0+0.9,11.5, 7.5-0.9,8.0+0.2, 'embeddings', '#0891B2')
    fl(4.0,11.5-0.9, 4.0,8.0+0.9, 'text+page', GRAY7)
    fl(4.0,8.0-0.9, 6.5,4.4, 'chunk records', GRAY7)
    fl(10.5,8.0-0.9, 6.5,3.9, 'FAISS update', PURPLE)
    fl(4.0-0.9,15.3, 1.5+1.1,15.3, 'raw text', '#16A34A')
    fl(7.5,8.0-0.9, 7.5,8.0-0.9-0.5, 'full text', RED)
    fl(7.5+0.9,8.0, 10.5-0.9,8.0, 'analysis JSON', RED)
    fl(10.5,8.0-0.9, 10.5,5.3, 'result_json', '#374151')
    fl(10.5,5.0-0.15, 1.5+1.1,5.0, 'paper updated', GRAY7)

    # ── Right side: P4 Decomposed — RAG Retrieval ──
    section_lbl(19.5, 17.5, 'P4: RAG Retrieval (Decomposed)', ORANGE)
    ax.add_patch(FancyBboxPatch((13.3, 3.5), 12.5, 13.6,
                                boxstyle="round,pad=0.1",
                                facecolor=ORANGE_L+'80', edgecolor=ORANGE, linewidth=1.5))

    ext(14.5, 16.0, 2.2, 0.7, 'User\n(Query)', INDIGO)
    ext(14.5, 5.0,  2.2, 0.7, 'Chat\nHistory', '#B45309')
    ext(25.5, 10.0, 2.0, 0.7, 'Gemini\nAI', GREEN)
    store(19.5, 4.2, 4.5, 'D3: FAISS Index', PURPLE)
    store(19.5, 3.7, 4.5, 'D4: document_chunks', GRAY7)

    proc(17.0, 15.0, 0.9, '4.1', 'Query\nEmbedding', '#0891B2')
    proc(21.0, 15.0, 0.9, '4.2', 'Redis Cache\nLookup', BLUE)
    proc(24.5, 15.0, 0.9, '4.3', 'FAISS\nVector Search', PURPLE)
    proc(17.0, 11.5, 0.9, '4.4', 'Chunk Meta\nLoad from DB', GRAY7)
    proc(21.0, 11.5, 0.9, '4.5', 'Paper ID\nFiltering', PINK)
    proc(24.5, 11.5, 0.9, '4.6', 'Semantic\nScoring', ORANGE)
    proc(17.0, 8.0, 0.9, '4.7', 'BM25\nReranking', '#B45309')
    proc(21.0, 8.0, 0.9, '4.8', 'Diversity\nCap', '#0F766E')
    proc(24.5, 8.0, 0.9, '4.9', 'Gemini\nGeneration', RED)
    proc(19.5, 5.5, 0.9, '4.10', 'Answer\n+ Citations', '#374151')

    fl(14.5+1.1,16.0, 17.0-0.9,15.0, 'query text', ORANGE)
    fl(17.0+0.9,15.0, 21.0-0.9,15.0, 'text', ORANGE)
    fl(21.0,15.0-0.9, 21.0,15.0+0.9-0.1, 'hit?', BLUE)
    fl(21.0+0.9,15.0, 24.5-0.9,15.0, 'query vector', BLUE)
    fl(24.5,15.0-0.9, 24.5,11.5+0.9, 'candidate IDs', PURPLE)
    fl(24.5,15.0-0.9-0.3, 19.5,4.4, 'search FAISS', PURPLE)
    fl(24.5,11.5-0.9, 24.5,8.0+0.9, 'l2 distances', ORANGE)
    fl(24.5,11.5, 21.0+0.9,11.5, 'candidates', PINK)
    fl(17.0,15.0-0.9, 17.0,11.5+0.9, 'chunk_ids', GRAY7)
    fl(17.0,11.5-0.9, 19.5,4.4, 'fetch chunks', GRAY7)
    fl(21.0,11.5-0.9, 21.0,8.0+0.9, 'filtered', PINK)
    fl(21.0+0.9,11.5, 24.5-0.9,11.5, 'scores 0-1', ORANGE)
    fl(21.0-0.9,8.0, 17.0+0.9,8.0, 'top-k', '#0F766E')
    fl(17.0,8.0-0.9, 19.5,5.7, 'reranked', '#B45309')
    fl(21.0,8.0-0.9, 19.5,5.7, 'diverse top-k', '#0F766E')
    fl(24.5,8.0-0.9, 24.5,5.7, 'context+history', RED)
    fl(24.5+0.9-0.1,10.0, 25.5-1.0,10.0, 'prompt', GREEN)
    fl(25.5-1.0,10.2, 24.5,8.0+0.3, 'LLM answer', GREEN)
    fl(19.5,5.5-0.9, 19.5,4.4, 'persist history', '#374151')
    fl(19.5-0.9,5.5, 14.5+1.1,5.1, 'answer+cites', '#374151')
    fl(14.5,5.0+0.35, 14.5,5.0+0.35+3.0, 'chat history', '#B45309')

    ax.text(13, 17.8, 'SciSynthesis — DFD Level 2',
            ha='center', fontsize=16, fontweight='bold', color=GRAY9)
    ax.text(13, 17.45,
            'P2: Document Ingestion (left)  ·  P4: RAG Retrieval Pipeline (right)',
            ha='center', fontsize=9, color=GRAY5)
    ax.text(13, 0.15, '© 2026 SciSynthesis — Krina Pansuriya',
            ha='center', fontsize=7.5, color='#94A3B8')

    save(fig, 'Diagram_8_DFD_Level2.png')


# ══════════════════════════════════════════════════════════════════════════════
# 9. ER DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════
def make_er():
    fig, ax = plt.subplots(figsize=(24, 16))
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 16)
    ax.axis('off')

    def entity(x, y, name, attrs, w=4.5, col=INDIGO):
        row_h = 0.4
        n = len(attrs)
        total_h = 0.65 + n * row_h + 0.15

        # Header
        ax.add_patch(FancyBboxPatch((x, y), w, 0.65,
                                    boxstyle="round,pad=0",
                                    facecolor=col, edgecolor=col))
        ax.text(x+w/2, y+0.32, name, ha='center', va='center',
                fontsize=10, fontweight='bold', color=WHITE)

        # Rows
        for i, (pk, attr, dtype) in enumerate(attrs):
            row_y = y - (i+1)*row_h
            bg = '#FEF9C3' if pk == 'PK' else '#F0FDF4' if pk == 'FK' else WHITE
            ax.add_patch(FancyBboxPatch((x, row_y), w, row_h,
                                        boxstyle="square,pad=0",
                                        facecolor=bg, edgecolor=GRAY2, linewidth=0.5))
            # Badge
            if pk in ('PK','FK','UK'):
                badge_col = '#F59E0B' if pk=='PK' else '#3B82F6' if pk=='FK' else GREEN
                ax.add_patch(FancyBboxPatch((x+0.05, row_y+0.07), 0.42, 0.26,
                                            boxstyle="round,pad=0.03",
                                            facecolor=badge_col, edgecolor='none'))
                ax.text(x+0.26, row_y+0.2, pk, ha='center', va='center',
                        fontsize=5.5, fontweight='bold', color=WHITE)
            ax.text(x+0.55, row_y+0.2, attr, va='center', fontsize=7.5, color=GRAY9)
            ax.text(x+w-0.08, row_y+0.2, dtype, ha='right', va='center',
                    fontsize=6.5, color=GRAY5, style='italic')

        # Outer border
        body_h = n * row_h
        ax.add_patch(FancyBboxPatch((x, y-body_h), w, body_h+0.65,
                                    boxstyle="round,pad=0.0",
                                    facecolor='none', edgecolor=col, linewidth=2.2))

        return x, y, x+w, y-body_h  # left top, right bottom

    def rel_line(x1,y1,x2,y2, lbl, card1, card2, col=GRAY5):
        ax.plot([x1,x2],[y1,y2], color=col, lw=1.8, zorder=2)
        ax.plot(x1,y1,'o', ms=5, color=col, zorder=3)
        ax.plot(x2,y2,'o', ms=5, color=col, zorder=3)
        mx,my = (x1+x2)/2,(y1+y2)/2
        ax.text(mx,my+0.15, lbl, ha='center', fontsize=7, color=col,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.08', facecolor=WHITE,
                          edgecolor=col+'55', linewidth=0.8))
        ax.text(x1+0.2*(x2-x1), y1+0.2*(y2-y1)+0.14, card1,
                fontsize=7.5, color=col, fontweight='bold')
        ax.text(x2-0.2*(x2-x1), y2+0.14, card2,
                fontsize=7.5, color=col, fontweight='bold')

    # ── Entities ──
    entity(0.3, 14.8, 'users', [
        ('PK', 'id',              'INTEGER'),
        ('UK', 'email',           'VARCHAR'),
        ('',   'hashed_password', 'VARCHAR'),
        ('',   'full_name',       'VARCHAR?'),
        ('',   'institution',     'VARCHAR?'),
        ('',   'bio',             'VARCHAR?'),
        ('',   'phone_number',    'VARCHAR?'),
        ('',   'profile_picture', 'VARCHAR?'),
        ('',   'created_at',      'DATETIME'),
    ], 4.6, INDIGO)

    entity(8.0, 14.8, 'papers', [
        ('PK', 'id',          'INTEGER'),
        ('FK', 'user_id',     'INTEGER'),
        ('FK', 'project_id',  'INTEGER?'),
        ('',   'title',       'VARCHAR'),
        ('',   'filename',    'VARCHAR'),
        ('',   'result_json', 'JSON'),
        ('',   'created_at',  'DATETIME'),
    ], 4.6, GREEN)

    entity(15.5, 14.8, 'document_chunks', [
        ('PK', 'id',           'INTEGER'),
        ('FK', 'paper_id',     'INTEGER'),
        ('',   'text',         'TEXT'),
        ('',   'page_number',  'INTEGER?'),
        ('',   'chunk_index',  'INTEGER'),
    ], 4.6, ORANGE)

    entity(0.3, 7.2, 'projects', [
        ('PK', 'id',          'INTEGER'),
        ('FK', 'user_id',     'INTEGER'),
        ('',   'name',        'VARCHAR'),
        ('',   'description', 'VARCHAR?'),
        ('',   'created_at',  'DATETIME'),
    ], 4.6, PURPLE)

    entity(8.0, 7.2, 'notes', [
        ('PK', 'id',         'INTEGER'),
        ('FK', 'paper_id',   'INTEGER'),
        ('FK', 'user_id',    'INTEGER'),
        ('',   'content',    'VARCHAR'),
        ('',   'created_at', 'DATETIME'),
    ], 4.6, PINK)

    entity(15.5, 7.2, 'search_history', [
        ('PK', 'id',         'INTEGER'),
        ('FK', 'user_id',    'INTEGER'),
        ('',   'query',      'VARCHAR'),
        ('',   'paper_ids',  'JSON?'),
        ('',   'created_at', 'DATETIME'),
    ], 4.6, BLUE)

    entity(20.5, 10.5, 'faiss_index\n(runtime)', [
        ('',  'chunk_id',   'INT64 ID'),
        ('',  'embedding',  'FLOAT[768]'),
        ('',  'index_path', 'STRING'),
    ], 3.2, '#0891B2')

    entity(20.5, 6.5, 'redis_store\n(runtime)', [
        ('',  'emb:{hash}',     'FLOAT[] TTL7d'),
        ('',  'chat:{user_id}', 'JSON TTL24h'),
        ('',  'otp:{phone}',    'STRING TTL5m'),
    ], 3.2, RED)

    # ── Relationships ──
    # users → papers (1:N)
    rel_line(4.9, 12.8, 8.0, 12.4, 'owns', '1', 'N', GREEN)
    # users → projects (1:N)
    rel_line(2.6, 11.1, 2.6, 7.2, 'creates', '1', 'N', PURPLE)
    # users → notes (1:N)
    rel_line(3.5, 11.1, 8.0, 5.4, 'writes', '1', 'N', PINK)
    # users → search_history (1:N)
    rel_line(4.9, 13.5, 15.5, 5.7, 'logs', '1', 'N', BLUE)
    # papers → document_chunks (1:N)
    rel_line(12.6, 12.8, 15.5, 12.4, 'has', '1', 'N', ORANGE)
    # papers → notes (1:N)
    rel_line(10.3, 11.1, 10.3, 5.3, 'annotated by', '1', 'N', PINK)
    # projects → papers (1:N)
    rel_line(4.9, 5.3, 8.0, 11.2, 'groups', '1', 'N', GREEN)
    # document_chunks → faiss_index
    rel_line(20.1, 12.5, 20.5, 12.0, 'indexed in', '1', '1', '#0891B2')
    # users → redis (via chat memory)
    rel_line(4.9, 13.0, 20.5, 6.2, 'chat memory', '1', '1', RED)

    # Legend
    for i, (col, lbl) in enumerate([
        ('#F59E0B', 'PK — Primary Key'),
        ('#3B82F6', 'FK — Foreign Key'),
        (GREEN, 'UK — Unique Key'),
    ]):
        lx = 0.5 + i*5.5
        ax.add_patch(FancyBboxPatch((lx, 0.55), 0.65, 0.28,
                                    boxstyle="round,pad=0.04",
                                    facecolor=col, edgecolor='none'))
        ax.text(lx+0.32, 0.69, lbl[:2], ha='center', va='center',
                fontsize=6.5, color=WHITE, fontweight='bold')
        ax.text(lx+0.8, 0.69, lbl[5:], va='center', fontsize=8, color=GRAY7)

    ax.plot([17.5,18.1],[0.69,0.69], color=GRAY5, lw=2)
    ax.plot(17.5,0.69,'o',ms=5,color=GRAY5)
    ax.plot(18.1,0.69,'o',ms=5,color=GRAY5)
    ax.text(18.2,0.69,'Relationship line', va='center', fontsize=8, color=GRAY7)

    ax.text(12, 15.7, 'SciSynthesis — ER Diagram',
            ha='center', fontsize=17, fontweight='bold', color=GRAY9)
    ax.text(12, 15.3, 'Entity-Relationship Model · SQLAlchemy ORM · SQLite Database',
            ha='center', fontsize=9, color=GRAY5)
    ax.text(12, 0.18, '© 2026 SciSynthesis — Krina Pansuriya',
            ha='center', fontsize=7.5, color='#94A3B8')

    save(fig, 'Diagram_9_ER.png')


# ══════════════════════════════════════════════════════════════════════════════
# RUN ALL
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating all diagrams...")
    make_timeline()
    make_usecase()
    make_sequence()
    make_activity()
    make_class()
    make_dfd0()
    make_dfd1()
    make_dfd2()
    make_er()
    print("\nAll 9 diagrams generated successfully!")
    print("  1. Diagram_1_Timeline.png")
    print("  2. Diagram_2_Use_Case.png")
    print("  3. Diagram_3_Sequence.png")
    print("  4. Diagram_4_Activity.png")
    print("  5. Diagram_5_Class.png")
    print("  6. Diagram_6_DFD_Level0.png")
    print("  7. Diagram_7_DFD_Level1.png")
    print("  8. Diagram_8_DFD_Level2.png")
    print("  9. Diagram_9_ER.png")

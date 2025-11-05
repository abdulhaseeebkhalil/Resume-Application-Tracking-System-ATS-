import base64
import html
import io
import os
from collections import OrderedDict

import pdf2image
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from fpdf import FPDF

load_dotenv()

st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="🧠",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #eef2ff 0%, #f8f9ff 55%, #ffffff 100%);
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(31,64,104,0.92), rgba(22,101,183,0.85));
        color: #f8fbff;
    }
    div[data-testid="stSidebar"] .stMarkdown p {
        color: #f5f7ff;
    }
    .hero {
        background: linear-gradient(135deg, rgba(49,46,129,0.95), rgba(22,163,74,0.92));
        border-radius: 1.6rem;
        padding: 2.6rem;
        color: #ffffff;
        box-shadow: 0 30px 60px rgba(17, 20, 45, 0.28);
        border: 1px solid rgba(255,255,255,0.18);
    }
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }
    .hero p {
        font-size: 1.05rem;
        opacity: 0.88;
        max-width: 700px;
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1f2a44;
        margin-top: 2.4rem;
        margin-bottom: 1rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.94);
        border-radius: 1.4rem;
        padding: 2rem;
        box-shadow: 0 22px 45px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(226,232,240,0.8);
    }
    .upload-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        padding: 0.6rem 1rem;
        border-radius: 999px;
        background: rgba(15,118,110,0.12);
        color: #036666;
        font-weight: 600;
        margin-top: 0.8rem;
    }
    .feature-card {
        background: linear-gradient(140deg, rgba(248,250,255,0.94), rgba(241,245,255,0.9));
        border-radius: 1.2rem;
        padding: 1.25rem;
        height: 100%;
        border: 1px solid rgba(190, 208, 255, 0.7);
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.05);
    }
    .feature-card h4 {
        margin-bottom: 0.35rem;
        color: #1d2746;
        font-size: 1.05rem;
        font-weight: 700;
    }
    .feature-card p {
        color: #4a5470;
        font-size: 0.92rem;
        line-height: 1.4rem;
    }
    .generate-btn button {
        width: 100%;
        background: linear-gradient(120deg, #4338ca, #10b981);
        color: #ffffff;
        font-weight: 700;
        font-size: 1.05rem;
        border-radius: 999px;
        padding: 0.9rem 1.5rem;
        border: none;
        box-shadow: 0 18px 30px rgba(16, 185, 129, 0.25);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }
    .generate-btn button:hover {
        transform: translateY(-2px);
        box-shadow: 0 22px 40px rgba(67, 56, 202, 0.28);
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        padding: 0.6rem 1.1rem;
        border-radius: 999px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, #4338ca, #14b8a6);
        color: #ffffff;
    }
    .result-card {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 1.2rem;
        padding: 1.5rem;
        border: 1px solid rgba(229, 231, 235, 0.9);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.65), 0 20px 30px rgba(15,23,42,0.08);
        min-height: 300px;
    }
    .stTextArea textarea {
        border-radius: 1.2rem !important;
        border: 1px solid rgba(148,163,184,0.6) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
        padding: 1rem !important;
        background: rgba(248,250,252,0.82) !important;
    }
    .stFileUploader > div > div {
        border-radius: 1.2rem;
        border: 1px dashed rgba(99,102,241,0.65);
        padding: 1.4rem;
        background: rgba(240, 249, 255, 0.75);
    }
    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 1rem;
    }
    .resume-card {
        background: rgba(249, 250, 255, 0.96);
        border-radius: 1.6rem;
        padding: 2.4rem;
        box-shadow: 0 28px 55px rgba(15, 23, 42, 0.12);
        border: 1px solid rgba(191, 219, 254, 0.8);
        font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
        color: #0f172a;
        line-height: 1.65;
    }
    .resume-card .resume-header {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        margin-bottom: 1.6rem;
    }
    .resume-card .resume-header h2 {
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.01em;
    }
    .resume-card .resume-header span {
        font-size: 0.98rem;
        color: rgba(15, 23, 42, 0.7);
    }
    .resume-card .resume-section {
        margin-bottom: 1.35rem;
    }
    .resume-card .resume-section h3 {
        font-size: 1.05rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: rgba(30, 64, 175, 0.95);
        margin-bottom: 0.6rem;
    }
    .resume-card .resume-section ul {
        list-style: none;
        padding-left: 0;
    }
    .resume-card .resume-section ul li {
        position: relative;
        padding-left: 1.4rem;
        margin-bottom: 0.35rem;
    }
    .resume-card .resume-section ul li::before {
        content: "";
        position: absolute;
        left: 0.35rem;
        top: 0.55rem;
        width: 0.45rem;
        height: 0.45rem;
        border-radius: 50%;
        background: linear-gradient(120deg, #4338ca, #14b8a6);
    }
    .resume-actions {
        margin-top: 1.8rem;
        display: flex;
        gap: 1rem;
    }
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(120deg, #4338ca, #0ea5e9);
        color: #ffffff;
        font-weight: 700;
        border-radius: 999px;
        border: none;
        box-shadow: 0 16px 32px rgba(14, 165, 233, 0.25);
        padding: 0.75rem 0.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        box-shadow: 0 18px 36px rgba(67, 56, 202, 0.32);
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(prompt_template: str, pdf_content, job_description: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        prompt_template,
        pdf_content[0],
        job_description or "",
    ])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")
    uploaded_file.seek(0)
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    first_page = images[0]
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format="JPEG")
    encoded_page = base64.b64encode(img_byte_arr.getvalue()).decode()
    uploaded_file.seek(0)
    pdf_parts = [{"mime_type": "image/jpeg", "data": encoded_page}]
    return pdf_parts

def input_pdf_setup(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")
    uploaded_file.seek(0)
    try:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
    except Exception as e:
        raise ValueError("Error converting PDF to image.") from e
    
    if not images:
        raise ValueError("No pages found in the uploaded PDF.")
    
    first_page = images[0]
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format="JPEG")
    encoded_page = base64.b64encode(img_byte_arr.getvalue()).decode()
    uploaded_file.seek(0)
    pdf_parts = [{"mime_type": "image/jpeg", "data": encoded_page}]
    return pdf_parts



def _looks_like_section_title(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if stripped.endswith(":"):
        return True
    letters = [c for c in stripped if c.isalpha()]
    if letters:
        upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
        if upper_ratio > 0.65 and len(stripped) <= 48:
            return True
    if len(stripped.split()) <= 3 and stripped == stripped.title():
        return True
    return False


def _prepare_resume_layout(content: str):
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not lines:
        return "", None

    header_title = html.escape(lines[0])
    header_subtitle = ""
    start_idx = 1
    if len(lines) > 1:
        second = lines[1]
        if _looks_like_section_title(second):
            start_idx = 1
        else:
            header_subtitle = html.escape(second)
            start_idx = 2

def _wrap_extreme_tokens(text: str, limit: int = 45) -> str:
    safe_tokens = []
    for token in text.split():
        if len(token) <= limit:
            safe_tokens.append(token)
        else:
            segments = [token[i:i+limit] for i in range(0, len(token), limit)]
            safe_tokens.append(" ".join(segments))
    return " ".join(safe_tokens)


    sections = []
    current_title = None
    current_items = []

    for line in lines[start_idx:]:
        if _looks_like_section_title(line):
            if current_title or current_items:
                sections.append((current_title, current_items))
            current_title = line.rstrip(":").strip()
            current_items = []
        else:
            current_items.append(line)

    if current_title or current_items:
        sections.append((current_title, current_items))

    html_parts = ["<div class='resume-card'>", "<div class='resume-header'>", f"<h2>{header_title}</h2>"]
    if header_subtitle:
        html_parts.append(f"<span>{header_subtitle}</span>")
    html_parts.append("</div>")

    for title, items in sections:
        html_parts.append("<div class='resume-section'>")
        if title:
            html_parts.append(f"<h3>{html.escape(title)}</h3>")

        bullet_items = []
        paragraph_items = []
        for item in items:
            stripped = item.strip()
            if not stripped:
                continue
            normalized = stripped.lstrip("-•· ")
            if stripped.startswith(("-", "*", "•", "·")):
                bullet_items.append(html.escape(normalized))
            else:
                paragraph_items.append(html.escape(stripped))

        if bullet_items:
            html_parts.append("<ul>")
            for bullet in bullet_items:
                html_parts.append(f"<li>{bullet}</li>")
            html_parts.append("</ul>")

        for paragraph in paragraph_items:
            html_parts.append(f"<p>{paragraph}</p>")

        html_parts.append("</div>")

    html_parts.append("</div>")
    resume_html = "".join(html_parts)
    pdf_bytes = _build_resume_pdf(content)
    return resume_html, pdf_bytes


def _build_resume_pdf(content: str) -> bytes:
    clean_text = (
        content.replace("•", "-")
        .replace("–", "-")
        .replace("—", "-")
        .replace("·", "-")
    )
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_title("Enhanced Resume")
    pdf.set_author("ATS Resume Expert")
    pdf.set_font("Helvetica", size=11)

    def _wrap_extreme_tokens(text: str, limit: int = 45) -> str:
        safe_tokens = []
        for token in text.split():
            if len(token) <= limit:
                safe_tokens.append(token)
            else:
                segments = [token[i : i + limit] for i in range(0, len(token), limit)]
                safe_tokens.append(" ".join(segments))
        return " ".join(safe_tokens)

    for raw_line in clean_text.splitlines():
        line = raw_line.strip()
        if not line:
            pdf.ln(4)
            continue
        safe_line = _wrap_extreme_tokens(line)
        fallback = safe_line[:150] + "..." if len(safe_line) > 180 else safe_line
        try:
            pdf.multi_cell(0, 6, fallback)
        except Exception:  # pragma: no cover
            pdf.multi_cell(0, 6, "[content trimmed]")

    pdf_output = pdf.output(dest="S").encode("latin-1", "replace")
    return pdf_output


ANALYSIS_OPTIONS = OrderedDict(
    {
        "Resume Snapshot": {
            "prompt": """
                As an experienced Technical Human Resource Manager with a deep understanding of hiring trends and industry-specific demands, 
                your task is to evaluate the provided resume against the job description with a detailed, professional lens. 
                First, provide a thorough analysis of how well the applicant’s profile aligns with the role's specific requirements. 
                Include a strengths and weaknesses breakdown, assessing qualifications, work experience, and technical skills in the context of the job description.
                Ensure your evaluation includes any gaps or mismatches in areas like educational background, experience, or specialized knowledge.
            """,
            "description": "A comprehensive HR assessment with a focus on qualification alignment and improvement opportunities.",
        },
        "Skill Uplift Roadmap": {
            "prompt": """
                You are an elite Career Coach, highly skilled in personal and professional development, specializing in crafting precise career growth roadmaps. 
                Your task is to critically review the resume against the job description and identify skill and experience areas that need refinement or enhancement. 
                Recommend specific skills, certifications, and experiences the candidate should acquire to improve alignment with the job’s requirements, 
                emphasizing both hard and soft skills. Provide actionable steps that include timelines, resources, and industry-recognized certifications.
            """,
            "description": "Strategic advice for skill enhancement, focusing on actionable steps for career growth.",
        },
        "ATS Match Score": {
            "prompt": """
                As a specialist in Applicant Tracking Systems (ATS) with in-depth knowledge of AI and machine learning-based resume scanning algorithms, 
                your task is to evaluate the provided resume against the job description with a focus on ATS optimization. 
                Begin by providing an ATS match percentage, then follow up with a detailed analysis of missing keywords and skills. 
                Conclude with suggestions for optimizing the resume to increase ATS compatibility, including keyword density, phrasing, and formatting improvements.
            """,
            "description": "Comprehensive ATS evaluation with keyword optimization and scoring analysis.",
        },
        "Role Fit Scorecard": {
            "prompt": """
                You are a seasoned Career Advisor, skilled in evaluating a candidate's overall compatibility with specific job roles. 
                Your task is to assess the resume and job description, offering a detailed breakdown of alignment across various key areas such as technical skills, industry experience, 
                and soft skills. In addition to providing a thorough analysis, conclude with a numerical rating out of 10, indicating the candidate’s overall fit for the role, 
                along with any recommended next steps for improving their candidacy.
            """,
            "description": "In-depth evaluation of candidate suitability with actionable feedback and fit rating.",
        },
        "Highlight Reel": {
            "prompt": """
                As a highly experienced Resume Analyst, your job is to extract the most impactful and relevant accomplishments from the resume, 
                highlighting those that align strongly with the job description. Emphasize quantifiable achievements that demonstrate clear results, 
                using metrics and KPIs whenever possible. Ensure that the selected accomplishments not only showcase the candidate's capabilities but also align with the hiring manager’s top priorities.
            """,
            "description": "Curate and present the candidate’s most impactful achievements in the context of the role.",
        },
        "Certification Pathfinder": {
            "prompt": """
                You are an expert in career advancement through certifications. Your task is to conduct an in-depth review of the resume and the job description, 
                recommending the most relevant industry certifications that will enhance the candidate’s qualifications for the position. 
                Provide a curated list of high-value certifications, including online programs, professional development courses, and certifications from leading organizations. 
                Focus on certifications that will elevate the candidate’s standing in the specific industry and help them stand out in a competitive job market.
            """,
            "description": "Curate a path of certifications that will significantly boost the candidate's qualifications.",
        },
        "Leadership Lens": {
            "prompt": """
                You are an experienced HR Manager with expertise in leadership assessment. Your task is to evaluate the resume with a focus on identifying leadership potential. 
                Look for specific examples of leadership skills demonstrated through achievements, team management, decision-making, and strategic thinking. 
                Assess the depth of the candidate’s leadership qualities by examining both direct and indirect leadership experiences, 
                such as leading projects, mentoring teams, and driving initiatives. Provide actionable insights into how they can further develop their leadership skills.
            """,
            "description": "Examine leadership qualities with examples, insights, and areas for leadership growth.",
        },
        "Transferable Skills Radar": {
            "prompt": """
                You are a Career Transition Specialist skilled in identifying versatile skills across industries. 
                Analyze the resume in the context of the job description to uncover transferable skills—those that can be adapted across various domains or roles. 
                Highlight skills that demonstrate adaptability and potential for successful transition, focusing on soft skills, technical capabilities, and cross-functional expertise. 
                Provide an analysis of how the candidate can leverage these skills to excel in the target role.
            """,
            "description": "Identify adaptable skills that can be transferred across roles and industries.",
        },
        "Resume Glow-Up": {
            "prompt": """
                You are a highly skilled Resume Analyst with a focus on creating professional, polished resumes. 
                Your task is to rewrite the candidate’s resume to highlight their strengths and achievements effectively in line with the job description. 
                Ensure the resume is well-structured, professionally formatted, and easy to read. 
                Use a tone that reflects the industry standards and aligns with the job role, and provide suggestions for optimizing the resume to maximize appeal to hiring managers.
            """,
            "description": "Craft a professional resume that showcases the candidate’s qualifications in the most compelling way.",
        },
        "Tailored Cover Letter": {
            "prompt": """
                As an expert in crafting personalized cover letters, your task is to write a cover letter tailored to the specific job description. 
                The letter should convey the candidate’s interest in the role, highlight their most relevant skills and achievements, and demonstrate their fit for the company culture. 
                Ensure that the tone of the letter aligns with the job description and reflects a professional yet engaging approach.
            """,
            "description": "Create a custom cover letter that aligns perfectly with the job description and the candidate’s profile.",
        },
    }
)

if "responses" not in st.session_state:
    st.session_state["responses"] = {}
if "last_selected" not in st.session_state:
    st.session_state["last_selected"] = []

with st.sidebar:
    st.title("Navigator")
    st.markdown(
        """
        **How to use**
        1. Drop in the target job description.
        2. Upload the candidate resume (PDF).
        3. Pick the insights you need and run the analysis.

        **Tips**
        - Combine multiple insights for a richer report.
        - Start with *Resume Snapshot* for a quick baseline.
        - Re-run after tweaking the resume to track progress.
        """
    )
    st.divider()
    st.markdown("**Need inspiration?** Try pairing `ATS Match Score` with `Highlight Reel` for a recruiter-ready summary.")

with st.container():
    st.markdown(
        """
        <div class="hero">
            <h1>ATS Resume Expert</h1>
            <p>Elevate your resume for every application. Mix and match expert analyses, ATS checks, and tailored content to build a standout candidate story in minutes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class=\"section-title\">1. Describe the opportunity</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    details_col, upload_col = st.columns((2.1, 1), gap="large")
    with details_col:
        job_description = st.text_area(
            "Job Description",
            placeholder="Paste the role summary, key responsibilities, and must-have skills here...",
            height=240,
            key="job_description_input",
        )
    with upload_col:
        uploaded_file = st.file_uploader(
            "Upload resume (PDF)",
            type=["pdf"],
            help="For best results, use a recent ATS-friendly resume export.",
        )
        if uploaded_file is not None:
            file_size_kb = uploaded_file.size / 1024
            st.markdown(
                f"<span class='upload-chip'>📄 {uploaded_file.name} · {file_size_kb:.1f} KB</span>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class=\"section-title\">2. Choose your insights</div>", unsafe_allow_html=True)

analysis_items = list(ANALYSIS_OPTIONS.items())
for row_start in range(0, len(analysis_items), 3):
    row_slice = analysis_items[row_start : row_start + 3]
    row_columns = st.columns(len(row_slice), gap="large")
    for column, (label, meta) in zip(row_columns, row_slice):
        with column:
            st.markdown(
                f"""
                <div class='feature-card'>
                    <h4>{label}</h4>
                    <p>{meta['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

selected_labels = st.multiselect(
    "Select one or more insights to generate",
    options=list(ANALYSIS_OPTIONS.keys()),
    default=st.session_state.get("last_selected", [])[:2],
)

run_analyses = st.container()
with run_analyses:
    st.markdown("<div class='section-title'>3. Generate tailored outputs</div>", unsafe_allow_html=True)
    st.markdown("<div class='generate-btn'>", unsafe_allow_html=True)
    generate_button = st.button(
        "Run Selected Insights",
        type="primary",
        use_container_width=True,
        key="run_insights",
        help="We will call Gemini to analyse the resume against your job description.",
    )
    st.markdown("</div>", unsafe_allow_html=True)

if generate_button:
    if not job_description or not job_description.strip():
        st.warning("Please provide a job description so we can contextualize the resume.")
    elif uploaded_file is None:
        st.warning("Please upload a resume PDF before running the analysis.")
    elif not selected_labels:
        st.warning("Select at least one insight to generate.")
    else:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            st.session_state["responses"] = {}
            for label in selected_labels:
                prompt_template = ANALYSIS_OPTIONS[label]["prompt"]
                with st.spinner(f"Generating {label}..."):
                    result = get_gemini_response(prompt_template, pdf_content, job_description)
                st.session_state["responses"][label] = result
            st.session_state["last_selected"] = selected_labels
            st.toast("Insights ready ✨")
        except Exception as exc:  # pragma: no cover
            st.error(f"Something went wrong while processing the resume: {exc}")

if st.session_state.get("responses"):
    tabs = st.tabs(list(st.session_state["responses"].keys()))
    for tab, label in zip(tabs, st.session_state["responses"].keys()):
        with tab:
            response_text = st.session_state["responses"][label]
            if label == "Resume Glow-Up":
                resume_html, resume_pdf = _prepare_resume_layout(response_text)
                if resume_html:
                    st.markdown(resume_html, unsafe_allow_html=True)
                else:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.markdown(response_text)
                    st.markdown("</div>", unsafe_allow_html=True)
                if resume_pdf:
                    st.download_button(
                        "Download enhanced resume as PDF",
                        data=resume_pdf,
                        file_name="enhanced_resume.pdf",
                        mime="application/pdf",
                        key="download_resume_pdf",
                        use_container_width=True,
                    )
            else:
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(response_text)
                st.markdown("</div>", unsafe_allow_html=True)

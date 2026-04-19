import streamlit as st
import os
import re
from parser import extract_text_from_pdf
from model import ResumeAnalyzer
from dotenv import load_dotenv
from fpdf import FPDF
import io

# Load environment variables
load_dotenv()

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Modern Glassmorphism for cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.2);
            text-align: center;
            backdrop-filter: blur(10px);
            margin-bottom: 1rem;
        }

        .stButton>button {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white !important;
            border-radius: 8px;
            padding: 0.6rem 2rem;
            font-weight: 700;
            border: none;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        }
        
        .star-rating {
            font-size: 2.5rem;
            color: #fbbf24;
            margin: 0.5rem 0;
            text-align: center;
        }

        .metric-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
            opacity: 0.8;
        }
        
        /* Ensure specific elements aren't lost in dark mode */
        h1, h2, h3, p, span {
            color: inherit;
        }
        </style>
    """, unsafe_allow_html=True)

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "SmartResume AI Analysis Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Sanitize Unicode characters
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\u2022": "*",
        "\u2026": "..."
    }
    
    clean_text = text
    for original, replacement in replacements.items():
        clean_text = clean_text.replace(original, replacement)
        
    clean_text = clean_text.replace("**", "").replace("#", "").replace("- ", "• ")
    clean_text = clean_text.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, clean_text)
    
    # Return as bytes (convert from bytearray)
    return bytes(pdf.output())

def render_stars(score):
    try:
        score = int(score)
    except:
        score = 0
    stars = "⭐" * score + "☆" * (5 - score)
    st.markdown(f'<div class="star-rating">{stars}</div>', unsafe_allow_html=True)

def parse_star_rating(report_text):
    """
    Extracts the star rating from the AI report.
    Looks for patterns like 'Star Rating: 4/5', '4/5 Stars', or just '4/5'.
    """
    # 1. Try to find the specific "Star Rating: X/5" format first
    match = re.search(r"Star Rating:\s*(\d)", report_text, re.IGNORECASE)
    if match:
        return match.group(1)
        
    # 2. Fallback: find any digit followed by /5
    match = re.search(r"(\d)/5", report_text)
    if match:
        return match.group(1)
        
    return "0"

def main():
    st.set_page_config(page_title="SmartResume AI", page_icon="🎯", layout="wide")
    apply_custom_css()

    st.title("🎯 SmartResume AI Report Tool")
    st.markdown("""
    <p style="font-size: 1.1rem; color: #475569; margin-bottom: 2rem;">
    Optimize your job application with state-of-the-art AI analysis.
    </p>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135673.png", width=80)
        st.header("SmartResume AI")
        st.info("Currently using **Google Gemini Pro** for high-precision analysis.")
        st.divider()
        st.caption("v2.1 Pro Edition")

    # Inputs Section
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("📁 Upload Resume")
        uploaded_file = st.file_uploader("Drop your PDF or TXT resume here", type=["pdf", "txt"], label_visibility="collapsed")
        
    with col2:
        st.subheader("📝 Job Description")
        jd_text = st.text_area("Paste the target job details", height=150, placeholder="Required skills, responsibilities...", label_visibility="collapsed")

    if st.button("🚀 EXECUTE AI ANALYSIS"):
        if uploaded_file is not None and jd_text:
            with st.spinner("🧠 AI is analyzing your profile..."):
                try:
                    resume_text = extract_text_from_pdf(uploaded_file)
                    
                    if resume_text:
                        analyzer = ResumeAnalyzer(provider="gemini")
                        report = analyzer.analyze(resume_text, jd_text)
                        
                        score = parse_star_rating(report)
                        
                        st.divider()
                        
                        # Results Section
                        res_col1, res_col2 = st.columns([1, 2], gap="large")
                        
                        with res_col1:
                            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                            st.markdown('<span class="metric-title">ATS MATCH SCORE</span>', unsafe_allow_html=True)
                            render_stars(score)
                            st.markdown(f"**Score: {score}/5 Stars**")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with res_col2:
                            st.subheader("📊 Detailed Report")
                            st.markdown(report)
                            
                            # PDF Generation
                            pdf_bytes = create_pdf(report)
                            st.download_button(
                                label="📥 Download Analysis (PDF)",
                                data=pdf_bytes,
                                file_name="SmartResume_Analysis.pdf",
                                mime="application/pdf"
                            )
                    else:
                        st.error("Text extraction failed. Please check the file format.")
                except Exception as e:
                    st.error(f"Analysis Error: {e}")
        else:
            st.warning("Please provide both a Resume and a Job Description.")

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #94a3b8;'>SmartResume AI v2.1 | Premium Analysis Suite</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

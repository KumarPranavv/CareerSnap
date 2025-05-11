import streamlit as st
from utils.parsers import extract_text_from_pdf, extract_text_from_docx
from utils.ai import (
    analyze_resume,
    get_ats_score,
    get_skill_gap,
    generate_resume_templates,
    analyze_linkedin_profile,
    get_career_projection,   # new
)

st.set_page_config(page_title="CareerSnap Pro", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .block-container {
        max-width: 800px;
        margin: auto;
        padding: 2rem 1rem;
        background-color: #121212;
        color: #e0e0e0;
    }
    h1, h2, h3, h4 {
        color: #0f508a  !important;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: #fff;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
    }
    .report-box {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

def render_in_card(md: str):
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.markdown(md)
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.title("🚀 CareerSnap Pro")
    st.write("Upload your resume/LinkedIn PDF or paste text, specify your target role, and click **Analyze**.")

    # Document type selector
    doc_type = st.radio("I’m uploading a:", ["Resume (PDF/DOCX)", "LinkedIn Profile PDF"])

    uploaded = st.file_uploader("📄 Select file", type=["pdf", "docx"])
    role     = st.text_input("🎯 Target Job Title", "Software Engineer")
    text     = ""

    if uploaded:
        if uploaded.type == "application/pdf":
            text = extract_text_from_pdf(uploaded)
        else:
            text = extract_text_from_docx(uploaded)

    text = st.text_area("✍️ Or paste your text here", text, height=200)

    if st.button("🔍 Analyze"):
        if not text.strip():
            st.error("Please upload or paste your text.")
            return

        with st.spinner("Crunching insights…"):
            if doc_type == "Resume (PDF/DOCX)":
                overview_md       = analyze_resume(text)
                ats_md            = get_ats_score(text)
                skill_gap_md      = get_skill_gap(text, role)
                templates         = generate_resume_templates(text, role)
                projection_md     = get_career_projection(text, role)
            else:
                overview_md       = analyze_linkedin_profile(text)
                skill_gap_md      = get_skill_gap(text, role)
                ats_md            = None
                templates         = {}
                projection_md     = get_career_projection(text, role)

        # Build tabs
        if doc_type.startswith("Resume"):
            tabs = st.tabs([
                "📊 Overview",
                "🎯 ATS Score",
                "🔍 Skill Gap",
                "📄 Templates",
                "🕒 Projection"
            ])
        else:
            tabs = st.tabs([
                "🔗 LinkedIn Tips",
                "🔍 Skill Gap",
                "🕒 Projection"
            ])

        # Tab 0: Overview or LinkedIn
        with tabs[0]:
            header = "Profile Overview & Suggestions" if doc_type.startswith("Resume") else "LinkedIn Optimization"
            st.header(header)
            render_in_card(overview_md)

        # Tab 1 (Resume) or Tab 1 (LinkedIn)
        if doc_type.startswith("Resume"):
            with tabs[1]:
                st.header("ATS Compatibility")
                render_in_card(ats_md)
            with tabs[2]:
                st.header(f"Skill Gap Analysis for: {role}")
                with st.expander("📈 View detailed recommendations", expanded=True):
                    render_in_card(skill_gap_md)
            with tabs[3]:
                st.header("ATS-Friendly Resume Templates")
                for name, md in templates.items():
                    st.subheader(name)
                    render_in_card(md)
                    st.download_button(f"Download {name}", md, file_name=f"{name.replace(' ', '_')}.md")
            with tabs[4]:
                st.header("🕒 Temporal Career Projection")
                render_in_card(projection_md)
        else:
            with tabs[1]:
                st.header(f"Skill Gap Analysis for: {role}")
                render_in_card(skill_gap_md)
            with tabs[2]:
                st.header("🕒 Temporal Career Projection")
                render_in_card(projection_md)

if __name__ == "__main__":
    main()
    # === Footer ===
    st.markdown("---")
    st.write("**Connect with Me**:")
    st.markdown(
        "[Connect on LinkedIn](https://www.linkedin.com/in/kumar-pranavv/)",
        unsafe_allow_html=True
    )
    st.markdown(
        "[Follow me on GitHub](https://github.com/KumarPranavv)",
        unsafe_allow_html=True
    )
    st.info(
        "For further suggestions or collaboration, "
        "feel free to reach out at kumar2pranav@gmail.com."
    )
    st.markdown("---")
    st.write("© 2025 | Pranav Kumar. All Rights Reserved.")
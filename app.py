import streamlit as st
from crew import build_crew
from pdf_export import convert_md_to_pdf

st.set_page_config(page_title="AI Research Report Generator", page_icon="📊")

st.title("📊 Multi-Agent AI Research Report Generator")
st.caption("Planner → Researcher → Analyst → Writer → Editor")

topic = st.text_input("Enter a research topic", placeholder="e.g. Impact of AI on jobs")

if st.button("Generate Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Running multi-agent pipeline... this takes 1-3 minutes"):
            crew = build_crew(topic)
            result = crew.kickoff()
            report_text = str(result)

            pdf_path = "outputs/report.pdf"
            import os
            os.makedirs("outputs", exist_ok=True)
            convert_md_to_pdf(report_text, pdf_path)

        st.markdown("---")
        st.markdown(report_text)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download Report (PDF)",
                data=f,
                file_name=f"{topic.replace(' ', '_')[:40]}.pdf",
                mime="application/pdf",
            )
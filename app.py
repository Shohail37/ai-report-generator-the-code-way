import streamlit as st
from crew import build_crew
from pdf_export import convert_md_to_pdf
import os

st.set_page_config(
    page_title="AI Research Report Generator",
    page_icon="📊",
    layout="centered",
)

st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        max-width: 780px;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        color: #888;
        font-size: 1.05rem;
        margin-bottom: 1.8rem;
    }
    .agent-pipeline {
        display: flex;
        justify-content: space-between;
        margin: 1.5rem 0 2rem 0;
        flex-wrap: wrap;
        gap: 8px;
    }
    .agent-step {
        flex: 1;
        min-width: 100px;
        text-align: center;
        padding: 10px 6px;
        border-radius: 10px;
        background: #f0f2f6;
        font-size: 0.82rem;
        font-weight: 600;
        color: #666;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    .agent-step.active {
        background: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    .agent-step.done {
        background: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
   div.stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.05rem;
        padding: 0.75rem 0.5rem;
        background-color: #4b6cb7;
        color: white !important;
        border: none;
        box-shadow: 0 2px 8px rgba(75, 108, 183, 0.35);
        transition: all 0.2s ease;
        letter-spacing: 0.3px;
    }
    div.stButton > button:hover {
        background-color: #3a5599;
        color: white !important;
        border: none;
        box-shadow: 0 4px 14px rgba(75, 108, 183, 0.5);
        transform: translateY(-2px);
    }
    div.stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 6px rgba(75, 108, 183, 0.4);
    }
    div.stButton > button:focus:not(:active) {
        border: none;
        box-shadow: 0 0 0 3px rgba(75, 108, 183, 0.3);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title">📊 AI Research Report Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Five AI agents research your topic and write a full report</div>', unsafe_allow_html=True)

steps = ["🧭 Planner", "🔍 Researcher", "🧩 Analyst", "✍️ Writer", "🧐 Editor"]
pipeline_placeholder = st.empty()

def render_pipeline(active_index=-1):
    html = '<div class="agent-pipeline">'
    for i, step in enumerate(steps):
        css_class = "agent-step"
        if i < active_index:
            css_class += " done"
        elif i == active_index:
            css_class += " active"
        html += f'<div class="{css_class}">{step}</div>'
    html += '</div>'
    pipeline_placeholder.markdown(html, unsafe_allow_html=True)

render_pipeline()

topic = st.text_input("Research topic", placeholder="e.g. Benefits of remote work", label_visibility="collapsed")

generate = st.button("✨ Generate Report", type="primary")

if generate:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        status_text = st.empty()
        for i in range(len(steps)):
            render_pipeline(i)
            status_text.caption(f"Running: {steps[i]}...")

        with st.spinner("Finishing up..."):
            crew = build_crew(topic)
            result = crew.kickoff()
            report_text = str(result)

            os.makedirs("outputs", exist_ok=True)
            pdf_path = "outputs/report.pdf"
            convert_md_to_pdf(report_text, pdf_path)

        render_pipeline(len(steps))
        status_text.caption("✅ Done!")

        st.divider()
        st.markdown(report_text)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download Report (PDF)",
                data=f,
                file_name=f"{topic.replace(' ', '_')[:40]}.pdf",
                mime="application/pdf",
            )
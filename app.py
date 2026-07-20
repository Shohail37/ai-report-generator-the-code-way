import streamlit as st
from crew import build_crew
from pdf_export import convert_md_to_pdf
import os
import time

st.set_page_config(
    page_title="AI Research Report Generator",
    page_icon="📊",
    layout="centered",
)

# ----------------------------------------------------------------------------
# GLOBAL STYLES
# ----------------------------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root {
    --accent-1: #6366f1;
    --accent-2: #8b5cf6;
    --ink: #1e1b2e;
    --muted: #7c7a8c;
    --card-bg: #ffffff;
    --card-border: #eceaf5;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

.main .block-container {
    padding-top: 2.5rem;
    max-width: 800px;
}

/* Hide default streamlit chrome for a cleaner look */
#MainMenu, footer, header {visibility: hidden;}

/* ---------- Hero ---------- */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-wrap {
    animation: fadeSlideIn 0.7s ease-out;
    margin-bottom: 0.5rem;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--accent-1);
    background: linear-gradient(90deg, rgba(99,102,241,0.12), rgba(236,72,153,0.12));
    padding: 5px 12px;
    border-radius: 999px;
    margin-bottom: 14px;
}

@keyframes underlineSweep {
    from { background-size: 0% 2px; }
    to   { background-size: 100% 2px; }
}

.hero-title {
    font-family: 'Manrope', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.04em;
    margin-bottom: 0.5rem;

    background: linear-gradient(
        135deg,
        #ffffff 0%,
        #dbe4ff 35%,
        #a5b4fc 70%,
        #818cf8 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;

    display: inline-block;

    text-shadow:
        0 0 20px rgba(99,102,241,0.25);

    animation: fadeSlideIn 0.8s ease-out;
}

.hero-sub {
    font-family: 'Inter', sans-serif;
    color: var(--muted);
    font-size: 1.08rem;
    margin-bottom: 2.2rem;
}

/* ---------- Agent pipeline ---------- */
.agent-pipeline {
    display: flex;
    justify-content: space-between;
    margin: 0 0 2rem 0;
    flex-wrap: wrap;
    gap: 10px;
    animation: fadeSlideIn 0.8s ease-out 0.1s backwards;
}

.agent-step {
    flex: 1;
    min-width: 100px;
    text-align: center;
    padding: 14px 8px;
    border-radius: 14px;
    background: var(--card-bg);
    font-family: 'Inter', sans-serif;
    font-size: 0.83rem;
    font-weight: 600;
    color: var(--muted);
    border: 1.5px solid var(--card-border);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.agent-step .emoji {
    display: block;
    font-size: 1.3rem;
    margin-bottom: 4px;
    transition: transform 0.35s ease;
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.35); }
    50%      { box-shadow: 0 0 0 8px rgba(255, 193, 7, 0); }
}

.agent-step.active {
    background: linear-gradient(135deg, #fff8e1, #fff3cd);
    border-color: #ffc107;
    color: #8a6d00;
    transform: translateY(-3px) scale(1.03);
    animation: pulseGlow 1.6s ease-out infinite;
}

.agent-step.active .emoji {
    transform: scale(1.2);
}

.agent-step.done {
    background: linear-gradient(135deg, #e9fbf0, #d4f7e0);
    border-color: #28a745;
    color: #17663a;
}

/* ---------- Input & button ---------- */
div[data-testid="stTextInput"] > div {
    background: transparent !important;
    border: none !important;
}

div[data-testid="stTextInput"] input {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    padding: 14px 18px;
    border-radius: 14px;
    border: 1.5px solid rgba(255, 255, 255, 0.35);
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(14px) saturate(160%);
    -webkit-backdrop-filter: blur(14px) saturate(160%);
    box-shadow: 0 4px 24px rgba(30, 27, 46, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.25);
    color: var(--ink);
    transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(124, 122, 140, 0.75);
}

div[data-testid="stTextInput"] input:focus {
    border-color: rgba(99, 102, 241, 0.55);
    background: rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 28px rgba(99, 102, 241, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.35);
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    padding: 0.85rem 0.5rem;
    margin-top: 0.6rem;
    color: white !important;
    border: none;
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    background-size: 200% 200%;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    letter-spacing: 0.2px;
}

div.stButton > button:hover {
    background-position: 100% 0;
    box-shadow: 0 6px 22px rgba(139, 92, 246, 0.45);
    transform: translateY(-2px);
}

div.stButton > button:active {
    transform: translateY(0px) scale(0.99);
}

/* ---------- Status caption ---------- */
.status-caption {
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    color: var(--accent-1);
    font-weight: 600;
    text-align: center;
    margin-top: -6px;
}

/* ---------- Report card ---------- */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.report-anchor) {
    animation: fadeSlideIn 0.6s ease-out;
    background: var(--card-bg);
    border-radius: 18px !important;
    border-color: var(--card-border) !important;
    padding: 0.4rem 0.6rem;
    box-shadow: 0 8px 30px rgba(30, 27, 46, 0.06);
}

.report-anchor ~ div h1, .report-anchor ~ div h2, .report-anchor ~ div h3 {
    font-family: 'Manrope', sans-serif;
    color: var(--ink);
}

.done-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    color: #17663a;
    background: #e9fbf0;
    padding: 5px 12px;
    border-radius: 999px;
    margin-bottom: 1rem;
    animation: fadeSlideIn 0.5s ease-out;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">⚡ Multi-Agent Pipeline</div>
    <div class="hero-title">AI Research Report Generator</div>
    <div class="hero-sub">Five specialized agents research your topic, analyze the findings, and write a polished report — end to end.</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# PIPELINE
# ----------------------------------------------------------------------------
steps = [
    ("🧭", "Planner"),
    ("🔍", "Researcher"),
    ("🧩", "Analyst"),
    ("✍️", "Writer"),
    ("🧐", "Editor"),
]
pipeline_placeholder = st.empty()

def render_pipeline(active_index=-1):
    html = '<div class="agent-pipeline">'
    for i, (emoji, label) in enumerate(steps):
        css_class = "agent-step"
        if i < active_index:
            css_class += " done"
        elif i == active_index:
            css_class += " active"
        html += f'<div class="{css_class}"><span class="emoji">{emoji}</span>{label}</div>'
    html += '</div>'
    pipeline_placeholder.markdown(html, unsafe_allow_html=True)

render_pipeline()

# ----------------------------------------------------------------------------
# ROTATING EXAMPLE HINT (typewriter animation)
# ----------------------------------------------------------------------------
import streamlit.components.v1 as components

EXAMPLE_TOPICS = [
    "Impact of AI on the job market",
    "Benefits of remote work",
    "Future of renewable energy",
    "How electric vehicles affect the economy",
]

components.html(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
  body {{ margin: 0; font-family: 'Inter', sans-serif; }}
  #hint {{
    font-size: 0.88rem;
    font-weight: 500;
    color: #7c7a8c;
    height: 20px;
    white-space: nowrap;
    overflow: hidden;
  }}
  #hint .prefix {{ color: #6366f1; font-weight: 600; }}
  #cursor {{
    display: inline-block;
    width: 1px;
    background: #6366f1;
    animation: blink 0.9s step-end infinite;
  }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<div id="hint"><span class="prefix">Try:&nbsp;</span><span id="text"></span><span id="cursor">&nbsp;</span></div>
<script>
  const topics = {EXAMPLE_TOPICS};
  let topicIdx = 0, charIdx = 0, deleting = false;
  const el = document.getElementById("text");
  function tick() {{
    const full = topics[topicIdx];
    if (!deleting) {{
      charIdx++;
      el.textContent = full.slice(0, charIdx);
      if (charIdx === full.length) {{ deleting = true; setTimeout(tick, 1400); return; }}
    }} else {{
      charIdx--;
      el.textContent = full.slice(0, charIdx);
      if (charIdx === 0) {{ deleting = false; topicIdx = (topicIdx + 1) % topics.length; }}
    }}
    setTimeout(tick, deleting ? 28 : 45);
  }}
  tick();
</script>
""", height=26)

topic = st.text_input(
    "Research topic",
    placeholder="e.g. Benefits of remote work",
    label_visibility="collapsed",
    key="topic_value",
)

generate = st.button("✨  Generate Report", type="primary")

# ----------------------------------------------------------------------------
# EXECUTION
# ----------------------------------------------------------------------------
if generate:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        status_text = st.empty()

        for i in range(len(steps)):
            render_pipeline(i)
            status_text.markdown(
                f'<div class="status-caption">Running: {steps[i][0]} {steps[i][1]}...</div>',
                unsafe_allow_html=True,
            )
            time.sleep(0.15)  # brief beat so the active-step animation is visible

        with st.spinner("Finishing up..."):
            crew = build_crew(topic)
            result = crew.kickoff()
            report_text = str(result)

            os.makedirs("outputs", exist_ok=True)
            pdf_path = "outputs/report.pdf"
            convert_md_to_pdf(report_text, pdf_path)

        render_pipeline(len(steps))
        status_text.empty()

        st.markdown('<div class="done-badge">✅ Report ready</div>', unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<span class="report-anchor"></span>', unsafe_allow_html=True)
            st.markdown(report_text)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️  Download Report (PDF)",
                data=f,
                file_name=f"{topic.replace(' ', '_')[:40]}.pdf",
                mime="application/pdf",
            )
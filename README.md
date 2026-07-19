# AI Research → Report Generator (Multi-Agent System)

A multi-agent AI pipeline that researches a topic on the web and produces a structured report — built with CrewAI, Groq (Llama 3.1), and Streamlit.

## How it works

Five specialized agents run in sequence, each passing its output to the next:

| Agent | Role |
|---|---|
| **Planner** | Breaks the topic into 3 focused research sub-questions |
| **Researcher** | Searches the web (via Serper) to answer each sub-question |
| **Analyst** | Organizes raw findings into clean, de-duplicated themes |
| **Writer** | Drafts a full Markdown report from the structured insights |
| **Editor** | Reviews and polishes the draft, checking for unsupported claims |

## Tech stack

- **Python** + **CrewAI** — multi-agent orchestration
- **Groq (Llama 3.1)** — LLM used by every agent
- **Serper API** — web search tool for the Researcher agent
- **Streamlit** — web interface
- **xhtml2pdf** — converts the final report to a downloadable PDF

## Setup

```bash
git clone https://github.com/Shohail37/ai-report-generator-the-code-way.git
cd ai-report-generator-the-code-way
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your free API keys:
- Groq: https://console.groq.com
- Serper: https://serper.dev

## Run it

```bash
streamlit run app.py
```

## Project structure

├── config.py       # LLM setup (Groq via CrewAI's LLM class)
├── crew.py         # Agent definitions and task pipeline
├── app.py          # Streamlit web UI
├── main.py         # CLI entry point
├── pdf_export.py   # Markdown → PDF conversion
└── requirements.txt

## Possible extensions

- Critic feedback loop (Editor sends work back to Researcher on major gaps)
- Vector DB (RAG) support for researching uploaded documents, not just the web
- Hierarchical process with a manager agent dynamically delegating tasks

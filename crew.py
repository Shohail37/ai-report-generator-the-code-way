from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from config import get_llm

llm = get_llm()
search_tool = SerperDevTool()

def build_crew(topic: str) -> Crew:

    planner = Agent(
        role="Research Planner",
        goal=f"Break down the topic '{topic}' into 3 focused research sub-questions",
        backstory="You are a senior research strategist who spots the key angles a topic needs.",
        llm=llm,
        verbose=True,
        max_iter=5,
    )

    researcher = Agent(
        role="Web Researcher",
        goal="Find accurate, up-to-date facts and credible sources for each sub-question",
        backstory="You are a meticulous researcher who always notes where each fact came from.",
        llm=llm,
        tools=[search_tool],
        verbose=True,
        max_iter=5,
    )

    analyst = Agent(
        role="Research Analyst",
        goal="Synthesize raw research into clean, well-organized insights",
        backstory="You are excellent at spotting patterns and removing redundancy from research notes.",
        llm=llm,
        verbose=True,
        max_iter=5,
    )

    writer = Agent(
        role="Report Writer",
        goal="Write a clear, well-structured report from the analyst's insights",
        backstory="You are a professional technical writer.",
        llm=llm,
        verbose=True,
        max_iter=5,
    )

    editor = Agent(
        role="Editor",
        goal="Review the draft for gaps or unsupported claims and polish it",
        backstory="You are a sharp editor who never lets a weak claim through.",
        llm=llm,
        verbose=True,
        max_iter=5,
    )

    plan_task = Task(
        description=f"Break '{topic}' into exactly 3 specific research sub-questions.",
        expected_output="A numbered list of 3 sub-questions.",
        agent=planner,
    )

    research_task = Task(
        description="For each sub-question, search the web ONCE and collect key facts with sources. Do not repeat searches.",
        expected_output="Research notes grouped by sub-question, with sources.",
        agent=researcher,
        context=[plan_task],
    )

    analysis_task = Task(
        description="Organize the research notes into clear themes, removing duplicates.",
        expected_output="Structured themes with supporting facts and sources.",
        agent=analyst,
        context=[research_task],
    )

    writing_task = Task(
        description=f"Write a full report on '{topic}': Title, Executive Summary, 3 sections, Conclusion.",
        expected_output="A complete report in Markdown.",
        agent=writer,
        context=[analysis_task],
    )

    edit_task = Task(
        description="Review and polish the draft report. Fix unsupported claims.",
        expected_output="The final, polished Markdown report.",
        agent=editor,
        context=[writing_task],
    )

    return Crew(
        agents=[planner, researcher, analyst, writer, editor],
        tasks=[plan_task, research_task, analysis_task, writing_task, edit_task],
        process=Process.sequential,
        verbose=True,
    )
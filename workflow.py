from langgraph.graph import StateGraph, START, END
from state import State
from agents.planner_agent import PlannerAgent
from agents.summary_agent import SummaryAgent
from agents.report_agent import ReportAgent
from config import setup_logging
from langchain_core.runnables.config import RunnableConfig

def save_report_to_md(state: dict) -> dict:
    import logging
    logger = logging.getLogger("AgenticAIPipeline")
    filename = "agentic_ai_report_2.md"
    lines = [
        f"# Доклад по теме: {state['topic']}\n",
        state["final_summary"],
        "\n## Summary по подпунктам:\n"
    ]
    for item in state["subtopic_summaries"]:
        lines.append(f"### {item['subtopic']}\n{item['summary']}\n")
    lines.append("\n## Оглавление подпунктов:\n")
    for item in state["subtopic_summaries"]:
        lines.append(f"- {item['subtopic']}")
    content = "\n".join(lines)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Репорт сохранён в {filename}")
    return state

def run_pipeline(initial_state):
    setup_logging()
    graph = StateGraph(State)
    planner = PlannerAgent()
    summarizer = SummaryAgent()
    reporter = ReportAgent()

    graph.add_node("plan_subtopics", planner.run)
    graph.add_node("process_subtopics", summarizer.run)
    graph.add_node("summarize_report", reporter.run)
    graph.add_node("save_report", save_report_to_md)

    graph.add_edge(START, "plan_subtopics")
    graph.add_edge("plan_subtopics", "process_subtopics")
    graph.add_edge("process_subtopics", "summarize_report")
    graph.add_edge("summarize_report", "save_report")
    graph.add_edge("save_report", END)

    graph.set_entry_point("plan_subtopics")
    graph.set_finish_point("save_report")

    compiled = graph.compile()

    config = RunnableConfig(recursion_limit=10)
    compiled.invoke(initial_state, config)
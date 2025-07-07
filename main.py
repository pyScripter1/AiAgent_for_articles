from workflow import run_pipeline

if __name__ == "__main__":
    initial_state = {
        "found_articles": [],
        "articles": [],
        "article_summaries": [],
        "subtopic_summaries": [],
        "final_summary": "",
        "topic": "Статьи на тему Agentic AI",
        "subtopics": []
    }
    run_pipeline(initial_state)



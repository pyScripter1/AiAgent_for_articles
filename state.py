from typing import TypedDict, List, Dict

class SubtopicSummary(TypedDict):
    subtopic: str
    summary: str

class State(TypedDict):
    found_articles: List[Dict]
    articles: List[Dict]
    article_summaries: List[Dict]
    subtopic_summaries: List[SubtopicSummary]
    final_summary: str
    topic: str
    subtopics: List[str]
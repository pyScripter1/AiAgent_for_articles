import logging
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from utils.article_parser import parse_article
from utils.text_cleaner import remove_think_blocks
from .review_agent import ReviewAgent

logger = logging.getLogger("AgenticAIPipeline")

class SummaryAgent:
    def __init__(self):
        self.llm = OllamaLLM(
            model="qwen3:1.7b",
            system="Ты — эксперт по искусственному интеллекту. Отвечай всегда только на русском языке, даже если вопрос или информация на другом языке."
        )
        self.search_tool = DuckDuckGoSearchAPIWrapper()
        self.reviewer = ReviewAgent()

    def run(self, state: dict) -> dict:
        subtopic_summaries = []
        for subtopic in state["subtopics"]:
            logger.info(f"Обработка подпункта: '{subtopic}'")
            n_articles = 5
            max_attempts = 2
            for attempt in range(max_attempts):
                try:
                    search_results = self.search_tool.results(f"{state['topic']} {subtopic}", n_articles)
                except Exception as e:
                    logger.error(f"Ошибка поиска для подпункта '{subtopic}': {e}")
                    break
                articles = []
                for art in search_results:
                    text = parse_article(art["link"], art["title"])
                    if text:
                        articles.append({"url": art["link"], "title": art["title"], "text": text})
                if not articles:
                    logger.warning(f"Не удалось найти статьи для подпункта '{subtopic}'. Пропускаем.")
                    break
                collected_texts = "\n\n".join(f"{a['title']}:\n{a['text'][:1000]}" for a in articles)[:5000]
                prompt = (
                    f"Сделай подробное summary по подпункту '{subtopic}' в контексте темы '{state['topic']}'. "
                    f"Используй только факты из текстов ниже, не добавляй ничего выдуманного. "
                    f"Пиши на русском, 1-2 абзаца, с примерами, если они есть.\n\n"
                    f"{collected_texts}"
                )
                msg = HumanMessage(content=prompt)
                summary = self.llm.invoke([msg])
                summary = summary if isinstance(summary, str) else getattr(summary, "content", str(summary))
                summary = remove_think_blocks(summary)

                need_more = self.reviewer.need_more_info(subtopic, summary)
                if not need_more or attempt == max_attempts - 1:
                    subtopic_summaries.append({"subtopic": subtopic, "summary": summary})
                    logger.info(f"Summary для подпункта '{subtopic}' сгенерировано (попытка {attempt+1}, статей: {n_articles}).")
                    break
                else:
                    logger.info(f"Агент-оценщик считает информацию недостаточной — повторяем сбор с большим количеством статей.")
                    n_articles = 10
        state.update({"subtopic_summaries": subtopic_summaries})
        return state
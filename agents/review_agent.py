
import logging
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage

logger = logging.getLogger("AgenticAIPipeline")

class ReviewAgent:
    def __init__(self):
        self.llm = OllamaLLM(
            model="qwen3:4b",
            system="Ты — эксперт-оценщик качества summary. Оценивай строго, отвечай только 'ok' или 'more'."
        )

    def need_more_info(self, subtopic, summary) -> bool:
        prompt = (
            f"Вот краткое summary по теме '{subtopic}':\n\n"
            f"{summary}\n\n"
            "Оцени, достаточно ли это информативно для качественного доклада. "
            "Если информации мало, нет примеров, нет конкретики или фактов, то напиши 'Повторить сбор (more)'. "
            "Если summary достаточно информативно и покрывает все важные аспекты, напиши 'Достаточно (ok)'. "
            "Пиши только 'ok' или 'more'!"
        )
        logger.info(f"[ReviewAgent] Анализ summary для подпункта: '{subtopic}'\nТекст summary:\n{summary}\n")
        msg = HumanMessage(content=prompt)
        out = self.llm.invoke([msg])
        logger.info(f"[ReviewAgent] Ответ LLM-оценщика для подпункта '{subtopic}': {out}")
        return 'more' in out.lower()

import logging
import  re
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage
from agents.base_agent import BaseAgent

logger = logging.getLogger("AgenticAIPipeline")

class PlannerAgent(BaseAgent):
    def __init__(self):
        self.llm = OllamaLLM(
            model="qwen3:4b",
            system="Ты — научный эксперт и планировщик. Твоя задача — разбить тему на наиболее информативные и важные подпункты для доклада. Отвечай на русском."
        )

    def run(self, state : dict) -> dict:
        prompt = (
            f"Разбей тему '{state['topic']}' на 4-7 информативных и важных подпунктов (аспектов) для подробного доклада. "
            "Каждый подпункт должен быть самостоятельной подтемой (например: определение, области применения, примеры, риски, перспективы и т.п.). "
            "Выведи подпункты в виде простого нумерованного списка, без пояснений и примечаний. Пиши только на русском!"
        )
        message = HumanMessage(content=prompt)
        out = self.llm.invoke([message])
        subtopics = []

        for line in out.splitlines():
            m = re.match(r"\d+\s*[.)-]?\s*(.+)", line)
            if m:
                subtopics.append(m.group(1).strip())
        if not subtopics and out.strip():
            subtopics = [x.strip() for x in re.split(r"\n|\.", out) if x.strip()]
        logger.info(f"LLM выделил следующие подпункты для раскрытия темы:\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(subtopics)))
        state.update({"subtopics" : subtopics})
        return state

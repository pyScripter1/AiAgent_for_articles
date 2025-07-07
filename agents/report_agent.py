import logging
import re
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage
from utils.text_cleaner import remove_think_blocks

logger = logging.getLogger("AgenticAIPipeline")

class ReportAgent:
    def __init__(self):
        self.llm = OllamaLLM(
            model="qwen3:1.7b",
            system="Ты — эксперт по искусственному интеллекту. Отвечай всегда только на русском языке."
        )

    def run(self, state: dict) -> dict:
        subtopic_blocks = "\n\n".join(
            f"### {item['subtopic']}\n{item['summary']}" for item in state["subtopic_summaries"]
        )
        prompt = (
            "Ты — эксперт по искусственному интеллекту. Пиши только на русском языке! "
            f"Вот summary по подпунктам темы '{state['topic']}':\n\n"
            f"{subtopic_blocks}\n\n"
            "На основе только этих summary напиши связный, подробный и структурированный доклад по теме (4-5 абзацев), переходя логично между подпунктами, делая выводы, давая примеры. "
            "Не добавляй ничего выдуманного. В самом конце дай список подпунктов как оглавление."
        )
        msg = HumanMessage(content=prompt)
        out = self.llm.invoke([msg])
        summary = out if isinstance(out, str) else getattr(out, "content", str(out))
        summary = remove_think_blocks(summary)
        logger.info("Финальный доклад сгенерирован.")
        state.update({"final_summary": summary})
        return state
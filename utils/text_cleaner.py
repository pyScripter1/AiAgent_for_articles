import re

def remove_think_blocks(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.split(r'\\think.*', text, flags=re.IGNORECASE)[0].strip()
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return text.strip()
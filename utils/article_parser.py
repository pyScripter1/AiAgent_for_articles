from PyPDF2 import PdfReader
from newspaper import Article
import requests
from io import BytesIO
import logging

logger = logging.getLogger("AgenticAIPipeline")

def parse_article(url: str, title: str) -> str:
    text = ""
    if url.lower().endswith('.pdf'):
        try:
            response = requests.get(url)
            reader = PdfReader(BytesIO(response.content))
            text = "".join([page.extract_text() or "" for page in reader.pages])
            logger.info(f"PDF парсинг {title}: {len(text)} символов")
        except Exception as e:
            logger.warning(f"PDF ошибка {url}: {e}")
    else:
        try:
            article = Article(url, browser_user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
            article.download()
            article.parse()
            text = article.text
            if text:
                logger.info(f"Парсинг {title}: {len(text)} символов")
            else:
                logger.warning(f"Нет текста для {title}")
        except Exception as e:
            logger.warning(f"Ошибка при парсинге {url}: {e}")
    return text
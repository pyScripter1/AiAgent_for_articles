# AiAgent_for_articles
ИИ агент для генерации статей на любую тему. Меняешь промпты и все. Построен на LangGraph и QWen, для поиска, анализа и генерации статей и отчетов на любую тему.
Проект иллюстрирует подход к созданию мультиагентной системы с критическим мышлением и планированием, в духе современных Agentic AI систем.


Возможности:

* Разбивка темы на подтемы с помощью планирующего агента (planner_agent)
* Создание отчетов по статьям (report_agent)
* Генерация кратких summary и оценка их качества (summary_agent, review_agent)
* Автоматический запуск новой итерации, если отчёт получился плохим
* Генерация Markdown-репорта по итогам работы
* Запуск из main.py с простым входом

**Структура проекта**
```
.
├── agents/
│   ├── base_agent.py         
│   ├── planner_agent.py       # Планировщик, разбивающий тему на подтемы
│   ├── report_agent.py        # Суммаризатор по статьям
│   ├── review_agent.py        # Агент-критик, проверяющий качество summary
│   └── summary_agent.py       # Агент для разбора по подтемам
│
├── utils/
│   ├── article_parser.py      # Парсинг HTML и PDF источников
│   └── text_cleaner.py        # Очистка текста и фильтрация
│
├── config.py                 
├── state.py                   # Описание состояния для LangGraph
├── workflow.py                # Граф исполнения
├── agentic_ai_report.md       # Сгенерированный отчёт
├── main.py                    # Точка входа
└── README.md
```


**Запуск**
Устанавливай requirements.txt
pip install -r requirements.txt

Запускай именно main.py

```
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
```

После выполнения кода будет создан md файлик со статьями.


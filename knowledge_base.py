import json
from pathlib import Path


KB_PATH = Path(__file__).resolve().parent / "data" / "kb_articles.json"


def load_kb_articles() -> list[dict]:
    with KB_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    articles = data.get("articles")

    if not isinstance(articles, list):
        raise ValueError("Knowledge base must contain an 'articles' list.")

    if len(articles) != 5:
        raise ValueError("Knowledge base must contain exactly 5 articles.")

    for article in articles:
        if "id" not in article or "text" not in article:
            raise ValueError(
                "Each knowledge article must contain 'id' and 'text'."
            )

    return articles


def format_kb_articles(articles: list[dict]) -> str:
    return "\n".join(
        f"Article {article['id']}: {article['text']}"
        for article in articles
    )
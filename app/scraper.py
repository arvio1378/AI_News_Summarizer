from newspaper import Article
from langdetect import detect

def get_article(url) -> dict:
    article = Article(url)
    article.download()
    article.parse()

    lang = detect(article.text)

    return {
        "title" : article.title,
        "text" : article.text,
        "lang" : lang
    }
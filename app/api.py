from fastapi import FastAPI
from pydantic import BaseModel
from .scraper import get_article
from .summarizer import article_summarize
from .translator import translate_long_text
from .history import history

app = FastAPI(title="AI Summarizer API")

class SummarizeItem(BaseModel):
    url: str # input url
    lang_output: str # input bahasa

@app.post("/summarize")
def summarize(req: SummarizeItem):
    try:
        # artikel dan bahasanya
        article = get_article(req.url)
        article_lang = article['lang']

        # judul
        title = article["title"]
        if req.lang_output == "Indonesia" and article_lang == "en":
            title = translate_long_text(title, "id")
        elif req.lang_output == "English" and article_lang == "id":
            title = translate_long_text(title, "en")
        
        # isi artikel
        content = article["text"]
        if req.lang_output == "Indonesia" and article_lang == "en":
            content = translate_long_text(content, "id")
        elif req.lang_output == "English" and article_lang == "id":
            content = translate_long_text(content, "en")
        
        # ringkasan artikel
        summary = article_summarize(article["text"])
        if req.lang_output == "Indonesia" and article_lang == "en":
            summary = translate_long_text(summary, "id")
        elif req.lang_output == "English" and article_lang == "id":
            summary = translate_long_text(summary, "en")
        
        # masukkan ke histori
        history(
            url=req.url, 
            title=title, 
            content=content, 
            content_lang=req.lang_output, 
            summary=summary, 
            summary_lang=req.lang_output
        )

        # keluarkan hasil
        return {
            "url" : req.url,
            "title" : title,
            "content" : content[:500] + "...",
            "summary" : summary,
            "language" : req.lang_output
        }
    
    except Exception as e:
        return {"error" : str(e)}
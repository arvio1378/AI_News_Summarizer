import gradio as gr
import pandas as pd
import os
from scraper import get_article
from summarizer import article_summarize
from translator import translate_long_text
from history import history
from topic import get_topics
from keywords import get_keywords
from functools import lru_cache

# Load Dataset
@lru_cache(maxsize=1)
def load_data():
    file_path = "./data/history.csv"
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return pd.DataFrame(columns=["url", "title", "content", "content language", "summary", "summary language"])
    return pd.read_csv(file_path, sep=";", encoding="utf-8")

# Fungsi summarizer utama
def summarize_news(url, lang_output):
    if not url:
        return "Please input URL!", "", "", "", None
    
    try:
        # ambil artikel
        article = get_article(url)
        article_lang = article['lang']

        # judul
        title = article["title"]
        if lang_output == "Indonesia" and article_lang == "en":
            title = translate_long_text(title, "id")
        elif lang_output == "English" and article_lang == "id":
            title = translate_long_text(title, "en")

        # isi artikel
        content = article["text"]
        if lang_output == "Indonesia" and article_lang == "en":
            content = translate_long_text(content, "id")
        elif lang_output == "English" and article_lang == "id":
            content = translate_long_text(content, "en")

        # ringkasan artikel
        summary = article_summarize(article["text"])
        if lang_output == "Indonesia" and article_lang == "en":
            summary = translate_long_text(summary, "id")
        elif lang_output == "English" and article_lang == "id":
            summary = translate_long_text(summary, "en")

        # simpan ke history
        history(url=url, 
                title=title, 
                content=content, 
                content_lang=lang_output, 
                summary=summary, 
                summary_lang=lang_output)

        return f"(Article Language: {article_lang})", title, content[:500] + "...", summary

    except Exception as e:
        return f"Error: {e}", "", "", "", None

# Fungsi history
def show_history():
    df = load_data()
    if df.empty:
        return "Belum ada data history.", None, None, None

    # topic
    topics_output = ""
    keywords_output = ""
    try:
        topic_results = get_topics(df)
        for t in topic_results:
            topics_output += f"**Kata kunci:** {', '.join(t['keywords'])}\n"
            for ex in t["examples"]:
                topics_output += f"- {ex[:200]}...\n"
    except Exception as e:
        topics_output = f"Failed to generate topics: {e}"

    try:
        keywords = get_keywords(df)
        keywords_output = "\n".join([f"- {word}: {freq}" for word, freq in keywords])
    except Exception as e:
        keywords_output = f"Failed to generate keywords: {e}"

    return "", topics_output, keywords_output, df

# Interface Gradio
with gr.Blocks(theme="soft") as demo:
    gr.Markdown("# 📰 AI Summarizer")

    with gr.Tab("Summarizer"):
        url = gr.Textbox(label="Input URL")
        lang = gr.Dropdown(["Indonesia", "English"], value="English", label="Output Language")
        btn = gr.Button("Summarize")

        out_lang = gr.Textbox(label="Detected Language")
        out_title = gr.Textbox(label="Title")
        out_content = gr.Textbox(label="Content (first 500 chars)")
        out_summary = gr.Textbox(label="Summary")

        btn.click(
            fn=summarize_news,
            inputs=[url, lang],
            outputs=[out_lang, out_title, out_content, out_summary]
        )

    with gr.Tab("History"):
        btn_hist = gr.Button("Load History")
        hist_msg = gr.Textbox(label="Info")
        hist_topics = gr.Textbox(label="Topics")
        hist_keywords = gr.Textbox(label="Keywords")
        hist_table = gr.Dataframe(label="History Table")

        btn_hist.click(fn=show_history, inputs=None, outputs=[hist_msg, hist_topics, hist_keywords, hist_table])

    with gr.Tab("About"):
        gr.Markdown("""
        ## 👨‍💻 Arvio Abe Suhendar  
        Career Shifter | From Network to AI | Designing Intelligent Futures |  
        Python Developer | Machine Learning Engineer | Data Scientist  

        ### 📝 About Me
        I'm a tech enthusiast with a strong foundation in Informatics Engineering from Universitas Gunadarma.  
        After starting as a Junior Network Engineer, I'm now transitioning into AI/ML with skills in Python, ML frameworks, and data analysis.  
        Open to collaborations, mentorship, and opportunities in AI/ML.  

        ### 📞 Contact
        - Email: 4rv10suhendar@gmail.com  
        - LinkedIn: [Arvio Abe Suhendar](https://www.linkedin.com/in/arvio-abe-suhendar/)  
        - GitHub: [Arvio1378](https://github.com/arvio1378)  
        """)

# run app
if __name__ == "__main__":
    demo.launch()
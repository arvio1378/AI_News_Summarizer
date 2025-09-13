import re
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Model multilingual asli
MODEL_NAME = "csebuetnlp/mT5_multilingual_XLSum"

# Cache model agar tidak reload setiap kali
@st.cache_resource(show_spinner="Loading summarization model...")
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return tokenizer, model

def chunk_text(text, max_tokens=512):
    """Split text menjadi chunks ≤ max_tokens untuk menghindari OOM."""
    tokenizer, _ = load_model()
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(tokenizer(" ".join(current_chunk))["input_ids"]) >= max_tokens:
            chunks.append(" ".join(current_chunk[:-1]))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def article_summarize(content: str) -> str:
    tokenizer, model = load_model()

    # Hilangkan whitespace berlebihan
    WHITESPACE_HANDLER = lambda k: re.sub(r'\s+', ' ', re.sub(r'\n+', ' ', k.strip()))
    content = WHITESPACE_HANDLER(content)

    # Split artikel panjang menjadi beberapa chunk
    chunks = chunk_text(content, max_tokens=512)
    summaries = []

    for chunk in chunks:
        input_ids = tokenizer(
            chunk,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=512
        )["input_ids"]

        output_ids = model.generate(
            input_ids=input_ids,
            min_length=50,
            max_length=150,
            no_repeat_ngram_size=2,
            num_beams=4
        )[0]

        summary = tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )
        summaries.append(summary)

    # Gabungkan semua ringkasan chunk
    final_summary = " ".join(summaries)
    return final_summary

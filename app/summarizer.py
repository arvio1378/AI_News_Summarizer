import re
from functools import lru_cache
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "csebuetnlp/mT5_multilingual_XLSum"

@lru_cache(maxsize=1)
def load_model():
    """Load model & tokenizer (cached supaya tidak reload berulang)"""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return tokenizer, model

def clean_text(text: str) -> str:
    """Bersihkan HTML, tag font, dan whitespace berlebihan"""
    text = re.sub(r'<.*?>', '', text)  # hapus tag HTML
    text = re.sub(r'\s+', ' ', text)   # hilangkan whitespace berlebihan
    return text.strip()

def chunk_text(text, max_tokens=512):
    """Split text menjadi chunk kecil agar model bisa handle artikel panjang"""
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
    try:
        tokenizer, model = load_model()

        # Bersihkan HTML & whitespace
        content = clean_text(content)

        # Split artikel panjang menjadi chunk
        chunks = chunk_text(content, max_tokens=512)
        summaries = []

        for i, chunk in enumerate(chunks):
            print(f"Summarizing chunk {i+1}/{len(chunks)}...")  # logging untuk Gradio/terminal

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
                max_length=250,
                no_repeat_ngram_size=2,
                num_beams=4
            )[0]

            summary = tokenizer.decode(
                output_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            summaries.append(summary)

        # Gabungkan ringkasan chunk
        final_summary = " ".join(summaries)
        return final_summary

    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""
import re
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "csebuetnlp/mT5_multilingual_XLSum"

@st.cache_resource(show_spinner="Loading summarization...")
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model


def article_summarize(content) -> str:
    tokenizer, model = load_model()

    WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))

    input_ids = tokenizer(
        [WHITESPACE_HANDLER(content)],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    )["input_ids"]

    output_ids = model.generate(
        input_ids=input_ids,
        min_length=100,
        max_length=200,
        no_repeat_ngram_size=2,
        num_beams=4
    )[0]

    summary = tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )
    
    return summary
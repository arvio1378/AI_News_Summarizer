import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from collections import Counter

df = pd.read_csv("./data/history.csv", delimiter=";")

# Ambil kolom content
texts = df["content"].dropna().tolist()

nltk.download("stopwords")
stopwords_id = stopwords.words("indonesian")
stopwords_en = stopwords.words("english")
stopwords_all = set(stopwords_id + stopwords_en)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]+", " ", text)  # hapus simbol
    tokens = text.split()
    tokens = [t for t in tokens if t not in stopwords_all and len(t) > 2]
    return " ".join(tokens)

texts_clean = [clean_text(t) for t in texts]

def get_keywords():
    words = " ".join(texts_clean).split()
    word_freq = Counter(words).most_common(10)
    return word_freq
import streamlit as st
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from keywords import clean_text

# Cache model supaya tidak dibuat ulang setiap panggilan
@st.cache_resource(show_spinner="Analyzing topics...")
def load_topic_model():
    return BERTopic(
        embedding_model=SentenceTransformer("all-mpnet-base-v2"),
        umap_model=UMAP(n_neighbors=15, n_components=10, min_dist=0.0, metric="cosine"),
        hdbscan_model=HDBSCAN(min_cluster_size=2, metric="euclidean", cluster_selection_method="eom"),
        nr_topics="auto",
        min_topic_size=2
    )

def get_topics(df):
    if df.empty or "content" not in df.columns:
        return []

    # Ambil teks dan bersihkan
    texts_clean = [clean_text(t) for t in df["content"].dropna()]

    if not texts_clean:
        return []

    # Fit & transform topik
    topic_model = load_topic_model()
    topic_model.fit_transform(texts_clean)

    # Ambil topik info
    results = []
    for _, row in topic_model.get_topic_info().iterrows():
        topic_id = row["Topic"]
        if topic_id == -1:
            continue

        results.append({
            "keywords": [w for w, _ in topic_model.get_topic(topic_id)[:6]],
            "examples": topic_model.get_representative_docs(topic_id)[:2]
        })
    return results
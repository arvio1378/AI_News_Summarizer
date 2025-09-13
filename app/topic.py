from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from keywords import clean_text
import streamlit as st

@st.cache_resource(show_spinner="Analyzing topics...")
def load_topic_model():
    embedding_model = SentenceTransformer("all-mpnet-base-v2")
    umap_model = UMAP(n_neighbors=15, n_components=10, min_dist=0.0, metric="cosine")
    hdbscan_model = HDBSCAN(min_cluster_size=2, metric="euclidean", cluster_selection_method="eom")
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        nr_topics="auto",
        min_topic_size=2
    )
    return topic_model

def get_topics(df):
    if df.empty:
        return []
    
    texts = df["content"].dropna().tolist()
    if not texts:
        return []

    texts_clean = [clean_text(t) for t in texts]
    
    topic_model = load_topic_model()
    topics, probs = topic_model.fit_transform(texts_clean)
    
    results = []
    topic_info = topic_model.get_topic_info()

    for _, row in topic_info.iterrows():
        topic_id = row["Topic"]
        if topic_id == -1:
            continue
        
        keywords = [w for w, _ in topic_model.get_topic(topic_id)[:6]]
        examples = topic_model.get_representative_docs(topic_id)[:2]
        
        results.append({
            "keywords": keywords,
            "examples": examples
        })
    return results
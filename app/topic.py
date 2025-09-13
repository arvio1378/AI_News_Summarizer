from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from keywords import clean_text, texts

# Buat model embedding multilingual
embedding_model = SentenceTransformer("all-mpnet-base-v2")

texts_clean = [clean_text(t) for t in texts]

umap_model = UMAP(n_neighbors=15, n_components=10, min_dist=0.0, metric="cosine")
hdbscan_model = HDBSCAN(min_cluster_size=2, metric="euclidean", cluster_selection_method="eom")

# Fit BERTopic
topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    nr_topics="auto"
)

topics, probs = topic_model.fit_transform(texts_clean)

def topics_user(topic_model, n_words=6, n_examples=2):
    results = []
    topic_info = topic_model.get_topic_info()

    for _, row in topic_info.iterrows():

        topic_id = row["Topic"]
        count = row["Count"]

        if topic_id == -1:
            continue

        keywords = [w for w, _ in topic_model.get_topic(topic_id)[:n_words]]
        examples = topic_model.get_representative_docs(topic_id)[:n_examples]

        results.append({
            "keywords": keywords,
            "examples": examples
        })
        
    return results
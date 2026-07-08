import os
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_FILE = "data/notes.txt"
EMBED_FILE = "data/embeddings.npy"

model = SentenceTransformer('all-MiniLM-L6-v2')


#  SAVE NOTES + EMBEDDINGS
def save_notes(text):
    os.makedirs("data", exist_ok=True)

    # Save text
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

    # Create embedding
    new_embedding = model.encode([text])

    # Append embedding
    if os.path.exists(EMBED_FILE):
        old_embeddings = np.load(EMBED_FILE)
        updated = np.vstack([old_embeddings, new_embedding])
    else:
        updated = new_embedding

    np.save(EMBED_FILE, updated)


#  GET CONTEXT (SMART SEARCH)
def get_context(query):
    if not os.path.exists(DATA_FILE) or not os.path.exists(EMBED_FILE):
        return ""

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        texts = f.readlines()

    embeddings = np.load(EMBED_FILE)

    query_embedding = model.encode([query])[0]

    # cosine similarity
    scores = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    top_indices = np.argsort(scores)[-5:][::-1]

    context = [texts[i] for i in top_indices]

    return " ".join(context)
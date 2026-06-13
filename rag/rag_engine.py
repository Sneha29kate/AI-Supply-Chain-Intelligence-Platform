from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_knowledge(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        docs = f.readlines()

    return docs

def get_answer(query, docs):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([query] + docs)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )

    best_match = similarity.argmax()

    return docs[best_match]
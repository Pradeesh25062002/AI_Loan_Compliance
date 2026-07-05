from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_PATH = "chroma_db"

db = None

def get_db():
    global db

    if db is None:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        db = Chroma(
            persist_directory=DB_PATH,
            embedding_function=embeddings
        )

    return db


def retrieve_policy(query):
    db = get_db()
    docs = db.similarity_search(query, k=3)

    text = ""
    for doc in docs:
        text += doc.page_content + "\n"

    return text
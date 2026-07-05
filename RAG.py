from langchain_community.vectorstores import Chroma
from embeddings import embedding
DB_PATH = "chroma_db"

db = None

def get_db():
    global db

    if db is None:


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
import os
import re
from dotenv import load_dotenv
import sqlite3

from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from RAG import retrieve_policy
from groq import Groq

load_dotenv()

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_ai(question):

    application_context = ""

    match = re.search(r"APP\d+", question.upper())

    if match:

        app_id = match.group()

        conn = sqlite3.connect("loan_workbench.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM loan_applications WHERE application_id=?",
            (app_id,)
        )

        row = cursor.fetchone()
        print("Application ID:", app_id)
        print("Fetched Row:", row)
        print("Number of columns:", len(row) if row else 0)
        conn.close()

        if row:
            application_context = f"""
Application ID : {row[0]}
Customer Name : {row[1]}
Age : {row[2]}
Mobile : {row[3]}
Email : {row[4]}
PAN : {row[5]}
Aadhaar : {row[6]}
Employment Type : {row[7]}
Experience : {row[8]} years
Loan Type : {row[9]}
Loan Amount : {row[10]}
Monthly Income : ₹{row[11]}
Existing EMI : ₹{row[12]}
Credit Score : {row[13]}
Status : {row[14]}
"""

    docs = vector_db.similarity_search(question, k=4)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a Home Loan Compliance Assistant.

Policy:
{context}


Applicant Details:
{application_context}

Question:
{question}

If applicant details are available, compare them with the policy and recommend:
- Approve
- Reject
- Manual Review

Explain the reason for each eligibility criterion.
"""

    response = llm.invoke(prompt)
    return response.content
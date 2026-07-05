from langchain_community.document_loaders import PyPDFLoader


def load_policy():

    loader = PyPDFLoader("policies/Home_Loan_Policy.pdf")

    docs = loader.load()

    text = ""

    for doc in docs:
        text += doc.page_content + "\n"

    return text
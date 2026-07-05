from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3")


def generate_compliance_report(application, policy_text):

    prompt = f"""
You are a Senior Loan Compliance Officer.

Loan Policy:

{policy_text}

Loan Application:

{application}

Generate:

1. Eligibility Status
2. Failed Policy Rules
3. Risk Level
4. Recommendation
5. Final Decision

Keep the answer professional.
"""

    response = llm.invoke(prompt)

    return response.content
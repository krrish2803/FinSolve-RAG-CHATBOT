from langchain_community.vectorstores import FAISS
from groq import Groq
import os
from config import DATA
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_answer(query, role):
    db = FAISS.load_local(f"{DATA}/{role}/faiss_index", HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en-v1.5"),allow_dangerous_deserialization=True)
    role_key = role.lower()
    if role == "C-Level":
        docs = db.similarity_search(query, k=4)
    elif role == "Employee":
        docs = db.similarity_search(query, k=4, filter={"role": "general"})
    else:
        docs = db.similarity_search(query, k=4, filter={"role": role_key})

        # Build context from retrieved docs
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("source", "unknown") for doc in docs]    

        # Prompt
    prompt = f"""
You are a helpful assistant at FinSolve Technologies. Use the context below to answer the query.

Query: {query}

    Context:
    {context}

Answer:"""    

    try:
        response = client.chat.completions.create(model="llama3-70b-8192",
                                                  messages=[
                                                      {"role": "system", "content": "You are a helpful assistant."},
                                                      {"role": "user", "content": prompt}
                                                  ])
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = "Error generating response"
        sources = [str(e)] 
    return answer, sources
        
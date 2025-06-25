import os
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS

# Supported departments and their file formats
DEPARTMENTS = {
    "Engineering": ".md",
    "Finance": ".md",
    "Marketing": ".md",
    "General": ".md",
    "HR": ".csv"
}

# Path to data folder
DATA_PATH = "data"

def build_faiss_index(dept: str, extension: str):
    folder = os.path.join(DATA_PATH, dept)
    docs = []

    # Load files
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if not file.endswith(extension):
            continue

        try:
            if extension == ".csv":
                loader = CSVLoader(path)
            else:
                loader = TextLoader(path)  # .md or .txt handled as plain text
            docs.extend(loader.load())
        except Exception as e:
            print(f"[{dept}] Error loading {file}: {e}")

    print(f"[{dept}] Loaded {len(docs)} documents.")

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"[{dept}] Split into {len(chunks)} chunks.")

    if not chunks:
        print(f"[{dept}] No chunks to embed. Skipping...")
        return

    # Load embedding model
    embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en-v1.5")

    # Create FAISS vectorstore
    db = FAISS.from_documents(chunks, embeddings)
    save_path = os.path.join(folder, "faiss_index")
    db.save_local(save_path)
    print(f"[{dept}] ✅ FAISS index saved at {save_path}\n")

if __name__ == "__main__":
    for dept, ext in DEPARTMENTS.items():
        print(f"=== Building FAISS index for {dept} ===")
        build_faiss_index(dept, ext)


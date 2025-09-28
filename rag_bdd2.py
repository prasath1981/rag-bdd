# rag_bdd2.py

from dotenv import load_dotenv
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from glob import glob

# -------------------
# 1. Load ENV variables
# -------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ No OpenAI API key found. Add it to your .env file as OPENAI_API_KEY=sk-xxxx")

# -------------------
# 2. Find all .feature files in features/ folder
# -------------------
feature_folder = "features"
feature_files = glob(os.path.join(feature_folder, "*.feature"))

if not feature_files:
    raise FileNotFoundError(f"No .feature files found in folder '{feature_folder}'")

print(f"Found {len(feature_files)} feature file(s): {feature_files}")

# -------------------
# 3. Load all feature files
# -------------------
docs = []
for file in feature_files:
    loader = TextLoader(file)
    docs.extend(loader.load())

# -------------------
# 4. Split into chunks
# -------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# -------------------
# 5. Embeddings + Vector DB
# -------------------
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_bdd_db")

# -------------------
# 6. LLM + Retrieval QA
# -------------------
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=api_key
)

retriever = vectordb.as_retriever(search_kwargs={"k": 3})  # top 3 matching chunks

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# -------------------
# 7. Ask query (requirement or review request)
# -------------------
query = "Rewrite the existing feature files in descriptive style"
result = qa.invoke({"query": query})

# -------------------
# 8. Show Answer + Matching Chunks
# -------------------
print("\n🔹 Answer / Generated Scenario:\n")
print(result["result"])

print("\n📄 Matching Feature File Chunks:\n")
for i, doc in enumerate(result["source_documents"], 1):
    print(f"--- Chunk {i} ---")
    print(doc.page_content)
    print()

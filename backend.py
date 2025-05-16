from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from pinecone import Pinecone
import os
load_dotenv()
pine_api_key = os.getenv("PINECONE_API_KEY")

# Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# iterate over files in user uploaded PDF files, one by one
def create_docs(user_pdf_list, unique_id):
    docs = []
    for filename in user_pdf_list:
        chunks = get_pdf_text(filename)
        docs.append(
            Document(
                page_content=chunks,
                metadata={
                    "name": filename.name,
                    "id": filename.file_id,
                    "type=": filename.type,
                    "size": filename.size,
                    "unique_id": unique_id,
                },
            )
        )
    return docs


# Create embeddings instance
def create_embeddings_load_data():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    )
    return embeddings


# Push documents and embeddings to Pinecone
def push_to_pine(embeddings, docs):
    pine = Pinecone(api_key=pine_api_key)
    vectorstore = PineconeVectorStore(index=pine.Index("resume"), embedding=embeddings)
    vectorstore.add_documents(documents=docs)
    return vectorstore


# Retrieve existing Pinecone index
def pull_to_pine(embeddings, api_key=pine_api_key):
    pine = Pinecone(api_key=api_key)
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name="resume", embedding=embeddings
    )
    return vectorstore


# Function to help us get relavant documents from vector store - based on user input
def similar_doc(embeddings, query, k, unique_id):
    index = pull_to_pine(embeddings)
    similar_docs = index.similarity_search_with_score(
        query, int(k), {"unique_id": unique_id}
    )
    return similar_docs


# Helps us get the summary of a document
def get_summary(current_doc):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.9,
    )
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run([current_doc])
    return summary

import os
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse

import google.generativeai as genai

from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import (
    ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uvicorn
from pydantic import BaseModel

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Load the Google API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "test")

# Create the FastAPI app
app = FastAPI()

# Static variables
VECTOR_STORE = None
LAST_UPDATE_TIME = 0
PDF_FOLDER_PATH = "pdfs"
VECTOR_STORE_PATH = "vector_store"

# Initialize Google Generative AI Model
genai.configure(api_key=GOOGLE_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

class QueryRequest(BaseModel):
    query_text: str


# Function to return embedding function
def get_embedding_function() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")


# Helper function to load PDFs and build the vectorstore
def load_pdfs_and_build_vectorstore() -> None:
    """Load PDFs from the PDF_FOLDER_PATH and build the vectorstore with the embeddings.
    """
    global VECTOR_STORE

    documents = []
    for filename in os.listdir(PDF_FOLDER_PATH):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(PDF_FOLDER_PATH, filename))
            documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100
    )
    splits = text_splitter.split_documents(documents)

    VECTOR_STORE = Chroma.from_documents(
        documents=splits,
        embedding=get_embedding_function(),
        persist_directory=VECTOR_STORE_PATH,
    )


def load_persistent_vectorstore() -> None:
    """Load the persistent vector store from the VECTOR_STORE_PATH.
    """
    global VECTOR_STORE
    VECTOR_STORE = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=get_embedding_function(),
    )


load_persistent_vectorstore()


# Check for new PDFs and update vectorstore if neededd
def check_for_new_pdfs() -> None:
    global LAST_UPDATE_TIME

    current_time = time.time()
    if current_time - LAST_UPDATE_TIME > 60:  # Update every 60 seconds
        LAST_UPDATE_TIME = current_time

        latest_mtime = 0
        for filename in os.listdir(PDF_FOLDER_PATH):
            if filename.endswith(".pdf"):
                mtime = os.path.getmtime(os.path.join(PDF_FOLDER_PATH, filename))
                latest_mtime = max(latest_mtime, mtime)

        if latest_mtime > LAST_UPDATE_TIME:
            load_pdfs_and_build_vectorstore()


def format_documents(documents) -> str:
    return "\n\n".join(document.page_content for document in documents)


@app.post("/query")
async def query(query_request: QueryRequest) -> JSONResponse:
    """Query the RAG model with the given query text.
    """
    # Check for new PDFs and update vectorstore if needed
    check_for_new_pdfs()

    # Check if the vectorstore is empty
    if not VECTOR_STORE:
        load_pdfs_and_build_vectorstore()

    # Create the chain
    retriever = VECTOR_STORE.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    rag_chain = (
        {
            "context": retriever | format_documents,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # Run the chain
    answer = rag_chain.invoke(query_request.query_text)

    return JSONResponse(content={"answer": answer})


# Initial vectorstore loading
load_pdfs_and_build_vectorstore()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        limit_concurrency=10,
        limit_max_requests=1000,
        ws_max_size=1000000,
    )

import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
import google.generativeai as genai
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from ttrpg_ai_rag_assistant import enums
from ttrpg_ai_rag_assistant import ingest

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Load the Google API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "test")

# Create the FastAPI app
app = FastAPI()

# Initialize Google Generative AI Model
genai.configure(api_key=GOOGLE_API_KEY)
llm = ChatGoogleGenerativeAI(model=enums.LLM_MODEL)


class QueryRequest(BaseModel):
    query_text: str


# Function to return embedding function
def get_embedding_function() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model=enums.EMBEDDING_MODEL)


# Load PDFs and build the vectorstore
embedding_function = get_embedding_function()
ingest.load_persistent_vectorstore(embedding_function=embedding_function)
if enums.VECTOR_STORE is None:
    ingest.load_pdfs_and_build_vectorstore(
        embedding_function=embedding_function
    )


@app.post("/query")
async def query(query_request: QueryRequest) -> JSONResponse:
    """Query the RAG model with the given query text."""
    # Check for new PDFs and update vectorstore if needed
    ingest.check_for_new_pdfs(embedding_function=embedding_function)

    # Check if the vectorstore is empty
    if not enums.VECTOR_STORE:
        ingest.load_pdfs_and_build_vectorstore(
            embedding_function=embedding_function
        )

    # Define the format_documents function
    def format_documents(documents) -> str:
        return "\n\n".join(document.page_content for document in documents)

    # Create the chain
    retriever = enums.VECTOR_STORE.as_retriever()
    prompt = hub.pull(enums.LANGCHAIN_OWNER_REPO_COMMIT)
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

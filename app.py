"""This module contains the FastAPI application and the main route for handling
query requests.
"""
import os
import logging
from typing import Dict, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Static variables
IS_LOCAL = os.getenv("IS_LOCAL")
if IS_LOCAL:
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        logger.warning(
            "python-dotenv is not installed. Environment variables must be set "
            "manually."
        )
    PATH_TO_TTRPG_PDFS = os.path.join(
        "..", "..", "Documents", "Tabletop RPGs"
    )
else:
    PATH_TO_TTRPG_PDFS = "/app/data"
GAME_SYSTEM_FOLDERS = [
    "Dragonbane",
    "Kids on Bikes 2e",
    "Star Wars 5e",
    "Risus The Anything RPG",
    "Gamma Wolves",
]

from fastapi import FastAPI, HTTPException

from utils import enums
from models.query import Query
from services.chromadb import ChromaDB
from services.generative_llm import GenerativeLLM
from services.document_processor import DocumentProcessor
from services.embedding_generator import EmbeddingGenerator
from services.embedding_function import GeminiEmbeddingFunction

# Initialize FastAPI app
app = FastAPI()

# Initialize embedding function
embedding_function = GeminiEmbeddingFunction(model_name=enums.EMBEDDING_MODEL)

# Initialize Gemini model
model = GenerativeLLM.get_model(model_name=enums.LLM_MODEL)

# Initialize Chroma client and get the collection
chroma_db = ChromaDB(
    embedding_function=embedding_function,
    chroma_db_path=enums.CHROMA_DB_PATH,
    collection_name=enums.COLLECTION_NAME,
)


# Initial document processing and embedding generation
if chroma_db.collection.count() == 0:
    logger.warning(
        "No documents found in the ChromaDB collection. Processing and "
        "generating embeddings for TTRPG rulebooks..."
    )
    for folder in GAME_SYSTEM_FOLDERS:
        # Process documents
        processor = DocumentProcessor(
            base_folder=os.path.join(PATH_TO_TTRPG_PDFS, folder)
        )
        documents = processor.process_documents()
        # Generate embeddings
        embedding_generator = EmbeddingGenerator(
            embedding_function=embedding_function
        )
        embeddings = embedding_generator.generate_embeddings(
            documents=documents
        )
        # Store embeddings in ChromaDB vector collection
        if len(embeddings) > 0:
            chroma_db.collection.add(
                ids=[doc.id for doc in documents],
                embeddings=embeddings,
                metadatas=[doc.metadata for doc in documents],
                documents=[doc.page_content for doc in documents],
            )
            logger.info(
                "ChromaDB collection now contains %s documents." % (
                    chroma_db.collection.count()
                )
            )
        else:
            logger.warning(
                "No embeddings generated for the %s documents." % (
                    len(documents)
                )
            )
else:
    logger.info(
        "ChromaDB collection already contains %s documents." % (
            chroma_db.collection.count()
        )
    )


@app.post("/query")
def handle_query(query: Query) -> Optional[Dict[str, Any]]:
    """Handles a query request by generating embeddings for the query text and
    finding the most similar documents in the ChromaDB collection.

    Parameters
    ----------
    query : Query
        A Pydantic model representing the query text

    Returns
    -------
    Optional[Dict[str, Any]]
        A dictionary containing the top 3 most similar documents to the query

    Raises
    ------
    HTTPException
        If no relevant documents are found
    """
    # Query the ChromaDB collection for the most similar documents
    results = chroma_db.collection.query(
        query_texts=[query.query],
        n_results=query.top_k,  # Return the top 10 results
    )

    # No relevant documents are found
    if not results["ids"][0]:
        raise HTTPException(
            status_code=404, detail="No relevant documents found"
        )

    # Retrieve document chunks
    document_ids = results["ids"][0]
    documents = [
        chroma_db.collection.get(
            ids=[doc_id], include=["documents", "metadatas"]
        ) for doc_id in document_ids
    ]
    relevant_chunks = [doc["documents"][0] for doc in documents]

    # Context formation
    context = f"User query: {query.query}\n\nRelevant document chunks:\n"
    for chunk in relevant_chunks:
        context += f"- {chunk}\n"
    logger.debug("Context: %s" % context)

    # Response generation
    contents = f"""
You are a helpful AI assistant providing information based on tabletop role-playing game (TTRPG) rulebooks.
Answer the following question using only the context provided. If you don't have enough information to answer, say you don't know.
Context: {context}
Question: {query.query}
Answer:"""
    logger.debug("Contents: %s" % contents)
    response = model.generate_content(contents=contents)

    # Format and return response
    return {"answer": response.text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000, log_level="debug")

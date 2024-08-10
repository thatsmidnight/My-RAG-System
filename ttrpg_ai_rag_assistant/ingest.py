import os
import time

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ttrpg_ai_rag_assistant import enums


# Helper function to load PDFs and build the vectorstore
def load_pdfs_and_build_vectorstore(
    embedding_function: GoogleGenerativeAIEmbeddings,
) -> None:
    """Load PDFs from the PDF_FOLDER_PATH and build the vectorstore with the embeddings.

    Parameters
    ----
    embedding_function : GoogleGenerativeAIEmbeddings
        The embedding function to use for the vectorstore.
    """
    documents = []
    for filename in os.listdir(enums.PDF_FOLDER_PATH):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(
                os.path.join(enums.PDF_FOLDER_PATH, filename)
            )
            documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=enums.CHUNK_SIZE, chunk_overlap=enums.CHUNK_OVERLAP
    )
    splits = text_splitter.split_documents(documents)

    enums.VECTOR_STORE = Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=enums.VECTOR_STORE_PATH,
    )


def load_persistent_vectorstore(
    embedding_function: GoogleGenerativeAIEmbeddings,
) -> None:
    """Load the persistent vector store from the VECTOR_STORE_PATH.

    Parameters
    ----
    embedding_function : GoogleGenerativeAIEmbeddings
        The embedding function to use for the vectorstore.
    """
    enums.VECTOR_STORE = Chroma(
        persist_directory=enums.VECTOR_STORE_PATH,
        embedding_function=embedding_function,
    )


# Check for new PDFs and update vectorstore if neededd
def check_for_new_pdfs(
    embedding_function: GoogleGenerativeAIEmbeddings,
) -> None:
    current_time = time.time()
    if current_time - enums.LAST_UPDATE_TIME > 60:  # Update every 60 seconds
        enums.LAST_UPDATE_TIME = current_time

        latest_mtime = 0
        for filename in os.listdir(enums.PDF_FOLDER_PATH):
            if filename.endswith(".pdf"):
                mtime = os.path.getmtime(
                    os.path.join(enums.PDF_FOLDER_PATH, filename)
                )
                latest_mtime = max(latest_mtime, mtime)

        if latest_mtime > enums.LAST_UPDATE_TIME:
            load_pdfs_and_build_vectorstore(
                embedding_function=embedding_function
            )

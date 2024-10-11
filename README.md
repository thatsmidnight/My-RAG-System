# My RAG System

## Docker

```shell
docker build -t my-rag-system .
```

```shell
docker run -d -p 8000:8000 -v "Z://Users//ThatsMidnight//Documents//Documentation:/app/data" -e GOOGLE_API_KEY=your_api_key aio-generative-ai
```

## Testing

```shell
curl -X POST -H "Content-Type: application/json" -d '{"query": "How do I change the tempo of an Ableton project?"}' http://localhost:8000/query
```

## API Development

### 0. Document Fetching & Downloading

[ ] As a developer, I want to be able to identify where a specific document is available for download on a given website.

[ ] As a developer I want to be able to download a file from a given link and save it to a specified location from the client.

### 1. Document Processing

[ ] As a developer, I want to be able to read and extract text data from various PDF documents within specified folders, so that I can prepare them for vectorization and storage.

### 2. Embedding Generation and Storage

[x] As a developer, I want to be able to generate embeddings for extracted text data using a selected Google Gemini model, so that I can efficiently store and retrieve relevant information for answering user queries.

[x] As a developer, I want to be able to store generated embeddings and associated metadata in Chromadb, so that I can maintain a persistent and searchable knowledge base of the documents.

### 3. Query Handling and Response Generation

[x] As a developer, I want to be able to receive user queries via an API endpoint, so that I can process them and provide relevant answers based on the documents.

[x] As a developer, I want to be able to retrieve relevant document chunks from Chromadb based on user queries, so that I can provide contextually accurate and informative responses.

[x] As a developer, I want to be able to generate natural language responses to user queries using the selected FM  (foundation model), so that I can provide clear and understandable answers.

### 4. API Endpoints and Data Structures

[x] As a developer, I want to define clear and well-structured API endpoints (e.g., `/query`, `/add_document`, `/update_document`) and data structures, so that the API is easy to use and integrate with external systems.

### 5. Containerization

[x] As a developer, I want to containerize the API application using Docker, so that it can be easily deployed and run in various environments.

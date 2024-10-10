# AIO Generative AI Solution

## Requirements and Scoping

1. PDF Document Analysis

    The folders containing the PDF documents are located in the following location on my hard drive:

    - `~\Documents\Tabletop RPGs\Dragonbane`
    - `~\Documents\Tabletop RPGs\Dungeons & Dragons 5e`
    - `~\Documents\Tabletop RPGs\Kids on Bikes`
    - `~\Documents\Tabletop RPGs\Star Wars 5e`

    Any PDF documents nested within other folders inside the locations above are irrelevant and out of scope.

    The structure and complexity of the files is minimum. All the PDF documents have pictures that will not be relevant. Lastly, the text in the documents can be easily selected and there is no need to implement an embedded computer vision model.

2. RAG Framework Implementation

    While both LangChain and Haystack are impressive, I will limit myself to Google Gemini, locally. Eventually, this will live in AWS, but the MVP only needs to be a Docker container application.

    The PDF documents will be read and vectorized using PyMuPDF and Chromadb, respectively.

3. Google Gemini (or Gemma) Integration

    I am restricting myself to the free models for now. Again, since this is just an MVP.

    I only care about two things with respect to the performance of this project: it should be deterministic and accurate.

    Google Gemini embedding models pros and cons:

    | Model | Pros | Cons |
    | --- | --- | --- |
    | Gemini Pro | Highest accuracy, best understing of complex language and content | May be more computationally expensive, impacting response times |
    | Gemini | Good balance of performance and accuracy | May struggle with intricate details or nuanced queries |
    | Gemini Lite | Most lightweight and computationally efficient | May struggle with complex questions or documents |

    Given these pros and cons, I'll go with the Gemini model for the embedding model MVP. If the performance is not satisfactory, I will switch to the Gemini Pro model.

4. MVP Definition

   - Containerized API application. Again, this is just going to live on my local machine for now deployed in a Docker container.

   - Limit scope to the following four folder paths:

     - `~\Documents\Tabletop RPGs\Dragonbane`
     - `~\Documents\Tabletop RPGs\Dungeons & Dragons 5e`
     - `~\Documents\Tabletop RPGs\Kids on Bikes`
     - `~\Documents\Tabletop RPGs\Star Wars 5e`

   - Use **PyMuPDF** for analyzing and extracting text data from the PDF documents.

   - Use **Chromadb** to store the vectorized text data. The database will live locally on my machine for the containerized application to access between sessions in order to reduce duplicate database builds.

   - Write some basic unit tests to validate functionality using familiar libraries like `pytest` and `unittest`.

   - Accuracy and determinism are the only important factors to validate the generative AI model.

## Epics

1. API Development
   - Design the endpoints:
     - `/query`
     - `/add_document`
     - `/update_document`
   - Implement the core functionality using PyMuPDF, Chromadb and the chosen Google Gemini model.
   - Containerize the application using Docker.
2. Unit Testing
   - Write comprehensive unit tests to cover all aspects of the API:
     - document processing
     - embedding genration
     - query handling
     - response formatting
   - Utilize `pytest` and `unittest` to ensure code quality and maintainability.
3. Evaluation and Iteration
   - Gather feedback on accuracy and determinism of the responses.
   - Identify areas of improvement and iterate on the model, prompt engineering, and API implementation.

### API Development

#### 1. Document Processing

> As a developer, I want to be able to read and extract text data from various PDF documents within specified folders, so that I can prepare them for vectorization and storage.

#### 2. Embedding Generation and Storage

> As a developer, I want to be able to generate embeddings for extracted text data using a selected Google Gemini model, so that I can efficiently store and retrieve relevant information for answering user queries.

Of the available Google Gemini models, which fit the "use case" we are trying to solve best? We have access to the following model variants from the Google Gemini models:

- `gemini-1.5-flash`
- `gemini-1.5.pro`
- `gemini-1.0-pro`
- `text-embedding-004`
- `aqa`

> As a developer, I want to be able to store generated embeddings and associated metadata in Chromadb, so that I can maintain a persistent and searchable knowledge base of the TTRPG documents.

#### 3. Query Handling and Response Generation

> As a developer, I want to be ablet oreceive user queries via an API endpoint, so that I can process them and provide relevant answers based on the TTRPG documents.
>
> As a developer, I want to be able to retrieve relevant document chunks from Chromadb based on user queries, so that I can provide contextually accurate and informative responses.
>
> As a developer, I want to be able to generate natural language responses to user queries using the selected Google Gemini model, so that I can provide clear and understandable answers.

#### 4. API Endpoints and Data Structures

> AS a developer, I want to define clear and well-structured API endpoints (e.g., `/query`, `/add_document`, `/update_document`) and data structures, so that the API is easy to use and integrate with external systems.

#### 5. Containerization

> As a developer, I want to containerize the API application using Docker, so that it can be easily deployed and run in various environments.

### Docker

```shell
docker build -t aio-generative-ai .
```

```shell
docker run -d -p 8000:8000 -v "Z://Users//ThatsMidnight//Documents//Documentation:/app/data" -e GOOGLE_API_KEY=your_api_key aio-generative-ai
```

### Testing

```shell
curl -X POST -H "Content-Type: application/json" -d '{"query": "Give me a summary of Dragonbane?"}' http://localhost:8000/query
curl -X POST -H "Content-Type: application/json" -d '{"query": "Give me a summary of the gameplay of Gamma Wolves?"}' http://localhost:8000/query
```

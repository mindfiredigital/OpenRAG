
# OpenRAG API Documentation

## Version: 0.1

### **Overview**

The OpenRAG API allows for interaction with a variety of endpoints to manage LLM (Large Language Model) operations, file uploads, and chat functionalities. This document outlines the available endpoints, parameters, and expected responses.

---

## **Endpoints**

### **1. Hello API**
- **Endpoint:** `/`
- **Method:** `GET`
- **Summary:** Returns a basic "Hello" message.
- **Operation ID:** `hello_api__get`
- **Responses:**
  - **200 (Successful Response):**
    - **Content Type:** `application/json`
    - **Schema:** An empty schema is defined here, meaning the response body will likely be a simple JSON object like `{}`.
- **Code Example**

  ```
  curl -X GET "http://<your-server-address>/" -H "accept: application/json"
  ```

---

### **2. Get LLM Options**
- **Endpoint:** `/llm-options`
- **Method:** `GET`
- **Summary:** Retrieves the available options for Large Language Models (LLM).
- **Operation ID:** `get_llm_options_llm_options_get`
- **Responses:**
  - **200 (Successful Response):**
    - **Content Type:** `application/json`
    - **Schema:** An empty schema, indicating the response will contain a simple JSON structure.
- **Code Example**

  ```
  curl -X GET "http://<your-server-address>/llm-options" -H "accept: application/json"
  ```

---

### **3. Upload PDF**
- **Endpoint:** `/upload`
- **Method:** `POST`
- **Summary:** Allows for uploading a PDF file.
- **Operation ID:** `upload_pdf_upload_post`
- **Request Body:**
  - **Content Type:** `multipart/form-data`
  - **Schema:**
    - **Body_upload_pdf_upload_post:**
      - **model_name (string, required):** Name of the model to be used.
      - **vector_db_name (string, required):** Name of the vector database where data will be stored.
      - **file (string, format: binary, required):** The PDF file to be uploaded.
- **Responses:**
  - **200 (Successful Response):**
    - **Content Type:** `application/json`
    - **Schema:**
      - **UploadResponse:**
        - **collection_name (string):** Name of the collection that was generated based on the uploaded PDF.
  - **422 (Validation Error):**
    - **Content Type:** `application/json`
    - **Schema:**
      - **HTTPValidationError:**
        - **detail (array of ValidationError):** Contains details of the validation error.
  - **Code Example**

  ```
  curl -X POST "http://<your-server-address>/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "model_name=<your-model-name>" \
  -F "vector_db_name=<your-vector-db-name>" \
  -F "file=@<path-to-your-pdf-file>" \
  -F "embedding_model=<embedding-model-name>"
  ```


---

### **4. Check Collection**
- **Endpoint:** `/check-collection`
- **Method:** `GET`
- **Summary:** Verifies if a specific collection exists in the vector database.
- **Operation ID:** `check_collection_check_collection_get`
- **Parameters:**
  - **collection_name (string, required, query):** The name of the collection to check.
  - **vector_db_name (string, required, query):** The name of the vector database to query.
- **Responses:**
  - **200 (Successful Response):**
    - **Content Type:** `application/json`
    - **Schema:** An empty schema indicating that the response will be a simple JSON object.
  - **422 (Validation Error):**
    - **Content Type:** `application/json`
    - **Schema:**
      - **HTTPValidationError:**
        - **detail (array of ValidationError):** Contains details of the validation error.
- **Code Example**

  ```
  curl -X GET "http://<your-server-address>/check-collection?collection_name=<your-collection-name>&vector_db_name=<your-vector-db-name>&embedding_model=<embedding-model-name>" \
  -H "accept: application/json"
  ```

---

### **5. Start Chat**
- **Endpoint:** `/chat`
- **Method:** `POST`
- **Summary:** Initiates a chat based on the provided collection and query.
- **Operation ID:** `start_chat_chat_post`
- **Parameters:**
  - **collection_name (string, required, query):** The name of the collection to be used.
  - **query (string, required, query):** The query or question to be sent to the model.
  - **model_name (string, required, query):** The name of the LLM model to use for generating responses.
  - **vector_db_name (string, required, query):** The name of the vector database where the context resides.
- **Responses:**
  - **200 (Successful Response):**
    - **Content Type:** `application/json`
    - **Schema:** An empty schema, indicating the response will contain a simple JSON structure.
  - **422 (Validation Error):**
    - **Content Type:** `application/json`
    - **Schema:**
      - **HTTPValidationError:**
        - **detail (array of ValidationError):** Contains details of the validation error.
- **Code Example**

  ```
  curl -X POST "http://<your-server-address>/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "<your-collection-name>",
    "query": "<your-query>",
    "model_name": "<your-model-name>",
    "vector_db_name": "<your-vector-db-name>",
    "embedding_model": "<your-embedding-model-name>",
    "custom_prompt": "<optional-custom-prompt>"  # Optional field, remove if not needed
  }'

  ```

---

### **6. Vector DB List**
- **Endpoint:** `/vector-db-list`
- **Method:** `GET`
- **Summary:** Retrieves the list of supported vector databases.
- **Operation ID:** `get_vector_db_list`
- **Parameters:** None
- **Responses:**
  - **200 (Successful Response):**
    - **Content Type:** `application/json`
    - **Schema:** A list of strings representing the names of supported vector databases.
      - **Example:**
        ```json
        [
          "chromadb",
          "qdrant",
          "faiss"
        ]
        ```
  - **422 (Validation Error):**
    - **Content Type:** `application/json`
    - **Schema:**
      - **HTTPValidationError:**
        - **detail (array of ValidationError):** Contains details of the validation error.

- **Code Example**

  ```
  curl -X GET "http://<your-server-address>/vector-db-list" \
  -H "accept: application/json"
  ```

---

## **Components**

### **Schemas**

#### **1. Body_upload_pdf_upload_post**
- **Type:** `object`
- **Properties:**
  - **model_name (string, required):** The name of the model to use for processing the PDF.
  - **vector_db_name (string, required):** The vector database name where the PDF data will be stored.
  - **file (string, format: binary, required):** The PDF file to upload.

#### **2. UploadResponse**
- **Type:** `object`
- **Properties:**
  - **collection_name (string, required):** The name of the collection that was generated after the file upload.

#### **3. HTTPValidationError**
- **Type:** `object`
- **Properties:**
  - **detail (array of ValidationError):** Detailed error messages if validation fails.

#### **4. ValidationError**
- **Type:** `object`
- **Properties:**
  - **loc (array of strings or integers):** The location where the error occurred.
  - **msg (string):** The error message.
  - **type (string):** The type of error.

---

### **Response Codes**

- **200 (Successful Response):** The request was successful, and the response contains the requested data.
- **422 (Validation Error):** The request failed due to invalid input parameters. The response will contain details about the validation error.

---

### **Notes**
- Make sure that when uploading PDFs, the file size and format are properly validated.
- The vector database name and model name are crucial parameters for all operations related to chat and data storage.
- All errors return a detailed message to help debug issues quickly. Ensure you handle `422` validation errors gracefully in your application logic.

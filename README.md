# OpenRAG

<img src="./OpenRAGLogo.png" alt="Project Logo" width="100" height="auto">

Short project description goes here.

## Table of Contents

- [OpenRAG](#OpenRAG)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Description

An open-source Generative AI (GenAI) application designed to provide
users with the flexibility and power to work with various open-source
large language models (LLMs). This application serves as a versatile tool,
enabling users to interact with and query their data using different AI models and vector databases.

## Features

- ### Support for All Open-Source LLM Models:
  - The application is built with comprehensive support for all major open-source LLMs. This allows users to select from a wide range of models, ensuring they can choose the one that best fits their specific needs and use cases.
- ### Integration with Multiple Open Source and Free to use Vector Databases:
  - The application currently supports three popular vector databases—Chroma, FAISS, and Qdrant—with plans to expand this list further. This feature enables users to leverage different indexing and search capabilities, enhancing the efficiency and accuracy of information retrieval within their data.
- ### PDF File Upload and Data Querying:
  - Users can easily upload their PDF files to the application. Once uploaded, they can select their preferred LLM and vector database to create a collection. This collection serves as a structured repository of the uploaded data, which users can then query to extract insights or generate responses based on the content of the PDF.
- ### Persistent Collection Names for Reusability:
  - Upon uploading a PDF, the application generates a unique collection name. This name is crucial as it allows users to reference their data in future sessions without needing to re-upload the PDF. Users can simply choose the previously generated collection name, along with any LLM and vector database of their choice, to query the same data seamlessly.
- ### Consistency in Vector Database Usage:
  - The vector database selected during the PDF upload process is tightly coupled with the data collection. When querying the data, the application ensures that only the initially chosen vector database is used. Attempting to switch to a different vector database for querying will result in an error, maintaining consistency and accuracy in data retrieval.

List the key features of your project.

## Getting Started

Instructions on how to get started with your project, including installation, prerequisites, and basic usage.

### Prerequisites

- API Understanding
- Make sure to have python version 3.9 or greater
- Qdrant docker image should be running [Qdrant Start](https://qdrant.tech/documentation/quickstart/)
- Check the port 6333 on localhost is accesible


### Installation

Provide detailed installation steps using code blocks to show commands or configuration files.
  * Clone the repo
  * Create virtualenv
  * Install requirements using requirements.txt ``pip install -r requirements.txt``
  * Install faiss as per your system 
    - for cpu : ``pip install faiss-cpu`` 
    - for gpu : ``pip install faiss-gpu`` 
  * Run this command to download spacy stuffs ``python3 -m spacy download en_core_web_sm``
  * Run the application using command ``uvicorn main:app``

### Usage

The application is API-first and can be integrated with various frontend tools. The primary use cases include:
  - Uploading a PDF and querying the content through a selected LLM model and vector database.
  - Retrieving previously created collections for querying data.
  - Switching between supported LLMs and vector databases for different sessions.

  ### Example API Usage:

  ```
  curl -X POST "https://example.com/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@yourfile.pdf" \
  -F "model_name=GPT-3.5" \
  -F "vector_db_name=Qdrant"

  ```

## API Hosting

This API can be hosted on your local machine or deployed to a production server. Once hosted, you can access and expose the API endpoints for your applications.

  - **Local Hosting:** You can run the application using uvicorn for local development and testing.
  - **Production Hosting:** For production environments, you can use tools like Docker, Kubernetes, or a cloud provider to scale the API. Consider using a WSGI/ASGI server like Gunicorn for production-grade performance.

  Check the API using Swagger UI by visiting ``https://example.com/docs`` or ``https://example.com/openapi.json`` after running the application.

## API Documentation

A complete API demo, including the frontend, is available at this [Link](https://codesandbox.io/p/github/abdulla-mindfire/open-rag-fe/main). The detailed API documentation, which includes all endpoints, parameters, and expected responses, can be found in the [API.md](API.md) file.

## Contributing

Guidelines for contributing to the project. Provide information on how users can contribute, submit issues, or make pull requests.
Add link to CONTRIBUTING.md file.

## Common Errors

While running this project, you might encounter the following error:


TypeError: Descriptors cannot be created directly.
If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
If you cannot immediately regenerate your protos, some other possible workarounds are:

1. Downgrade the protobuf package to 3.20.x or lower.
2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).""

For more information or to resolve this issue, you can refer to this [discussion](https://github.com/chroma-core/chroma/issues/2571#issuecomment-2250328476).



## License

This project is licensed under the MIT license - see LICENSE.md for details.

## Acknowledgments

Give credit to any resources or individuals whose work or support has been instrumental to your project.

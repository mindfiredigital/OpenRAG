import sys
from setuptools import setup

__version__ = "0.0.1"

setup(
    name="open-rag",
    version=__version__,
    description='''An open-source Generative AI (GenAI) application designed to provide users
                  with the flexibility and power to work with various open-source large
                  language models (LLMs). This application serves as a versatile tool, 
                  enabling users to interact with and query their data using different
                  AI models and vector databases.''',
    long_description='''An open-source Generative AI (GenAI) application designed to
                       provide users with the flexibility and power to work with
                       various open-source large language models (LLMs). This
                       application serves as a versatile tool, enabling users to
                       interact with and query their data using different AI models
                       and vector databases.

                    Key Features:
                    Support for All Open-Source LLM Models: The application is built
                    with comprehensive support for all major open-source LLMs. This
                    allows users to select from a wide range of models, ensuring
                    they can choose the one that best fits their specific needs and use cases.

                    Integration with Multiple Open Source and Free to use Vector Databases:
                    The application currently supports three popular vector databases—Chroma,
                    FAISS, and Qdrant—with plans to expand this list further. This feature
                    enables users to leverage different indexing and search capabilities,
                    enhancing the efficiency and accuracy of information retrieval within their data.

                    PDF File Upload and Data Querying: Users can easily upload their PDF
                    files to the application. Once uploaded, they can select their preferred
                    LLM and vector database to create a collection. This collection serves
                    as a structured repository of the uploaded data, which users can then
                    query to extract insights or generate responses based on the content of the PDF.

                    Persistent Collection Names for Reusability: Upon uploading a PDF,
                    the application generates a unique collection name. This name is
                    crucial as it allows users to reference their data in future
                    sessions without needing to re-upload the PDF. Users can simply
                    choose the previously generated collection name, along with any
                    LLM and vector database of their choice, to query the same data seamlessly.

                    Consistency in Vector Database Usage: The vector database
                    selected during the PDF upload process is tightly coupled
                    with the data collection. When querying the data, the
                    application ensures that only the initially chosen vector
                    database is used. Attempting to switch to a different vector
                    database for querying will result in an error, maintaining
                    consistency and accuracy in data retrieval.''',
    author="Abdulla Ansari",
    author_email="abdulla.ansari@mindfiresolutions.com",
    maintainer="Chirag Patil",
    maintainer_email="Chiragp@mindfiresolutions.com"
)


try:
    from semantic_release import setup_hook
    setup_hook(sys.argv)
except ImportError:
    pass

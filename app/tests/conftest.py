import os
import sys

import pytest
from fastapi.testclient import TestClient

from main import app
from utils.constant import LLM_OPTIONS, VectorDB
from controller.Openembedder import OpenEmbedder
from controller.upload_file import extract_and_create_temp_file

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Mock OpenEmbedder class to bypass real database interactions
class MockOpenEmbedder:
    # pylint: disable=too-few-public-methods
    def __init__(self, vectordb_name, collection_name):
        self.vectordb_name = vectordb_name
        self.collection_name = collection_name

    def create_database(self, _file_path):
        return True  # Mock success, no actual database interaction


def mock_extract_and_create_temp_file(_file, _tmp_file_path):
    pass


def mock_embed_documents():
    texts = ["hello", "hi"]
    # Return mock embeddings (e.g., random embeddings or just dummy data)
    return [[0.1] * 768 for _ in texts]  # Assuming embeddings have size 768


app.dependency_overrides[
    extract_and_create_temp_file
] = mock_extract_and_create_temp_file
app.dependency_overrides[OpenEmbedder] = MockOpenEmbedder
app.dependency_overrides[
    OpenEmbedder.create_database
] = MockOpenEmbedder.create_database
app.dependency_overrides[
    "sentence_transformers.SentenceTransformer.encode"
] = mock_embed_documents


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def get_llm_list():  # pylint: disable=unused-argument
    return LLM_OPTIONS


@pytest.fixture
def get_vector_db_list():  # pylint: disable=unused-argument
    vector_dbs = [db.name.lower() for db in VectorDB]
    return vector_dbs

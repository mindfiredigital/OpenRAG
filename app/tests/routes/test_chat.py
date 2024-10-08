# import pytest
# from unittest.mock import patch, MagicMock


# @pytest.fixture
# def mock_openembedder():
#     with patch("controller.Openembedder") as MockOpenEmbedder:
#         # Mock instance returned by OpenEmbedder()
#         mock_embedder_instance = MagicMock()
#         # Mock the return value of query_database
#         mock_embedder_instance.query_database.return_value = [
#             MagicMock(page_content="This is a test result from the collection.")
#         ]
#         # Mock the vectordb attribute and its similarity_search method
#         mock_embedder_instance.vectordb.similarity_search.return_value = [
#             MagicMock(page_content="This is a similarity search result.")
#         ]
#         # Set the return value for the patched OpenEmbedder
#         MockOpenEmbedder.return_value = mock_embedder_instance
#         yield MockOpenEmbedder.return_value

# @pytest.fixture
# def mock_openllm():
#     with patch("controller.Openllm.OpenLLM") as MockOpenLLM:
#         mock_llm_instance = MagicMock()
#         mock_llm_instance.generate_response.return_value = "This is the LLM's response."
#         MockOpenLLM.return_value = mock_llm_instance
#         yield mock_llm_instance  # Yield the actual instance for assertions

# def test_start_chat(client, mock_openembedder, mock_openllm):
#     # Mock the OpenEmbedder object and its methods
#     mock_openembedder.query_database.return_value = [
#         MagicMock(page_content="This is a test result from the collection.")
#     ]

#     # Make the POST request to the /chat endpoint
# response = client.post(
#     "/chat?collection_name=test_collection"
#     "&query=What is the test result?"
#     "&model_name=Meta-Llama-3-8B-Instruct.Q4_0.gguf"
#     "&vector_db_name=faiss"
# )

#     # Check the response status code
#     assert response.status_code == 200

#     # Check the response data
#     response_data = response.json()
#     assert response_data["response"] == "This is the LLM's response."

#     # Ensure the mock objects were called with the expected arguments
#     mock_openembedder.query_database.assert_called_once_with(
#               query="What is the test result?", k=3)
#     mock_openllm.generate_response.assert_called_once()
#     # Check the response data
#     response_data = response.json()
#     assert response_data["response"] == "This is the LLM's response."

#     # Ensure the mock objects were called with the expected arguments
#     mock_openembedder.query_database.assert_called_once_with(
#               query="What is the test result?", k=3)
#     mock_openllm.generate_response.assert_called_once()

from enum import Enum

from gpt4all import GPT4All
from hurry.filesize import size


class VectorDB(str, Enum):
    """
    Enum representing supported vector databases.

    Attributes:
        CHROMADB (str): Represents the ChromaDB vector database.
        QDRANT (str): Represents the Qdrant vector database.
        FAISS (str): Represents the FAISS vector database.
    """

    CHROMADB = "chromadb"
    QDRANT = "qdrant"
    FAISS = "faiss"


# Dynamically create an enum from MODEL_LIST
class ModelEnum(str, Enum):
    """
    Enum dynamically created from the model list.

    The models will be used to validate the available Large Language Models (LLMs)
    that can be selected in the application.

    Methods:
        _generate_next_value_: Automatically generates the next value for the enum member
                               by converting the member name to lowercase.
    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Automatically generate the next value for the enum member.

        Args:
            name (str): The name of the enum member.
            start (int): The starting value (unused here).
            count (int): The index of the current member (unused here).
            last_values (list): Previously generated values (unused here).

        Returns:
            str: Lowercased string of the member name.
        """

        return name.lower()


LLM_OPTIONS = []
MODEL_LIST = []
for model in GPT4All.list_models():
    if "embeddingModel" in model:
        continue

    tmp_dict = {}
    tmp_dict["Model"] = model["filename"]
    tmp_dict["model_size"] = size(float(model["filesize"]))
    tmp_dict["RAM_required"] = f"{model['ramrequired'] }G"
    LLM_OPTIONS.append(tmp_dict)
    MODEL_LIST.append(model["filename"])
    setattr(ModelEnum, model["filename"], model["filename"])


class EmbeddingModel(str, Enum):
    """
    Enum representing different embedding models used for generating vector representations of text.

    Each model is identified by its unique string identifier, which corresponds to a specific
    pre-trainedmodel from popular libraries such as `sentence-transformers` or `facebook/dpr`.
    These models are used for tasks such as question answering, document retrieval, and
    general-purpose text embeddings.

    Attributes:
        MULTI_QA_MPNET (str): "multi-qa-mpnet-base-dot-v1"
            A model designed for question answering, optimized for generating high-quality
            embeddings.

        ST_ALL_MPNET (str): "sentence-transformers/all-mpnet-base-v2"
            A sentence-transformer model that provides strong general-purpose embeddings.

        META_DPR_QUESTION (str): "facebook/dpr-question_encoder-single-nq-base"
            Facebook's dense passage retrieval (DPR) model, optimized for question encoding.

        MIXEDBREAD_EMBED (str): "mixedbread-ai/mxbai-embed-large-v1"
            A large embedding model from Mixedbread AI designed for generating robust text
            embeddings.

        ST_ALL_MINILM (str): "sentence-transformers/all-MiniLM-L6-v2"
            A smaller, efficient model from sentence-transformers designed for general-purpose
            embeddings.
    """

    MULTI_QA_MPNET = "multi-qa-mpnet-base-dot-v1"
    ST_ALL_MPNET = "sentence-transformers/all-mpnet-base-v2"
    META_DPR_QUESTION = "facebook/dpr-question_encoder-single-nq-base"
    MIXEDBREAD_EMBED = "mixedbread-ai/mxbai-embed-large-v1"
    ST_ALL_MINILM = "sentence-transformers/all-MiniLM-L6-v2"

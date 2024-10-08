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
    MULTI_QA_MPNET = "multi-qa-mpnet-base-dot-v1"
    ST_ALL_MPNET = "sentence-transformers/all-mpnet-base-v2"
    META_DPR_QUESTION = "facebook/dpr-question_encoder-single-nq-base"
    MIXEDBREAD_EMBED = "mixedbread-ai/mxbai-embed-large-v1"
    ST_ALL_MINILM = "sentence-transformers/all-MiniLM-L6-v2"

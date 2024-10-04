from enum import Enum

from gpt4all import GPT4All
from hurry.filesize import size


class VectorDB(str, Enum):
    CHROMADB = "chromadb"
    QDRANT = "qdrant"
    FAISS = "faiss"


# Dynamically create an enum from MODEL_LIST
class ModelEnum(str, Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
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

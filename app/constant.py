from gpt4all import GPT4All
from hurry.filesize import size

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

VECTOR_DB_LIST = ["chromadb", "qdrant", "faiss"]

import os
import threading
import time
from typing import Iterator

import gpt4all

from utils.utils import preprocess_text, chat_histories
from config.log_config import logger


class ModelNotFoundError(Exception):
    """Custom exception for model not found locally."""

    def __init__(self, model_name):
        super().__init__(
            f"Model '{model_name}' not found locally. Please download it first."
        )


class ModelDownloadInProgressError(Exception):
    """Custom exception for model download already in progress."""

    def __init__(self, model_name):
        super().__init__(
            f"Model '{model_name}' download is in progress. Please wait until it completes."
        )


class OpenLLM:
    download_in_progress = False  # Class-level variable to track download status

    def __init__(self, model_name: str = "orca-mini-3b-gguf2-q4_0.gguf", device="cpu"):
        """_summary_

        Args:
            model_name (str, optional): model name supported by gpt4all.
                                        To get list of models and description use list_models method
                                        Defaults to 'orca-mini-3b-gguf2-q4_0.gguf'.
        """

        self.model_name = model_name
        self.device = device

        if not OpenLLM.model_exists(self.model_name):
            raise ModelNotFoundError(model_name)

        self.model = gpt4all.GPT4All(model_name=model_name, device=device)

    @classmethod
    def model_exists(cls, model_name: str) -> bool:
        """
        Check if the model is already downloaded locally.

        Parameters:
        ----------
        model_name : str
            The name of the model to check.

        Returns:
        -------
        bool
            True if the model exists locally, False otherwise.
        """
        # Assuming the models are downloaded to a default directory in gpt4all
        model_path = os.path.join(
            os.path.expanduser("~"), ".cache", "gpt4all", model_name
        )
        return os.path.exists(model_path)

    def list_models(self) -> list[dict]:
        """return list of model supported by gpt4all with its description

        Returns:
            list[dict]: list of dictionary
        """
        return gpt4all.GPT4All.list_models()

    @classmethod
    def download_model(cls, model_name: str) -> None:
        """
        Downloads the specified model if it is not already available locally.

        Parameters:
        ----------
        model_name : str
            The name of the model to download.
        """

        # Assuming the models are downloaded to a default directory in gpt4all
        if cls.model_exists(model_name):
            print(f"Model '{model_name}' is already downloaded.")
            return True

        if OpenLLM.download_in_progress:
            raise ModelDownloadInProgressError(model_name)

        OpenLLM.download_in_progress = True

        def download():
            try:
                print(f"Downloading model '{model_name}'...")
                gpt4all.GPT4All(model_name=model_name)  # This triggers the download
                print(f"Model '{model_name}' downloaded successfully.")
            finally:
                OpenLLM.download_in_progress = False

        # Run download in a separate thread to avoid blocking
        threading.Thread(target=download).start()
        return False

    def generate_response(
        self, prompt: str, max_tokens: int = 3000, stream: bool = False
    ) -> str:
        """
        Generates a response from the selected LLM based on the given prompt.

        Parameters:
        ----------
        prompt : str
            The input text prompt to generate a response for.

        max_tokens : int, optional
            The maximum number of tokens to generate. Default is 150.

        Returns:
        -------
        str
            The generated response from the LLM.
        """

        if not OpenLLM.model_exists(self.model_name):
            raise ModelNotFoundError(self.model_name)

        if stream:
            return self.model.generate(prompt, max_tokens=max_tokens, streaming=True)
        return self.model.generate(prompt, max_tokens=max_tokens)


# Generator function to stream the LLM response
def llm_response_stream(llm, final_prompt: str, session_id: str) -> Iterator[str]:
    full_response = (
        ""  # To collect the full response for logging and further processing
    )

    for token in llm.generate_response(final_prompt, stream=True):
        yield token
        time.sleep(0.1)  # To simulate real-time response

    logger.info("LLM Response: %s", full_response)
    processed_text = preprocess_text(full_response)
    chat_histories[session_id].append({"role": "assistant", "content": processed_text})
    logger.info("Updated chat history for session: %s", session_id)

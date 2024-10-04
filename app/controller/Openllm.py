import gpt4all


class OpenLLM:
    def __init__(self, model_name: str = "orca-mini-3b-gguf2-q4_0.gguf", device="cpu"):
        """_summary_

        Args:
            model_name (str, optional): model name supported by gpt4all.
                                        To get list of models and description use list_models method
                                        Defaults to 'orca-mini-3b-gguf2-q4_0.gguf'.
        """

        self.model = gpt4all.GPT4All(model_name=model_name, device=device)

    def list_models(self) -> list[dict]:
        """return list of model supported by gpt4all with its description

        Returns:
            list[dict]: list of dictionary
        """
        return gpt4all.GPT4All.list_models()

    def generate_response(self, prompt: str, max_tokens: int = 3000) -> str:
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
        response = self.model.generate(prompt, max_tokens=max_tokens)
        return response

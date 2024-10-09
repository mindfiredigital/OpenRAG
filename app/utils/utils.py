import re
from typing import Dict, List
import tiktoken
from pydantic import BaseModel
from fastapi import HTTPException

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

nltk.download("punkt_tab")
nltk.download("stopwords")

# Example token limit for GPT-3.5-turbo
TOKEN_LIMIT = 4000

# In-memory chat history store (replace with a database for persistence)
chat_histories: Dict[str, List[Dict[str, str]]] = {}


class ChatMessage(BaseModel):
    """
    A model representing a chat message in the conversation.

    Attributes:
        role (str): The role of the message sender. Typically either 'user' or 'assistant'.
        content (str): The actual content of the message.
    """

    role: str
    content: str


def calculate_token_length(text: str) -> int:
    """
    Calculates the number of tokens in the given text based on the encoding for the
    GPT-3.5-turbo model.

    Args:
        text (str): The input text for which the token length is calculated.

    Returns:
        int: The number of tokens in the input text.
    """

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))


def manage_chat_history(session_id: str):
    """
    Manages the chat history by ensuring the total token count does not exceed the TOKEN_LIMIT.
    If the limit is exceeded, older messages are removed from the history.

    Args:
        session_id (str): The unique identifier for the chat session. Used to retrieve and manage
        the chat history.

    Modifies:
        chat_histories[session_id]: Removes the oldest messages in the chat history if the token
        count exceeds the limit.
    """

    total_tokens = 0
    index = 0
    while index < len(chat_histories[session_id]):
        message = chat_histories[session_id][index]
        total_tokens += calculate_token_length(message["content"])
        if total_tokens > TOKEN_LIMIT:
            chat_histories[session_id].pop(0)
        else:
            index += 1


def preprocess_text(text):
    """
    Preprocesses the given text by removing special characters, converting to lowercase,
    tokenizing the text, removing stop words, removing verbs using spaCy, and joining
    the tokens back into a string.
    Args:
        text (str): The text to be preprocessed.
    Returns:
        str: The processed text after applying the preprocessing steps.
    """
    # Remove special characters and convert to lowercase
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]

    # Remove verbs using spaCy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(" ".join(tokens))
    tokens = [str(token.lemma_) for token in doc if token.pos_ != "VERB"]

    # Join the tokens back into a string
    processed_text = " ".join(tokens)

    return processed_text


def generate_final_prompt(history_prompt, results, query):
    final_prompt = f"""
            Chat History:
            {history_prompt}

            Context:
            {results}

            Prompt:
            1. Give a response matching with the query.
            2. Only respond from the above context.
            3. Provide an answer in a good format.
            4. Do not repeat the query.
            5. Do not add questions in the response.
            6. Do not repeat the prompt in the response.

            Query:
            {query}
        """
    return final_prompt


# Helper function to validate custom prompt
def validate_custom_prompt(custom_prompt: str):
    """
    Validates the custom prompt to ensure it contains the required placeholders.

    Args:
        custom_prompt (str): The custom prompt provided by the user.

    Raises:
        HTTPException: If the custom prompt does not contain all required placeholders
        ('{query}', '{chat_history}', '{results}').
    """

    required_placeholders = ["{query}", "{chat_history}", "{results}"]
    for placeholder in required_placeholders:
        if placeholder not in custom_prompt:
            raise HTTPException(
                status_code=400,
                detail=f"""Custom prompt must include {placeholder} placeholder.
                    Here is the example how you can construct your prompt around this

                    Chat History:
                    {"history_prompt"}

                    Context:
                    {"results"}

                    Prompt:
                    1. Give a response matching with the query.
                    2. Only respond from the above context.
                    3. Provide an answer in a good format.
                    4. Do not repeat the query.
                    5. Do not add questions in the response.
                    6. Do not repeat the prompt in the response.

                    Query:
                    {"query"}
                """,
            )

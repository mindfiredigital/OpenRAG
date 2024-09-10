import re
from typing import Dict, List
import tiktoken
from pydantic import BaseModel

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
    role: str
    content: str


def calculate_token_length(text: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))


def manage_chat_history(session_id: str):
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

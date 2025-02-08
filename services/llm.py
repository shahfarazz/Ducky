import os
import traceback
from typing import List, Dict, AsyncGenerator

import openai
from openai import AsyncOpenAI

from dotenv import load_dotenv
from openai import OpenAIError, OpenAI
import streamlit as st

# Load .env file
load_dotenv()


openai_model = os.getenv('OPENAI_API_MODEL')

print(
    f"openai_model: {openai_model} openai.api_key: {os.getenv('OPENAI_API_KEY')} openai.api_base: {os.getenv('OPENAI_API_BASE_URL')}")


async def converse(messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """
    Given a conversation history, generate an iterative response of strings from the OpenAI API.

    :param messages: a conversation history with the following format:
    `[ { "role": "user", "content": "Hello, how are you?" },
       { "role": "assistant", "content": "I am doing well, how can I help you today?" } ]`

    :return: a generator of delta string responses
    """
    aclient = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'),
                          base_url=os.getenv('OPENAI_API_BASE_URL'))
    try:
        async for chunk in await aclient.chat.completions.create(model=openai_model,
                                                                 messages=messages,
                                                                 max_tokens=1600,
                                                                 stream=True):
            content = chunk.choices[0].delta.content
            if content:
                yield content

    except OpenAIError as e:
        traceback.print_exc()
        yield f"oaiEXCEPTION {str(e)}"
    except Exception as e:
        yield f"EXCEPTION {str(e)}"


def create_conversation_starter(user_prompt: str) -> List[Dict[str, str]]:
    """
    Given a user prompt, create a conversation history with the following format:
    `[ { "role": "user", "content": user_prompt } ]`

    :param user_prompt: a user prompt string
    :return: a conversation history
    """
    return [{"role": "user", "content": user_prompt}]


@st.cache_data(show_spinner=True,experimental_allow_widgets=True)
def embed_documents_service(documents: List[str]) -> List[List[float]]:
    """
    Embeds documents using an embeddings model and caches the results.
    Returns a list of document embeddings.

    :param documents: a list of document strings
    :return: a list of document embeddings
    """
    client = OpenAI(
        base_url=os.getenv('OPENAI_API_BASE_URL'),
        api_key=os.getenv('OPENAI_API_KEY')
    )
    EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI's best embeddings as of Feb 2024
    BATCH_SIZE = 20  # you can submit up to 2048 embedding inputs per request
    embeddings = []

    for batch_start in range(0, len(documents), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = documents[batch_start:batch_end]
        response = client.embeddings.create(
            model=EMBEDDING_MODEL, input=batch, encoding_format="float")

        for i, be in enumerate(response.data):
            assert i == be.index  # double check embeddings are in same order as input
        batch_embeddings = [e.embedding for e in response.data]
        embeddings.extend(batch_embeddings)

    return embeddings
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import pathlib
import os
import tempfile
import subprocess
import json
# from PyPDF2 import PdfReader
import asyncio

# Assuming the correct import paths based on your provided structure
from services.llm import converse, create_conversation_starter, embed_documents_service
from helpers.util import run_conversation, run_prompt
from services.prompts import (
    general_ducky_code_starter_prompt,
    review_prompt,
    modify_code_prompt,
    debug_prompt,
    system_learning_prompt,
    learning_prompt
)
from sklearn.neighbors import NearestNeighbors

from openai import OpenAI


# get model from env variable
@st.cache_data(show_spinner=True)
def converse2(prompt, messages=None, model=os.getenv('OPENAI_API_MODEL'),
              max_tokens=4000,
              temperature=0,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0):
    client = OpenAI(
        base_url=os.getenv('OPENAI_API_BASE_URL'),
        api_key=os.getenv('OPENAI_API_KEY')
    )

    # Initialize messages if not provided
    if messages is None:
        messages = []

    # Add the user's message to the conversation history
    messages.append({"role": "user", "content": prompt})

    # Call the OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    ).choices[0].message.content

    # Return only the assistant's response text
    return response


prompt_template = """
Answer the following question using the context provided:
%Question: 
```
{question}
``` 
%Context: 
```
{context}
```
"""


async def interact_with_llm_async(prompt):
    messages = create_conversation_starter(prompt)
    response = await run_conversation(messages, st.empty())
    return response[-1]["content"]


def interact_with_llm(prompt):
    return asyncio.run(interact_with_llm_async(prompt))


def chunk_prompt(prompt, chunk_size=500, overlap=50):
    """
    Given a prompt, chunk the prompt into smaller segments.
    """
    return [prompt[i:i + chunk_size] for i in range(0, len(prompt), chunk_size - overlap)]


def embed_documents(documents):
    """
    Placeholder function to embed documents using an embeddings model.
    Returns a list of document embeddings.
    """
    # use openais text-embedding-3-small to embed the documents
    return embed_documents_service(documents)


def find_nearest_chunks(query_embedding, embeddings, documents, n=1):
    """
    Finds and returns the nearest document chunks to the query embedding.
    """
    nbrs = NearestNeighbors(
        n_neighbors=n, algorithm='ball_tree').fit(embeddings)
    distances, indices = nbrs.kneighbors(query_embedding)
    return [(documents[idx], distances[0][i]) for i, idx in enumerate(indices[0])]


# def tips_from_the_pragmatic_programmer():
#     st.header("Tips from The Pragmatic Programmer")

#     pdf_path = pathlib.Path("data", "ThePragmaticProgrammer.pdf")
#     pdf = PdfReader(pdf_path)
#     pragmatic_programmer_text = " ".join(
#         page.extract_text() for page in pdf.pages if page.extract_text())

#     # Process the text for better readability and to avoid issues with special characters
#     pragmatic_programmer_text = pragmatic_programmer_text.replace(
#         "\n", " ").replace("\r", " ").replace("\t", " ").replace("  ", " ")

#     # Here, you'd chunk the text based on the token limit and overlap as explained in the chunking information.
#     # For simplicity, let's assume we have a function 'chunk_text' that does this.
#     # Adjust 'chunk_size' and 'overlap' as needed.
#     documents = chunk_prompt(pragmatic_programmer_text,
#                              chunk_size=500, overlap=50)

#     # Embed the chunks for semantic search
#     embeddings = embed_documents(documents)

#     # User query
#     user_query = st.text_input(
#         "Ask a question about 'The Pragmatic Programmer':")
#     # Initialize a key for this specific query in the session state
#     session_key = f"response_{user_query}"

#     if user_query:

#         # OpenAI's best embeddings as of Feb 2024
#         EMBEDDING_MODEL = "text-embedding-3-small"
#         client = OpenAI(
#             # This is the default and can be omitted
#             base_url=os.getenv('OPENAI_API_BASE_URL'),
#             api_key=os.getenv('OPENAI_API_KEY')
#         )

#         response = client.embeddings.create(model=EMBEDDING_MODEL, input=[
#                                             user_query], encoding_format="float")
#         query_embedding = np.array(response.data[0].embedding).reshape(1, -1)
#         nearest_chunks = find_nearest_chunks(
#             query_embedding, embeddings, documents, n=2)  # Find the top 2 nearest chunks

#         for chunk, distance in nearest_chunks:
#             # use converse2 to get the response by giving the chunk as prompt and also using
#             prompt = prompt_template.format(question=user_query, context=chunk)
#             response = converse2(prompt)
#             # Store the response in session state
#             st.session_state[session_key] = response

#         # Display the response stored in session state
#         st.write(st.session_state[session_key])


# Initialize the page configuration
st.set_page_config(page_title="Generate Code", page_icon="💻", layout="wide")

# Sidebar for feature navigation
st.sidebar.title("Features")
feature = st.sidebar.radio("Select a feature", [
                           "Code Review", "Debug Code", "Modify Code", "Tips from The Pragmatic Programmer"])

if feature == "Code Review":
    st.header("Code Review")
    code = st.text_area("Enter your code here for review", height=300)
    if st.button("Review Code"):
        review_info = interact_with_llm(review_prompt(code))
        # review_info contains a duplicate response, so we will remove the first response
        review_info = review_info.split("\n", 1)[0]
        st.write(review_info)

elif feature == "Debug Code":
    st.header("Debug Code")
    code = st.text_area("Enter your code here", height=250)
    error_string = st.text_input("Enter the error string (optional)")
    if st.button("Debug Code"):
        debug_info = interact_with_llm(debug_prompt(code, error_string))
        debug_info = debug_info.split("\n", 1)[0]
        st.write(debug_info)

elif feature == "Modify Code":
    # Ensure the session state is initialized for storing conversation and code modification requests
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    st.header("Ducky Code Modifier")
    st.write(
        "Let's modify your code together! Tell me what you need, and I'll help you step by step.")

    # Ensure the session state is initialized
    if "messages" not in st.session_state:
        initial_messages = [{"role": "system",
                            "content": general_ducky_code_starter_prompt()}]
        st.session_state.messages = initial_messages

    # Print all messages in the session state
    for message in [m for m in st.session_state.messages if m["role"] != "system"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat with the LLM, and update the messages list with the response.
    # Handles the chat UI and partial responses along the way.

    async def chat(messages):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            messages = await run_conversation(messages, message_placeholder)
            st.session_state.messages = messages
        return messages

    # React to the user prompt
    if prompt := st.chat_input("Modify your code here..."):
        st.session_state.messages.append(
            {"role": "user", "content": modify_code_prompt(prompt)})
        asyncio.run(chat(st.session_state.messages))


# elif feature == "Tips from The Pragmatic Programmer":
    # tips_from_the_pragmatic_programmer()

# Reset functionality
if st.sidebar.button("Reset"):
    st.experimental_rerun()

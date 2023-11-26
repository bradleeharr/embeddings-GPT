import openai
import numpy as np
import pandas as pd
import tiktoken
import time

from get_element_data import load_config
from openai.embeddings_utils import cosine_similarity, get_embedding
from flask_socketio import emit

config = load_config("credentials.json")
openai.api_key = config["openai-api-key"]

# read the datafile
datafile_path = "processed/embeddings.csv"
df = pd.read_csv(datafile_path)
df["embeddings"] = df.embeddings.apply(eval).apply(np.array)
print("Loaded GitHub Embeddings")


def count_tokens(text):
    """Count the number of tokens in a text string using OpenAI's tokenizer."""
    tokenizer = tiktoken.get_encoding("cl100k_base")
    print(text)
    print(len(tokenizer.encode(text)))
    return len(tokenizer.encode(text))


def manage_context_length(messages):
    """Ensure the total tokens in the context (including the new message) don't exceed 4000."""
    total_tokens = sum(count_tokens(msg["content"]) for msg in messages)
    print("Total Tokens:", total_tokens)
    # While we are over the token limit, remove the earliest messages
    while total_tokens > 8000:
        removed_message = messages.pop(0)
        print("Removed message: ", removed_message)
        total_tokens -= count_tokens(removed_message["content"])
        print("Total tokens: ", total_tokens)

    return messages


def search_justice(df, search, threshold=0.8):
    """ Search through the rows of data using embeddings """
    print("Search: ", search)
    row_embedding = get_embedding(
        search,
        engine="text-embedding-ada-002"
    )
    df["similarity"] = df.embeddings.apply(lambda x: cosine_similarity(x, row_embedding))
    new = df.sort_values("similarity", ascending=False)
    highScores = new[new['similarity'] >= threshold]
    return highScores


messages = [{"role": "system", "content": """
You are signal processing expert. 
Check my understanding in any further questions that I ask:
In answering, please write code with the goal of verifying that the correct answer has been given.
As you go think aloud step by step. Plot the time and frequency domain of ALL signals.
Now take a deep breath and begin. This is very important for my career, so do your best please. 
Surround code blocks in HTML formatting to automatically display them.
"""}]


def handle_message(text):
    """handle search and chat when a new message is input by a user"""
    results = search_justice(df, text)
    print(results.head(10))
    if results.empty:
        prompt = text
    else:
        prompt = "Look through this information to answer the question: " + results[['text']].head(10).to_string(
            header=False,
            index=False).strip() + "(if it doesn't make sense you can disregard it. If you use it, please repeat the " \
                                   "information listed or give the examples). The question is: " + text
    new_content = "The question is: " + text
    messages.append({"role": "user", "content": new_content})

    response_stream = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=manage_context_length(messages),
        stream=True
    )
    stopFlag = False
    for chunk in response_stream:
        # print(chunk)

        if chunk.choices[0].finish_reason is None and stopFlag is False:
            emit('response', chunk.choices[0].delta.content)
        else:
            emit('stop_reason', chunk.choices[0].finish_reason)
            stopFlag = True


if __name__ == "__main__":
    text = input('\r\n User: ')
    handle_message(text)

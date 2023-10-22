import openai
import numpy as np
import pandas as pd
import time

from get_element_data import load_config
from openai.embeddings_utils import cosine_similarity, get_embedding
from flask_socketio import emit

config = load_config("credentials.json")
openai.api_key = config["openai-api-key"]

messages = [
    {"role": "system", "content": "You're a terse GNU Radio assistant..."}]
datafile_path = "processed/embeddings.csv"

# read the datafile
df = pd.read_csv(datafile_path)
df["embeddings"] = df.embeddings.apply(eval).apply(np.array)
print("Loaded GitHub Embeddings")


def count_tokens(text):
    """Count the number of tokens in a text string using OpenAI's tokenizer."""
    return len(openai.tokenize(text))


def manage_context_length(messages, new_message_content):
    """Ensure the total tokens in the context (including the new message) don't exceed 4000."""
    total_tokens = sum(count_tokens(msg["content"]) for msg in messages)
    total_tokens += count_tokens(new_message_content)

    # While we are over the token limit, remove the earliest messages
    while total_tokens > 4000:
        removed_message = messages.pop(0)
        total_tokens -= count_tokens(removed_message["content"])

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


def handle_message(text):
    results = search_justice(df, text)
    print(results.head(10))


if results.empty:
    prompt = text
else:
    prompt = "Look through this information to answer the question: " + results[['text']].head(10).to_string(
        header=False,
        index=False).strip() + "(if it doesn't make sense you can disregard it. If you use it, please repeat the " \
                               "information listed ). The question is: " + text
new_content = "The question is: " + text
messages = manage_context_length(messages, new_content)
messages.append({"role": "user", "content": new_content})

response_stream = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    stream=True
)
stopFlag = False
for chunk in response_stream:
    print(chunk)

    if chunk.choices[0].finish_reason is None and stopFlag is False:
        emit('response', chunk.choices[0].delta.content)
        # TODO: Figure out how to add previous context into message messages.append(chunk.choices[0].delta)
    else:
        emit('stop_reason', chunk.choices[0].finish_reason)
        stopFlag = True

if __name__ == "__main__":
    text = input('\r\n User: ')
    handle_message(text)

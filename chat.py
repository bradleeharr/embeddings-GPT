import openai
import numpy as np
import pandas as pd
from get_element_data import load_config
from openai.embeddings_utils import cosine_similarity, get_embedding

config = load_config("credentials.json")
openai.api_key = config["openai-api-key"]

messagesOb = [
    {"role": "system", "content": "You're a GNU Radio assistant..."}]
datafile_path = "processed/embeddings.csv"

# read the datafile
df = pd.read_csv(datafile_path)
df["embeddings"] = df.embeddings.apply(eval).apply(np.array)
print("Loaded GitHub Embeddings")


def search_justice(df, search, threshold=0.8):
    """ Search through the rows of data using embeddings """
    print("Search: ", search)
    row_embedding = get_embedding(
        search,
        engine="text-embedding-ada-002"
    )
    df["similarity"] = df.embeddings.apply(lambda x: cosine_similarity(x, row_embedding))
    new = df.sort_values("similarity", ascending=False)
    # only return the rows with a higher than threshold
    highScores = new[new['similarity'] >= threshold]
    return highScores


def handleMentions():
    text = input('\r\n User: ')

    results = search_justice(df, text)
    print(results.head(5))

    if results.empty:
        prompt = text
    else:
        prompt = "Look through this information to answer the question: " + results[['text']].head(5).to_string(
            header=False,
            index=False).strip() + "(if it doesn't make sense you can disregard it). The question is: " + text
    messagesOb.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messagesOb,
    )
    print(response)
    messagesOb.append(response)


handleMentions()

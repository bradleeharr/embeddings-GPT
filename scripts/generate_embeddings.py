from data_to_csv import *
import tiktoken
import openai
from get_element_data import load_config

config = load_config("credentials.json")
openai.api_key = config["openai-api-key"]

element_data_fp = "element_data"
github_data_fp = "github_data"

max_tokens = 500


def split_into_many(text, tokenizer, max_tokens=max_tokens):
    sentences = text.split('. ')
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    for sentence, token in zip(sentences, n_tokens):
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0
        if token > max_tokens:
            continue

        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks


def main():
    if not os.path.exists(element_data_fp):
        os.makedirs(element_data_fp)
        element_to_csv(element_data_fp)
    if not os.path.exists(github_data_fp):
        os.makedirs(github_data_fp)
        github_to_csv(github_data_fp)
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv('processed/github_repo_contents.csv', index_col=0)
    df = df.reset_index()
    print(df.head())

    df.columns = ['title', 'text']

    print(df.text)
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    shortened = []

    for row in df.iterrows():

        # If the text is None, go to the next row
        if row[1]['text'] is None:
            continue
        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'], tokenizer)
        else:
            shortened.append(row[1]['text'])

    df = pd.DataFrame(shortened, columns=['text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    print("Generating Embeddings")
    df['embeddings'] = df.text.apply(
        lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])

    df.to_csv('processed/embeddings.csv')
    df.head()


if __name__ == "__main__":
    main()

from github import Github
import os

# Authenticate with GitHub (replace with your token)
g = Github("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")


def clone_gnuradio_repo():
    repo_url = "https://github.com/gnuradio/gnuradio.git"
    dest_dir = "github_data"

    if not os.path.exists(dest_dir):
        os.system(f"git clone {repo_url} {dest_dir}")

def convert_to_openai_embeddings(text):
    # Use the OpenAI embeddings API here
    return text

# Replace 'openai' with the user or organization of interest
for repo in g.get_user('openai').get_repos():
    repo_name = repo.full_name
    dest_dir = f"./github_data/{repo_name}"
    clone_gnuradio_repo();

# Walk through the downloaded data and convert to embeddings
for root, dirs, files in os.walk("./github_data"):
    for file in files:
        with open(os.path.join(root, file), 'r', errors='replace') as f:
            data = f.read()
            embedding = convert_to_openai_embeddings(data)
            # Store the embedding or use it as needed


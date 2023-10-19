from github import Github
import os

# Authenticate with GitHub (replace with your token)
g = Github("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")


def clone_gnuradio_repo():
    repo_url = "https://github.com/gnuradio/gnuradio.git"
    dest_dir = "github_data"

    if not os.path.exists(dest_dir):
        os.system(f"git clone {repo_url} {dest_dir}")


clone_gnuradio_repo();

from github import Github
import os

# Authenticate with GitHub (replace with your token)
g = Github("GITHUB_ACCESS_TOKEN")


def clone_gnuradio_repo():
    repo_url = "https://github.com/gnuradio/gnuradio.git"
    dest_dir = "github_data"

    if not os.path.exists(dest_dir):
        os.system(f"git clone {repo_url} {dest_dir}")


clone_gnuradio_repo();

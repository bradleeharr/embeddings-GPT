from github import Github
import os

# Authenticate with GitHub (replace with your token)
g = Github("GITHUB_ACCESS_TOKEN")


def clone_gnuradio_repo(repo_url):
    dest_dir = "github_data"

    if not os.path.exists(dest_dir):
        os.system(f"git clone {repo_url} {dest_dir}")


repo_url = "https://github.com/REPONAME/REPONAME.git"
clone_gnuradio_repo(repo_url);

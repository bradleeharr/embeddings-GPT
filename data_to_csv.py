import pandas as pd
import os
import json


def remove_newlines(series):
    series = series.replace('\n', ' ')
    series = series.replace('\\n', ' ')
    series = series.replace('  ', ' ')
    series = series.replace('  ', ' ')
    return series


def element_to_csv(element_path):
    all_messages = []
    # Loop through each JSON file in the folder
    for filename in os.listdir(element_path):
        if filename.endswith(".json"):
            with open(os.path.join(element_path, filename), 'r') as f:
                data = json.load(f)

            # Extract the messages
            messages = [message['content']['body'] for message in data if
                        'content' in message and 'body' in message['content']]
            all_messages.extend(messages)

    # Convert list of messages to DataFrame
    df = pd.DataFrame(all_messages, columns=['message'])

    # Save the DataFrame to CSV
    df.to_csv('processed/element_data_messages.csv', index=False)


def github_to_csv(repo_path):
    all_files_content = []
    # Recursively list all files in the GitHub Repo
    for subdir, _, files in os.walk(repo_path):
        for file in files:
            filepath = os.path.join(subdir, file)

            # Read each file's content
            try:
                with open(filepath, 'r', encoding="UTF-8") as f:
                    content = f.read()
                all_files_content.append((filepath, remove_newlines(content)))
            except Exception as e:
                print(f"Could not read file {filepath} due to {e}")

    # Convert list of file contents to DataFrame
    df_repo = pd.DataFrame(all_files_content, columns=['fname', 'text'])
    df_repo['text'] = df_repo.fname + ". " + remove_newlines(df_repo.text)
    # Save the DataFrame to CSV
    df_repo.to_csv('processed/github_repo_contents.csv', index=False)

import pandas as pd
import os
import json

element_path = 'element_data'
github_path = 'github_data'
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
df.to_csv('element_data_messages.csv', index=False)

repo_path = 'path_to_cloned_repo'  # Replace with the path to your cloned repo

all_files_content = []

# Recursively list all files in the GitHub Repo
for subdir, _, files in os.walk(repo_path):
    for file in files:
        filepath = os.path.join(subdir, file)

        # Read each file's content
        try:
            with open(filepath, 'r', encoding="UTF-8") as f:
                content = f.read()
            all_files_content.append((filepath, content))
        except Exception as e:
            print(f"Could not read file {filepath} due to {e}")

# Convert list of file contents to DataFrame
df_repo = pd.DataFrame(all_files_content, columns=['filename', 'content'])

# Save the DataFrame to CSV
df_repo.to_csv('github_repo_contents.csv', index=False)

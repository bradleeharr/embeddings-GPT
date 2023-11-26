# GPT Documentation Embeddings

This project focuses on processing another project's associated GitHub source code to generate embeddings. These embeddings aim to allow efficient and relevant searches, aiding in providing context for chat-based interactions.

## Repository Contents

- `.gitignore`: Git ignore file.
- `README.md`: This file.
- `chat.py`: Script to interact with the chat interface.
- `data_to_csv.py`: Script to convert scraped data to CSV format.
- `generate_embeddings.py`: Script to process the data and create embeddings.
- `get_element_data.py`: Script to scrape and process documentation.
- `get_github_data.py`: Script to scrape and process GitHub source code.

## Overview

1. **Data Collection**: 
   - The project first clones the chosen GitHub and stores it in a structured manner.
   
2. **Data Processing**:
   - Data is cleaned and converted to a CSV format.
   - Text from the documentation and code is tokenized.
   - Large chunks of text are split into smaller ones to ensure each chunk has a manageable number of tokens.
   
3. **Embeddings Generation**:
   - Using OpenAI's API, embeddings are generated for the text chunks.
   - These embeddings allow for cosine similarity-based searches to find relevant parts of the documentation or code.

4. **Chat Interface**:
   - A chat interface lets users input queries.
   - The system searches the embeddings for relevant documentation or code snippets and presents them as context to the OpenAI GPT model.
   - GPT then generates a response based on the provided context.

## Requirements

- OpenAI Python Client
- Pandas
- Tiktoken
- Matplotlib
- Numpy

## Credentials Setup 

Your credentials should be stored in a `credentials.json` file in the root directory of the project in the following format:

```json
{
  "openai-api-key": "YOUR_API_KEY"
}
```

Make sure to replace `YOUR_API_KEY` with your openai api key.

## How to Run

1. **Setup**:
   - Install the required libraries:
     ```bash
     pip install openai pandas tiktoken matplotlib numpy
     ```

2. **Data Collection**:
   - Replace "GITHUB_ACCESS_TOKEN" with your GitHub access token and run `get_github_data.py` to clone the GitHub repository
   - Run `data_to_csv.py` to convert the text in the repository to csv data.
   
3. **Embeddings Generation**:
   - Run `generate_embeddings.py` to process the data and create embeddings.
   
4. **Start the Chat Interface**:
   - Run `chat.py` to start the chat and read the embeddings to interact with the system.
   - Input your queries and receive responses based on the context from the documentation and code.

## Notes

- The current implementation pulls context from the GitHub source code. However, the model has trouble understanding raw source code. Data in a Q&A format or structured documentation from either mailing lists, element server, or Wiki would be more useful and lead to better responses.

---

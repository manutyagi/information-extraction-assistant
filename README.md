# 🏙️ **Information Extraction Assistant (RAG Research Tool)**

A Retrieval-Augmented Generation (RAG) application that extracts accurate numerical and factual information from URLs (such as news articles) and answers contextual user questions backed by citations.

### Features

- Scrapes news articles using a custom browser-spoofing loader
- Splits text into overlapping semantic chunks
- Embeds chunks using MiniLM sentence transformers
- Stores embeddings in a persistent Chroma vector store
- Retrieves top-k relevant chunks
- Uses Groq’s Llama-3.3-70B model for answer generation
- Provides accurate numerical extraction
- Returns source URL citations

### How it works?
- Indexing phase
	- User submits URLs
	- Scraper fetches full article
	- Content is chunked (800 chars, 150 overlap)
	- Embeddings stored in Chroma
- Query Phase
	- User asks a question
	- Retriever fetches relevant chunks
	- LLM answers using a strict prompt:
		- Only use provided context
		- Extract numbers verbatim
		- No hallucination fallback
- Sources
	- System returns citation URLs for transparency


### Tech Stack
- Streamlit (UI)
- LangChain (retrieval + chains)
- ChromaDB (vector store)
- Newspaper3k (article extraction)
- HuggingFace Embeddings
- Groq Llama-3.3-70B (LLM inference)


### Set-up

1. Run the following command to install all dependencies. 

    ```bash
    pip install -r requirements.txt
    ```

2. Create a .env file with your GROQ credentials as follows:
    ```text
    GROQ_MODEL=MODEL_NAME_HERE
    GROQ_API_KEY=GROQ_API_KEY_HERE
    ```

3. Run the streamlit app by running the following command.

    ```bash
    streamlit run main.py
    ```


### Usage/Examples

The web app will open in your browser after the set-up is complete.

- In the input box, you can input URLs directly.

- Initiate the data loading and processing by clicking "Process URLs."

- Observe the system as it performs text splitting, generates embedding vectors using HuggingFace's Embedding Model.

- The embeddings will be stored in ChromaDB.

- One can now ask a question and get the answer based on those news articles

- For example, use the following news articles
  - https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html
  - https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html
  - https://www.cnbc.com/2024/12/17/wall-street-sees-upside-in-2025-for-these-dividend-paying-real-estate-stocks.html

- Example Query
	“What was the 30-year fixed mortgage rate for the week ending Dec 19?”
	Output: 6.72 %
	Source: https://www.cnbc.com/...


</br>

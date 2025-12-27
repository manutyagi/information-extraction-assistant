from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
#from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains import RetrievalQA
#from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from langchain.schema import Document
from browser_loader import fetch_page_html
from langchain.prompts import PromptTemplate



load_dotenv()

# Constants
CHUNK_SIZE = 1000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
#COLLECTION_NAME = "real_estate"
COLLECTION_NAME = "generic_info_store"

llm = None
vector_store = None


def initialize_components():
    global llm, vector_store

    if llm is None:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=500)

    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR)
        )


def process_urls(urls):
    """
    This function scraps data from a url and stores it in a vector db
    :param urls: input urls
    :return:
    """
    yield "Initializing Components"
    initialize_components()

    yield "Resetting vector store...✅"
    vector_store.reset_collection()

    yield "Loading data...✅"
    #loader = UnstructuredURLLoader(urls=urls)
    #data = loader.load()
    data = []
    for url in urls:
        html = fetch_page_html(url)
        data.append(Document(page_content=html, metadata={"source": url}))
        print("SCRAPED LENGTH:", len(html), "URL:", url)

    yield "Splitting text into chunks...✅"
    # text_splitter = RecursiveCharacterTextSplitter(
    #     separators=["\n\n", "\n", ".", " "],
    #     chunk_size=CHUNK_SIZE
    # )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", "? ", "! "]
    )
    docs = text_splitter.split_documents(data)

    yield "Add chunks to vector database...✅"
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)

    yield "Done adding docs to vector database...✅"

# def generate_answer(query):
#     if not vector_store:
#         raise RuntimeError("Vector database is not initialized ")
#
#     #chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vector_store.as_retriever())
#     retriever = vector_store.as_retriever(
#         search_kwargs={"k": 6}  # increase recall
#     )
#
#     chain = RetrievalQAWithSourcesChain.from_llm(
#         llm=llm,
#         retriever=retriever,
#     )
#
#     result = chain.invoke({"question": query}, return_only_outputs=True)
#     sources = result.get("sources", "")
#
#     return result['answer'], sources


def generate_answer(query):
    if not vector_store:
        raise RuntimeError("Vector database is not initialized ")

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 6}  # increase recall
    )

    # Custom prompt to avoid default "I don't know"
    template = """
Use only the provided context to answer the question.
If context partially answers, give a partial answer.
Do not say "I don't know" unless the context is completely empty.

Context:
{context}

Question:
{question}

Extract numerical values exactly as written in the article.
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    chain = RetrievalQA.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        prompt=prompt
    )
    # chain = RetrievalQAWithSourcesChain.from_llm(
    #     llm=llm,
    #     retriever=retriever,
    #     prompt=prompt
    # )

    # result = chain.invoke({"question": query}, return_only_outputs=True)
    # sources = result.get("sources", "")
    # return result['answer'], sources
    out = chain({"query": query})

    answer = out["result"]
    source_docs = out["source_documents"]

    sources = "\n".join([doc.metadata.get("source", "") for doc in source_docs])

    return answer, sources


if __name__ == "__main__":
    urls = [
        "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
        "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html"
    ]

    process_urls(urls)
    answer, sources = generate_answer("Tell me what was the 30 year fixed mortagate rate along with the date?")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")
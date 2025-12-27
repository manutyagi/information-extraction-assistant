import pysqlite3
import sys
sys.modules['sqlite3'] = pysqlite3

import streamlit as st
from rag import process_urls, generate_answer

st.title("Information Extraction Assistant: Ask anything from web links")

# -----------------------------
# SESSION STATE FOR URL STORAGE
# -----------------------------
if "url_list" not in st.session_state:
    st.session_state.url_list = []

# -----------------------------
# ADD URL INPUT
# -----------------------------
st.sidebar.subheader("Add URLs (max 10)")

new_url = st.sidebar.text_input("Enter a URL")

add_button = st.sidebar.button("Add URL")

if add_button:
    if len(st.session_state.url_list) >= 10:
        st.sidebar.error("You can add a maximum of 10 URLs.")
    elif new_url.strip() == "":
        st.sidebar.error("Please enter a valid URL.")
    else:
        st.session_state.url_list.append(new_url.strip())
        st.sidebar.success("URL added successfully.")

# -----------------------------
# SHOW CURRENT URL LIST
# -----------------------------
st.sidebar.write("### Added URLs:")
if len(st.session_state.url_list) == 0:
    st.sidebar.info("No URLs added yet.")
else:
    for i, url in enumerate(st.session_state.url_list, start=1):
        st.sidebar.write(f"{i}. {url}")

# CLEAR ALL BUTTON
clear_button = st.sidebar.button("Clear All URLs")
if clear_button:
    st.session_state.url_list = []
    st.sidebar.success("URL list cleared.")

# -----------------------------
# PROCESS URLS
# -----------------------------
placeholder = st.empty()

process_url_button = st.sidebar.button("Click to process URLs before asking any question")

if process_url_button:
    if len(st.session_state.url_list) == 0:
        placeholder.text("You must provide at least one valid URL.")
    else:
        for status in process_urls(st.session_state.url_list):
            placeholder.text(status)

# -----------------------------
# QUESTION INPUT
# -----------------------------
query = placeholder.text_input("Write the question you want to ask about the processed URLs")

if query:
    try:
        answer, sources = generate_answer(query)

        st.header("Answer:")
        st.write(answer)

        if sources:
            st.subheader("Sources:")
            for source in sources.split("\n"):
                if source.strip():
                    st.write(f"- {source}")

    except RuntimeError:
        placeholder.text("You must process URLs first.")





# import pysqlite3
# import sys
# sys.modules['sqlite3'] = pysqlite3
#
# import streamlit as st
# from rag import process_urls, generate_answer
#
# #st.title("Real Estate Research Tool")
# st.title("Information Extraction Assistant: Ask anything from web links")
#
# #url1 = st.sidebar.text_input("URL 1")
# #url2 = st.sidebar.text_input("URL 2")
# #url3 = st.sidebar.text_input("URL 3")
# st.sidebar.subheader("Enter URLs")
# url_list_text = st.sidebar.text_area("Paste comma-separated links")
# urls = [u.strip() for u in url_list_text.split("\n") if u.strip()]
#
# placeholder = st.empty()
#
# process_url_button = st.sidebar.button("Process URLs before asking any question")
# if process_url_button:
#     #urls = [url for url in (url1, url2, url3) if url!='']
#     if len(urls) == 0:
#         placeholder.text("You must provide at least one valid url")
#     else:
#         for status in process_urls(urls):
#             placeholder.text(status)
#
# query = placeholder.text_input("Write the question you want to ask about the pasted URLs")
# if query:
#     try:
#         answer, sources = generate_answer(query)
#         st.header("Answer:")
#         st.write(answer)
#
#         if sources:
#             st.subheader("Sources:")
#             for source in sources.split(","):
#                 st.write(source)
#     except RuntimeError as e:
#         placeholder.text("You must process urls first")

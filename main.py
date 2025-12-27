__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from rag import process_urls, generate_answer

#st.title("Real Estate Research Tool")
st.title("Information Extraction Assistant")

#url1 = st.sidebar.text_input("URL 1")
#url2 = st.sidebar.text_input("URL 2")
#url3 = st.sidebar.text_input("URL 3")
st.sidebar.subheader("Enter URLs")
url_list_text = st.sidebar.text_area("Paste one URL per line")
urls = [u.strip() for u in url_list_text.split("\n") if u.strip()]

placeholder = st.empty()

process_url_button = st.sidebar.button("Process URLs")
if process_url_button:
    #urls = [url for url in (url1, url2, url3) if url!='']
    if len(urls) == 0:
        placeholder.text("You must provide at least one valid url")
    else:
        for status in process_urls(urls):
            placeholder.text(status)

query = placeholder.text_input("Question")
if query:
    try:
        answer, sources = generate_answer(query)
        st.header("Answer:")
        st.write(answer)

        if sources:
            st.subheader("Sources:")
            for source in sources.split("\n"):
                st.write(source)
    except RuntimeError as e:
        placeholder.text("You must process urls first")

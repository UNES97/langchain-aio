import os, tempfile
import streamlit as st
from langchain.llms.openai import OpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader

openai_api_key = st.session_state.openai_api_key

st.subheader('Document Summary')
source_doc = st.file_uploader("Upload Source Document", type="pdf")

if st.button("Summarize"):
    if not openai_api_key:
        st.error("Provide the Missing API keys in Settings.")
    elif not source_doc:
        st.error("Provide the Document Source.")
    else:
        try:
            with st.spinner('Please wait...'):
              with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                  tmp_file.write(source_doc.read())
              loader = PyPDFLoader(tmp_file.name)
              pages = loader.load_and_split()
              os.remove(tmp_file.name)

              embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key)
              vectordb = Chroma.from_documents(pages, embeddings)

              llm=OpenAI(temperature=0, openai_api_key=openai_api_key)
              chain = load_summarize_chain(llm, chain_type="stuff")
              search = vectordb.similarity_search(" ")
              summary = chain.run(input_documents=search, question="Write a Summary within 150 Words.")

              st.success(summary)
        except Exception as e:
            st.exception(f"An error occurred: {e}")

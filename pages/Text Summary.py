import os, streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain

openai_api_key = st.session_state.openai_api_key

st.subheader('Text Summary')
source_text = st.text_area("Enter Source Text", height=200)

if st.button("Summarize"):
    if not openai_api_key:
        st.error("Please provide the missing API keys in Settings.")
    elif not source_text.strip():
        st.error("Please provide the source text.")
    else:
        try:
            with st.spinner('Please wait...'):
              text_splitter = CharacterTextSplitter()
              texts = text_splitter.split_text(source_text)

              docs = [Document(page_content=t) for t in texts[:3]]

              llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
              chain = load_summarize_chain(llm, chain_type="map_reduce")
              summary = chain.run(docs)

              st.success(summary)
        except Exception as e:
            st.exception(f"An error occurred: {e}")

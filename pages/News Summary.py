import streamlit as st, tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

openai_api_key = st.session_state.openai_api_key
serper_api_key = st.session_state.serper_api_key

st.subheader('News Summary')
num_results = st.number_input("Number of Search Results", min_value=3, max_value=10) 
search_query = st.text_input("Enter Search Query")
col1, col2 = st.columns(2)

if col1.button("Search"):
    if not openai_api_key or not serper_api_key:
        st.error("Please provide the missing API keys in Settings.")
    elif not search_query.strip():
        st.error("Please provide the search query.")
    else:
        try:
            with st.spinner("Please wait..."):
                search = GoogleSerperAPIWrapper(type="news", tbs="qdr:w1", serper_api_key=serper_api_key)
                result_dict = search.results(search_query)

                if not result_dict['news']:
                    st.error(f"No search results for: {search_query}.")
                else:
                    for i, item in zip(range(num_results), result_dict['news']):
                        st.success(f"Title: {item['title']}\n\nLink: {item['link']}\n\nSnippet: {item['snippet']}")
        except Exception as e:
            st.exception(f"Exception: {e}")

if col2.button("Search & Summarize"):
    if not openai_api_key or not serper_api_key:
        st.error("Provide the Missing API keys in Settings.")
    elif not search_query.strip():
        st.error("Provide the Search Query.")
    else:
        try:
            with st.spinner("Please wait..."):
                search = GoogleSerperAPIWrapper(type="news", tbs="qdr:w1", serper_api_key=serper_api_key)
                result_dict = search.results(search_query)

                if not result_dict['news']:
                    st.error(f"No Results for: {search_query}.")
                else:
                    for i, item in zip(range(num_results), result_dict['news']):
                        loader = UnstructuredURLLoader(urls=[item['link']], ssl_verify=False, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                        data = loader.load()
                
                        llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
                        prompt_template = """Write a Summary of the Following in 100-200 words:
                            
                            {text}
        
                        """
                        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
                        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                        summary = chain.run(data)
        
                        st.success(f"Title: {item['title']}\n\nLink: {item['link']}\n\nSummary: {summary}")
        except Exception as e:
            st.exception(f"Exception: {e}")

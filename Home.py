import streamlit as st

# Initialize session state variables
if 'openai_api_key' not in st.session_state:
	st.session_state.openai_api_key = ""

if 'serper_api_key' not in st.session_state:
	st.session_state.serper_api_key = ""

st.set_page_config(page_title="Home")

st.header("Welcome to Yato KAMI Utilities! 👋😊")

st.markdown(
    """
    **👈 Kindly Access the Access Credentials in the Configuration Panel, and Select a Functionality from the Sidebar to Begin.**

    ##### Web Search
    * A sample App for Web Search Queries using LangChain and Serper API.

    ##### URL Summary
    * A Sample App for Summarizing URL Content Using LangChain and OpenAI.

    ##### Text Summary
    * A Sample app for Summarizing Text Using LangChain and OpenAI.

    ##### Document Summary
    * A Sample App for Summarizing Documents using LangChain and Chroma.

    ##### News Summary
    * A Sample app for Google news Search and Summaries using LangChain and Serper API.
    """
)

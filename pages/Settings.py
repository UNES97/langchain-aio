import streamlit as st

st.subheader('Settings')

openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
st.caption("*Required for all apps.*")

serper_api_key = st.text_input("Serper API Key", value=st.session_state.serper_api_key, type="password")
st.caption("*Required for News and Search.*")

if st.button("Save"):
    if not openai_api_key.strip() or not serper_api_key.strip():
        st.error("Please Provide the Missing API keys.")
    else:
        st.session_state.openai_api_key = openai_api_key
        st.session_state.serper_api_key = serper_api_key

import validators, streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

openai_api_key = st.session_state.openai_api_key

st.subheader('URL Summary')
url = st.text_input("Enter Source URL")

if st.button("Summarize"):
    if not openai_api_key:
        st.error("Provide the Missing API keys in Settings.")
    elif not url:
        st.error("Provide the URL.")
    elif not validators.url(url):
        st.error("Enter a valid URL.")
    else:
        try:
            with st.spinner("Please wait..."):
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                data = loader.load()
                
                llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo', openai_api_key=openai_api_key)
                prompt_template = """Write a summary of the following in 250-300 words.
                    
                    {text}

                """
                prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                summary = chain.run(data)

                st.success(summary)
        except Exception as e:
            st.exception(f"Exception: {e}")

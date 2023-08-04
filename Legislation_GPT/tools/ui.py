from typing import List
import streamlit as st
#from langchain.docstore.document import Document
import openai
from streamlit.logger import get_logger
from typing import NoReturn

logger = get_logger(__name__)



def is_query_valid(query: str) -> bool:
    if not query:
        st.error("Please enter a question!")
        return False
    return True

@st.cache_data(show_spinner=False)
def is_open_ai_key_valid(openai_api_key) -> bool:
    if not openai_api_key:
        st.error("Please enter your OpenAI API key in the sidebar!")
        return False
    try:
        openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            api_key=openai_api_key,
        )
    except Exception as e:
        st.error(f"{e.__class__.__name__}: {e}")
        logger.error(f"{e.__class__.__name__}: {e}")
        return False
    return True

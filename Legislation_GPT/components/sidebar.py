
import streamlit as st

from dotenv import load_dotenv
import os
load_dotenv()

def sidebar():
    with (st.sidebar):
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
            "2. Enter the ammendment PDF document.\n"
            "3. Enter the name of the MP that you wish to investigate further.\n"
            )

        api_key_input = st.text_input(
            "Enter OpenAI API Key, then press ENTER.",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )

        st.session_state["OPENAI_API_KEY"] =  api_key_input.replace('\ufeff', '')

        st.markdown("---")


        st.markdown("# About")
        st.markdown(
            "LPT allows you to enquire about an MP  who contributed to a particular bill  "
            "and get his/her priorities. "
        )

        st.markdown("---")


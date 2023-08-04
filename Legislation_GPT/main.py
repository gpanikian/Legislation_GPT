import streamlit as st

import openai
import os

from Legislation_GPT.components.sidebar import sidebar

from Legislation_GPT.tools.ui import is_open_ai_key_valid

from Legislation_GPT.core.Query import set_member_name

st.set_page_config(page_title="Legislative Passage Toolkit", page_icon="📖", layout="wide")
st.header("📖Legislative Passage Toolkit")

current_directory = os.getcwd()
file_path = ''.join([current_directory, '/logo/logo.png'])
st.sidebar.image(file_path, width=100)

sidebar()
openai.api_key = st.session_state.get("OPENAI_API_KEY")


if not openai.api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )


if not is_open_ai_key_valid(openai.api_key):
    st.stop()

membernam = st.text_input(
            "name of the MP",
            type="default",
            placeholder="Enter the name of the MP that you would like further detail on",
            help="You can get the MP names from https://mps.gov.uk",
            value = ""
            )
if st.button("Search MP"):
    set_member_name(membernam)

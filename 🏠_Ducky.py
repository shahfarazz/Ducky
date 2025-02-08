import streamlit as st

import helpers.sidebar

st.set_page_config(
	page_title="Ducky",
	page_icon="🦆",
	layout="wide"
)

helpers.sidebar.show()

st.toast("Welcome to Ducky!", icon="🦆")

#updating the text to reflect ducky which is an AI powered coding assistant, rather than a finance assistant.

st.markdown("Welcome to Ducky, your AI-powered personal coding assistant!")
st.write("Ducky is designed to help you explore and learn about the world of coding. You can ask Ducky questions about coding, and Ducky will provide you with helpful responses. Ducky is also capable of running code, so you can experiment with different code snippets and see the results in real-time. Ducky is here to help you learn and grow as a coder, so don't be afraid to ask questions and try new things!")


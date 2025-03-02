import streamlit as st

# import readme
with open("README.md", "r", encoding="utf-8") as file:
    f = file.read()

st.markdown(f, unsafe_allow_html=True)

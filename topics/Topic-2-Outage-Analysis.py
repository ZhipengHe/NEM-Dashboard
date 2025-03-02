import os
import streamlit as st
import pandas as pd
import altair as alt
import warnings
import datetime
warnings.filterwarnings("ignore", message="Could not infer format, so each element will be parsed individually")


# st.set_page_config(
#     page_title="NEM Trade Price Analysis",
#     page_icon=":chart_with_upwards_trend:",
#     layout="wide",
#     menu_items={
#         'Get Help': None,
#         'Report a bug': None,
#         'About': "This is a web app to explore NEM trade price data."
#     }
#     )

st.title("Topic 2: Outage Analysis")


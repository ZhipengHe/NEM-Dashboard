import streamlit as st
import warnings


st.set_page_config(
    page_title="NEM Dashboard | A simple dashboard for Australia's National Electricity Market (NEM) data",
    page_icon=":rocket:",
    layout="wide",
    menu_items={
        'Get Help': "https://github.com/ZhipengHe/NEM-Dashboard",
        'Report a bug': "https://github.com/ZhipengHe/NEM-Dashboard/blob/main/CONTRIBUTING.md#reporting-bugs",
        'About': "A simple dashboard for Australia's National Electricity Market (NEM) data."
    }
    )


# import home page: home.py
home = st.Page("home.py", title="Home", icon="🏠", default=True)
about = st.Page("about.py", title="About", icon="📖")

# Import the topics as pages from folder `./topics`
topic1 = st.Page("topics/Topic-1-Price-Anomaly-Detection.py", title="Topic 1: Price Anomaly Detection", icon="📈")
topic2 = st.Page("topics/Topic-2-Outage-Analysis.py", title="Topic 2: Outage Analysis", icon="🚨")
topic3 = st.Page("topics/Topic-3-Renewable-Integration.py", title="Topic 3: Renewable Integration", icon="♻️")
topic4 = st.Page("topics/Topic-4-Infrastructure-Analysis.py", title="Topic 4: Infrastructure Analysis", icon="🗼")

# guide for using aemo dataset
how_to_download = st.Page("data/NEMWEB-Data-Download-Guide.py", title="Download Data from NEMWeb", icon="📥")

# Create the navigation bar

pg = st.navigation(
    {
        "Home": [home],
        "Topic": [topic1, topic2, topic3, topic4],
        "Guide": [how_to_download],
        "About": [about]
    }
)

pg.run()
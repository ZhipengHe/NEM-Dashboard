import streamlit as st
import warnings
warnings.filterwarnings("ignore", message="Could not infer format, so each element will be parsed individually")


st.set_page_config(
    page_title="NEM Dashboard | A simple dashboard for Australia's National Electricity Market (NEM) data",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded",
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


# Create the navigation bar

pg = st.navigation(
    {
        "Home": [home],
        "Topics": [topic1, topic2, topic3, topic4],
        "About": [about]
    }
)

pg.run()
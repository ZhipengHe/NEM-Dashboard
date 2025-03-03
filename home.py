import streamlit as st

## Page Meta Information

st.warning('This dashboard is a work in progress. It is intended for educational purposes only. If you have any feedback \
           or suggestions, please feel free to open an issue on the [GitHub](https://github.com/ZhipengHe/NEM-Dashboard/issues).', icon="⚠️")

st.header("NEM Dashboard")

st.write('''
         *A simple dashboard for Australia's National Electricity Market (NEM) data*

         [![Docker Image Version](https://img.shields.io/docker/v/zhipenghe/nem-dashboard)](https://hub.docker.com/r/zhipenghe/nem-dashboard) \
         [![Docker Image Size](https://img.shields.io/docker/image-size/zhipenghe/nem-dashboard)](https://hub.docker.com/r/zhipenghe/nem-dashboard) \
         [![License](https://img.shields.io/github/license/ZhipengHe/NEM-Dashboard)](LICENSE)

         ***Author: Zhipeng He ([zhipeng.he@hdr.qut.edu.au](mailto:zhipeng.he@hdr.qut.edu.au))***
         
         ***Last Updated: March 04, 2025***
        ''')

# st.write("---")


## About Project

st.subheader("About Project")

st.markdown('''
        The **National Electricity Market (NEM)** is Australia's interconnected electricity system and wholesale market, \
         supplying power to the eastern and southern states. Covering over 5,000 kilometres, it is \
         one of the world's longest electricity networks, serving more than 10 million customers. The NEM operates as \
         a real-time spot market, where electricity is traded based on supply and demand fluctuations. \
         The **Australian Energy Market Operator (AEMO)** manages this market by coordinating electricity generation \
         and consumption every five minutes, ensuring system reliability and efficiency. 

        This dashboard aims to provide insights into the NEM's operation, focusing on four key topics: \
         ***price anomaly detection***, ***outage analysis***, ***renewable integration***, and ***infrastructure analysis***. \
         By analysing historical data, we can identify patterns and trends in the NEM, helping \
         to improve market transparency and decision-making.
        ''')



## Topics
st.subheader("Project Topics")

st.write("Each topic features a curated sample visualization designed for exploration and insight. \
         We trust that this dashboard will deepen your understanding of the NEM while sparking \
         innovative ideas for your own analysis.")

st.page_link("topics/Topic-1-Price-Anomaly-Detection.py", label="**Topic 1: Electricity Pricing Anomaly Detection and Analysis**", icon="📈") 
st.page_link("topics/Topic-2-Outage-Analysis.py", label="**Topic 2: Power Outage Root Cause and Impact Analysis**", icon="🚨")
st.page_link("topics/Topic-3-Renewable-Integration.py", label="**Topic 3: Renewable Integration Analysis and Impact Forecast**", icon="♻️")
st.page_link("topics/Topic-4-Infrastructure-Analysis.py", label="**Topic 4: Electricity Infrastructure Analysis and Performance Assessment**", icon="🗼")

## External Resources
st.subheader("External Resources")

st.write("For more information on the NEM and related topics, please refer to the following resources:")

st.markdown('''
            - [A Hackers Guide to AEMO & NEM Data](https://adgefficiency.com/hackers-aemo/): An awesome guide for \
                the newbies to the NEM data
            - [AEMO NEM Data Dashboard](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem): \
                The official data dashboard for the NEM data on the AEMO website
            - [OpenElectricity](https://openelectricity.org.au/): An open-source platform for exploring NEM data (Limited access to data,
                but great for learning the [documentation](https://docs.openelectricity.org.au/introduction))
            - [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS): A Python package for downloading and processing NEM \
                data. It also includes a packaged GUI executable file. ([Documentation](https://github.com/UNSW-CEEM/NEMOSIS/wiki))
            - [nem-data](https://github.com/ADGEfficiency/nem-data): A Python CLI to access NEM data
            - [nemwebR](https://github.com/aleemon/nemwebR): An R package for downloading and processing NEM data \
                (Limited functionality, last updated in 2022)
            ''')


## Acknowledgements
st.subheader("Acknowledgements")

st.write("The copyright of the NEM data, dashboard and related materials belongs to the Australian Energy Market Operator (AEMO). Use of the data is \
         subject to the [AEMO Copyright Permissions](https://www.aemo.com.au/privacy-and-legal-notices/copyright-permissions).")

import os
import streamlit as st
import pandas as pd
import altair as alt
import warnings
import datetime
warnings.filterwarnings("ignore", message="Could not infer format, so each element will be parsed individually")


st.header("Topic 3: Renewable Integration Analysis and Impact Forecast")

st.subheader("About Topic")

st.write("This topic explores the sustainability dimension of the NEM by examining the growing role of renewable energy source \
         in the market. It will analyse how the integration of solar, wind, hydro, and other renewables is reshaping market dynamics, \
         affecting pricing and the supply-demand balance, and contributing to Australia's transition to a lower-carbon future. The topic \
         may also consider the economic and environmental trade-offs involved, offering insights for strategic energy management and policy formulation.")

st.write("---")

## Main Content

st.warning('This dashboard is a work in progress. It is intended for educational purposes only. If you have any feedback \
           or suggestions, please feel free to open an issue on the [GitHub](https://github.com/ZhipengHe/NEM-Dashboard/issues).', icon="⚠️")


st.write("---")

st.subheader("Data Sources")

st.info('''
        Before starting your analysis,
        - Please select one or more of the datasets below, or choose other datasets that best align with your proposed research objectives. 
        - Make sure your selection reflects your project's goals and the features you need for analysis.
        ''', icon="💡")

st.markdown('''
            ##### Available Datasets

            For investigating renewable integration in the NEM, you need to consider multiple datasets from different sources and combine them to get a comprehensive view of \
            the renewable energy generation in the NEM. Here are some of the key datasets that you may consider for your analysis.

            You can find the information about generators and their registration details, such as fuel type, capacity, location, and connection points, in the \
            [NEM Registration and Exemption List](https://www.aemo.com.au/-/media/files/electricity/nem/participant_information/nem-registration-and-exemption-list.xlsx?). \
            This dataset is in Excel format. Check `Production Units (PU) and Scheduled Loads` tab for generator details.

            These tables are publicly available \
            on the [NEMWEB](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/market-data-nemweb). \
            Please refer to the [MMS Data Model](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report.htm) \
            for detailed information on the data structure and definitions. 
            - [`DISPATCH.DISPATCH_UNIT_SCADA`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report.htm): \
            This table contains the real-time MW reading from generators and scheduled loads for each dispatch unit, including renewable energy sources, \
            by SCADA (Supervisory Control and Data Acquisition) systems.
            - [`PARTICIPANT_REGISTRATION.DUDETAILSUMMARY`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec44.htm#60): \
            This table provides detailed information about generator registration, including region, connection point, and capacity details, but does not include fuel type information.
            
            
            ##### Data Download

            - You can manually download these datasets from the [Monthly Archive](https://visualisations.aemo.com.au/aemo/nemweb/#mms-data-model) section of the NEMWEB portal by month and year.
            - Alternatively, you can use the out-of-box packages to download these datasets from the NEMWEB portal, such as:
                - Python package: [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS)
                - R package: [nemwebR](https://github.com/aleemon/nemwebR)
            ''')

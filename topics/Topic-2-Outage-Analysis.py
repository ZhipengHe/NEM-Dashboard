import os
import streamlit as st
import pandas as pd
import altair as alt
import warnings
import datetime
warnings.filterwarnings("ignore", message="Could not infer format, so each element will be parsed individually")


st.header("Topic 2: Power Outage Root Cause and Impact Analysis")

st.subheader("About Topic")

st.write("This topic examines the occurrence and impact of power outages across Australia's NEM grid. By analysing historical outage events \
         alongside real-time operational data and AEMO reports, the study aims to identify the primary causes of power outages and the \
         relationships between key factors such as infrastructure health and maintenance practices, and behaviours like outage frequency. \
         The study will also assess how outages disrupt market operations and influence energy management strategies, providing actionable \
         insights for enhancing grid resilience. ")

st.write("---")

## Main Content


st.write("---")

st.subheader("Data Sources")

st.info('''
        Before starting your analysis,
        - Please select one or more of the datasets below, or choose other datasets that best align with your proposed research objectives. 
        - Make sure your selection reflects your project's goals and the features you need for analysis.
        ''', icon="💡")

st.markdown('''
            ##### Available Datasets

            The data used in the above analysis is sourced from the Australian Energy Market Operator (AEMO) and is publicly available \
            on the [NEMWEB](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/market-data-nemweb). \
            Please refer to the [MMS Data Model](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report.htm) \
            for detailed information on the data structure and definitions. Here lists the relevant table names and features from MMS Data Model used in above example:
            - [`NETWORK.NETWORK_OUTAGEDETAIL`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec72.htm#15): \
            This table contains detailed information about network outages, including the start and end times, duration, affected substations, \
            equipment types, and outage causes.
            - [`NETWORK.NETWORK_OUTAGESTATUSCODE`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec72.htm#23): \
            This table provides the status codes for network outages, such as 'Information', 'Medium term timeframe likely to proceed', 'Unlikely to proceed', 'Withdraw Request', etc.
            
            AMEO also provides a dedicated page for introducing the network outages [Link](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/nem-events-and-reports/network-outages), \
            where you can find more information about the network outages, including the high impact outages:
            - [High Impact Outages](https://www.nemweb.com.au/REPORTS/CURRENT/HighImpactOutages/): This page provides datasets on high-impact outages, in addition to standard \
            network outage information. It includes details such as potential impacts, outage recall times, and outage reasons. The data is stored in a tabular format; however, \
            for datasets before September 2019, only PDF files are available. More recent datasets are provided in CSV or XLSX format.

            If you are interested in exploring the root causes and impacts of critical outages in the last few years, AEMO provides incident investigation reports related to *unusual power system events*:
            - [Power System Incident Reports](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/nem-events-and-reports/power-system-operating-incident-reports): \
            This page contains detailed reports on power system incidents, including root cause analysis, event timelines, and recommendations for system improvements. The reports are \
            categorised by incident type, such as voltage disturbances, frequency deviations, and system black events. The data is available in PDF format and can be downloaded for further analysis.

            
            ##### Data Download

            - You can manually download outage tables from the [Monthly Archive](https://visualisations.aemo.com.au/aemo/nemweb/#mms-data-model) section of the NEMWEB portal. \
            Since `NETWORK.NETWORK_OUTAGEDETAIL` stores the details of network outages from 2003 to nearest available month, you do not need to download the data every month. \
            `NETWORK.NETWORK_OUTAGESTATUSCODE` is a static table, so you only need to download it once.
            - For High Impact Outages, you can download the datasets from the [High Impact Outages](https://www.nemweb.com.au/REPORTS/CURRENT/HighImpactOutages/) page.
            - For Power System Incident Reports, you can download the reports from the [Power System Incident Reports](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/nem-events-and-reports/power-system-operating-incident-reports) page.
            ''')



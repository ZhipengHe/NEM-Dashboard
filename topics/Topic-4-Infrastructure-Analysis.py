import streamlit as st
import pandas as pd
import altair as alt


st.header("Topic 4: Electricity Infrastructure Analysis and Performance Assessment")

st.subheader("About Topic")

st.write("This topic investigates the physical and operational facets of the NEM infrastructure—including generation, \
         transmission, and distribution networks—to analyse and assess its performance. The study aims to identify and \
         evaluate the impact of infrastructure challenges, such as supply-demand imbalances, regional disparities, and \
         system limitations, on grid performance, market efficiency, and long-term system resilience. The study will also \
         assess how these infrastructure constraints influence market pricing, reliability, and the decision-making processes \
         of market operators, regulators, and policymakers.")

st.write("---")

## Main Content

## embedding aemo official dashboard as example:
# https://aemo.com.au/aemo/apps/visualisations/elec-nem-summary-tiles.html

with st.container():
    st.subheader("Example: **NEM Electricity Summary Dashboard**")

    st.write("This is an official dashboard for real-time NEM summary provided by AEMO. \
            ")
    st.warning('''
            **Copyright Notice**
            - The NEM Official Dashboard displayed on this website is the property of the Australian \
               Energy Market Operator (AEMO). All rights, including data, design, and content, belong \
               to AEMO and are used here for ***educational purposes only****.
            - This website does ***not*** claim ownership of the dashboard or its content. For official \
               information, licensing, or permissions, please visit [AEMO Website](https://aemo.com.au/).
            - The dashboard is sourced ***directly from AEMO***, and we do ***not*** modify or control its \
               content, data accuracy, or availability.  
            - This integration aims to help students understand the project and the workings of the \
               ***National Electricity Market (NEM)***. Users should refer to ***AEMO's official website*** \
               for authoritative data and operational decisions.  
            ''', icon="⚠️")

    st.components.v1.iframe("https://aemo.com.au/aemo/apps/visualisations/elec-nem-summary-tiles.html", height=860)
    st.caption("Source: [AEMO NEM Summary Dashboard](https://aemo.com.au/aemo/apps/visualisations/elec-nem-summary-tiles.html)")

st.write("---")

st.subheader("Data Sources")

st.info('''
        Before starting your analysis,
        - Please select one or more of the datasets below, or choose other datasets that best align with your proposed research objectives. 
        - Make sure your selection reflects your project's goals and the features you need for analysis.
        ''', icon="💡")

st.markdown('''
            ##### Available Datasets

            The infrastructure analysis can cover a wide range of datasets related to the NEM's physical assets, operational data, and market performance. \
            Here provides some key datasets from different perspectives that you may consider for your analysis.

            These tables are publicly available \
            on the [NEMWEB](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/market-data-nemweb).

            (1) If you are interested in exploring the interconnection and flow of electricity across regions, you may consider the following datasets:
            - [`DISPATCH.DISPATCHINTERCONNECTORRES`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec20.htm#123): \
            This table contains the dispatch interconnector flow results, including the flow direction, MW flow, and constraints for each interconnector in the NEM. 
            - [`DISPATCH.DISPATCHREGIONSUM`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec22.htm#163): \
            This table sets out the 5-minute solution for each dispatch run for each region, including the total demand, generation, and interconnector flows.

            (2) If you are interested in analysing the demand and supply balance in the NEM, you may consider the following datasets:
            - [`DEMAND_FORECAST.DEMANDOPERATIONALACTUAL`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec18.htm#1): \
            This table provides the actual operational demand data for 30-minute intervals.
            - [`DEMAND_FORECAST.DEMANDOPERATIONALFORECAST`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec18.htm#9): \
            This table provides the operational demand forecast data for 30-minute intervals, including the 10%, 50%, and 90% of exceedance operational demand forecast value.
            - [`DISPATCH.DISPATCH_UNIT_SCADA`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report.htm): \
            This table contains the real-time MW reading from generators and scheduled loads for each dispatch unit, including renewable energy sources, \
            by SCADA (Supervisory Control and Data Acquisition) systems.

            Please refer to the [MMS Data Model](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report.htm) \
            for detailed information on the data structure and definitions. 

            (3) If you are interested in geographical and locational aspects of the NEM infrastructure, you may consider the following datasets:
            - [Electricity Transmission Lines](https://digital.atlas.gov.au/datasets/digitalatlas::electricity-transmission-lines/about): \
            This dataset provides the spatial information of electricity transmission lines across Australia, including the line type, voltage, and ownership details.
            - [Transmission Substations](https://digital.atlas.gov.au/datasets/digitalatlas::transmission-substations/about): \
            This dataset provides the spatial information of transmission substations across Australia, including the substation name, type, and capacity details.
            - [Major Power Stations](https://digital.atlas.gov.au/datasets/digitalatlas::major-power-stations/about): \
            This dataset provides the spatial information of major power stations across Australia, including the power station name, type, and capacity details.

            
            ##### Data Download

            - You can manually download these datasets from the [Monthly Archive](https://visualisations.aemo.com.au/aemo/nemweb/#mms-data-model) section of the NEMWEB portal by month and year. \
               We recommend downloading zipped CSV files for your chosen datasets rather than the entire zipped monthly database. 
            - Alternatively, you can use the out-of-box packages to download these datasets from the NEMWEB portal, such as:
                - Python package: [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS)
                - R package: [nemwebR](https://github.com/aleemon/nemwebR)
            - If you consider the weather data for analysis, you can download the climate data from the \
                [Bureau of Meteorology (BOM)](http://www.bom.gov.au/climate/data/index.shtml).
            - For spatial datasets, you can download the shapefiles from the [Australian Government Digital Atlas](https://digital.atlas.gov.au/) portal.
            ''')

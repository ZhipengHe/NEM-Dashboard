import streamlit as st
import pandas as pd
import altair as alt


st.header("Topic 2: Power Outage Root Cause and Impact Analysis")

st.subheader("About Topic")

st.write("This topic examines the occurrence and impact of power outages across Australia's NEM grid. By analysing historical outage events \
         alongside real-time operational data and AEMO reports, the study aims to identify the primary causes of power outages and the \
         relationships between key factors such as infrastructure health and maintenance practices, and behaviours like outage frequency. \
         The study will also assess how outages disrupt market operations and influence energy management strategies, providing actionable \
         insights for enhancing grid resilience. ")

st.write("---")

## Main Content

# Load data function
def load_data(file_path, date_columns):
    try:
        data = pd.read_csv(file_path, parse_dates=date_columns)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

with st.container():
    st.subheader("Example: **Network Planned Outage Analysis**")
    st.write("In this example, we will explore the network planned outages in the NEM. The analysis will focus on the planned outage \
             start from 2022 to 2025. ")
    
    ## show the data
    # Load the data
    file_path = f"data/analysis/NETWORK_OUTAGEDETAIL_202201_202501.csv"
    date_cols = ["STARTTIME", "ENDTIME", "SUBMITTEDDATE", "ACTUAL_STARTTIME", "ACTUAL_ENDTIME"]
    data = load_data(file_path, date_columns=date_cols)

    # Filter data for years 2022 to 2025
    data = data[(data["STARTTIME"].dt.year >= 2022) & (data["STARTTIME"].dt.year <= 2024)]

    # Display the data
    st.write("The planned outage logs look like this:")
    st.write(data.head())

    # Visualize the data
    st.write("Let's start by visualising from both temporal and reason analysis.")

    temporal, reason = st.tabs(["Temporal Analysis", "Reason Analysis"])

    with temporal:
        # ---- Temporal Analysis ----
        if data is not None:
            # Extract year and month from STARTTIME
            data["YEAR_MONTH"] = data["STARTTIME"].dt.to_period("M").astype(str)

            # Count outages per month
            outages_per_month = data.groupby("YEAR_MONTH").size().reset_index(name="COUNT")

            # Compute the overall mean of outages.
            mean_value = outages_per_month['COUNT'].mean()

            # Plot outages over time
            base = alt.Chart(outages_per_month).encode(
                x=alt.X("YEAR_MONTH:T", title="Time (Year-Month)",
                axis=alt.Axis(labelAngle=0), timeUnit="yearmonth"),
            )

            outage_bar = base.mark_bar().encode(
                y=alt.Y("COUNT:Q", title="Number of Outages"),
                tooltip=["YEAR_MONTH:T", "COUNT"],
            )

            # For bars where COUNT is above the overall mean, overlay the extra portion in red.
            highlight = base.mark_bar(color="red").encode(
                y=alt.Y("baseline:Q"),
                y2=alt.Y2("COUNT:Q")
            ).transform_filter(
                alt.datum.COUNT > mean_value
            ).transform_calculate(
                baseline=str(mean_value)
            )

            # Create a rule for the mean of COUNT across the dataset.
            mean_line = alt.Chart(outages_per_month).mark_rule(color='red', strokeDash=[5,5]).encode(
                y=alt.Y("mean(COUNT):Q", title="Number of Outages")
            )
            

            chart_outages = alt.layer(outage_bar, highlight, mean_line).interactive()

            st.write("The chart below shows the number of planned outages per month from 2022 to 2024. \
                     :blue[Monthly outages] are represented by :blue[blue bars], with :red[red overlays] highlighting the \
                     portion that :red[exceeds the overall mean value].")
            st.altair_chart(chart_outages, theme="streamlit", use_container_width=True)
            
        else:
            st.warning("Please provide a valid file path to load data.")

    with reason:
        # ---- Status and Reason Analysis ----
        # Count outages by status
        status_counts = data["OUTAGESTATUSCODE"].value_counts().reset_index()
        status_counts.columns = ["OUTAGESTATUSCODE", "COUNT"]

        # Plot outage status distribution
        chart_status = alt.Chart(status_counts).mark_arc(innerRadius=50).encode(
            theta="COUNT:Q",
            color="OUTAGESTATUSCODE:N",
            tooltip=["OUTAGESTATUSCODE", "COUNT"],
             order=alt.Order("COUNT:Q", sort="descending")  # orders slices by count
        ).properties(title="Outage Status Distribution").interactive()

        # Count outages by reason
        reason_counts = data["REASON"].value_counts().reset_index().head(10)
        reason_counts.columns = ["REASON", "COUNT"]

        # Plot outage reasons distribution
        chart_reason = alt.Chart(reason_counts).encode(
            alt.Theta("COUNT").stack(True),
            alt.Radius("COUNT").scale(alt.Scale(type='sqrt'), zero=True, rangeMin=5000),
            color="REASON:N",
            tooltip=["REASON", "COUNT"],
             order=alt.Order("COUNT:Q", sort="descending")  # orders slices by count
        ).mark_arc(innerRadius=20, stroke="white").properties(title="Outage Reasons Distribution").interactive()

        st.write("The charts below show the proportion of planned outages by status and reasons. \
                  The left chart is a donut chart showing the breakdown of outage status codes, \
                  with 'Complete' and 'Withdrawn' being the two main categories. \
                 The right chart is a pie chart highlighting the top outage reasons,  \
                 where slice sizes reflect their counts, and interactive tooltips provide detailed insights.")

        co1, co2 = st.columns(2)
        with co1:
            st.altair_chart(chart_status, theme="streamlit", use_container_width=True)
        with co2:
            st.altair_chart(chart_reason, theme="streamlit", use_container_width=True)




st.write("---")

st.subheader("Data Sources")

st.info('''
        Before starting your analysis,
        - Please select one or more of the datasets below, or choose/add other datasets that best align with your proposed research objectives. 
        - Make sure your selection reflects your project's goals and the features you need for analysis.
        ''', icon="💡")

st.markdown('''
            ##### Available Datasets

            These tables are publicly available \
            on the [NEMWEB](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/market-data-nemweb). \
            Here lists the relevant table names and features from MMS Data Model used in above example:
            - [`NETWORK.NETWORK_OUTAGEDETAIL`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec72.htm#15): \
            This table contains detailed information about network outages, including the start and end times, duration, affected substations, \
            equipment types, and outage causes.
            - [`NETWORK.NETWORK_OUTAGESTATUSCODE`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec72.htm#23): \
            This table provides the status codes for network outages, such as 'Information', 'Medium term timeframe likely to proceed', 'Unlikely to proceed', 'Withdraw Request', etc.
            - Please refer to the [MMS Data Model](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report.htm) \
            for detailed information on the data structure and definitions. 
            
            AMEO also provides a dedicated page for introducing the network outages [Link](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/nem-events-and-reports/network-outages), \
            where you can find more information about the network outages, including the high impact outages:
            - [High Impact Outages](https://www.nemweb.com.au/REPORTS/CURRENT/HighImpactOutages/): This page provides datasets on high-impact outages, in addition to standard \
            network outage information. It includes details such as potential impacts, outage recall times, and outage reasons. The data is stored in a tabular format; however, \
            for datasets before September 2019, only PDF files are available. After September 2019, datasets are provided in CSV or XLSX format.

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



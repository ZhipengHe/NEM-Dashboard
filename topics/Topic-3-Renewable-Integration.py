import streamlit as st
import pandas as pd
import altair as alt


st.header("Topic 3: Renewable Integration Analysis and Impact Forecast")

st.subheader("About Topic")

st.write("This topic explores the sustainability dimension of the NEM by examining the growing role of renewable energy source \
         in the market. It will analyse how the integration of solar, wind, hydro, and other renewables is reshaping market dynamics, \
         affecting pricing and the supply-demand balance, and contributing to Australia's transition to a lower-carbon future. The topic \
         may also consider the economic and environmental trade-offs involved, offering insights for strategic energy management and policy formulation.")

st.write("---")

## Main Content

# List of regions
REGIONS =['ALL', 'NSW1', 'QLD1', 'SA1', 'TAS1', 'VIC1']

# Load data function
def load_data(file_path, date_columns):
    try:
        data = pd.read_csv(file_path, parse_dates=date_columns)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Selecta region to start
selected_region = st.sidebar.selectbox("Select a region to analyse the fuel mix", REGIONS, index=0)


with st.container():
    st.subheader("Example: **Generation Fuel Mix in the NEM (Jan 2025)**")
    st.write("In this example, we will explore the generation fuel mix in the NEM for January 2025.")

    reg_file_path = "data/analysis/NEM_Registration.csv"
    screenshot_path = "data/analysis/DISPATCH_UNIT_SCADA_202501_screenshot.csv"
    file_path = "data/analysis/DISPATCH_UNIT_SCADA_202501_daily.csv"
    date_cols = ["DATE"]

    data_screenshot = load_data(screenshot_path, date_columns=["SETTLEMENTDATE", "LASTCHANGED"])
    data_reg = load_data(reg_file_path, date_columns=None)
    ## aggregated data
    data = load_data(file_path, date_columns=date_cols)

    ### display data
    if data_reg is not None:
        st.write("The registration details of the generators in the NEM is shown below:")
        st.dataframe(data_reg.head())
        st.caption("The registration table includes the generator's fuel type, technology, capacity and classification.")
    if data_screenshot is not None:
        st.write("The generation and load data by each participant in January 2025 is shown below:")
        st.dataframe(data_screenshot.head())
        st.caption("The postive SCADAVALUE indicates the generation, and the negative SCADAVALUE indicates the load.")

    ### visualisation

    fuel, technology = st.tabs(["Fuel Mix", "Technology Mix"])

    # column name Fuel Source - Primary
    with fuel:
        option = ['total', 'percent']
        selection = st.pills("Select a statistic to display", 
                            option, 
                            selection_mode='single', 
                            default=['total'],
                            key="by_fuel")
        
        if selection:
            if 'total' in selection:
                fuel_mix = data.groupby(["Fuel Source - Primary", "DATE"]).agg({"SCADAVALUE_sum": "sum"}).reset_index()
                fuel_chart = alt.Chart(fuel_mix).mark_area().encode(
                    x=alt.X("DATE:T", title="Date"),
                    y=alt.Y("SCADAVALUE_sum:Q", title="Total Generation (MWh)", stack=True),
                    color=alt.Color("Fuel Source - Primary:N", title="Fuel Source"),
                    order=alt.Order("Fuel Source - Primary:N", sort="ascending")
                )

            elif 'percent' in selection:
                fuel_mix = data.groupby(["Fuel Source - Primary", "DATE"]).agg({"SCADAVALUE_sum": "sum"}).reset_index()
                fuel_mix["Total"] = fuel_mix.groupby("DATE")["SCADAVALUE_sum"].transform("sum")
                fuel_mix["Percent"] = fuel_mix["SCADAVALUE_sum"] / fuel_mix["Total"] * 100

                fuel_chart = alt.Chart(fuel_mix).mark_area().encode(
                    x=alt.X("DATE:T", title="Date"),
                    y=alt.Y("Percent:Q", title="Generation (%)", stack=True),
                    color=alt.Color("Fuel Source - Primary:N", title="Fuel Source"),
                    order=alt.Order("Fuel Source - Primary:N", sort="ascending")
                )

            st.write("The generation fuel mix in the NEM for January 2025 is shown below:")
            st.altair_chart(fuel_chart, theme="streamlit", use_container_width=True)
            st.caption("The fuel sources are extracted from the registration table of the generators.")

        else:
            st.warning("Please select a statistic to display.")
    
    # column name Technology Type - Primary
    with technology:
        option = ['total', 'percent']
        selection = st.pills("Select a statistic to display", 
                    option, 
                    selection_mode='single', 
                    default=['total'],
                    key="by_tech")
        
        if selection:
            if 'total' in selection:
                tech_mix = data.groupby(["Technology Type - Primary", "DATE"]).agg({"SCADAVALUE_sum": "sum"}).reset_index()
                tech_chart = alt.Chart(tech_mix).mark_area().encode(
                    x=alt.X("DATE:T", title="Date"),
                    y=alt.Y("SCADAVALUE_sum:Q", title="Total Generation (MWh)", stack=True),
                    color=alt.Color("Technology Type - Primary:N", title="Technology Type"),
                    order=alt.Order("Technology Type - Primary:N", sort="ascending")
                )
            
            elif 'percent' in selection:
                tech_mix = data.groupby(["Technology Type - Primary", "DATE"]).agg({"SCADAVALUE_sum": "sum"}).reset_index()
                tech_mix["Total"] = tech_mix.groupby("DATE")["SCADAVALUE_sum"].transform("sum")
                tech_mix["Percent"] = tech_mix["SCADAVALUE_sum"] / tech_mix["Total"] * 100

                tech_chart = alt.Chart(tech_mix).mark_area().encode(
                    x=alt.X("DATE:T", title="Date"),
                    y=alt.Y("Percent:Q", title="Generation (%)", stack=True),
                    color=alt.Color("Technology Type - Primary:N", title="Technology Type"),
                    order=alt.Order("Technology Type - Primary:N", sort="ascending")
                )
            
            st.write("The generation technology mix in the NEM for January 2025 is shown below:")
            st.altair_chart(tech_chart, theme="streamlit", use_container_width=True)
            st.caption("The technology types are extracted from the registration table of the generators.")
        else:
            st.warning("Please select a statistic to display.")



st.write("---")

st.subheader("Data Sources")

st.info('''
        Before starting your analysis,
        - Please select one or more of the datasets below, or choose/add other datasets that best align with your proposed research objectives. 
        - Make sure your selection reflects your project's goals and the features you need for analysis.
        ''', icon="💡")

st.markdown('''
            ##### Available Datasets

            For investigating renewable integration in the NEM, you need to consider multiple datasets from different sources and combine them to get a comprehensive view of \
            the renewable energy generation in the NEM. Here are some of the key datasets that you may consider for your analysis.

            You can find the information about generators and their registration details, such as such as fuel source, technology type, capacity, location, and connection points, in the \
            [NEM Registration and Exemption List](https://www.aemo.com.au/-/media/files/electricity/nem/participant_information/nem-registration-and-exemption-list.xlsx?). \
            This dataset is in Excel format. Check `Production Units (PU) and Scheduled Loads` tab for generator details.

            These tables are publicly available \
            on the [NEMWEB](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/market-data-nemweb). \
            Here lists the relevant table names and features from MMS Data Model used in above example:
            - [`DISPATCH.DISPATCH_UNIT_SCADA`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report.htm): \
            This table contains the real-time MW reading from generators and scheduled loads for each dispatch unit, including renewable energy sources, \
            by SCADA (Supervisory Control and Data Acquisition) systems.
            - [`PARTICIPANT_REGISTRATION.DUDETAILSUMMARY`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec44.htm#60): \
            This table provides detailed information about generator registration, including region, connection point, and capacity details, but does not include fuel type information.
            - Please refer to the [MMS Data Model](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report.htm) \
            for detailed information on the data structure and definitions. 
            
            ##### Data Download

            - You can manually download these datasets from the [Monthly Archive](https://visualisations.aemo.com.au/aemo/nemweb/#mms-data-model) section of the NEMWEB portal by month and year. \
                We recommend downloading zipped CSV files for your chosen datasets rather than the entire zipped monthly database. 
            - Alternatively, you can use the out-of-box packages to download these datasets from the NEMWEB portal, such as:
                - Python package: [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS)
                - R package: [nemwebR](https://github.com/aleemon/nemwebR) (Limited functionality, last updated in 2022)
            - If you consider the weather data for analysis, you can download the climate data from the \
                [Bureau of Meteorology (BOM)](http://www.bom.gov.au/climate/data/index.shtml).
            ''')

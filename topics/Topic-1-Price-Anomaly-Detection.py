import streamlit as st
import pandas as pd
import altair as alt
import warnings

warnings.filterwarnings("ignore", message="Could not infer format, so each element will be parsed individually")


st.header("Topic 1: Price Anomaly Detection")

st.subheader("About Topic")

st.write("This topic focuses on identifying and analysing unusual fluctuations in electricity prices within the NEM. \
         By detecting and examining patterns that deviate from expected market behaviour, the study aims to uncover \
         the underlying factors driving price anomalies, including, for example, supply-demand imbalances, network congestion, \
         generation outages, and external market influences. Additionally, the study may also evaluate the broader implications \
         of these price fluctuations on market stability, electricity costs, and the overall efficiency of energy management strategies.")


st.write("---")

# List of regions
REGIONS =[ 'NSW1', 'QLD1', 'SA1', 'TAS1', 'VIC1']

# Load data function
def load_data(file_path, date_column):
    try:
        data = pd.read_csv(file_path, parse_dates=[date_column])
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


# Selecta region to start
selected_region = st.sidebar.selectbox("Select a region to analyse the electricity price data", REGIONS, index=1)


# Main content

### Chart: Trade Price Daily Distribution for selected_region
### x-axis: day, x-range: hour, y-axis: mean, median, min, max

with st.container():
    st.subheader(f"Example: *Electricity Price Daily Distribution for {selected_region}*")

    ## Caption

    st.write("Electricity Price Daily Distribution for the selected region showing hourly and dispatch-level aggregations of price (RRP) \
            and total demand using a chosen statistic (mean, median, min, or max). Data is filtered by year (2022-2024), with independent y-axes \
            for each metric.")

    col1, col2,  _ = st.columns([0.25, 0.20, 0.55])

    with col2:
        year = st.selectbox("Select a year to display the data", list(range(2022, 2025)), index=1, key="year-select")

    with col1:
        option = ['mean', 'median', 'min', 'max']
        selection = st.pills("Select a statistic to display", 
                            option, 
                            selection_mode='single', 
                            default=['median'],
                            key="by_day")

    
    hours, dispatch = st.tabs(["1 Hour", "Dispatch"])

    with hours:
        file_path = f"data/analysis/PRICE_STATS_BY_HOUR_{selected_region}.csv"
        if selected_region:
            data = load_data(file_path, date_column='YEAR_MONTH_DAY_HOUR')
            if data is not None:
                # get year in the selected range
                data = data[data['YEAR'] == year]
                # calculate mean, median, min, max for each hour in the day over the whole year
                data = data.groupby(['HOUR']).agg({'RRP_mean': 'mean', 'RRP_median': 'median', 
                                                'RRP_min': 'min', 'RRP_max': 'max',
                                                'TOTALDEMAND_mean': 'mean', 'TOTALDEMAND_median': 'median',
                                                    'TOTALDEMAND_min': 'min', 'TOTALDEMAND_max': 'max'}).round(2).reset_index()
                
                if selection:
                    _selection_RRP = f'RRP_{selection}'
                    _selection_DEMAND = f'TOTALDEMAND_{selection}'
                    
                    base = alt.Chart(data).encode(
                        x=alt.X('HOUR:O', title="Hour", axis=alt.Axis(labelAngle=0))
                    )
                    
                    rrp_line = base.mark_line(color='red').encode(
                        y=alt.Y(f'{_selection_RRP}:Q', title='Electricity Price',
                                scale=alt.Scale(zero=False, nice=True)),
                        tooltip=['HOUR', f'{_selection_RRP}']
                    )
                    
                    demand_line = base.mark_line(color='blue', strokeDash=(5,5)).encode(
                        y=alt.Y(f'{_selection_DEMAND}:Q', title='Total Demand',
                                scale=alt.Scale(zero=False, nice=True)),
                        tooltip=['HOUR', f'{_selection_DEMAND}']
                    )
                    
                    chart = alt.layer(rrp_line, demand_line).resolve_scale(
                        y='independent'
                    ).interactive()
                    st.altair_chart(chart, theme="streamlit", use_container_width=True)
                    st.caption("Legend: Red line = :red[Electricity Price]; Blue dashed line = :blue[Total Demand] (aggregated by hour).")
                else:
                    st.warning("Please select one statistic to display the plot.")
            else:
                st.warning("Please provide a valid file path to load data.")
        else:
            st.warning("Please select a region to analyse.")

    with dispatch:

        file_path = f"data/analysis/PRICE_AND_DEMAND_ALL_YEARS_{selected_region}.csv"
        if selected_region:
            data = load_data(file_path, date_column='SETTLEMENTDATE')
            if data is not None:
                # get year in the selected range
                data = data[data['YEAR'] == year]
                # calculate mean, median, min, max for each hour in the day over the whole year
                data = data.groupby(['HOUR', 'MINUTE']).agg(                
                    RRP_mean=('RRP', 'mean'),
                    RRP_median=('RRP', 'median'),
                    RRP_min=('RRP', 'min'),
                    RRP_max=('RRP', 'max'),
                    TOTALDEMAND_mean=('TOTALDEMAND', 'mean'),
                    TOTALDEMAND_median=('TOTALDEMAND', 'median'),
                    TOTALDEMAND_min=('TOTALDEMAND', 'min'),
                    TOTALDEMAND_max=('TOTALDEMAND', 'max')
                ).round(2).reset_index()
                
                data['time'] = data['HOUR'].astype(str).str.zfill(2) + ':' + data['MINUTE'].astype(str).str.zfill(2)

                if selection:
                    _selection_RRP = f'RRP_{selection}'
                    _selection_DEMAND = f'TOTALDEMAND_{selection}'
                    
                    base = alt.Chart(data).encode(
                        x=alt.X('time:O', title="Time", axis=alt.Axis(labelAngle=0))
                    )
                    
                    rrp_line = base.mark_line(color='red').encode(
                        y=alt.Y(f'{_selection_RRP}:Q', title='Electricity Price',
                                scale=alt.Scale(zero=False, nice=True)),
                        tooltip=['time', f'{_selection_RRP}']
                    )
                    
                    demand_line = base.mark_line(color='blue', strokeDash=(5,5)).encode(
                        y=alt.Y(f'{_selection_DEMAND}:Q', title='Total Demand',
                                scale=alt.Scale(zero=False, nice=True)),
                        tooltip=['time', f'{_selection_DEMAND}']
                    )
                    
                    chart = alt.layer(rrp_line, demand_line).resolve_scale(
                        y='independent'
                    ).interactive()

                    st.warning("Since AEMC changed the settlement period from 30 minutes to 5 minutes in 2022, the data before 2022 is not included in the analysis of dispatch level.")

                    st.altair_chart(chart, theme="streamlit", use_container_width=True)
                    st.caption("Legend: Red line = :red[Electricity Price]; Blue dashed line = :blue[Total Demand] (aggregated by dispatch).")

                else:
                    st.warning("Please select one statistic to display the plot.")
            else:
                st.warning("Please provide a valid file path to load data.")
        else:
            st.warning("Please select a region to analyse.")


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
            for detailed information on the data structure and definitions. 
            
            Here lists the relevant table names and features from MMS Data Model used in above example:
            - [`DISPATCH.DISPATCHPRICE`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec21.htm#154): \
                This table provides records each 5 minute dispatch price for each region, including whether an intervention has occurred, or price override (e.g. for Administered Price Cap).
                - `DISPATCHPRICE.RRP` = Dispatch price in $/MWh
            - [`DISPATCH.DISPATCHREGIONSUM`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec22.htm#163): \
                This table sets out the 5-minute solution for each dispatch run for each region, including the total demand, generation, and interconnector flows.
                - `DISPATCHREGIONSUM.TOTALDEMAND` = Total demand in MW
            - [`TRADING_DATA.TRADINGPRICE`](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/Electricity%20Data%20Model%20Report_files/Elec60.htm#16): \
                This table provides similar information to DISPATCH.DISPATCHPRICE, but updated every 30 minutes.
            
            ##### Data Download

            - You can manually download these datasets from the [Monthly Archive](https://visualisations.aemo.com.au/aemo/nemweb/#mms-data-model) section of the NEMWEB portal by month and year.
            - Alternatively, you can use the out-of-box packages to download these datasets from the NEMWEB portal, such as:
                - Python package: [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS)
                - R package: [nemwebR](https://github.com/aleemon/nemwebR)
            ''')



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

# List of regions
REGIONS =[ 'NSW1', 'QLD1', 'SA1', 'TAS1', 'VIC1']

# File path
data_folder = os.path.join(os.path.dirname(__file__), "data/concatenated_data")

# Load data function
def load_data(file_path, date_column):
    try:
        data = pd.read_csv(file_path, parse_dates=[date_column])
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def chart_by_years(data, y_column, color=None, x_column='MONTH', year_column='YEAR',
                             y_title='Trade Price', x_title='Month'):
    """
    Creates an interactive Altair chart with line, highlight points, and tooltips.

    Parameters:
        data (pd.DataFrame): The data to be used in the chart.
        y_column (str): The column name for the y-axis values.
        x_column (str, optional): The column name for the x-axis (default is 'MONTH').
        year_column (str, optional): The column name for the year (default is 'YEAR').
        y_title (str, optional): Title for the y-axis (default is 'Trade Price').
        x_title (str, optional): Title for the x-axis (default is 'Month').

    Returns:
        alt.Chart: An Altair chart object.
    """
    # Base line chart
    if color is None:
        line = alt.Chart(data).mark_line().encode(
            x=alt.X(f'{x_column}:O', title=x_title, axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f'{y_column}:Q', title=y_title)
        )
    else:
        line = alt.Chart(data).mark_line().encode(
            x=alt.X(f'{x_column}:O', title=x_title, axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f'{y_column}:Q', title=y_title),
            color=alt.Color(f'{color}:N', title='Year')
        )

    # Transparent selectors across the chart for hover interactivity
    nearest = alt.selection_point(
        nearest=True,
        on="mouseover",
        fields=[x_column],
        empty="none"
    )

    selectors = alt.Chart(data).mark_point().encode(
        x=alt.X(f'{x_column}:O'),
        opacity=alt.value(0)  # Transparent points for interactivity
    ).add_params(nearest)

    # Highlight points on the line based on the selection
    highlight_points = line.mark_point(filled=True, size=80).encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        tooltip=[x_column, year_column, y_column]
    )

    # Tooltips for the selected point
    tooltips = alt.Chart(data).mark_text(align="left", dx=5, dy=-5).encode(
        x=alt.X(f'{x_column}:O'),
        y=alt.Y(f'{y_column}:Q'),
        text=alt.condition(nearest, f'{y_column}:Q', alt.value(''))
    )

    # Combine the layers
    chart = alt.layer(line, selectors, highlight_points, tooltips).interactive()

    return chart



# Title of the app
st.title("Exploratory Data Analysis for NEM Trade Price")



# Sidebar
st.sidebar.title("NEM Trade Price Analysis")
st.sidebar.write("Welcome to the NEM Trade Price Analysis Web App.")
st.sidebar.write("Please select a region to analyse the trade price data.")
selected_region = st.sidebar.selectbox("Select a region:", REGIONS, index=1)


# start_date = st.sidebar.date_input("Start date:", pd.to_datetime('2019-01-01'))
# end_date = st.sidebar.date_input("End date:", pd.to_datetime('2024-12-31'))

# Load data

# file_path = os.path.join(data_folder, f"PRICE_AND_DEMAND_ALL_YEARS_{selected_region}.csv")


### Chart 1: Trade Price Over 2019-2024 for selected region by month
### x-axis: year_month, x-range: 2019-2024, y-axis: mean, median, min, max

with st.container():
    file_path = f"data/analysis/PRICE_STATS_BY_MONTH_{selected_region}.csv"
    st.subheader(f"Trade Price from 2019 to 2024 for {selected_region} by Months")

    option = ['mean', 'median', 'min', 'max']
    selection = st.pills("Select one or more statistic to display", 
                         option, 
                         selection_mode='multi', 
                         default=['mean', 'median'],
                         key="overall")
    

    if selected_region:
        data = load_data(file_path, date_column='YEAR_MONTH')
        if data is not None:

            if selection:
                    _selection = [f'RRP_{s}' for s in selection]
                    mychart = st.line_chart(data, x='YEAR_MONTH', y=_selection, x_label= "Year", y_label='Trade Price')
            else:
                st.warning("Please select one or more statistics to display the plot.")
        else:
            st.warning("Please provide a valid file path to load data.")
    else:
        st.warning("Please select a region to analyse.")

### Chart 2: Trade Price by month for selected region (each line represents a year)
### x-axis: month, x-range: Jan-Dec, y-axis: mean, median, min, max

with st.container():

    st.subheader(f"Trade Price for {selected_region} by Different Years")

    option = ['mean', 'median', 'min', 'max']
    selection = st.pills("Select a statistic to display", 
                         option, 
                         selection_mode='single', 
                         default=['median'],
                         key="by_year")
    
    month, quarter, fortnight, week = st.tabs(["Month", "Quarter", "Fortnight", "Week"])

    with month:
        file_path = f"data/analysis/PRICE_STATS_BY_MONTH_{selected_region}.csv"

        if selected_region:
            data = load_data(file_path, date_column='YEAR_MONTH')

            if data is not None:
                if selection:
                    _selection = f'RRP_{selection}'

                    chart = chart_by_years(data, y_column=_selection, x_column='MONTH', x_title='Month', color='YEAR')

                    st.altair_chart(chart, theme="streamlit", use_container_width=True)
                else:
                    st.warning("Please select one statistic to display the plot.")
            else:
                st.warning("Please provide a valid file path to load data.")
        else:
            st.warning("Please select a region to analyse.")
    
    with quarter:
        file_path = f"data/analysis/PRICE_STATS_BY_MONTH_{selected_region}.csv"

        if selected_region:
            data = load_data(file_path, date_column='YEAR_MONTH')

            if data is not None:
                # aggregate monthly data to quarterly data, month 1-3 is Q1, 4-6 is Q2, 7-9 is Q3, 10-12 is Q4
                data['QUARTER'] = data['MONTH'].apply(lambda x: f"Q{int((x-1)/3)+1}")
                data = data.groupby(['YEAR', 'QUARTER']).agg({'RRP_mean': 'mean', 'RRP_median': 'median', 'RRP_min': 'min', 'RRP_max': 'max'}).round(2).reset_index()

                if selection:
                    _selection = f'RRP_{selection}'

                    chart = chart_by_years(data, y_column=_selection, x_column='QUARTER', x_title='Quarter', color='YEAR')
                    st.altair_chart(chart, theme="streamlit", use_container_width=True)
                else:
                    st.warning("Please select one statistic to display the plot.")
            else:
                st.warning("Please provide a valid file path to load data.")
        else:
            st.warning("Please select a region to analyse.")

    with fortnight:
        file_path = f"data/analysis/PRICE_STATS_BY_WEEK_{selected_region}.csv"

        if selected_region:
            data = load_data(file_path, date_column='YEAR_WEEK')

            if data is not None:
                data['FORTNIGHT'] = data['WEEK'].apply(lambda x: int(((x-1)/2))+1)
                data = data.groupby(['YEAR', 'FORTNIGHT']).agg({'RRP_mean': 'mean', 'RRP_median': 'median', 'RRP_min': 'min', 'RRP_max': 'max'}).round(2).reset_index()
                if selection:
                    _selection = f'RRP_{selection}'
                    chart = chart_by_years(data, y_column=_selection, x_column='FORTNIGHT', x_title='Fortnight', color='YEAR')
                    st.altair_chart(chart, theme="streamlit", use_container_width=True)
                else:
                    st.warning("Please select one statistic to display the plot.")
            else:
                st.warning("Please provide a valid file path to load data.")

    with week:
        file_path = f"data/analysis/PRICE_STATS_BY_WEEK_{selected_region}.csv"

        if selected_region:
            data = load_data(file_path, date_column='YEAR_WEEK')

            if data is not None:
                if selection:
                    _selection = f'RRP_{selection}'
                    chart = chart_by_years(data, y_column=_selection, x_column='WEEK', x_title='Week', color='YEAR')
                    st.altair_chart(chart, theme="streamlit", use_container_width=True)
                else:
                    st.warning("Please select one statistic to display the plot.")
            else:
                st.warning("Please provide a valid file path to load data.")
        else:
            st.warning("Please select a region to analyse.")

### Chart 3: Trade Price Monthly Distribution for selected_region
### x-axis: month, x-range: day, y-axis: mean, median, min, max

with st.container():
    st.subheader(f"Trade Price Monthly Distribution for {selected_region}")

    file_path = f"data/analysis/PRICE_STATS_BY_DAY_{selected_region}.csv"

    col1, col2, _ = st.columns([0.25, 0.25, 0.4])
    with col2:
        year_range = st.slider("Select year range to display the data", 2019, 2024, (2020, 2024), 1, key="year-slider")
    with col1:
        option = ['mean', 'median', 'min', 'max']
        selection = st.pills("Select a statistic to display", 
                            option, 
                            selection_mode='single', 
                            default=['median'],
                            key="by_month")

    if selected_region:
        data = load_data(file_path, date_column='YEAR_MONTH_DAY')
        if data is not None:
            # get year in the selected range
            data = data[(data['YEAR'] >= year_range[0]) & (data['YEAR'] <= year_range[1])]
            # calculate mean, median, min, max for each day in the month over the years
            data = data.groupby(['DAY']).agg({'RRP_mean': 'mean', 'RRP_median': 'median', 
                                              'RRP_min': 'min', 'RRP_max': 'max',
                                              'TOTALDEMAND_mean': 'mean', 'TOTALDEMAND_median': 'median',
                                                'TOTALDEMAND_min': 'min', 'TOTALDEMAND_max': 'max'}).round(2).reset_index()

            if selection:
                _selection_RRP = f'RRP_{selection}'
                _selection_DEMAND = f'TOTALDEMAND_{selection}'
                
                base = alt.Chart(data).encode(
                    x=alt.X('DAY:O', title="Day", axis=alt.Axis(labelAngle=0))
                )
                
                rrp_line = base.mark_line(color='red').encode(
                    y=alt.Y(f'{_selection_RRP}:Q', title='Trade Price',
                            scale=alt.Scale(zero=False, nice=True)),
                    tooltip=['DAY', f'{_selection_RRP}'],
                    color=alt.value('red')
                ).properties(
                    title='Trade Price'
                )
                
                demand_line = base.mark_line(color='blue', strokeDash=[5, 5]).encode(
                    y=alt.Y(f'{_selection_DEMAND}:Q', title='Total Demand', 
                            scale=alt.Scale(zero=False, nice=True)),
                    tooltip=['DAY', f'{_selection_DEMAND}'],
                    color=alt.value('blue')
                ).properties(
                    title='Total Demand'
                )
                
                chart = alt.layer(rrp_line, demand_line).resolve_scale(
                    y='independent'
                ).interactive()
                
                chart = chart.configure_legend(
                    orient='bottom',
                    title=None,
                    labelFontSize=12
                )
                
                st.altair_chart(chart, theme="streamlit", use_container_width=True)
            else:
                st.warning("Please select one statistic to display the plot.")

### Chart 4: Trade Price Weekly Distribution for selected_region
### x-axis: week, x-range: day, y-axis: mean, median, min, max

with st.container():
    st.subheader(f"Trade Price Weekly Distribution for {selected_region}")

    file_path = f"data/analysis/PRICE_STATS_BY_DAY_{selected_region}.csv"

    col1, col2, _ = st.columns([0.25, 0.25, 0.4])
    with col2:
        year_range = st.slider("Select year range to display the data", 2019, 2024, (2020, 2024), 1, key="year-slider-2")
    with col1:
        option = ['mean', 'median', 'min', 'max']
        selection = st.pills("Select a statistic to display", 
                            option, 
                            selection_mode='single', 
                            default=['median'],
                            key="by_week")

    if selected_region:
        data = load_data(file_path, date_column='YEAR_MONTH_DAY')
        if data is not None:
            # get year in the selected range
            data = data[(data['YEAR'] >= year_range[0]) & (data['YEAR'] <= year_range[1])]
            # calculate mean, median, min, max for each day in the month over the years
            data = data.groupby(['WEEKDAY']).agg({'RRP_mean': 'mean', 'RRP_median': 'median', 
                                              'RRP_min': 'min', 'RRP_max': 'max',
                                              'TOTALDEMAND_mean': 'mean', 'TOTALDEMAND_median': 'median',
                                                'TOTALDEMAND_min': 'min', 'TOTALDEMAND_max': 'max'}).round(2).reset_index()
            
            if selection:
                _selection_RRP = f'RRP_{selection}'
                _selection_DEMAND = f'TOTALDEMAND_{selection}'
                
                base = alt.Chart(data).encode(
                    x=alt.X('WEEKDAY:O', title="Day", axis=alt.Axis(labelAngle=0,
                            labelExpr="{'0': 'Mon', '1': 'Tue', '2': 'Wed', '3': 'Thu', '4': 'Fri', '5': 'Sat', '6': 'Sun'}[datum.value]")),)
                
                rrp_line = base.mark_line(color='blue').encode(
                    y=alt.Y(f'{_selection_RRP}:Q', title='Trade Price',
                            scale=alt.Scale(zero=False, nice=True)),
                    tooltip=['WEEKDAY', f'{_selection_RRP}']
                )
                
                demand_line = base.mark_line(color='red', strokeDash=(5,5)).encode(
                    y=alt.Y(f'{_selection_DEMAND}:Q', title='Total Demand',
                            scale=alt.Scale(zero=False, nice=True)),
                    tooltip=['WEEKDAY', f'{_selection_DEMAND}']
                )
                
                chart = alt.layer(rrp_line, demand_line).resolve_scale(
                    y='independent'
                ).interactive()
                st.altair_chart(chart, theme="streamlit", use_container_width=True)
            else:
                st.warning("Please select one statistic to display the plot.")
        else:
            st.warning("Please provide a valid file path to load data.")
    else:
        st.warning("Please select a region to analyse.")

### Chart 5: Trade Price Daily Distribution for selected_region
### x-axis: day, x-range: hour, y-axis: mean, median, min, max

with st.container():
    st.subheader(f"Trade Price Daily Distribution for {selected_region}")

    col1, col2, _ = st.columns([0.25, 0.20, 0.55])

    with col1:
        option = ['mean', 'median', 'min', 'max']
        selection = st.pills("Select a statistic to display", 
                            option, 
                            selection_mode='single', 
                            default=['median'],
                            key="by_day")
    with col2:
        year = st.selectbox("Select a year to display the data", list(range(2022, 2025)), index=1, key="year-select")
    
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
                        y=alt.Y(f'{_selection_RRP}:Q', title='Trade Price',
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
                        y=alt.Y(f'{_selection_RRP}:Q', title='Trade Price',
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

                else:
                    st.warning("Please select one statistic to display the plot.")
            else:
                st.warning("Please provide a valid file path to load data.")
        else:
            st.warning("Please select a region to analyse.")

### Chart 6: Trade Price for selected_region in 2022 (Monday 30 May – Sunday 12 June​)
### x-axis: day, x-range: 5 minutes, y-axis: mean, median, min, max
with st.container():
    st.subheader(f"Trade Price for {selected_region} in Monday 30 May – Sunday 12 June 2022")

    # col1, _ = st.columns([0.22, 0.78])

    # with col1:
    #     date_range = st.date_input("Select the date range to display the data", 
    #                         [pd.to_datetime('2022-05-30'), pd.to_datetime('2022-06-12')], 
    #                         key="date-range")
    #     # date_range is (datetime.date(2022, 5, 30), datetime.date(2022, 6, 12))
    #     start_date, end_date = date_range

    start_date = datetime.date(2022, 5, 30)
    end_date = datetime.date(2022, 6, 12)

    all_disptach, daily = st.tabs(["All", "Daily"])

    with all_disptach:
        # input select box for date
        col2, _ = st.columns([0.3, 0.7])
        with col2:
            selected_date_range = st.slider("Select date range to display the data", start_date, end_date, 
                                            (start_date, end_date), format="YYYY-MM-DD", key="date-slider")
            start_date, end_date = selected_date_range
        
        file_path = f"data/analysis/PRICE_AND_DEMAND_ALL_YEARS_{selected_region}.csv"
        if selected_region:
            data = load_data(file_path, date_column='SETTLEMENTDATE')
            data["SETTLEMENTDATE"] = pd.to_datetime(data["SETTLEMENTDATE"])
            if data is not None:
                # based on the start_date and end_date to filter the data
                data = data[(data['SETTLEMENTDATE'].dt.date >= start_date) 
                            & (data['SETTLEMENTDATE'].dt.date <= end_date)]
                
                base = alt.Chart(data).encode(
                    x=alt.X('SETTLEMENTDATE', title="Date", axis=alt.Axis(labelAngle=0),
                            scale=alt.Scale(domain=alt.selection_interval(bind='scales')), # Enables scrolling
                            )  
                )
                
                rrp_line = base.mark_line(color='red').encode(
                    y=alt.Y(f'RRP', title='Trade Price',
                            scale=alt.Scale(zero=False, nice=True)),
                    tooltip=['SETTLEMENTDATE', f'RRP']
                )
                
                demand_line = base.mark_line(color='blue', strokeDash=(5,5)).encode(
                    y=alt.Y(f'TOTALDEMAND', title='Total Demand',
                            scale=alt.Scale(zero=False, nice=True)),
                    tooltip=['SETTLEMENTDATE', f'TOTALDEMAND']
                )
                
                chart = alt.layer(rrp_line, demand_line).resolve_scale(
                    y='independent'
                ).interactive()

                st.altair_chart(chart, theme="streamlit", use_container_width=True)
            else:
                st.warning("Please provide a valid file path to load data.")
        else:
            st.warning("Please select a region to analyse.")


    with daily:

        # select statistic
        option = ['mean', 'median', 'min', 'max']
        selection = st.pills("Select a statistic to display", 
                            option, 
                            selection_mode='single', 
                            default=['median'],
                            key="by_day_range")
        
        file_path = f"data/analysis/PRICE_AND_DEMAND_ALL_YEARS_{selected_region}.csv"
        if selected_region:
            data = load_data(file_path, date_column='SETTLEMENTDATE')
            data["SETTLEMENTDATE"] = pd.to_datetime(data["SETTLEMENTDATE"])
            if data is not None:
                # based on the start_date and end_date to filter the data
                data = data[(data['SETTLEMENTDATE'].dt.date >= start_date) 
                            & (data['SETTLEMENTDATE'].dt.date <= end_date)]
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
                        y=alt.Y(f'{_selection_RRP}:Q', title='Trade Price',
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

                    st.altair_chart(chart, theme="streamlit", use_container_width=True)

                else:
                    st.warning("Please select one statistic to display the plot.")
            else:
                st.warning("Please provide a valid file path to load data.")
        else:
            st.warning("Please select a region to analyse.")
        
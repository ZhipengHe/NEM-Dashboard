import os
import streamlit as st
import pandas as pd
import altair as alt
import warnings
import datetime
warnings.filterwarnings("ignore", message="Could not infer format, so each element will be parsed individually")


st.title("Topic 1: Price Anomaly Detection")


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




# Sidebar
st.sidebar.title("Price Anomaly Detection")
st.sidebar.write("Please select a region to analyse the trade price data.")
selected_region = st.sidebar.selectbox("Select a region:", REGIONS, index=1)


# Main content

### Chart: Trade Price for selected_region in 2022 (Monday 30 May – Sunday 12 June​)
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
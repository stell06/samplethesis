import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px

# Read data from a CSV file (replace with your actual data source)
df = pd.read_csv("waterlevel.csv")

# Check for required columns
if "water_level" not in df.columns:
    st.error("The 'water_level' column is not present in the DataFrame.")
    st.stop()

st.set_page_config(
    page_title="Flood Monitoring Dashboard",
    page_icon="",  # You can replace this with your actual icon
    layout="wide",
)

# Add logo and associated text
logo_col, text_col = st.columns([2, 6])

# Replace "your_logo.png" with the actual file path or URL of your logo
logo_col.image("logo.png", width=200)  # Adjust width as needed

# Add associated text
text_col.title("Flood Monitoring Repository in Hinaguimitan River")
text_col.write("Hinaguimitan River, Brgy. San Juan, Sison, Surigao del Norte.")

# Adjust spacing between logo and text
text_col.markdown("&nbsp;")  # Add a non-breaking space for spacing

st.title("Dashboard")

# Ensure timestamp column is in datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Initialize filtered_df as a copy of df
filtered_df = df.copy()

placeholder = st.empty()

# Calculate key metrics
avg_water_level = np.mean(filtered_df["water_level"])
avg_humidity = np.mean(filtered_df["humidity"])
avg_temperature = np.mean(filtered_df["temperature"])

with placeholder.container():
    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        label="Water Level",
        value=round(avg_water_level, 2),
        delta=round(avg_water_level) - 10,
    )
    kpi2.metric(
        label="Humidity", value=int(avg_humidity), delta=-10 + int(avg_humidity)
    )
    kpi3.metric(
        label="Temperature",
        value=round(avg_temperature, 2),
        delta=-round(avg_temperature / avg_humidity) * 100,
    )

    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Water Level Over Time")
        fig = px.line(data_frame=filtered_df, y="water_level", x="timestamp")
        st.plotly_chart(fig, use_container_width=True)  # Adjust width to fit the column
    with fig_col2:
        st.markdown("### Humidity and Temperature Distribution")
        fig2 = px.scatter(data_frame=filtered_df, x="humidity", y="temperature")
        st.plotly_chart(fig2, use_container_width=True)  # Adjust width to fit the column

    st.markdown("### Detailed Data View")
    date_filter_col = st.columns(2)
    start_date = date_filter_col[0].date_input("Start Date", value=None)
    end_date = date_filter_col[1].date_input("End Date", value=None)

    # Filter data based on selected date range (if dates are provided)
    if start_date is not None and end_date is not None:
        # Convert start_date and end_date to datetime objects for comparison
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)
        filtered_df = df[
            (df["timestamp"] >= start_datetime) & (df["timestamp"] <= end_datetime)
        ]
    else:
        filtered_df = df.copy()

    st.dataframe(filtered_df, use_container_width=True)  # Adjust width to fit the screen

    # Download button for the filtered data
    st.download_button(
        label="Download Filtered Data",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_environmental_data.csv",
        mime="text/csv",
        key="download_button_filtered",
    )

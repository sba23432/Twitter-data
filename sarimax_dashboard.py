import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Page config
st.set_page_config(page_title="SARIMAX Forecast Dashboard", layout="wide")

# Title
st.title("Energy Load Forecast Dashboard using SARIMAX")
st.markdown("---")

# Load and parse the CSV
forecast_df = pd.read_csv("sarimax_forecast_results.csv")
forecast_df['timestamp'] = pd.to_datetime(forecast_df['timestamp'])  # Ensure timestamp is parsed

# Sidebar selection
horizon = st.sidebar.selectbox(
    "Select Forecast Horizon",
    [24, 72, 168],
    format_func=lambda x: f"{x//24}-Day Ahead"
)

# Filter data based on selected forecast horizon
filtered = forecast_df[forecast_df['horizon'] == horizon]

# Plot
st.subheader(f"Forecast vs Actual — {horizon//24}-Day Ahead")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered['timestamp'], filtered['actual'], label='Actual', linewidth=2)
ax.plot(filtered['timestamp'], filtered['forecast'], label='Forecast', linestyle='--')

# Improve X-axis formatting
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:%M'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
fig.autofmt_xdate()

ax.set_title(f"{horizon//24}-Day Ahead Energy Forecast", fontsize=14)
ax.set_xlabel("Time")
ax.set_ylabel("Load (MW)")
ax.legend()
st.pyplot(fig)

# Forecast Table
st.subheader("Forecast Table")
st.dataframe(filtered[['timestamp', 'actual', 'forecast']].round(2))

# RMSE Metric
rmse_val = ((filtered['actual'] - filtered['forecast'])**2).mean()**0.5
st.metric(f"RMSE for {horizon//24}-Day Ahead Forecast", f"{rmse_val:.2f} MW")

# Tufte Design Explanation
st.markdown("""
### Dashboard Design & Tufte Principles
This dashboard adheres to Tufte's principles of effective visualization:
- **Data-Ink Ratio**: Only essential elements (actual and forecast lines) are visualized.
- **Small Multiples**: Horizon selection enables targeted comparisons across forecast windows.
- **Clarity**: RMSE is shown directly with minimal clutter.
- **Data Density**: Tables and plots maximize insight per pixel.
""")

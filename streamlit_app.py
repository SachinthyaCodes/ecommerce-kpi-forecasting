import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data ---
kpis = pd.read_csv('ecommerce-kpi-forecasting/data/monthly_kpis.csv')
revenue_forecast = pd.read_csv('ecommerce-kpi-forecasting/data/revenue_forecast.csv')        
quantity_forecast = pd.read_csv('ecommerce-kpi-forecasting/data/quantity_forecast.csv')
orders_forecast = pd.read_csv('ecommerce-kpi-forecasting/data/orders_forecast.csv')


# --- Convert Dates ---
kpis['Month'] = pd.to_datetime(kpis['Month'])
revenue_forecast['ds'] = pd.to_datetime(revenue_forecast['ds'])
quantity_forecast['ds'] = pd.to_datetime(quantity_forecast['ds'])
orders_forecast['ds'] = pd.to_datetime(orders_forecast['ds'])

# --- Streamlit Layout ---
st.set_page_config(page_title="KPI Forecast Dashboard", layout="wide")
st.title("Financial KPI Forecasting Dashboard")

# --- Sidebar Controls ---
kpi_choice = st.sidebar.selectbox("Select KPI", ["Total Revenue", "Total Quantity", "Total Orders"])

# --- KPI Metadata ---
kpi_col_map = {
    "Total Revenue": "TotalRevenue",
    "Total Quantity": "TotalQuantity",
    "Total Orders": "TotalOrders"
}
kpi_explanations = {
    "Total Revenue": "**Total Revenue** is the total amount of sales (in monetary terms) recorded each month.",
    "Total Quantity": "**Total Quantity** represents the total number of units sold each month.",
    "Total Orders": "**Total Orders** refers to the number of unique transactions or invoices per month."
}
forecast_map = {
    "Total Revenue": revenue_forecast,
    "Total Quantity": quantity_forecast,
    "Total Orders": orders_forecast
}

forecast_col = kpi_col_map[kpi_choice]
forecast_df = forecast_map[kpi_choice]

# --- KPI Description ---
st.markdown(kpi_explanations[kpi_choice])

# --- Expandable Help Section ---
with st.expander("ℹ️ How to use this dashboard"):
    st.markdown("""
    - Select a KPI from the sidebar.
    - View historical trends and future forecasts.
    - Use the **Summary Insights** to quickly grasp key numbers.
    - Forecasts are statistical estimates using time series models.
    """)

# --- Summary Metrics ---
latest_actual = kpis[forecast_col].iloc[-1]
forecast6 = forecast_df['yhat'].tail(6).sum()
historical_avg = kpis[forecast_col].tail(6).mean()
growth_pct = ((forecast6 / (historical_avg * 6)) - 1) * 100

st.markdown("### Summary Insights")
col1, col2, col3 = st.columns(3)
col1.metric("Latest Actual", f"{latest_actual:,.0f}")
col2.metric("6-Month Forecast", f"{forecast6:,.0f}")
col3.metric("Growth vs Past Avg", f"{growth_pct:.2f} %")

# --- Tabs for Charts and Data ---
tab1, tab2 = st.tabs(["KPI Trend & Forecast", "Forecast Table"])

with tab1:
    # Historical Chart
    fig_hist = px.line(
        kpis, 
        x='Month', 
        y=forecast_col, 
        title=f"Historical Trend - {kpi_choice}",
        labels={'Month': 'Month', forecast_col: kpi_choice}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Forecast Chart with Better Labels
    fig_forecast = px.line(
        forecast_df,
        x='ds',
        y='yhat',
        title=f"Forecast for {kpi_choice}",
        labels={'ds': 'Month', 'yhat': f'{kpi_choice} (Forecast)'}
    )
    fig_forecast.update_traces(line=dict(color='green', width=2))
    fig_forecast.update_layout(
        xaxis_title="Month",
        yaxis_title=kpi_choice,
        legend_title="",
        title_x=0.1
    )
    st.plotly_chart(fig_forecast, use_container_width=True)

with tab2:
    st.markdown("#### Forecasted Values")
    display_df = forecast_df[['ds', 'yhat']].copy()
    display_df.columns = ['Month', kpi_choice]
    display_df[kpi_choice] = display_df[kpi_choice].round(0).astype(int)
    st.dataframe(display_df.tail(6), use_container_width=True, hide_index=True)

# --- Footer ---
st.markdown("---")
st.caption("Built with Streamlit | Model: Prophet | Developer: Sachinthya | Data: Retail E-commerce Sales")

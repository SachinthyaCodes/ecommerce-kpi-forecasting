import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Load Data ---
kpis = pd.read_csv('../data/monthly_kpis.csv')
revenue_forecast = pd.read_csv('../data/revenue_forecast.csv')        
quantity_forecast = pd.read_csv('../data/quantity_forecast.csv')
orders_forecast = pd.read_csv('../data/orders_forecast.csv')

# ARIMA forecasts
revenue_arima = pd.read_csv('../data/arima_revenue_forecast.csv')
quantity_arima = pd.read_csv('../data/quantity_arima_forecast.csv')
orders_arima = pd.read_csv('../data/orders_arima_forecast.csv')

# --- Convert Dates ---
kpis['Month'] = pd.to_datetime(kpis['Month'])
revenue_forecast['ds'] = pd.to_datetime(revenue_forecast['ds'])
quantity_forecast['ds'] = pd.to_datetime(quantity_forecast['ds'])
orders_forecast['ds'] = pd.to_datetime(orders_forecast['ds'])
revenue_arima['Month'] = pd.to_datetime(revenue_arima['Month'])
quantity_arima['Month'] = pd.to_datetime(quantity_arima['Month'])
orders_arima['Month'] = pd.to_datetime(orders_arima['Month'])

# --- Streamlit Layout ---
st.set_page_config(page_title="📊 KPI Forecast Dashboard", layout="wide")
st.title("📊 Financial KPI Forecasting Dashboard")

# --- Sidebar Controls ---
kpi_choice = st.sidebar.selectbox("📌 Select KPI", ["Total Revenue", "Total Quantity", "Total Orders"])
model_choice = st.sidebar.radio("🔮 Forecasting Model", ["Prophet", "ARIMA"])

# --- KPI Metadata ---
kpi_col_map = {
    "Total Revenue": "TotalRevenue",
    "Total Quantity": "TotalQuantity",
    "Total Orders": "TotalOrders"
}
kpi_explanations = {
    "Total Revenue": "🧾 **Total Revenue** is the total amount of sales (in monetary terms) recorded each month.",
    "Total Quantity": "📦 **Total Quantity** represents the total number of units sold each month.",
    "Total Orders": "🧾 **Total Orders** refers to the number of unique transactions or invoices per month."
}
forecast_map = {
    "Total Revenue": (revenue_forecast, revenue_arima),
    "Total Quantity": (quantity_forecast, quantity_arima),
    "Total Orders": (orders_forecast, orders_arima)
}
forecast_col = kpi_col_map[kpi_choice]
forecast_df, arima_df = forecast_map[kpi_choice]

# --- KPI Description ---
st.markdown(kpi_explanations[kpi_choice])

# --- Expandable Help Section ---
with st.expander("ℹ️ How to use this dashboard"):
    st.markdown("""
    - Select a KPI and forecasting model from the sidebar.
    - View historical trends and future forecasts.
    - Use the **Summary Insights** to quickly grasp key numbers.
    - Forecasts are statistical estimates using time series models.
    """)

# --- Summary Metrics ---
latest_actual = kpis[forecast_col].iloc[-1]
forecast6 = (
    forecast_df['yhat'].tail(6).sum()
    if model_choice == "Prophet"
    else arima_df[arima_df['Month'] > kpis['Month'].max()][arima_df.columns[-1]].sum()
)
historical_avg = kpis[forecast_col].tail(6).mean()
growth_pct = ((forecast6 / (historical_avg * 6)) - 1) * 100

st.markdown("### 📌 Summary Insights")
col1, col2, col3 = st.columns(3)
col1.metric("📅 Latest Actual", f"{latest_actual:,.0f}")
col2.metric("📈 6-Month Forecast", f"{forecast6:,.0f}")
col3.metric("📊 Growth vs Past Avg", f"{growth_pct:.2f} %")

# --- Tabs for Charts and Data ---
tab1, tab2 = st.tabs(["📈 KPI Trend & Forecast", "🔍 Forecast Table"])

with tab1:
    # Historical Chart
    fig_hist = px.line(kpis, x='Month', y=forecast_col, title=f"📈 Historical Trend - {kpi_choice}")
    st.plotly_chart(fig_hist, use_container_width=True)

    # Forecast Chart
    if model_choice == "Prophet":
        fig_prophet = px.line(forecast_df, x='ds', y='yhat', title=f"🔮 Prophet Forecast - {kpi_choice}")
        st.plotly_chart(fig_prophet, use_container_width=True)
    else:
        historical = kpis[['Month', forecast_col]].copy()
        last_month = historical['Month'].max()
        forecast = arima_df[arima_df['Month'] >= last_month]
        arima_col = arima_df.columns[-1]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=historical['Month'], y=historical[forecast_col],
                                 mode='lines', name='Historical', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=forecast['Month'], y=forecast[arima_col],
                                 mode='lines', name='ARIMA Forecast', line=dict(dash='dash', color='red')))
        fig.update_layout(
            title=f"🔮 ARIMA Forecast - {kpi_choice}",
            xaxis_title="Month",
            yaxis_title=kpi_choice,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("#### 🔍 Forecasted Values")

    if model_choice == "Prophet":
        display_df = forecast_df[['ds', 'yhat']].copy()
        display_df.columns = ['Month', kpi_choice]
    else:
        display_df = arima_df[arima_df['Month'] > kpis['Month'].max()][['Month', arima_df.columns[-1]]].copy()
        display_df.columns = ['Month', kpi_choice]

    display_df[kpi_choice] = display_df[kpi_choice].round(0).astype(int)
    st.dataframe(display_df.tail(6), use_container_width=True, hide_index=True)

# --- Footer ---
st.markdown("---")
st.caption("✅ Built with Streamlit | Models: Prophet & ARIMA | Developer: Sachinthya | Data: Retail E-commerce Sales")

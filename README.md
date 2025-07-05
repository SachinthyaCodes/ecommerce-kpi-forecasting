# Financial KPI Forecasting Dashboard

A real-world time series forecasting project to predict key performance indicators (KPIs) for a retail e-commerce business. This interactive dashboard was built using **Prophet**, **Pandas**, and **Streamlit**, designed to assist business stakeholders in making data-driven decisions by forecasting sales, quantity, and order volumes.

---

## Project Overview

In today's competitive business landscape, **accurate forecasting of financial metrics** is critical for demand planning, inventory control, and revenue optimization. This project builds a forecasting system using real transactional data from an online retailer and presents it through a user-friendly dashboard.

---

## Key Objectives

- Clean and transform raw retail sales data into meaningful KPIs
- Use **Prophet time series models** to forecast:
  - Total Revenue
  - Total Quantity Sold
  - Total Orders
- Present historical trends and future projections in an interactive dashboard using **Streamlit**
- Empower users to interpret and compare forecast vs actual KPI performance

---

## Project Structure

```
ecommerce-kpi-forecasting
├── app/
│   └── streamlit_app.py         # Streamlit dashboard code
├── data/
│   ├── ecommerce_data.csv       # Original cleaned dataset
│   ├── monthly_kpis.csv         # Aggregated monthly KPIs
│   ├── revenue_forecast.csv     # Prophet forecast for revenue
│   ├── quantity_forecast.csv    # Prophet forecast for quantity
│   ├── orders_forecast.csv      # Prophet forecast for orders
│   ├── arima_revenue_forecast.csv
│   ├── orders_arima_forecast.csv
│   └── quantity_arima_forecast.csv
├── models/                      # Saved model files
├── notebooks/
│   └── 01_data_cleaning_eda.ipynb  # Data cleaning and KPI calculation
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## Forecasting Approach

We use **Facebook Prophet**, a robust and easy-to-use time series forecasting library, ideal for business data. It automatically handles:

- Trends
- Seasonality
- Holiday effects
- Missing values and outliers

> Prophet is especially powerful for data with strong seasonal patterns — like sales.

---

##  KPIs Forecasted

| KPI             | Description |
|------------------|-------------|
| **Total Revenue** | Total sales revenue per month |
| **Total Quantity** | Number of units sold |
| **Total Orders**   | Number of unique invoices per month |

All KPIs are derived from real e-commerce transactions.

---

##  Tools & Technologies

| Category        | Stack |
|------------------|-------|
| **Data Handling** | `Pandas`, `NumPy` |
| **Time Series Model** | `Facebook Prophet` |
| **Dashboard** | `Streamlit`, `Plotly` |
| **Forecast Evaluation** | `sklearn.metrics` (MSE) |

---

##  Dashboard Preview

> Accessible via: `streamlit run app/streamlit_app.py`

### Main Features:
- Visualize KPI trends over time
- 6-month forecast using Prophet
- Summary metrics like growth rate vs past average
- Table of future values with download/export potential

▶️[Dashboard Demo](https://youtu.be/kAJ2TPjXUhU)

---

##  How to Run Locally

### 1. Clone the Repo
```bash
git clone https://github.com/SachinthyaCodes/ecommerce-kpi-forecasting.git
cd ecommerce-kpi-forecasting
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

If prophet fails on Windows, try:
```bash
pip install prophet --force-reinstall --no-binary :all:
```

### 3. Run the App
```bash
streamlit run app/streamlit_app.py
```

---

##  Results Summary

| KPI | Model Used | MSE (last 6 months) | Notes |
|-----|------------|---------------------|-------|
| Total Revenue | Prophet | Lower than ARIMA | Prophet performed better |
| Total Quantity | Prophet | Accurate and stable | |
| Total Orders | Prophet | Stable forecast | |

ARIMA was tested but Prophet was selected for its superior accuracy, flexibility, and usability.

---

##  Key Learnings

- Handling real-world messy transactional data
- Building robust forecasting pipelines with Prophet
- Creating end-to-end, deployable dashboards with Streamlit
- Evaluating models with real KPIs like MSE
- Translating technical insights into business-friendly visuals

---

##  Author

**Sachinthya Lakshitha**   
Reach me on [LinkedIn](https://www.linkedin.com/in/sachinthya-lakshitha/) or sachinthyaofficial@gmail.com

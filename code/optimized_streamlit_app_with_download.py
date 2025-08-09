import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet
from io import BytesIO

# Title
st.title("?? Stock Market Forecasting App")
st.markdown("Forecast stock prices using Facebook Prophet with interactive charts and CSV export.")

# Sidebar - User input
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g. AAPL, MSFT)", value="AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2015-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Download Data
@st.cache_data
def load_data(ticker):
    return yf.download(ticker, start=start_date, end=end_date)

data = load_data(ticker)
if data.empty:
    st.error("No data found. Try a different stock ticker or date range.")
    st.stop()

# Display raw data
st.subheader("Raw Stock Data")
st.write(data.tail())

# Plot closing price
st.subheader("Closing Price Chart")
st.line_chart(data["Close"])

# Forecasting with Prophet
df_train = data.reset_index()[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})

model = Prophet()
model.fit(df_train)

future = model.make_future_dataframe(periods=180)
forecast = model.predict(future)

# Show forecast chart
st.subheader("Forecast Chart")
fig1 = model.plot(forecast)
st.pyplot(fig1)

# Forecast components
st.subheader("Forecast Components")
fig2 = model.plot_components(forecast)
st.pyplot(fig2)

# CSV Download
st.subheader("?? Download Forecast as CSV")

def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

csv_data = convert_df(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]])

st.download_button(
    label="Download Forecast CSV",
    data=csv_data,
    file_name=f"{ticker}_forecast.csv",
    mime="text/csv"
)

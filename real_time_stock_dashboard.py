import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import logging
import time
from typing import Optional

#...............configuration..............#

st.set_page_config(page_title="real-time stock dashboard", layout="wide")
update_frequency = 60 # in sec
CACHE_EXPIRY = 300 #  5-minute cache
MAX_ENTRIES = 3 # api retries
PRICE_ALERTS = {} #user defined alerts

#.............LOGGING SETUP ..............#
logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")

def log_message(level,message):
    """logs message at different levels: info, warning, error"""
    if level == "error":
        logging.error(f"[error] {message}")
    elif level == "warning":
        logging.warning(f"[warning] {message}")
    else:
        logging.info(f"[info] {message}")

#..........CACHING MECHANISM ............#
@st.cache_resource(ttl = CACHE_EXPIRY)
def get_stock_data(ticker: str) -> pd.DataFrame:
    """fetch historical data with caching"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period = "6mo")
        if df.empty:
            raise ValueError("received empty dataset fro api")
        df.reset_index(inplace = True)
        return df
    except Exception as e:
        log_message("error",f"failed to fetch data for {ticker}: {e} ")
        return pd.DataFrame()

@st.cache_resource(ttl=update_frequency)
def get_stock_price(ticker: str) -> Optional[float]:
    """fetch real-time stock price with retries"""
    for attempt in range(MAX_ENTRIES):
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period = "1d",interval='1m').iloc[-1]['Close']
            if pd.isna(price):
                raise ValueError("invalid price data received")
            return price
        except Exception as e:
            log_message("message", f"Retrying {ticker} ({attempt+1}/{MAX_ENTRIES})): {e}")
            time.sleep(2 ** attempt)
    log_message("error", f"failed to fetch real time price for {ticker} ")
    return None
#..............CHART FUNCTIONS..........#
def create_figure() -> go.Figure:
    """create an empty plotly figure"""
    return go.Figure()

def plot_chart(df: pd.DataFrame,title: str, chart_type: str) -> go.Figure:
    """Generate stock charts dynamically based on the selected type"""
    if df.empty:
        return create_figure()
    fig = create_figure()
    if chart_type == "candlestick":
        fig.add_trace(go.Candlestick(
            x=df.index,open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],
            increasing_line_color = 'green', decreasing_line_color = 'red'
        ))
    else:
        fig.add_trace(go.Scatter(x=df['Date'],y= df['Close'],mode = 'lines',name = 'stock price'))
        fig.update_layout(title=title,xaxis_title="date",yaxis_title="price")
    return fig

#............UI LAYOUT.........#

def main():
    """main function to render the streamlit dashboard UI """
    st.title("Real-Time Stock Market Dashboard")
    st.sidebar.header("Stock Selection")
    stocks = st.sidebar.multiselect("select stocks:",["AAPL","TSLA","MSFT","GOOGL","AMAZN"],default=["AAPL"])

    for stock in stocks:
        st.subheader(f"{stock} stock performance")
        df = get_stock_data(stock)
        if not df.empty:
            col1,col2 = st.columns(2)
            col1.plotly_chart(plot_chart(df,f"{stock}-line chart","line"),use_container_width=True)
            col1.plotly_chart(plot_chart(df, f"{stock}-Candlestick Chart", "candlestick"), use_container_width=True)
            current_price = get_stock_price(stock)
            if current_price:
                st.metric(label=f"{stock} current price",value=f"${current_price: .2f}")
            else:
                st.error(f"could not load data for {stock}.")
                st.divider()

if __name__ == "__main__":
   main()































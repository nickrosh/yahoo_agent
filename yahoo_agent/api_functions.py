import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit as st

SPGCI = False

def get_stock_df(symbol: str, days_ago: int):
    ticker = yf.Ticker(symbol)
    if not ticker:
        print(f'BAD TICKER {symbol}')
        raise NameError(f"Ticker {symbol} not found")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    historical_data = ticker.history(start=start_date, end=end_date)
    return historical_data


def get_commodity_df(symbol: str, days_ago: int):
    raise NotImplementedError('Need the SPGCI Key')


def get_data_df(symbol: str, days_ago: int):
    if SPGCI:
        return get_commodity_df(symbol, days_ago)
    else:
        return get_stock_df(symbol, days_ago)


def get_todays_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return round(todays_data['Close'].iloc[0], 2)


def generate_candlestick(df, symbol, days_ago):
    fig = go.Figure(layout_title_text=f'{symbol} over {days_ago} days',
        data=[
        go.Candlestick(name=symbol,
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
    )])
    fig.update_xaxes(rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
        dict(values=["2015-12-25", "2016-01-01"]),  # hide Christmas and New Year's
    ],
    title_text='Date',
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1D", step="day", stepmode="backward"),
            dict(count=5, label="5D", step="day", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
    )
    fig.update_yaxes(title_text='Stock Price')
    return fig


def get_price_change_percent(symbol, days_ago):
    historical_data = get_data_df(symbol, days_ago)
    old_price = historical_data['Close'].iloc[0]
    new_price = historical_data['Close'].iloc[-1]
    percent_change = ((new_price - old_price) / old_price) * 100
    fig = generate_candlestick(df=historical_data, symbol=symbol, days_ago=days_ago)
    st.plotly_chart(fig, use_container_width=True)
    return round(percent_change, 2)


def get_simple_moving_average(symbol, days_ago, span):
    historical_data = get_data_df(symbol, days_ago+max(span))
    fig = generate_candlestick(df=historical_data, symbol=symbol, days_ago=days_ago)

    for val in span:
        historical_data[f'{val} SMA'] = historical_data['Close'].rolling(val).mean()
        fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data[f'{val} SMA'], mode='lines', name=f'{val} SMA'))
    st.plotly_chart(fig, use_container_width=True)
    # old_SMA = historical_data['SMA'].iloc[0]
    # new_SMA = historical_data['SMA'].iloc[-1]
    # percent_change = ((new_SMA - old_SMA) / old_SMA) * 100
    # return round(percent_change, 2)


def get_exponential_moving_average(symbol, days_ago, span):
    historical_data = get_data_df(symbol, days_ago+max(span))
    fig = generate_candlestick(df=historical_data, symbol=symbol, days_ago=days_ago)

    for val in span:
        historical_data[f'{val} EMA'] = historical_data['Close'].ewm(span=val).mean()
        fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data[f'{val} EMA'], mode='lines', name=f'{val} EMA'))
    st.plotly_chart(fig, use_container_width=True)
    # old_EMA = historical_data['EMA'].iloc[0]
    # new_EMA = historical_data['EMA'].iloc[-1]
    # percent_change = ((new_EMA - old_EMA) / old_EMA) * 100
    # return round(percent_change, 2)


def get_best_performing(stocks, days_ago):
    best_stock = None
    best_performance = None
    fig = go.Figure()

    for stock in stocks:
        try:
            historical_data = get_data_df(stock, days_ago)
            old_price = historical_data['Close'].iloc[0]
            new_price = historical_data['Close'].iloc[-1]
            performance = ((new_price - old_price) / old_price) * 100
            fig.add_trace(go.Scatter(
                x=historical_data.index, 
                y=historical_data['Close'],
                mode='lines',
                name=f'{stock}'
                ))
            if best_performance is None or performance > best_performance:
                best_stock = stock
                best_performance = performance
        except Exception as e:
            print(f'Could not calculate performance for {stock}: {e}')
    fig.update_xaxes(rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
        dict(values=["2015-12-25", "2016-01-01"]),  # hide Christmas and New Year's
    ],
    title_text='Date',
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1D", step="day", stepmode="backward"),
            dict(count=5, label="5D", step="day", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
    )
    fig.update_yaxes(title_text='Stock Price')
    st.plotly_chart(fig, use_container_width=True)
    return best_stock, best_performance

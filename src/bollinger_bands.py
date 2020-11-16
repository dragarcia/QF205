import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime

def get_prices(ticker,startdate,enddate):
    prices_df = web.get_data_yahoo(ticker,
                               start = startdate,
                               end = enddate)
    prices_df = prices_df.drop(columns=['High', 'Low','Open','Close','Volume'])
    return prices_df

def bollinger_bands(prices,ticker):
    prices['20 Day MA'] = prices['Adj Close'].rolling(window=20).mean()
    
    # set .std(ddof=0) for population std instead of sample
    prices['20 Day STD'] = prices['Adj Close'].rolling(window=20).std() 
    
    prices['Upper Band'] = prices['20 Day MA'] + (prices['20 Day STD'] * 1.96)
    prices['Lower Band'] = prices['20 Day MA'] - (prices['20 Day STD'] * 1.96)

    # Simple Plot
    # set style, empty figure and axes
    plt.style.use('fivethirtyeight')
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(111)

    # Get index values for the X axis for facebook DataFrame
    x_axis = prices.index.get_level_values(0)

    # Plot shaded 21 Day Bollinger Band for Facebook
    ax.fill_between(x_axis, prices['Upper Band'], prices['Lower Band'], color='grey')

    # Plot Adjust Closing Price and Moving Averages
    ax.plot(x_axis, prices['Adj Close'], color='blue', lw=2)
    ax.plot(x_axis, prices['20 Day MA'], color='black', lw=2)

    # Set Title & Show the Image
    ax.set_title('20 Day Bollinger Band For ' + ticker)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price(USD)')
    ax.legend(prices[['Adj Close', '20 Day MA']])
    plt.show()


def main():
    
    ticker = input("Please input the stock ticker:").upper()
    startdate = input("Please input the start date in YYYY-MM-DD format:")
    enddate = input("Please input the end date in YYYY-MM-DD format:")

    prices = get_prices(ticker,startdate,enddate)
    bollinger_bands(prices,ticker)

if __name__ == "__main__":
    main()

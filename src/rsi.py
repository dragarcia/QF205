import pandas_datareader.data as web
import matplotlib.pyplot as plt


def rsi(ticker, startdate, enddate):
    # Window length for moving average
    window_length = 14

    # Get data
    # data = web.DataReader('AAPL', 'yahoo', startdate, enddate)
    data = web.DataReader(ticker, 'yahoo', startdate, enddate)
    # Get just the adjusted close
    close = data['Adj Close']
    # Get the difference in price from previous step
    delta = close.diff()
    # Get rid of the first row, which is NaN since it did not have a previous
    # row to calculate the differences
    delta = delta[1:]

    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the EWMA
    roll_up1 = up.ewm(span=window_length).mean()
    roll_down1 = down.abs().ewm(span=window_length).mean()

    # Calculate the RSI based on EWMA
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))

    # Calculate the SMA
    roll_up2 = up.rolling(window_length).mean()
    roll_down2 = down.abs().rolling(window_length).mean()

    # Calculate the RSI based on SMA
    RS2 = roll_up2 / roll_down2
    RSI2 = 100.0 - (100.0 / (1.0 + RS2))

    # Compare graphically
    plt.figure(figsize=(8, 6))
    RSI1.plot()
    RSI2.plot()
    plt.legend(['RSI via EWMA', 'RSI via SMA'])
    plt.show()


def main():
    ticker = input("Please input the stock ticker:").upper()
    startdate = input("Please input the start date in YYYY-MM-DD format:")
    enddate = input("Please input the end date in YYYY-MM-DD format:")

    rsi(ticker, startdate, enddate)


if __name__ == "main":
    main()

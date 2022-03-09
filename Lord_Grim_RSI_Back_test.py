import ccxt
import pandas as pd
import pandas_ta as ta
from portfolio_class_def import *  # (important class that can be copied at eh top before (#1) or you can download the file to your python path/project)
import numpy as np
import array
import matplotlib.pyplot as plt

# 1. Call financial data from binance us (because USD)
exchange = ccxt.binanceus()
# 2. This records our OHLCV (Open, High, Low, Close, Volume) data. 'currency', 'kline stick frame', 'number of data points'

# choose your currency
currency = str(input('What would you like to buy and sell today? Remember it has to be a buying pair for crypto')).upper()
# pick your Kline time frame
kline_sticks = str(input("Pick a timeframe: 1m, 5m, 1h, 1M etc"))
data_points = int(input("How many data points would you like?"))

markets = exchange.fetch_ohlcv(currency, kline_sticks, limit = data_points)
# 3. Puts the data into a data frame
tframe = pd.DataFrame(data = markets, columns = ['time', 'O', 'H', 'L', 'C', 'V'])
# 4. Specific closing prices
caesar = tframe['C']
# 5. Refactor RSI column into dataframe

tframe['RSI'] = ta.rsi(close = tframe['C'], talib = None, length = 14)
currency_x_axis = np.arange(0, data_points)
currency_y_axis = caesar
price_graph = plt.subplot(1, 2, 1)
price_graph.set_title(f'{currency}, price graph')
plt.plot(currency_x_axis, currency_y_axis)

ta_x_axis = np.arange(0, data_points)
ta_y_axis = tframe['RSI']

rsi_graph = plt.subplot(1, 2, 2)
rsi_graph.set_title(f'{currency}, RSI graph')
plt.plot(ta_x_axis, ta_y_axis)
plt.show()

# 6. Initialize portfolio values
beta, delta = None, None

beta = float(input("How much money do we have to start to invest?"))
delta = float(input("How much crypto do we currently have?"))
alpha = Portfolio(cash_to_invest = beta, holding_amt = delta)
buys = 0
sells = 0

# 7. How much to buy or sell
d_inv = float(input("When buying what is the percentage of your investing cash you'd stake on each data point?")) * alpha.cash_to_invest
a_sell = float(input("What is the percent of your portfolio you would like to sell?")) * alpha.holding_amt

# 8. RSI strategy logic
buy_signal = float(input("What is your RSI buy signal?"))
sell_signal = float(input("What is your RSI sell signal?"))
price_array = []
history = []
for i in tframe.index:

    if tframe['RSI'][i] <= buy_signal:
        alpha.buy_asset(invest_amt = float(d_inv), asset_price = tframe['C'][i])
        buys += 1
        price_array.append((alpha.holding_amt * tframe['C'][i] + alpha.cash_to_invest))
        last_price = tframe['C'][i]
        history.append(f'RSI Buy, buy number {buys}. Price : {last_price}')
    elif tframe['RSI'][i] >= sell_signal:
        alpha.sell_asset(sell_amt = float(a_sell), asset_price = tframe['C'][i])
        sells += 1
        price_array.append((alpha.holding_amt * tframe['C'][i] + alpha.cash_to_invest))
        last_price = tframe['C'][i]
        history.append(f'RSI Sell, sell number {sells}. Price : {last_price}')
    else:
        price_array.append((alpha.holding_amt * tframe['C'][i] + alpha.cash_to_invest))
        last_price = tframe['C'][i]
        history.append(f'RSI Sell, sell number {sells}. Price : {last_price}')

final_point = int(data_points - 1)
final_sell = alpha.holding_amt
print(
    f'We ended up holding {round(alpha.holding_amt, 2)} of our asset. And we have ${round(alpha.cash_to_invest, 2)}. Both rounded to 2nd decimal place.')
# 9. Sell off to see how it did
alpha.sell_asset(sell_amt = final_sell, asset_price = tframe['C'][final_point])
print(alpha.cash_to_invest)
percent_change = ((alpha.cash_to_invest - beta) / beta) * 100
print(f'Our percent change is {round(percent_change, 2)}%')
print(f'We Bought assets {buys} times')
print(f'We sold assets {sells} times')
percent_change_over_time = ((tframe['C'][data_points - 1] - tframe['C'][0]) / (tframe['C'][0])) * (100)
print(f'The asset {currency}, has changed by {percent_change_over_time}%. \n'
      f' our asset had an time period of {kline_sticks}, over {data_points} data points \n')

zell = len(price_array)
x = np.arange(0,zell)
y = price_array
plt.title("Portfolio performance over time")
plt.plot(x,y)
plt.show()

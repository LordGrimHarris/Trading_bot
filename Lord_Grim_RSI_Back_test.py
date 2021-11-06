import ccxt
import pandas as pd
import pandas_ta as ta
from portfolio_class_def import * # (important class that can be copied at eh top before (#1) or you can download the file to your python path/project)
import numpy as np
import array

# 1. Call financial data from binance us (because USD)
exchange = ccxt.binanceus()
# 2. This records our OHLCV (Open, High, Low, Close, Volume) data. 'currency', 'kline stick frame', 'number of data points'
# choose your currency
currency = str(input('What would you like to buy and sell today? Remember it has to be a buying pair for crypto'))
# pick your Kline time frame
kline_sticks = str(input("Pick a timeframe: 1m, 5m, 1hr, etc"))
data_points = int(input("How many data points would you like?"))
markets = exchange.fetch_ohlcv(currency, kline_sticks, limit=data_points)
# 3. Puts the data into a data frame
tframe = pd.DataFrame(data=markets, columns=['time', 'O', 'H', 'L', 'C', 'V'])
# 4. Specific closing prices
caesar = tframe['C']
# 5. Refactor RSI column into dataframe
tframe['RSI'] = ta.rsi(close=tframe['C'], talib=None, length=14)

# 6. Initialize portfolio values
beta, delta = 0, 0

beta = float(input("How much money do we have to  start to invest?"))
delta = float(input("How much crypto do we currently have?"))
alpha = Portfolio(cash_to_invest=beta, holding_amt=delta)
buys = 0
sells = 0

for i in tframe.index:
    # 7. How much to buy or sell
    d_inv = 0.2 * alpha.cash_to_invest
    a_sell = 0.85 * alpha.holding_amt
# 8. RSI strategy logic
    if tframe['RSI'][i] < 28:
        alpha.buy_asset(invest_amt=float(d_inv), asset_price=tframe['C'][i])
        buys += 1
    elif tframe['RSI'][i] > 70:
        alpha.sell_asset(sell_amt=float(a_sell), asset_price=tframe['C'][i])
        sells += 1
    else:
        print("nothing to see here")

final_point = int(data_points - 1)
final_sell = alpha.holding_amt
# 9. Sell off to see how it did
alpha.sell_asset(sell_amt=final_sell, asset_price=tframe['C'][final_point])
print(alpha.cash_to_invest)
percent_change = ((alpha.cash_to_invest - beta) / beta) * 100
print(f'Our percent change is {percent_change}%')
print(f'We Bought assets {buys} times')
print(f'We sold assets {sells} times')

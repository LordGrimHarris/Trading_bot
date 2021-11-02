import ccxt
import pandas as pd
import pandas_ta as ta


# 1. Call financial data from binance us (because USD)
exchange = ccxt.binanceus()
# 2. This records our OHLCV (Open, High, Low, Close, Volume) data. 'currency', 'kline stick frame', 'number of data points'
markets = exchange.fetch_ohlcv('DOGE/USD', '1m', limit=60)
# 3. Puts the data into a data frame
tframe = pd.DataFrame(data=markets, columns=['time', 'O', 'H', 'L', 'C', 'V'])
# 4. Specific closing prices
caesar = tframe['C']
# 5. Refactor RSI column into dataframe
tframe['RSI'] = ta.rsi(close=tframe['C'], talib=None, length=14)

print(tframe)

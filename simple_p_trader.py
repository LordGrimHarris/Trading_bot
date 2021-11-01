from portfolio_class_def import Portfolio
import pandas as pd
import websocket
import json
import ccxt
import requests

beta, delta = [], []

beta.append(input("How much money do we have to  start to invest?"))
delta.append(input("How much crypto do we currently have?"))
alpha = Portfolio(cash_to_invest=beta[-1], holding_amt=delta[-1])

while alpha:

    exchange = ccxt.binanceus()
    markets = exchange.fetch_ohlcv('DOGE/USD', '1m', limit=1)
    last_price = []
    dragon = markets[0]
    last_price = dragon[4]
    print(f'The last price was ${last_price} USD')
    buy_or_sell = (int(input("Would you like to buy:0 or sell:1?")))

    if buy_or_sell == 0:
        alpha.buy_asset(invest_amt=float(input("How much should we invest?")), asset_price=float(last_price))
        portfolio_array = [alpha.cash_to_invest, alpha.holding_amt]
        df = pd.DataFrame(portfolio_array, index=['Money to invest', 'Discrete asset quantity'])
        print(df)
    elif buy_or_sell == 1:
        alpha.sell_asset(sell_amt=float(input("How much should we sell?")), asset_price=float(last_price))
        portfolio_array = [alpha.cash_to_invest, alpha.holding_amt]
        df = pd.DataFrame(portfolio_array, index=['Money to invest', 'Discrete asset quantity'])
        print(df)
    else:
        print("Pick a valid value Shit Lord")
        portfolio_array = [alpha.cash_to_invest, alpha.holding_amt]
        df = pd.DataFrame(portfolio_array, index=['Money to invest', 'Discrete asset quantity'])
        print(df)

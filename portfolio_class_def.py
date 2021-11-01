class Portfolio:

    def __init__(self, cash_to_invest, holding_amt):
        self.cash_to_invest = float(cash_to_invest)
        self.holding_amt = float(holding_amt)

    def buy_asset(self, invest_amt, asset_price):

        if self.cash_to_invest >= invest_amt:
            c_quant = invest_amt / asset_price
            self.holding_amt += c_quant
            self.cash_to_invest -= invest_amt
            print(f'We have bought {c_quant} tokens, of our asset. Shit Lord')
        else:
            print("You Don't have enough money Shit Lord!")

    def sell_asset(self, sell_amt, asset_price):

        if self.holding_amt >= sell_amt:
            c_quant = sell_amt * asset_price
            self.holding_amt -= sell_amt
            self.cash_to_invest += c_quant
            print(f'We have sold {c_quant} tokens, of our asset. Shit Lord')
        else:
            print("You don't have enough asset Shit Lord!")




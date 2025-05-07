import pandas as pd
from backtesting import Backtest, Strategy

# Load your cleaned data
data = pd.read_csv('aapl_clean.csv', parse_dates=['Date'])
data.set_index('Date', inplace=True)
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]


# Define the RSI strategy
class RSIStrategy(Strategy):
    rsi_period = 14

    def init(self):
        self.rsi = self.I(
            lambda x: pd.Series(x).rolling(window=self.rsi_period).apply(
                lambda prices: 100 - (100 / (1 + (
                    (prices.diff().clip(lower=0).sum()) / 
                    (-prices.diff().clip(upper=0).sum())
                ))),
                raw=False
            ),
            self.data.Close
        )

    def next(self):
        if self.rsi[-1] < 30:
            self.buy()
        elif self.rsi[-1] > 70:
            self.sell()


# Run RSI backtest
bt_rsi = Backtest(data, RSIStrategy, cash=10000, commission=0.002)
rsi_results = bt_rsi.run()
print("RSI Strategy Results:")
print(rsi_results)
bt_rsi.plot()

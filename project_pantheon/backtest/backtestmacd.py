import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load your cleaned data
data = pd.read_csv('aapl_clean.csv', parse_dates=['Date'])
data.set_index('Date', inplace=True)
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]


# Define MACD Strategy
class MACDStrategy(Strategy):
    fast_ema_period = 12
    slow_ema_period = 26
    signal_period = 9

    def init(self):
        self.fast_ema = self.I(
            lambda x: pd.Series(x).ewm(
                span=self.fast_ema_period, 
                adjust=False
            ).mean(),
            self.data.Close
        )
        self.slow_ema = self.I(
            lambda x: pd.Series(x).ewm(
                span=self.slow_ema_period, 
                adjust=False
            ).mean(),
            self.data.Close
        )
        self.macd_line = self.I(
            lambda x, y: x - y, 
            self.fast_ema, 
            self.slow_ema
        )
        self.signal_line = self.I(
            lambda x: pd.Series(x).ewm(
                span=self.signal_period, 
                adjust=False
            ).mean(),
            self.macd_line
        )

    def next(self):
        if crossover(self.macd_line, self.signal_line):
            self.buy()
        elif crossover(self.signal_line, self.macd_line):
            self.sell()


# Run MACD backtest
bt_macd = Backtest(data, MACDStrategy, cash=10000, commission=0.002)
macd_results = bt_macd.run()
print("MACD Strategy Results:")
print(macd_results)
bt_macd.plot()

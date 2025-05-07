# import yfinance as yf
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Read the cleaned CSV file
data = pd.read_csv('aapl_clean.csv', parse_dates=['Date'])
data.set_index('Date', inplace=True)
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]


# Define the EMA crossover strategy
class EMAStrategy(Strategy):
    # Define EMA periods
    short_ema_period = 10
    long_ema_period = 50

    def init(self):
        # Calculate short and long EMAs
        self.short_ema = self.I(
            lambda x: pd.Series(x).ewm(
                span=self.short_ema_period,
                adjust=False
            ).mean(),
            self.data.Close
        )
        self.long_ema = self.I(
            lambda x: pd.Series(x).ewm(
                span=self.long_ema_period,
                adjust=False
            ).mean(),
            self.data.Close
        )

    def next(self):
        # Buy when the short EMA crosses above the long EMA
        if crossover(self.short_ema, self.long_ema):
            self.buy()
        # Sell when the short EMA crosses below the long EMA
        elif crossover(self.long_ema, self.short_ema):
            self.sell()


# Prepare data for backtest
bt = Backtest(data, EMAStrategy, cash=10000, commission=0.002)

# Run the backtest
output = bt.run()
print(output)

# Plot the results
bt.plot()
import pandas as pd
from technical import generate_trading_signals
from risk_manager import RiskManager
from portfolio_manager import PortfolioManager
# import yfinance as yf


START_CASH = 10000.0
SYMBOL = 'AAPL'


def main(): 
    print(f"Downloading data for {SYMBOL}...")
    
    # Load historical stock data from a CSV file
    data = pd.read_csv("CSV/aapl_clean.csv", 
                       index_col="Date", 
                       parse_dates=True)
      
    print(f"Downloaded {len(data)} days of data")
    
    # Generate signals
    signals = generate_trading_signals(data)
    
    # Initialize both managers
    rm = RiskManager()
    pm = PortfolioManager(START_CASH)
    
    trade_logs = [] # store daily logs 
    
    # Wait until there's enough historical data to calculate indicators
    min_lookback = max(26, 40)  # Using max of MACD long period and original lookback
    
    if len(signals) <= min_lookback:
        print(f"Not enough data points. ")
        return

    print("Starting trading simulation...")
    
    # Process each trading day
    for i in range(min_lookback, len(signals)):
        row = signals.iloc[i]
        price = row['Close']
        signal = row['Signal']
        date = row.name  # Works for both single and multi-index
        
        # Get current portfolio value
        portfolio_value = pm.get_value({SYMBOL: price})

        # Record keeping for this day
        record = {
            "Date": date,
            "Ticker": SYMBOL,
            "Action": 'HOLD',  # Default
            "Quantity": pm.positions.get(SYMBOL, {}).get('shares', 0),
            "Price": price,
            "Cash": pm.cash,
            "Stock": pm.positions.get(SYMBOL, {}).get('shares', 0) * price,
            "Total Value": portfolio_value
        }
        
        # Process signals (BUY, SELL)
        if signal in ['BUY', 'SELL']:
            result = rm.evaluate_trade(
                SYMBOL,
                signals['Close'][:i+1],
                signal,
                price,
                portfolio_value
            )
            
            record["Action"] = signal  # Update action in record
            
            if result['decision'] == 'APPROVED':
                pm.process_trade(result)
                date_str = str(date)
                if hasattr(date, 'strftime'):
                    date_str = date.strftime('%Y-%m-%d')
                print(f"{date_str}: {signal} at ${price:.2f}")

        trade_logs.append(record)

    # Create results dataframe
    results_df = pd.DataFrame(trade_logs)
    
    # Display summary
    if not results_df.empty:
        print("\nFull Trade Log:")
        columns = ['Date', 'Action', 'Price', 'Cash', 'Total Value']
        print(results_df[columns].to_string(index=False))
    
        # Calculate performance metrics
        initial_value = START_CASH
        final_value = pm.get_value({SYMBOL: signals.iloc[-1]['Close']})
        total_return = (final_value - initial_value) / initial_value * 100
        
        # Shows performance summary for results
        print(f"\nPerformance Summary:")
        print(f"Initial Value: ${initial_value:.2f}")
        print(f"Final Value: ${final_value:.2f}")
        print(f"Total Return: {total_return:.2f}%")
        
        # Count trades
        buys = sum(1 for log in trade_logs if log['Action'] == 'BUY')
        sells = sum(1 for log in trade_logs if log['Action'] == 'SELL')
        print(f"Total Trades: {buys + sells} (Buys: {buys}, Sells: {sells})")
    else:
        print("No trades were executed.")


if __name__ == '__main__':
    main()
from typing import Dict, Any, List


class PortfolioManager:
    def __init__(self, starting_cash: float):
        # Initialize starting cash, empty positions, and trade history log
        self.cash = starting_cash
        self.positions = {} # Stores current positions
        self.trade_log = [] # Logs each executed trade

    def process_trade(self, trade: Dict[str, Any]):
        symbol = trade['symbol']
        action = trade['action']
        price = trade['price']
        size = trade['position_size']  # Value of position

        # BUY action
        if action == 'BUY' and self.cash >= size:
            shares = int(size / price)
            # Skip trade if not enough cash to buy at least 1 share
            if shares <= 0:
                print(f"Not enough cash for 1 share of {symbol}")
                return
            # Actual cost of buying shares
            actual_size = shares * price
            # Retrieve or initialize current position
            self.positions[symbol] = self.positions.get(symbol, {'shares': 0, 'entry_price': 0})

            # Update avg entry price if it's already holding this symbol
            if self.positions[symbol]['shares'] > 0:
                current_shares = self.positions[symbol]['shares']
                current_price = self.positions[symbol]['entry_price']
                total_shares = current_shares + shares
                # Weighted average entry price calculation
                self.positions[symbol]['entry_price'] = (
                    (current_shares * current_price + shares * price) / total_shares
                )
                self.positions[symbol]['shares'] = total_shares
                
            else:
                # New position entry
                self.positions[symbol] = {'shares': shares, 'entry_price': price}

            self.cash -= actual_size # Subtract cash used for buying
            # Log the trade
            self.trade_log.append({**trade, 'shares': shares, 'actual_size': actual_size})
        # SELL action
        elif action == 'SELL' and symbol in self.positions:
            shares = self.positions[symbol]['shares']
            proceeds = shares * price
            self.cash += proceeds # Add proceeds to cash
            del self.positions[symbol] # delete the position from HOLD
            self.trade_log.append({**trade, 'shares': shares, 'actual_size': proceeds})

    def get_value(self, current_prices: Dict[str, float]) -> float:
        # Calculate total portfolio value (cash + current value of holdings)
        value = self.cash
        for symbol, data in self.positions.items():
            if symbol in current_prices:
                value += data['shares'] * current_prices[symbol]
        return value

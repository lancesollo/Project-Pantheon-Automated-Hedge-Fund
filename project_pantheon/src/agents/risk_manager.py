import pandas as pd
from typing import Dict, Any


class RiskManager:
    def __init__(self, max_risk: float = 0.02):
        # Maximum percentage of portfolio value to risk per trade
        self.max_risk = max_risk

    def calculate_volatility(self, prices: pd.Series) -> float:
        # Return 0 if there's not enough data for a rolling calculation
        if prices.shape[0] < 15:
            return 0.0

        # Calculate daily returns from price data
        returns = prices.pct_change().dropna()
        if returns.empty:
            return 0.0

         # Returns daily volatility in 14-day window
        daily_volatility = returns.rolling(window=14).std()
        # Get the most recent volatility value
        latest_daily_vol = daily_volatility.iloc[-1] if not daily_volatility.empty else 0.0
        # Return 0 if the result is NaN, else return the computed volatility
        return 0.0 if pd.isna(latest_daily_vol) else latest_daily_vol

    def evaluate_trade(self, symbol: str, prices: pd.Series, signal: str,
                       price: float, portfolio_value: float) -> Dict[str, Any]:
        # Calculate recent volatility
        volatility = self.calculate_volatility(prices)
        # Calculate confidence score from inverse of normalized volatility (cap at 1.0)
        confidence = 1.0 - min(volatility / 0.05, 1.0) if volatility >= 0 else 1.0
        # Reject trade if confidence is too low (highly volatile)
        if confidence < 0.3:
            return {
                "symbol": symbol,
                "action": signal,
                "decision": "REJECTED",
                "reason": f"Low confidence ({confidence:.2f})",
                "confidence": confidence,
                "price": price
            }
        # Calculate the size of the position based on max risk
        position_size = round(self.max_risk * portfolio_value, 2)
        if position_size <= 0:
            return {
                "symbol": symbol,
                "action": signal,
                "decision": "REJECTED",
                "reason": f"Calculated position size is not positive ({position_size:.2f})",
                "confidence": confidence,
                "price": price
            }
        # if confidence meets acceptance & position is valid, trade is approved
        return {
            "symbol": symbol,
            "action": signal,
            "decision": "APPROVED",
            "confidence": confidence,
            "position_size": position_size,
            "price": price
        }
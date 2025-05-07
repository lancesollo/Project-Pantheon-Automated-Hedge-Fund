import pandas as pd
import numpy as np


def calculate_ema(data: pd.Series, span: int = 14) -> pd.Series:
    return data.ewm(span=span, adjust=False).mean()


def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
    delta = data.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rs = rs.replace([np.inf, -np.inf], np.nan).fillna(1e6)
    return 100 - (100 / (1 + rs))


def calculate_macd(data: pd.Series, short: int = 12, long: int = 26, signal: int = 9) -> pd.DataFrame:
    data = data.dropna()
    if len(data) < long:
        return pd.DataFrame(index=data.index, columns=['MACD', 'MACD_Signal'])

    short_ema = calculate_ema(data, short)
    long_ema = calculate_ema(data, long)
    macd_line = short_ema - long_ema
    macd_signal = macd_line.ewm(span=signal, adjust=False).mean()
    macd_line = macd_line.squeeze()
    macd_signal = macd_signal.squeeze()

    return pd.DataFrame({
        'MACD': macd_line,
        'MACD_Signal': macd_signal
    }, index=data.index)


def generate_trading_signals(data: pd.DataFrame) -> pd.DataFrame:
    if 'Close' not in data:
        raise ValueError("Missing 'Close' column")

    data_copy = data.copy()
    data_copy['EMA_14'] = calculate_ema(data_copy['Close'])
    data_copy['RSI_14'] = calculate_rsi(data_copy['Close'])

    macd = calculate_macd(data_copy['Close'])
    if macd.empty:
        data_copy['MACD'] = np.nan
        data_copy['MACD_Signal'] = np.nan
    else:
        data_copy['MACD'] = macd['MACD']
        data_copy['MACD_Signal'] = macd['MACD_Signal']

    buy = (
        (data_copy['RSI_14'] < 60) &
        (data_copy['MACD'] > data_copy['MACD_Signal'])
    )
    sell = (
        (data_copy['RSI_14'] > 60) &
        (data_copy['MACD'] < data_copy['MACD_Signal'])
    )
    data_copy['Signal'] = np.where(buy, 'BUY', np.where(sell, 'SELL', 'HOLD'))
    data_copy['Signal'] = data_copy['Signal'].fillna('HOLD')
    return data_copy
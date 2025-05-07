import pandas as pd


def clean_aapl_csv(input_file, output_file):
    data = pd.read_csv(input_file, skiprows=3, header=None)
    data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')    
    data = data.dropna(subset=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
    data = data.sort_values('Date').reset_index(drop=True)
    data.to_csv(output_file, index=False)
    print(f"Clean file saved as: {output_file}")


if __name__ == "__main__":
    clean_aapl_csv('aapl.csv', 'aapl_clean.csv')

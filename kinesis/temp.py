import pandas as pd


def get_historical_data(symbol):
    print("Stock Symbol:", symbol)

    df = pd.read_csv(f'./data/historical_data/hist-{symbol}.csv')

    jsondf = df.to_json()

    print(jsondf)


get_historical_data('AAPL')

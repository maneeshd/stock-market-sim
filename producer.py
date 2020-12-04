"""
Kafka Producer
READ DATA FROM EXCEL AND SIMULATE REAL TIME Data Feed to Kafka
"""
from os import path
import pandas as pd


CUR_DIR = path.realpath(path.dirname(__file__))
DATA_DIR_ROOT = path.join(CUR_DIR, "data")


def simulate(df):
    """
    Simualte real time stream and post to Kafka topic
    All companies at regular interval
    """
    # TODO

    return


def prepare_data(df):
    """
    Drops unwanted colunmns and
    change format if needed
    """
    # TODO

    return


def init():
    """
    Main Function
    """

    fname = 'intraday-22-oct-merged'

    df = pd.read_csv(
        f"{DATA_DIR_ROOT}/{fname}.csv",
        sep=",",
    )

    print(df.shape)
    print(df.tail())

    prepare_data(df)

    print("Starting Kafka producer...")
    simulate(df)
    print("Exiting")

    return


if __name__ == "__main__":
    print(DATA_DIR_ROOT)

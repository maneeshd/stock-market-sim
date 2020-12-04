"""
Author: Maneesh Divana <maneeshd77@gmail.com>
Date: 2020-12-03
Python: 3.7.9

Reads stock data from CSV files and simulates stock streaming into AWS Kinesis Data Stream
"""
from os import path
from datetime import datetime
from time import sleep
import pandas as pd
from kinesis_api import KinesisAPI


CUR_DIR = path.realpath(path.dirname(__file__))
DATA_DIR_ROOT = path.join(CUR_DIR, "data")

CSV_FILENAME = "intraday-22-oct-merged.csv"
KINESIS_STREAM_NAME = "stock-stream"
KINESIS_SHARD_PARTITION_KEY = "stock"


def simulate():
    """
    Simualte real time stream and post to Kinesis Data Stream Shard
    All companies at regular interval
    """

    # Load CSV into DataFrame
    df = pd.read_csv(path.join(DATA_DIR_ROOT, CSV_FILENAME))

    print(f"Shape of DataFrame: {df.shape}")
    print("DataFrame:")
    print(df, "\n")

    # Groups of 10 rows
    group = df.groupby(df.index // 10)

    # Connect to Kinesis using API
    api = KinesisAPI(stream_name=KINESIS_STREAM_NAME)

    print("-" * 64, "\n")

    start = datetime.now()
    print(f"[{start.strftime('%Y-%m-%d %H:%M:%S')}] Starting Kinesis producer...\n")

    count = 0
    # Send records for a group of 10 companies every 1 minute
    for idx, group in df.groupby(df.index // 10):
        now = datetime.now()
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Sending data:")
        print(group)
        api.write_record(
            data=group.to_dict(),
            partition_key=KINESIS_SHARD_PARTITION_KEY
        )
        count += 1
        print("")
        if count == 7:
            break
        sleep(60.0)

    end = datetime.now()
    print(f"[{end.strftime('%Y-%m-%d %H:%M:%S')}] Finished producing. Exiting...\n")
    api.close()


if __name__ == "__main__":
    print("====================================")
    print("Stock Data Producer for AWS Kinesis")
    print("====================================")
    simulate()

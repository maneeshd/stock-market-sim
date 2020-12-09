"""
Author:
Date:
Python: 3.7.9

Consumer for AWS Kinesis Stock Data Stream
"""
from datetime import datetime
import time
from kinesis_api import KinesisAPI, DynamoDbAPI


KINESIS_STREAM_NAME = "stock-stream"
KINESIS_SHARD_PARTITION_KEY = "stock"
DYNAMO_DB_TABLE = "stock-stream-data"
DYNAMO_DB_PARTITION_KEY = "symbol"
SYNAMO_DB_SORT_KEY = "minute"


def push_data():
    """
    Push to front end
    """
    pass


def insert_db():
    """
    Insert to database
    """
    pass


def parse_records():
    """
    parse consumed records
    """
    pass


def consume():
    api = KinesisAPI(stream_name=KINESIS_STREAM_NAME)

    last_seq_num = ""

    for record in api.read_records(time_limit=1.0):
        data = record.get("data")
        last_seq_num = record.get("sequence_number")
        print(f"\nDATA: {data}\nLAST_SEQ_NUM: {last_seq_num}\n")

    while True:
        print("Retrieving...")
        shard_iter = api.get_shard_iterator(
            iterator_type="AFTER_SEQUENCE_NUMBER",
            sequence_number=last_seq_num
        )

        for record in api.read_records(time_limit=1.0, shard_iterator=shard_iter):
            data = record.get("data")
            last_seq_num = record.get("sequence_number")
            print(f"\nDATA: {data}\nLAST_SEQ_NUM: {last_seq_num}\n")

        print("Sleeping...")
        time.sleep(60)


if __name__ == "__main__":
    print("====================================")
    print("Stock Data Consumer for AWS Kinesis")
    print("====================================")
    consume()

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


def insert_db(db_api, data):
    """
    Insert to database
    """
    print("Writing to dynamo DB")
    for row in data:
        db_api.put(row)
    return


def parse_record(data):
    """
    parse consumed records
    """
    required_keys = ["minute", "symbol", "open",
                     "high", "low", "close", "volume"]

    # get relavent keys
    parsed_data = {key: data[key] for key in required_keys}

    # Create array structure
    arrayed = []
    for _ in range(10):
        arrayed.append({key: '0' for key in required_keys})

    # Unpack dict and load to array
    for key, value in parsed_data.items():
        for subkey in sorted(value):
            arrayed[int(subkey) % 10][key] = value[subkey]

    return arrayed


def consume():
    api = KinesisAPI(stream_name=KINESIS_STREAM_NAME)
    db_api = DynamoDbAPI(DYNAMO_DB_TABLE)
    last_seq_num = ""

    for record in api.read_records(time_limit=1.0):
        data = record.get("data")
        last_seq_num = record.get("sequence_number")
        # print(f"\nDATA: {data}\nLAST_SEQ_NUM: {last_seq_num}\n")
        print("---------------------------")
        parsed_data = parse_record(data)
        print(parsed_data)
        insert_db(db_api, parsed_data)
        print("---------------------------")

    starttime = time.time()

    while True:
        print("Retrieving...")
        shard_iter = api.get_shard_iterator(
            iterator_type="AFTER_SEQUENCE_NUMBER",
            sequence_number=last_seq_num
        )

        for record in api.read_records(time_limit=1.0, shard_iterator=shard_iter):
            data = record.get("data")
            last_seq_num = record.get("sequence_number")
            # print(f"\nDATA: {data}\nLAST_SEQ_NUM: {last_seq_num}\n")
            print("---------------------------")
            parsed_data = parse_record(data)
            print(parsed_data)
            insert_db(db_api, parsed_data)
            print("---------------------------")

        print("Sleeping...")
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


if __name__ == "__main__":
    print("====================================")
    print("Stock Data Consumer for AWS Kinesis")
    print("====================================")
    consume()

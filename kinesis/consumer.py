"""
Author:
Date:
Python: 3.7.9

Consumer for AWS Kinesis Stock Data Stream
"""
from kinesis_api import KinesisAPI

KINESIS_STREAM_NAME = "stock-stream"
KINESIS_SHARD_PARTITION_KEY = "stock"


def consume():
    api = KinesisAPI(stream_name=KINESIS_STREAM_NAME)
    pass


if __name__ == "__main__":
    print("====================================")
    print("Stock Data Consumer for AWS Kinesis")
    print("====================================")
    consume()

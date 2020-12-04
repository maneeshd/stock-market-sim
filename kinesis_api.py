"""
Author: Maneesh Divana <maneeshd77@gmail.com>
Date: 2020-12-03
Python: 3.7.9

AWS Kinesis Stream Producer and Consumer API using boto3
"""
from os import getenv
from boto3 import Session as BotoSession


class KinesisAPI:
    def __init__(self, stream_name: str):
        if not stream_name:
            raise ValueError("! Stream name (stream_name) is requied !")
        self.stream_name = stream_name

        # Get AWS Access Keys from Environment Varibales
        self.__access_key_id = getenv("AWS_ACCESS_KEY_ID")
        self.__secret_access_key = getenv("AWS_SECRET_ACCESS_KEY")
        self.__region = getenv("AWS_REGION_NAME")

        if self.__access_key_id is None:
            raise ValueError(
                "! AWS_ACCESS_KEY_ID was not found/not set in environment variables. !"
            )

        if self.__secret_access_key is None:
            raise ValueError(
                "! AWS_ACCESS_KEY_ID was not found/not set in environment variables. !"
            )

        if self.__region is None:
            raise ValueError(
                "! AWS_ACCESS_KEY_ID was not found/not set in environment variables. !"
            )

        # Creating a boto3 session, connect to AWS
        self.session = BotoSession(
            aws_access_key_id=self.__access_key_id,
            aws_secret_access_key=self.__secret_access_key,
            region_name=self.__region
        )

        # Get the kinesis client
        self.client = self.session.client("kinesis")

        # Get shard IDs
        self.shard_ids = None
        stream = self.client.describe_stream(StreamName=self.stream_name)
        try:
            shards = stream["StreamDescription"]["Shards"]
            self.shard_ids = [shard["ShardId"] for shard in shards]
            _ = self.shard_ids[0]
        except Exception as err:
            raise ValueError(f"! Failed to get Shard ID's !\n{err}")

    def write_record(self):
        """
        Put a record into Kinesis Data Stream
        """
        pass

    def write_records(self):
        """
        Put a list of records into Kinesis Data Stream
        Limit: 500 records
        """
        pass

    def get_shard_iterator(self, iterator_type: str = "TRIM_HORIZON"):
        """
        Get the first shard iterator for get_records

        param iterator_type (str): Iterator type

        TRIM_HORIZON          : Start reading at the last untrimmed record in the shard in the
                                system, which is the oldest data record in the shard.
        LATEST                : Start reading just after the most recent record in the shard,
                                so that you always read the most recent data in the shard.
        """
        try:
            iter_resp = self.client.get_shard_iterator(
                StreamName=self.stream_name,
                ShardId=self.shard_ids[0],
                ShardIteratorType=iterator_type
            )
            iter_resp["ShardIterator"]
        except Exception as err:
            raise ValueError(f"! Failed to get Shard Iterator !\n{err}")
        else:
            return iter_resp["ShardIterator"]

    def read_records():
        pass


if __name__ == "__main__":
    print("TEST")

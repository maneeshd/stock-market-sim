"""
Author: Maneesh Divana <maneeshd77@gmail.com>
Date: 2020-12-03
Python: 3.7.9

AWS Kinesis Stream Producer and Consumer API using boto3
"""
from os import getenv
from json import dumps, loads
from typing import List, Any
from datetime import datetime, timedelta
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

        # Shard Itertator type to read Records from Kinesis Data Stream
        self.iterator_type = None

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
            print("! Failed to get Shard ID's !")
            raise err

    def __str__(self) -> str:
        return f"<KinesisAPI(stream_name='{self.stream_name}', shard_ids={self.shard_ids})>"

    def write_record(self, data: Any, partition_key: str) -> dict:
        """
        Writes a single data record into an Amazon Kinesis data stream
        """
        try:
            return self.client.put_record(
                StreamName=self.stream_name,
                Data=dumps(data),
                PartitionKey=f"{partition_key}"
            )
        except Exception as err:
            print(f"! Failed to write data to stream: {self.stream_name} !")
            raise err

    def write_records(self, data: List[Any], partition_key: str) -> None:
        """
        Writes multiple data records into a Kinesis data stream in a single call
        Limit: 500 records in 'data'
        """
        if len(data) > 500:
            raise ValueError("! Number of records in data exceeded limit(500) !")

        records = [
            {"Data": dumps(ele), "PartitionKey": partition_key} for ele in data
        ]
        try:
            return self.client.put_record(
                StreamName=self.stream_name,
                Records=records
            )
        except Exception as err:
            print(f"! Failed to write data to stream: {self.stream_name} !")
            raise err

    def set_shard_iterator_type(self, iterator_type: str) -> None:
        self.iterator_type = iterator_type

    def get_shard_iterator(self, iterator_type: str = None, sequence_number: str = None) -> str:
        """
        Get the first shard iterator for get_records

        param iterator_type (str): Iterator type

        AFTER_SEQUENCE_NUMBER : Start reading right after the position denoted by a specific
                                sequence number, provided in the value StartingSequenceNumber
        TRIM_HORIZON          : Start reading at the last untrimmed record in the shard in the
                                system, which is the oldest data record in the shard.
        LATEST                : Start reading just after the most recent record in the shard,
                                so that you always read the most recent data in the shard.
        """
        if not iterator_type:
            iterator_type = self.iterator_type if self.iterator_type else "TRIM_HORIZON"
        if iterator_type not in ["AFTER_SEQUENCE_NUMBER", "TRIM_HORIZON", "LATEST"]:
            iterator_type = "TRIM_HORIZON"
        if iterator_type == "AFTER_SEQUENCE_NUMBER" and not sequence_number:
            iterator_type = "TRIM_HORIZON"
        self.iterator_type = iterator_type
        try:
            if iterator_type == "AFTER_SEQUENCE_NUMBER":
                iter_resp = self.client.get_shard_iterator(
                    StreamName=self.stream_name,
                    ShardId=self.shard_ids[0],
                    ShardIteratorType=iterator_type,
                    StartingSequenceNumber=sequence_number
                )
            else:
                iter_resp = self.client.get_shard_iterator(
                    StreamName=self.stream_name,
                    ShardId=self.shard_ids[0],
                    ShardIteratorType=iterator_type
                )
            iter_resp["ShardIterator"]
        except Exception as err:
            print(f"! Failed to get Shard Iterator for stream: {self.stream_name} !")
            raise err
        else:
            return iter_resp["ShardIterator"]

    def read_records(
        self,
        time_limit: float,
        shard_iterator: str = None,
        records_limit: int = 5000,
        debug: bool = False
    ) -> dict:
        """
        Gets data records from a Kinesis data stream's shard.

        time_limit: Time in MINUTES to keep scanning for records
        """
        # Calculate end time
        end_time = datetime.now() + timedelta(minutes=time_limit)

        if not shard_iterator:
            shard_iterator = self.get_shard_iterator()

        while True:
            try:
                # Get data
                record_resp = self.client.get_records(
                    ShardIterator=shard_iterator,
                    Limit=records_limit
                )
                # Only run for a certain amount of time.
                # Stop looping if no data returned. This means it's done
                now = datetime.now()

                if debug:
                    print("")
                    print(f"[read_records] ShardIterator: {shard_iterator}")
                    print(f"[read_records][{now.strftime('%Y-%m-%d %H:%M:%S')}] {record_resp}")
                    print("")

                if end_time < now or not record_resp:
                    break
                # yield data to outside calling iterator
                for record in record_resp["Records"]:
                    sequence_number = record["SequenceNumber"]
                    try:
                        yield {"data": loads(record["Data"]), "sequence_number": sequence_number}
                    except Exception as err:
                        print(f"[WARN] Error deserializing record's data: {err}")
                        yield {"data": record["Data"], "sequence_number": sequence_number}
                # Get next iterator for shard from previous request
                shard_iterator = record_resp["NextShardIterator"]
            except Exception as err:
                print(f"! Error getting records from stream: {self.stream_name} !")
                print(err, "\n")
                break

    def close(self):
        self.__del__()

    def __del__(self):
        self.__access_key_id = None
        self.__secret_access_key = None
        self.__region = None
        self.client = None
        self.session = None


if __name__ == "__main__":
    print("TEST")
    api = KinesisAPI("stock-stream")
    print(api)

    # api.set_shard_iterator_type("LATEST")
    # Default Shard Iterator Type: TRIM_HORIZON
    for record in api.read_records(time_limit=1.0):
        data = record.get("data")
        last_seq_num = record.get("sequence_number")
        print(f"\nDATA: {data}\nLAST_SEQ_NUM: {last_seq_num}\n")

    # Use AFTER_SEQUENCE_NUMBER to only read data after last read
    # shard_iter = api.get_shard_iterator(
    #     iterator_type="AFTER_SEQUENCE_NUMBER",
    #     sequence_number="49613271809655507031116572764155274724471449482516496386"
    # )
    # for record in api.read_records(time_limit=1.0, shard_iterator=shard_iter):
    #     data = record.get("data")
    #     last_seq_num = record.get("sequence_number")
    #     print(f"\nDATA: {data}\nLAST_SEQ_NUM: {last_seq_num}\n")

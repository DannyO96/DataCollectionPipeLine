import tempfile
import boto3
from botocore.exceptions import ClientError
import json
import os
import urllib.request
import shutil


class StoreData():
    """
    This class is to interact with the s3 bucket to store images and features and to interact with the relational database
    """
    def __init__(self, s3_params) -> None:
        self.bucket_name = s3_params['bucket_name']
        self.aws_access_key_id = s3_params['aws_access_key_id']
        self.aws_secret_access_key = s3_params['aws_secret_access_key']
        self.s3_client = boto3.client("s3")


    def upload_raw_data_to_datalake(self):
        path = '/home/danny/git/DataCollectionPipeline/raw_data/'
        
        #bucket_name = ['asoss3bucket']
        try:
            #response = self.s3_client.upload_file(os.path.join(path,'testfile'), self.bucket_name, "testfile")
            for root,dirs,files in os.walk(path):
                for file in files:
                    response = self.s3_client.upload_file(os.path.join(root,file), self.bucket_name, file)
            return True
        except ClientError as E:
            print("test upload 2 s3 exception",E)
            return False


    def upload_raw_data_s3(self):
        # Let's use Amazon S3
        s3 = boto3.resource("s3")

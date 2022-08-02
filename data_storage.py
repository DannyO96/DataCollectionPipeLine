import tempfile
import boto3
import json
import os
import urllib.request
import shutil
import sqlalchemy
import pandas
import psycopg2
import psycopg
from botocore.exceptions import ClientError
from datetime import datetime


class StoreData():
    """
    This class is to interact with the s3 bucket to store images and features and to interact with the relational database
    """
    def __init__(self, rds_params, s3_params) -> None:
        """
        This init method takes the s3 params from my.secrets.AWSbucket.json
        and initialises the boto3 s3 client module for interacting with my s3 buckets.
        It also takes rds params from my.secrets.RDSdb.json to interact with my postgresql database.
        """
        self.bucket_name = s3_params['bucket_name']
        self.aws_access_key_id = s3_params['aws_access_key_id']
        self.aws_secret_access_key = s3_params['aws_secret_access_key']
        self.s3_client = boto3.client("s3")

        #self.rds_params = {"database_type":self.database_type, "dbapi":self.dbapi, "endpoint":self.endpoint, "user":self.user, "password":self.password, "database":self.database, "port":self.port}
        self.database_type = rds_params['database_type']
        self.dbapi = rds_params['dbapi']
        self.endpoint = rds_params['endpoint']
        self.user = rds_params['user']
        self.password = rds_params['password']
        self.database = rds_params['database']
        self.port = rds_params['port']

    def save_dataframe_and_image_locally(self, prods_frame):
        """
        This is a function that locally saves the dataframe and the gallery image of the product in the raw data folder

        Args:
            param1: self
            param2: frame - this is the dataframe returned from scraping one of the types of product page
            param3: filename - this is the name of the product file

        Returns:
            This returns a folder in the raw_data folder where the name of the product is turned into a slug so it can be used as a foldername the foldername also incoperates 
            sys dtime to avoid duplicate folders and allow for time period analysis of the data. The folder returned is named after the product and contains the gallery image jpeg and
            the dataframe in json format.

        Raises:
            TypeError: decoding to str: need a bytes-like object, int found. occurs when attempting to slugify file this occurs because the the type is not byte like.
        """
        #filename = product_name.text
        sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
        os.makedirs("/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
        folder = (r"/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
        filepath = os.path.join(folder, f"{filename}{sys_dtime}.json")
        frame.to_json(filepath, orient = 'table', default_handler=str)
        filepath2 = os.path.join(folder, f"{filename}{sys_dtime}.jpeg")
        #img_tag = self.driver.find_element(*ProductPageLocators.GALLERY_IMAGE)
        #image_link = img_tag.get_attribute('src')
        #urllib.request.urlretrieve(image_link, filepath2)


    def save_images_locally(self, image_link_list):
        for image in image_link_list:
            pass


    def upload_raw_data_to_datalake(self):
        """
        This is a function to upload the contents of the raw_data folder to and s3 bucket

        Args:
            param1:self 

        Returns:
            Returns a bool indicating if the upload was successfull.

        Raises:
            TypeError
            ClientError

        """
        path = '/home/danny/git/DataCollectionPipeline/raw_data/'
        try:
            #response = self.s3_client.upload_file(os.path.join(path,'testfile'), self.bucket_name, "testfile")
            for root,dirs,files in os.walk(path):
                for file in files:
                    response = self.s3_client.upload_file(os.path.join(root,file), self.bucket_name, file)
            return True
        except ClientError as E:
            print("test upload 2 s3 exception",E)
            return False

    def create_engine(self):
        engine = sqlalchemy.create_engine(f"{self.database_type}://{self.user}:{self.password}@{self.endpoint}:{self.port}/{self.database}")
        return engine

    def send_dataframe_to_rds(self, frame):
        """
        This is a function to convert the pandas dataframe to sql

        Args:
            param1: self 
            param2: frame :the dataframe thats is being converted to an sql table

        Returns:
            The function uploads the dataframe to my relational database using the init methods of the data storage class and the asos scraper class

        Raises:
            ValueError: this error is raised when the incorrect datatype is passed to the function.
        
        """
        engine = self.create_engine()
        frame.to_sql('products_new', con=engine, if_exists='append', index=sqlalchemy.false)
        

    def process_data(self, frame):
        """
        The dataframe is uloaded to rds by calling the send dataframe to rds method
        """
        #frame.insert(0, "filename",filename)
        self.send_dataframe_to_rds(frame)
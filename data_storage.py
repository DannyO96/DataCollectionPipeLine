import tempfile
import boto3
import json
import os
import urllib.request
import shutil
import sqlalchemy
import pandas as pd
import psycopg2
import psycopg
from botocore.exceptions import ClientError
from datetime import datetime



class StoreData():
    """
    This class is to interact with an s3 bucket to store images and features and to interact a relational database
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
        # Create a dictionary of the current image checksums(assumed md5 as < 16MB) I have stored in the bucket.
        '''
        self.s3_etags = {}
        keys = self.s3_client.list_objects(Bucket=self.bucket_name)['Contents']
        for key in keys:
        self.s3_etags[self.s3_client.head_object(Bucket=self.bucket_name,Key=key)['ResponseMetadata']['HTTPHeaders']['etag']]=key
        print()
        '''
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
        #rows = prods_frame.loc[]
        #filename = product_name.text
        #sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
        #os.makedirs("/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
        #folder = (r"/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
        #filepath = os.path.join(folder, f"{filename}{sys_dtime}.json")
        #frame.to_json(filepath, orient = 'table', default_handler=str)
        #filepath2 = os.path.join(folder, f"{filename}{sys_dtime}.jpeg")
        #img_tag = self.driver.find_element(*ProductPageLocators.GALLERY_IMAGE)
        #image_link = img_tag.get_attribute('src')
        #urllib.request.urlretrieve(image_link, filepath2)


    def save_images_to_s3(self, prods_frame: pd.DataFrame, engine):
        '''
        This is a funtion to check the relational database for matching image links drop duplicates and upload any new images to the s3 bucket.
        '''
        #df = pd.DataFrame
        #dfd = pd.concat([df, prods_frame])
        old_frame = pd.read_sql_table('products_new', engine)
        old_imgs = []

        for index, row in old_frame.iterrows():
            img_link = row.at['img_link']
            old_imgs.append(img_link)

        #current_imgs = prods_frame.loc[:,'img_link']
        merged_dfs = pd.concat([old_frame, prods_frame])
        merged_dfs = merged_dfs.astype("str")
        final_df = merged_dfs.drop_duplicates(subset=['img_link'], keep = False)

        for index,row in final_df.iterrows():
            filename = row.at['filename']
            image_link = row.at['img_link']
            image_link_list = []
            image_link_list.append(image_link)
            for image_link in image_link_list:
                if image_link in old_imgs:
                    continue
                else:
                    self.save_image_to_s3(self, image_link, filename)

    def save_image_to_s3(self,image_link,filename):
        '''
        This is a function to upload a single image to s3
        Args:
            param1:self 
            param2:image_link: link to the image
            param3:filename:this is a slug of the products name suitable for use as a filename.

        Returns:
            Returns a bool indicating if the upload was successfull.

        Raises:
            TypeError
            ClientError
        '''
        try:
            image = urllib.request.urlretrieve(image_link)
            response = self.s3_client.upload_file(filename, self.bucket_name, image)
        except ClientError as E:
            print("test upload 2 s3 exception",E)
            
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
        """
        This funtion creates an engine to connect with my relational database.
        """
        engine = sqlalchemy.create_engine(f"{self.database_type}://{self.user}:{self.password}@{self.endpoint}:{self.port}/{self.database}")
        return engine

    def send_dataframe_to_rds(self, frame):
        """
        This is a function to check the database for name and price duplicates then convert the resulting pandas dataframe to sql
        and send it to my relational database.

        Args:
            param1: self 
            param2: frame :the dataframe thats is being converted to an sql table

        Returns:
            The function uploads the dataframe to my relational database using the init methods of the data storage class and the asos scraper class

        Raises:
            ValueError: this error is raised when the incorrect datatype is passed to the function.
        
        """
        engine = self.create_engine()
        old_frame = pd.read_sql_table('products_new', engine)
        merged_dfs = pd.concat([old_frame, frame])
        merged_dfs = merged_dfs.astype("str")
        final_df = merged_dfs.drop_duplicates(subset=['filename', 'product_name', 'href', 'price_info'], keep = False)
        final_df.to_sql('products_new', con=engine, if_exists='append', index=False)
        
    def process_data(self, prods_frame):
        """
        The dataframe is uloaded to rds by calling the send dataframe to rds method
        """
        engine = self.create_engine()
        self.send_dataframe_to_rds(prods_frame)
        self.save_images_to_s3(prods_frame, engine)

    def locally_save_frame_and_image(self, frame : pd.DataFrame, filename):
        image_link = frame.loc['img_link']
        sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
        os.makedirs("/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
        folder = (r"/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
        filepath = os.path.join(folder, f"{filename}{sys_dtime}.json")
        frame.to_json(filepath, orient = 'table', default_handler=str)
        filepath2 = os.path.join(folder, f"{filename}{sys_dtime}.jpeg")
        urllib.request.urlretrieve(image_link, filepath2)

    def check_for_duplicates(self):
        '''
        SELECT * FROM
        (SELECT *, count(*)
        OVER
        (PARTITION BY
        product_name,
        filename
        ) AS count
        FROM products_new) tableWithCount
        WHERE tableWithCount.count > 1;
        '''


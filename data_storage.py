import boto3
import io
import os
import pandas as pd
import requests
import sqlalchemy
import tempfile
import urllib.request
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

        #self.engine = sqlalchemy.create_engine(f"{self.database_type}://{self.user}:{self.password}@{self.endpoint}:{self.port}/{self.database}")

        self.bucket_name = s3_params['bucket_name']
        self.aws_access_key_id = s3_params['aws_access_key_id']
        self.aws_secret_access_key = s3_params['aws_secret_access_key']
        self.s3_client = boto3.client("s3")
     
        self.database_type = rds_params['database_type']
        self.dbapi = rds_params['dbapi']
        self.endpoint = rds_params['endpoint']
        self.user = rds_params['user']
        self.password = rds_params['password']
        self.database = rds_params['database']
        self.port = rds_params['port']

    def save_locally(self, prods_frame:pd.DataFrame):
        """
        This is a function that iterates over the rows of the prods frame to locally save each dataframe and image locally

        Args:
            param1: self
            param2: frame - this is the dataframe returned from scraping one of the types of product page
            param3: filename - this is the name of the product file

        Returns:
            This returns a folder in the raw_data folder the foldername also incoperates sys dtime to avoid duplicate folders and allow for time period 
            analysis of the data. The folder returned is named after the product and contains the gallery image jpeg and
            the dataframe in json format.

        Raises:
        
        """
        for index,row in prods_frame.iterrows():
            filename = row.at['filename']
            self.locally_save_frame_and_image(row, filename)

    def locally_save_frame_and_image(self, frame : pd.DataFrame, filename):
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
            T
        """
        image_link = frame.at['img_link']
        sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
        os.makedirs("/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
        folder = (r"/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
        filepath = os.path.join(folder, f"{filename}{sys_dtime}.json")
        frame.to_json(filepath, orient = 'table', default_handler=str)
        filepath2 = os.path.join(folder, f"{filename}{sys_dtime}.jpeg")
        urllib.request.urlretrieve(image_link, filepath2)


    def save_images_to_s3(self, prods_frame: pd.DataFrame, engine):
        '''
        This is a funtion to check the relational database for matching image links drop duplicates and upload any new images to the s3 bucket.
        '''
        old_frame = pd.read_sql_table('products_new', engine)
        dataframes = [prods_frame, old_frame]
        template = pd.DataFrame( columns = ['date_time', 'filename', 'product_name', 'href', 'UUID', 'product_code', 'size_info', 'img_info', 'product_details', 'about_product', 'price_info', 'img_link'])
        dataframes= [i if not i.empty else template for i in dataframes]
        merged_df = pd.concat(dataframes)
        final_df = merged_df.drop_duplicates(subset = ['img_link'], keep = False)


        print("DEBUG: line 124 final_df=",final_df)
        print("starting s3 upload....")

        for index,row in final_df.iterrows():
            filename = row.at['filename']
            image_link = row.at['img_link']
            if self.save_image_to_s3(image_link, filename):
                print("image uploaded to s3")
            

    def save_image_to_s3(self, image_link, filename: str):
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
            image = requests.get(image_link).content
            tmp = tempfile.NamedTemporaryFile(mode = 'w+b')
            temp = tmp.write(image)
            response = self.s3_client.upload_fileobj(io.BytesIO(image), self.bucket_name, tmp.name)
        
            print("Binary image uploaded to s3")
        except ClientError as E:
            print("test upload 2 s3 exception",E)
            return False
        return True
            
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

    def send_dataframe_to_rds(self, frame, engine):
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
        old_frame = pd.read_sql_table('products_new', engine)
        merged_dfs = pd.concat([old_frame, frame])
        merged_dfs = merged_dfs.astype("str")
        final_df = merged_dfs.drop_duplicates(subset=['filename', 'product_name', 'href', 'price_info'], keep = False)
        final_df.to_sql('products_new', con=engine, if_exists='append', index=False)
        
    def process_data(self, prods_frame, engine):
        """
        The dataframe is uloaded to rds by calling the send dataframe to rds method
        """
        #engine = self.create_engine()
        print("uploading images to s3....")
        self.save_images_to_s3(prods_frame, engine)
        print("done")
        


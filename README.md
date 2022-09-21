'''
DATA COLLECTION PIPELINE

work in progress - Grabs T-Shirts from ASOS - to generate a repo of products & prices. 

I have created funtions to dynamically scrape asos and append the information to dictionaries and dictionaries of lists and then initialise a pandas dataframe. However manipulating and storing the data has been put on hold as my project has been interuppted by an asos student discount pop up that appears to be an iframe
I have implemented methods to close the iframe although they are increasing the time taken for the scraper to scrape data.

Although I wrote a try and except block to close the discount it appears to not be an issue anymore the dataframe is currently only printing as a single row I need to make the program create a row for each uuid/product, and then arrange to store the data in a manner whereby my list of product dictionaries is stored in a time/date sensetive manner.

Recently asos appear to have updated the website with a new product page type I have had to write a try and except block to manage the variation of product page types this and the student discount iframe have severly hindered my progress as tests rarely get to the point where i can see my dataframes form.

Have implemented the dataframe to json pandas method to locally store my dataframes in a date time sensitive manner. I have also implemented urllib retrive to download images from the src link from the image tag of the html element corresponding to the image.

After rethinking my page object model to improve the efficiency of my program I need to separate the page scraping methods and create a method to assert the type of product page before the link is scraped

The dataframes obtained from scraping are now saved in a folder with gallery images from the products page and these folders are saved in a date time sensitive manner to allow for analysis of product information over time. Its likely that we might want to make predictions based upon the data and being able to study the data over time allows for more accurate predictions.

The asos product pages appear to have different instances when loaded by the webdriver although my code accounts for this one of the product page types takes considerably longer to scrape almost 10x as long so reducing this time complexity is my current focus. I have also encountered the out of stock page these appear to be removed relatively fast although its an exception that is not currently handled by my code.

Recently i have been attempting to reduce the runtime of the scraper by reducing the amount of actions and reducing the amount of time I spend waiting for elements to appear so far this has reduced the runtime of the longest instance of the scraPer by almost 80%

I have finally solved the out of stock page issue with a try and except block, if else statements and the selenium web elemnt module the scraper now skips out of stock products when scraping i have also used extend of the href list in order to scrape multiple search result pages of products

I have got headless mode working it wasnt working as i was using the default user agent setting the user agent in my setUp function solved issues I was having with headless mode

I have finally got the error handling for out of stock something went wrong and outlets pages so the scraper can run without errors due to unscrapable product pages.

In order to set up the relational database and s3 bucket I created JSON files of the sensetive information credentials that I needed to gain access to my data stores and then initialised these parameters. The JSON files are opened and read in the setUp method of main.py then the parameters are specified in the init method of my StoreData class.

After setting up my s3 bucket and RDS I have created methods to upload the contents of the raw data folder to my s3 bucket, this method save the files locally then uploads the contents of the local raw_data folder to the specified s3 bucket.

I have written a test to upload a single dataframe to my database and confirmed it in a terminal window connected to the database however I will need to
do some more work to ensure all the data is as i expect and ready for analysis and manipulation.

Uploading an dataframe of scraped product info proved to be harder than expected do to some required reworking of my object model and level of abstraction in different parts of the code. and now i can succefully upload a 72 row dataframe of product information to my relational database. The scraper can now upload images and frames from single products to the datalake as JSON and Jpeg and then concatonates the frames to a frame off all the products from that scrape which is the uploaded to my relational database. 

My tests are all working however im unhappy with the architecture of my scraper ands i have to rework some functions and think about the level of abstraction that certain processes are occuring on. Namely I want to locally save my data in the data storage module so i need to rework this function and ensure that in main.py whenever a returning function is called the return of that function is used as several tests did not meet this criteria. This means
that in order to save images and dataframes locally I will need to use pandas to extract information from the prods_dataframe in order to locally save my scraped data. My other current focus is to be able to extend the href_list to scrape a larger number of products in a single scrape without scraping duplicates.

All tests are working successfully now I am beggining to focus on learning sql to allow for better database management and to prevent rescraping of images and dataframes where the dataframes are analagous as we still want to rescrape any changes in products information most notably price. I have implemented the pandas drop_duplicates method to avoid rescraping of previously scraped information using the filename, href  and price as the subset for my duplicates.
Although this may need to also include size information so I can track changes in price and size availabillity within my dataset. After attempting to connect to the s3 bucket and check the etags of each item in the bucket im going to check the relational database for duplicate image links that have already been uploaded. The initial logic for this process is passing the unit test but doesnt actually appear to be uploading to the s3 bucket yet.

The arcitecture of my code means that methods in the data storage method are not seperated enough so I've had to rewrite the code to upload to s3 so i can upload to s3 and save my data locally seperately. Ive also realised that my test arcitecture is also insufficient and im scraping to many products at once to check that my uploads are working correctly annoyingly this revelation has come far to late in the testing stage. 

Testing has finished for the most part with regards to the scraper and im beggining to create a dockerfile and and requirements.txt file for the dockerfile
so my scraper can run in a docer container on an ec2 instance. My dockerfile is working although i need to create .env files for my database and s3bucket credentials as currently im unable to connect to them from the container. Creating the environment variable files is proving more diffiocult than I initially expected. The python decouple module allows for configuration of environment varibles from an .env file this then has to be passed to the container in order for it to be able to connect to the relational database and s3 bucket.

I have created an ec2 instance on amazon rds and after specifying security credentials for allowed for inbound connections. I have been able to connect to the instance and install docker to pull my docker image to run the containerised scraper on the ec2 instance although the scraper isnt currently working there as there appears to be an issue with locating web elements on asos from the ec2 instance. This appears to be related to the ec2 instance itself as the containerised scraper runs as expected on my local machine. As i have try some other solutions to the ec2 issue and so far none have worked it seems likely the ip of the ec2 iunstance is blocked by asos and that is why I cant detect the element so the next solution i will try is to run the ec2 instance through a proxy to see if i have any success. After running the ec2 through a proxy to a timeout error several times ive decided to change the location of the ec2 instance to euw to see if i have better success although its currently looking pretty bleak. After some unsuccessful tweaking with proxy servers i decided to revert to my initial solution of changing the location of the ec2 instance. I am happy to say that after moving the location of the ec2 instance to europe the scraper is running although upon the first run it appears i may need to make some small changes to waits in the code to increase the number of products that are successfully scraped.



'''
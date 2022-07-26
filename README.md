'''
DATA COLLECTION PIPELINE

Grabs T-Shirts from ASOS - to generate a repo of products & prices. 

I have created funtions to dynamically scrape asos and append the information to dictionaries and dictionaries of lists and then initialise a pandas dataframe. However manipulating and storing the data has been put on hold as my project has been interuppted by an asos student discount pop up that appears to be an iframe
I have implemented methods to close the iframe although they are increasing the time taken for the scraper to scrape data.

Although I wrote a try and except block to close the discount it appears to not be an issue anymore the dataframe is currently only printing as a single row I need to make the program create a row for each uuid/product, and then arrange to store the data in a manner whereby my list of product dictionaries is stored in a time/date sensetive manner.

Recently asos appear to have updated the website with a new product page type i have had to write a try and except block to manage the variation of product page types this and the student discount iframe have severly hindered my progress as tests rarely get to the point where i can see my dataframes form.

Have implemented the dataframe to json pandas method to locally store my dataframes in a date time sensitive manner. I have also implemented urllib retrive to download images from the src link from the image tag of the html element corresponding to the image.

After rethinking my page object model to improve the efficiency of my program i need to separate the page scraping methods and create a method to assert the type of product page before the link is scraped

The dataframes obtained from scraping are now saved in a folder with gallery images from the products page and these folders are saved in a date time sensitive manner to allow for analysis of product information over time. Its likely that we might want to make predictions based upon the data and being able to study the data over time allows for more accurate predictions.

The asos product pages appear to have different instances when loaded by the webdriver although my code accounts for this one of the product page types takes considerably longer to scrape almost 10x as long so reducing this time complexity is my current focus. I have also encountered the out of stock page these appear to be removed relatively fast although its an exception that is not currently handled by my code.

Recently i have been attempting to reduce the runtime of the scraper by reducing the amount of actions and reducing the amount of time i spend waiting for elements to appear so far this has reduced the runtime of the longest instance of the scraPer by almost 80%

I have finally solved the out of stock page issue with a try and except block, if else statements and the selenium web elemnt module the scraper now skips out of stock products when scraping i have also used extend of the href list in order to scrape multiple search result pages of products

I have got headless mode working it wasnt working as i was using the default user agent setting the user agent in my setUp function solved issues i was having with headless mode

I have finally got the error handling for out of stock something went wrong and outlets pages so the scraper can run without errors due to unscrapable product pages.

In order to set up the relational database and s3 bucket I created JSON files of the sensetive information credentials that I needed to gain access to my data stores and then initialised these parameters. The JSON files are opened and read in the setUp method of main.py then the parameters are specified in the init method of my StoreData class.

After setting up my s3 bucket and RDS I have created methods to upload the contents of the raw data folder to my s3 bucket, this method save the files locally then uploads the contents of the local raw_data folder to the specified s3 bucket.

I have written a test to upload a single dataframe to my database and confirmed it in a terminal window connected to the database however i will need to
do some more work to ensure all the data is as i expect and ready for analysis and manipulation.

Uploading an dataframe of scraped product info proved to be harder than expected do to some required reworking of my object model and level of abstraction in different parts of the code. and now i can succefully upload a 72 row dataframe of product information to my relational database. My next focus is to ensure I can run tests to upload to my s3 bucket and my relational database in the same test run as my current version
'''
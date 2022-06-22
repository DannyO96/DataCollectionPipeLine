'''
DATA COLLECTION PIPELINE

Grabs T-Shirts from ASOS - to generate a repo of products & prices. 

I have created funtions to dynamically scrape asos and append the information to dictionaries and dictionaries of lists and then initialise a pandas dataframe. However manipulating and storing the data has been put on hold as my project has been interuppted by an asos student discount pop up that appears to be an iframe
I have implemented methods to close the iframe although they are increasing the time taken for the scraper to scrape data.

Although I wrote a try and except block to close the discount it appears to not be an issue anymore the dataframe is currently only printing as a single row I need to make the program create a row for each uuid/product, and then arrange to store the data in a manner whereby my list of product dictionaries is stored in a time/date sensetive manner.

Recently asos appear to have updated the website with a new product page type i have had to write a try and except block to manage the variation of product page types this and the student discount iframe have severly hindered my progress as tests rarely get to the point where i can see my dataframes form.

Have implemented the dataframe to json pandas method to locally store my dataframes in a date time sensitive manner. I have also implemented urllib retrive to download images from the src link from the image tag of the html element corresponding to the image.





'''
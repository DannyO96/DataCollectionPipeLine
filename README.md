'''
DATA COLLECTION PIPELINE

Grabs T-Shirts from ASOS - to generate a repo of products & prices. 

I have created funtions to dynically scrape asos and append the information to nested dictionarieds and initialise a pandas dataframe, however manipulating and storing the data has been put on hold as my project has been interuppted by an asos student discount pop up that appears to be random i have tried running the scraper with various chrome options to stop the popup and several try and except block in my code however im yet to work out how to close it.

Although I wrote a try and except block to close the discount it appears to not be an issue anymore the dataframe is currently only printing as a single row I need to make the program create a row for each uuid/product, and then arrange to store the data in a manner whereby my list of product dictionaries is stored in a time/date sensetive manner.




'''
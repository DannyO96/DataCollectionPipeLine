import re
import os
import uuid
import pandas as pd
import urllib.request
import selenium
import requests
from sqlalchemy import true
import data_storage
from slugify import slugify
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from locators import MainPageLocators
from locators import ProductPageLocators
from locators import SearchResultsPageLocators
from element import BasePageElement
from data_storage import StoreData
from tqdm import tqdm

"""
I have separated methods for scraping in a page object model meaning each page object contains methods 
relevant to scraping that type of page on my chosen website.
"""
class BasePage(object):
    """
    This is the base page class it instanciates the webdriver and its method is inherited by every page class
    """
    def __init__(self, driver):
        self.driver = driver


#The main page class containing methods occuring on the main page of the website
class MainPage(BasePage):

    def does_title_match(self):
        """
        This is a function to check is the name of the site is in the title of the webpage.

        Args:
            param1:self 

        Returns:
            Returns a bool for if a phrase is in the title of the webpage in this case ASOS

        Raises:
            Error "ASOS" not in self.driver.title
        """
        return "ASOS" in self.driver.title
    
    def print_page_source(self):
        """
        This is a function to print out the source html of the page im using, essentially its the function that helps to understand 
        why headless mode isnt working correctly
        """
        url = ('https://www.asos.com/')
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            'Content-Type': 'text/html',
        }

        response = requests.get(url, headers=headers)
        html = response.text
        print(html)

    def navigate_to_men(self):
        """
        This is a function to check is the name of the site is in the title of the webpage.

        Args:
            param1:self 

        Returns:
            clicks the mens section BUTTON
        Raises:
            
        """
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(MainPageLocators.MEN_SECTION))
        element.click()

    def navigate_to_women(self):
        """
        This is a function to navigate to the womens section

        Args:
            param1:self 

        Returns:
            Clicks the womens section button

        Raises:
            Error "ASOS" not in self.driver.title
        """
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(MainPageLocators.WOMEN_SECTION))
        element.click()

    def click_search_bar(self):
        """
        This function clicks the searchbar on the website homepage

        Args:
            param1:self
        Returns:

        Raises:
            Element not found if search bar isnt present on the page
        """
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.click()
    
    def accept_cookies(self):
        """
        This is a function to accept cookies after loading the webpage

        Args:
            param1:self

        Returns:
            Clears cookie cache and clicks the accept cookies button

        Raises:
            ElementNotFound: If the presence of the element is not located
        """
        self.driver.delete_all_cookies()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((MainPageLocators.ACCEPT_COOKIES)))
        element.click()
        
    def headless_accept_cookies(self):
        self.driver.delete_all_cookies()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((MainPageLocators.ACCEPT_COOKIES)))
        element.click()
        print("cookies accepted")

    def search_asos(self):
        """
        This is an example of Google style.

        Args:
            param1:self

        Returns:
            Searches a phrase into the searchbar and enters the search results page

        Raises:
            KeyError: Raises an exception.
        """
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.send_keys("tshirt")
        element.send_keys(Keys.RETURN)

#Search results page class containing methods occuring on the search results page of the website
class SearchResultPage(BasePage):

    def get_image_links(self):
        """
        This function generates a list of image links from the search results page

        Args:
            param1:self

        Returns:
            A list of image links located using the img tag and the src attribute

        Raises:
            KeyError: Raises an exception.
        """
        product_container = self.driver.find_element(*SearchResultsPageLocators.PRODUCT_CONTAINER)
        products = product_container.find_elements(*SearchResultsPageLocators.PRODUCT_LIST)
        image_links = []

        for product in products:
            img_tag = product.find_element(*SearchResultsPageLocators.IMG_TAG)
            image_link = img_tag.get_attribute('src')

            if image_link in image_links:
                pass
            else:
                image_links.append(image_link)
        print(image_links)
        return(image_links)

    def get_href_list(self):
        """
        This is a function to generate a list of products links(hrefs)

        Args:
            param1:self

        Returns:
            Returns a list of links to product pages

        Raises:
            KeyError: Raises an exception.
        """
        product_container = self.driver.find_element(*SearchResultsPageLocators.PRODUCT_CONTAINER)
        products = product_container.find_elements(*SearchResultsPageLocators.PRODUCT_LIST)
        href_list = []

        for product in products:
            a_tag = product.find_element(*SearchResultsPageLocators.A_TAG)
            href = a_tag.get_attribute('href')

            if href in href_list:
                pass
            else:
                href_list.append(href)
        return(href_list)

    def is_results_found(self):
        """
        This is an example of Google style.

        Args:
            param1: self

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        return "No results found." not in self.driver.page_source

     #function to load more search results after the initial search
    def load_more_results(self):
        """
        This is a function to click the load more button on the search results page

        Args:
            param1: self.

        Returns:
            This returns a search results page with more search results loaded

        Raises:
            KeyError: Raises an exception.
        """
        element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SearchResultsPageLocators.LOAD_MORE))
        element.click()

#Product page class containing methods occuring on the page of a product 
class ProductPage(BasePage):
    def close_modal_popup(self):
        """
        This is a function i created in an attempt to close the student discount modal popups

        Args:
            param1: This is the first param.
            param2: This is a second param.

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        try: 
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(ProductPageLocators.STUDENT_DISCOUNT_CLOSE))
            self.driver.execute_script("arguments[0].click();", element)
            print('discount closed')
        except Exception as ex:
            print('no discounts yet')

    def frame_switch(self):
        """
        This is an example of Google style.

        Args:
            param1: This is the first param.
            param2: This is a second param.

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        self.driver.switch_to.frame(ProductPageLocators.STUDENT_DISCOUNT_IFRAME)
        element = self.driver.find_element(*ProductPageLocators.STUDENT_DISCOUNT_CLOSE)
        element.click()
        self.driver.Switch_to.default_content()

    def switch_iframes(self):
        """
        This is an example of Google style.

        Args:
            param1: This is the first param.
            param2: This is a second param.

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        iframes = self.driver.find_elements(*ProductPageLocators.IFRAMES)
        print(len(iframes))
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)        
            self.driver.switch_to.default_content()

    def close_alert(self):
        """
        This is an example of Google style.

        Args:
            param1: This is the first param.
            param2: This is a second param.

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        iframes = self.driver.find_elements(*ProductPageLocators.IFRAMES)
        print(len(iframes))
        for iframe in iframes:
            try:
                self.driver.switch_to.frame()
                element = self.driver.find_element(*ProductPageLocators.STUDENT_DISCOUNT_CLOSE)
                element.click()
            except:
                pass
        self.driver.switch_to.default_content()

    def create_uuid(self):
        """
        This function creates a unique user id and returns it.
        Args:
            param1: self.
        Returns:
            A unique user id is created and returned.
        Raises:
            
        """
        UUID = str(uuid.uuid4())
        return UUID

    def scrape_links(self, href_list):
        """
        This is my original function to scrape links from asos product pages this function was made before asos introduced multiple product page types and as such no longer works
        successfully.

        Args:
            param1: self.
            param2: href_list, this is a list of links to product pages.

        Returns:
            Tis function returns a pandas dataframe.

        Raises:
            KeyError: Raises an exception.
        """
        image_link_list = []
        productname_list = []
        uuid_list = []
        prodcode_list = []
        sizeinfo_list = []
        imginfo_list = []
        proddetails_list = []
        aboutprod_list = []
        priceinfo_list = []
        #frame = pd.DataFrame(prod_dict, index = UUID, columns = list('prodcode', 'sizeinfo', 'imginfo', 'proddetails', 'aboutprod', 'priceinfo'))
        #frame = pd.DataFrame()

        for i in tqdm(href_list):
            self.driver.get(i)
            print("current href is ?", i)
            UUID = self.create_uuid()
            self.switch_iframes()
            element = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS_CONTAINER)
            #self.switch_iframes()
            element.click()
            self.switch_iframes()
            
            
            #(/html/body)

            product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
            product_code = self.driver.find_element(*ProductPageLocators.PRODUCT_CODE)
            size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
            img_info = self.driver.find_element(*ProductPageLocators.IMG_INFO)
            product_details = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS)
            about_product = self.driver.find_element(*ProductPageLocators.ABOUT_PRODUCT)
            price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
            img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
            image_link = img_tag.get_attribute('src')
            
            image_link_list.append(image_link)
            productname_list.append(product_name.text)
            uuid_list.append(UUID)
            prodcode_list.append(product_code.text)
            sizeinfo_list.append(size_info.text)
            imginfo_list.append(img_info.text)
            proddetails_list.append(product_details.text)
            aboutprod_list.append(about_product.text)
            priceinfo_list.append(price_info.text)

            prod_dict = {'product_name': productname_list,'href': i, 'UUID': uuid_list, 'product_code': prodcode_list, 'size_info' : sizeinfo_list, 'img_info' : imginfo_list, 'product_details' : proddetails_list, 'about_product' : aboutprod_list, 'price_info'  : priceinfo_list, 'img_link' : image_link_list}
        frame = pd.DataFrame.from_dict(prod_dict, ignore_index=True)
            #frame.reindex(UUID)
            #frame = frame.append(prod_dict, ignore_index=True)
        print(frame)
        return(frame)

    def assert_prod_page_type(self, UUID, i):
        """
        This is a function to determine the type of product page the webdriver is on.

        Args:
            param1: self.
            param2: i - this is the href of the product.
            param3: UUID the generated unique user id for the product in this instance of scraping.

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        frame = 1
        filename = 1
        
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DETAILS_CONTAINER))
            frame, filename = self.scrape_primary_prodpage(UUID, i)
        except:
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON))
                frame, filename = self.scrape_altprod_pages(UUID, i)
            except:
                pass
            #try:
            #    frame, filename = self.scrape_secondary_product_page(UUID, i)
            #except:
            #    frame, filename = self.scrape_tertiary_product_page(UUID, i)
        return(frame, filename)
        

        #number of buttons = sec or tert
    

    def scrape_primary_prodpage(self, i, UUID):
        """
        This is a function to scrape the primary product page type for information it clicks the product details container the creates a dataframe 
        of product information

        Args:
            param1: self
            param2: i - this is the href of the product
            param3: UUID the generated unique user id for the product in this instance of scraping

        Returns:
            This function returns the dataframe of product information and the filename which is the full product name

        Raises:
            KeyError: Raises an exception.
        """
        element = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DETAILS_CONTAINER))
        element.click()
        print('clicked container')
        #self.close_alert()
        #self.switch_iframes()
    
        product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
        product_code = self.driver.find_element(*ProductPageLocators.PRODUCT_CODE)
        size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
        img_info = self.driver.find_element(*ProductPageLocators.IMG_INFO)
        product_details = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS)
        about_product = self.driver.find_element(*ProductPageLocators.ABOUT_PRODUCT)
        price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
        img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
        image_link = img_tag.get_attribute('src')

        image_link_list = []
        product_name_list = []
        uuid_list = []
        product_code_list = []
        size_info_list = []
        img_info_list = []
        product_details_list = []
        about_product_list = []
        price_info_list = []

        image_link_list.append(image_link)
        product_name_list.append(product_name.text)
        uuid_list.append(UUID)
        product_code_list.append(product_code.text)
        size_info_list.append(size_info.text)
        img_info_list.append(img_info.text)
        product_details_list.append(product_details.text)
        about_product_list.append(about_product.text)
        price_info_list.append(price_info.text)
        name = (product_name.text)

        prod_dict = {'product_name': name,'href': i, 'UUID': uuid_list, 'product_code': product_code_list, 'size_info' : size_info_list, 'img_info' : img_info_list, 'product_details' : product_details_list, 'about_product' : about_product_list, 'price_info'  : price_info_list, 'img_link' : image_link}
        frame = pd.DataFrame.from_dict(prod_dict)
        print(frame)
        filename = name
        return(frame, filename)

    def scrape_altprod_pages(self, i ,UUID):
        """
        This is a function to scrape the 
        Args:
            param1: self
            param2: i - this is the href of the product
            param3: UUID the generated unique user id for the product in this instance of scraping

        Returns:
            This function returns the dataframe of product information and the filename which is the full product name

        Raises:
            KeyError: Raises an exception.
        """
        product_description_list = []
        brand_list = []
        size_and_fit_list = []
        look_after_me_list = []
        about_me_list = []
        
        #buttons = self.driver.find_elements(*ProductPageLocators.SECONDARY_BUTTONS)
        #for button in buttons:
        #    button.click()
            #text = button.get_attribute("aria-label")
        try:
            #product_description = self.driver.find_element(ProductPageLocators.PRODUCT_DESCRIPTION)
            product_description = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DESCRIPTION))
            product_description_list.append(product_description.get_attribute("textContent"))
        except:
            product_description_list.append("NULL")
        try:
            #brand = self.driver.find_element(ProductPageLocators.BRAND)
            brand = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(ProductPageLocators.BRAND))
            brand_list.append(brand.get_attribute("textContent"))
        except:
            brand_list.append('NULL')
        try:
            #size_and_fit = self.driver.find_element(ProductPageLocators.SIZE_AND_FIT)
            size_and_fit = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(ProductPageLocators.SIZE_AND_FIT))
            size_and_fit_list.append(size_and_fit.get_attribute("textContent"))
        except:
            size_and_fit_list.append('NULL')
        try:
            #look_after_me = self.driver.find_element(ProductPageLocators.LOOK_AFTER_ME)
            look_after_me = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(ProductPageLocators.LOOK_AFTER_ME))
            look_after_me_list.append(look_after_me.get_attribute("textContent"))
        except:
            look_after_me_list.append('NULL')
        try:
            #about_me = self.driver.find_element(ProductPageLocators.ABOUT_ME)
            about_me = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(ProductPageLocators.ABOUT_ME))
            about_me_list.append(about_me.get_attribute("textContent"))
        except:
            about_me_list.append('NULL')

        product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
        size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
        price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
        img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
        image_link = img_tag.get_attribute('src')

        prod_dict = {'product_name': (product_name.text),'href': i, 'UUID': UUID, 'product_description' : product_description_list, 'brand' : brand_list, 'size_and_fit' : size_and_fit_list, 'look_after_me' : look_after_me_list, 'about_me' : about_me_list, 'price_info' : (price_info.text), 'img_link' : image_link}
        self.switch_iframes()
        frame = pd.DataFrame.from_dict(prod_dict)
        print(frame)
        filename = (product_name.text)
        return(frame, filename)
    
    def format_filename(self, filename):
        """
        This is a function to turn the name of the file in to a system date time stamped slug ready to be save locally or on the cloud

        Args:
            param1: self
            param2: filename - this is the name of the product file before processing

        Returns:
            This function reeturns the filename ready to be save locally or on the cloud without issues

        Raises:
            TypeError: decoding to str: need a bytes-like object, int found. occurs when attempting to slugify file this occurs because the
        """
        sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
        new_filename = slugify(filename)
        newest_filename = new_filename + sys_dtime
        return(newest_filename)
        

    
    def save_dataframe_locally(self, frame, filename):
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
            TypeError: decoding to str: need a bytes-like object, int found. occurs when attempting to slugify file this occurs because the
        """
        #filename = product_name.text
        new_filename = slugify(filename)
        sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
        os.makedirs("/home/danny/git/DataCollectionPipeline/raw_data/"f"{new_filename}{sys_dtime}")
        folder = (r"/home/danny/git/DataCollectionPipeline/raw_data/"f"{new_filename}{sys_dtime}")
        filepath = os.path.join(folder, f"{new_filename}{sys_dtime}.json")
        frame.to_json(filepath, orient = 'table', default_handler=str)
        filepath2 = os.path.join(folder, f"{new_filename}{sys_dtime}.jpeg")
        img_tag = self.driver.find_element(*ProductPageLocators.GALLERY_IMAGE)
        image_link = img_tag.get_attribute('src')
        urllib.request.urlretrieve(image_link, filepath2)

        return (frame, new_filename)

    def save_dataframe_and_image_locally(self, frame, filename):
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
            TypeError: decoding to str: need a bytes-like object, int found. occurs when attempting to slugify file this occurs because the
        """
        #filename = product_name.text
        os.makedirs("/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}")
        folder = (r"/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}")
        filepath = os.path.join(folder, f"{filename}.json")
        frame.to_json(filepath, orient = 'table', default_handler=str)
        filepath2 = os.path.join(folder, f"{filename}.jpeg")
        img_tag = self.driver.find_element(*ProductPageLocators.GALLERY_IMAGE)
        image_link = img_tag.get_attribute('src')
        urllib.request.urlretrieve(image_link, filepath2)

        return (frame, filename)

    def scrape_prod_pages(self, href_list, data_store):
        """
        This is a function to scrape multiple product page types

        Args:
            param1: self.
            param2: href_list, this is a list of links to product pages returned from the function get href list.

        Returns:
            This function iterates through every link in the href list, checks for know exceptions then creates a UUID for the product asserts the type of product page then creates a dataframe and saves it locally
            in a folder in the raw data folder with the image and dataframe contained in the folder.

        Raises:
            TypeError: decoding to str: this occurs when the dataframe has not been created correctly usually due to an unhandled out of stock label or a something gone wrong label although try and accept blocks 
            have now been implemented to avoid this error.
        """
        for i in tqdm(href_list):
            self.driver.get(i)
            prods_frame = pd.DataFrame()
            try:
                try:
                    out_of_stock = self.driver.find_element(*ProductPageLocators.OUT_OF_STOCK)
                    oos = WebElement.is_displayed(out_of_stock)
                except selenium.common.exceptions.NoSuchElementException:
                    oos=False
                try:
                    something_gone_wrong = self.driver.find_element(*ProductPageLocators.SOMETHING_GONE_WRONG)
                    sgw = WebElement.is_displayed(something_gone_wrong)
                except selenium.common.exceptions.NoSuchElementException:
                    sgw=False
                try:
                    container = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS_CONTAINER)
                    pdc = WebElement.is_displayed(container)
                except selenium.common.exceptions.NoSuchElementException:
                    pdc = False
                try:
                    desc_button = self.driver.find_element(*ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON)
                    pdb = WebElement.is_displayed(desc_button)
                except selenium.common.exceptions.NoSuchElementException:
                    pdb = False
                scrapable = pdc or pdb 
            except Exception as E:
                print('Exception: ', E)
            print("oos=",oos," sgw=",sgw," scrapable=",scrapable)    

            if oos == True or sgw == True or scrapable == False:
                print('something wrong')
                continue
            
            else:
                UUID = self.create_uuid()
                print('uuid created')
                frame, self.filename = self.assert_prod_page_type(i, UUID)
                #frame, filename = self.save_dataframe_locally(self.frame, self.filename)
                filename = self.format_filename(self.filename)
                frame.insert(0, "filename",filename)
                prods_frame.append(frame, ignore_index=True)
                
        data_store.process_data(prods_frame)
        print(prods_frame)
        return(frame, filename)
            
        
    def test_rds_upload(self, href_list):
        for i in tqdm(href_list):
            pass
        self.driver.get(i)
        UUID = self.create_uuid()
        print('uuid created')
        frame, self.filename = self.assert_prod_page_type(i, UUID)
        filename = self.format_filename(self.filename)
        self.save_dataframe_and_image_locally(frame, filename)
        return(frame, filename)
        








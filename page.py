import uuid
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from locators import MainPageLocators
from locators import ProductPageLocators
from locators import SearchResultsPageLocators
from element import BasePageElement
from tqdm import tqdm


#The parent Page class containing general page object methods
class BasePage(object):

    def __init__(self, driver):
        self.driver = driver

#The main page class containing methods occuring on the main page of the website
class MainPage(BasePage):

    def does_title_match(self):
        return "ASOS" in self.driver.title

    def click_search_bar(self):
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.click()
    
    def accept_cookies(self):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((MainPageLocators.ACCEPT_COOKIES)))
        element.click()
        

    def search_asos(self):
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.send_keys("t shirt")
        element.send_keys(Keys.RETURN)

#Search results page class containing methods occuring on the search results page of the website
class SearchResultPage(BasePage):

    def get_href_List(self):
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
        return "No results found." not in self.driver.page_source

#Product page class containing methods occuring on the page of a product 
class ProductPage(BasePage):

    def create_uuid(self):
        UUID = str(uuid.uuid4())
        return UUID

    def scrape_links(self):

        href_list = SearchResultPage.get_href_List(self)
        #prodcode_list = []
        #sizeinfo_list = []
        #imginfo_list = []
        #proddetails_list = []
        #aboutprod_list = []
        #priceinfo_list = []
        #frame = pd.DataFrame(prod_dict, index = UUID, columns = list('prodcode', 'sizeinfo', 'imginfo', 'proddetails', 'aboutprod', 'priceinfo'))
        frame = pd.DataFrame()

        for i in tqdm(href_list):
            self.driver.get(i)
            UUID = self.create_uuid()
            element = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS_CONTAINER)
            element.click()

            prodcode = self.driver.find_element(*ProductPageLocators.PRODUCT_CODE)
            sizeinfo = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
            imginfo = self.driver.find_element(*ProductPageLocators.IMG_INFO)
            proddetails = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS)
            aboutprod = self.driver.find_element(*ProductPageLocators.ABOUT_PRODUCT)
            priceinfo = self.driver.find_element(*ProductPageLocators.PRICE_INFO)

            #prodcode_list.append(prodcode.text)
            #sizeinfo_list.append(sizeinfo.text)
            #imginfo_list.append(imginfo.text)
            #proddetails_list.append(proddetails.text)
            #aboutprod_list.append(aboutprod.text)
            #.append(priceinfo.text)
            
            prod_dict = { UUID : {'prodcode': prodcode.text, 'sizeinfo' : sizeinfo.text, 'imginfo' : imginfo.text, 'proddetails' : proddetails.text, 'aboutprod' : aboutprod.text, 'priceinfo'  : priceinfo.text}}
            frame = frame.append(prod_dict,ignore_index=True)
        print(frame.T)
        return(frame.T)
    

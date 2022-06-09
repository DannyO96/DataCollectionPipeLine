from cgitb import text
import uuid
import pandas as pd
from telnetlib import SE
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from locators import MainPageLocators
from locators import ProductPageLocators
from locators import SearchResultsPageLocators
from element import BasePageElement
from tqdm import tqdm



class BasePage(object):

    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):

    def does_title_match(self):
        return "ASOS" in self.driver.title

    def click_search_bar(self):
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.click()
    
    def accept_cookies(self):
        element = BasePageElement
        locator = self.driver.find_element(*MainPageLocators.ACCEPT_COOKIES)
        element.wait_to_locate(locator)
        locator.click()


    def search_asos(self):
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.send_keys("t shirt")
        element.send_keys(Keys.RETURN)



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

class ProductPage(BasePage):

    def create_uuid(self):
        UUID = str(uuid.uuid4())
        return UUID

    def scrape_links(self):
        href_list = SearchResultPage.get_href_List(self)
        prodcode_list = []
        sizeinfo_list = []
        imginfo_list = []
        proddetails_list = []
        aboutprod_list = []
        priceinfo_list = []

        for href in tqdm(href_list):
            UUID = self.create_uuid()
            self.driver.get(href)
            element = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS_CONTAINER)
            element.click()
            prodcode_list.append(*ProductPageLocators.PRODUCT_CODE)
            sizeinfo_list.append(*ProductPageLocators.SIZE_INFO)
            imginfo_list.append(*ProductPageLocators.IMG_INFO)
            proddetails_list.append(*ProductPageLocators.PRODUCT_DETAILS)
            aboutprod_list.append(*ProductPageLocators.ABOUT_PRODUCT)
            priceinfo_list.append(*ProductPageLocators.PRICE_INFO)
            prod_dict = { UUID : {'prodcode': prodcode_list, 'sizeinfo' : sizeinfo_list, 'imginfo' : imginfo_list, 'proddetails' : proddetails_list, 'aboutprod' : aboutprod_list, 'priceinfo'  : priceinfo_list}}
        frame = pd.DataFrame(prod_dict)
        print(frame.T)
        return(frame.T)
    

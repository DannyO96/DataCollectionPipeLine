from telnetlib import SE
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from locator import MainPageLocators
from locator import SearchResultsPageLocators
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
        element = self.driver.find_element(*MainPageLocators.ACCEPT_COOKIES)
        element.click()

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

    def scrape_links(self):
        href_list = self.get_href_List()

        prodcode_list = []
        sizeinfo_list = []
        imginfo_list = []
        proddetails_list = []
        aboutprod_list = []
        priceinfo_list = []
        
        
        

    def is_results_found(self):
        return "No results found." not in self.driver.page_source



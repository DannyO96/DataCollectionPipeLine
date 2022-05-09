from telnetlib import SE
from xml.dom.minidom import Element
from selenium.webdriver.common.keys import Keys
from locator import MainPageLocators
from locator import SearchResultsPageLocators
from element import BasePageElement

class SearchTextElement(BasePageElement):
    locator = 'q'

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):

    search_text_element = SearchTextElement()

    def does_title_match(self):
        return "ASOS" in self.driver.title

    def click_go_button(self):
        element = self.driver.find_element(*MainPageLocators.GO_BUTTON)
        element.click()
    
    def accept_cookies(self):
        element = self.driver.find_element(*MainPageLocators.ACCEPT_COOKIES)
        element.click()


class SearchResultPage(BasePage):

    def Print_Product_List(self):
        element = self.driver.find_element(*SearchResultsPageLocators.PRODUCT_LIST)
        print(element)

    def is_results_found(self):
        return "No results found." not in self.driver.page_source



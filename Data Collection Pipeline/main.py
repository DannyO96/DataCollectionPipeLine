import unittest
from selenium import webdriver
import page
import locator
import time
from selenium.webdriver.common.keys import Keys


class AsosScraper(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("/home/danny/chromedriver")
        self.driver.get("https://www.asos.com/")

    def click_button(self, ID):
        button = self.driver.find_element_by_ID(ID)
        button.click()

    def press_enter(self, ID):
        button = self.driver.find_element_by_ID(ID)
        button(Keys.RETURN)

    def _title(self):
        mainPage = page.MainPage
        assert mainPage.does_title_match(self)

    def _accept_cookies(self):
        mainPage = page.MainPage
        mainPage.accept_cookies

    def test_search_asos(self):
        mainPage = page.MainPage
        mainPage.search_text_element = "T Shirt"
        mainPage.search_text_element = (Keys.RETURN)
        search_result_page = page.SearchResultPage(self.driver)
        assert search_result_page.is_results_found()
    
    def _print_product_list(self):
        mainPage = page.MainPage
        mainPage.search_text_element = "T Shirt"
        mainPage.click_go_button
        search_result_page = page.SearchResultPage(self.driver)
        assert search_result_page.Print_Product_List()

    def tearDown(self):
        self.driver.close


if __name__ == "__main__":
    unittest.main()
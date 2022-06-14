import unittest
import page
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AsosScraper(unittest.TestCase):

    def setUp(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-notifications')
        option.add_argument('--disable-forms')
        option.add_argument('--disable-scripts')
        #option.add_argument('--headless')
        #option.add_argument('--disable-gpu')  
        self.driver = webdriver.Chrome("/home/danny/chromedriver",options = option)
        self.driver.get("https://www.asos.com/")

    def title(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.does_title_match(self)

    def est_accept_cookies(self):
        mainPage = page.MainPage(self.driver)
        mainPage.accept_cookies()

    def est_search_asos(self):
        mainPage = page.MainPage(self.driver)
        mainPage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
    
    def est_print_product_list(self):
        mainPage = page.MainPage
        mainPage.search_text_element = "T Shirt"
        mainPage.click_go_button
        search_result_page = page.SearchResultPage(self.driver)
        
    def est_get_href_list(self):
        mainPage = page.MainPage(self.driver)
        mainPage.accept_cookies()
        mainPage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        search_result_page.get_href_List()

    def test_create_pd_dataframe(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        search_result_page.get_href_List()
        product_page = page.ProductPage(self.driver)
        product_page.scrape_links()
        
    def tearDown(self):
        self.driver.close


if __name__ == "__main__":
    unittest.main()
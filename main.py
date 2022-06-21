import unittest
import page
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#Scraper class
class AsosScraper(unittest.TestCase):

    #Method to initialize the chromedriver
    def setUp(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-notifications')
        option.add_argument('--disable-forms')
        option.add_argument('--disable-scripts')
        option.add_argument('--disable-secure-containers')
        option.add_argument('--disable-same-origin')
        option.add_argument('--disable-secure-scripts')
        #option.add_argument("--window-size=1920,1080")
        #option.add_argument("--disable-extensions")
        option.add_argument('--no-sandbox')
        #option.add_argument('--allow-insecure-localhost')
        #option.add_argument('--disable-blink-features=AutomationControlled')
        #option.add_argument('--disable-modal-content')
        #option.add_argument('--headless')
        option.add_argument('--disable-gpu')  
        #option.add_argument("start-maximized")

        self.driver = webdriver.Chrome("/home/danny/chromedriver",options = option)
        self.driver.get("https://www.asos.com/")

    #Test that we are on the webpage
    def title(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.does_title_match(self)

    #test to accept cookies
    def est_accept_cookies(self):
        mainPage = page.MainPage(self.driver)
        mainPage.accept_cookies()

    #Test to search asos
    def est_search_asos(self):
        mainPage = page.MainPage(self.driver)
        mainPage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)

    #Test to obtain a list of links to images  
    def est_get_image_links(self):
        mainPage = page.MainPage(self.driver)
        mainPage.accept_cookies()
        mainPage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.image_link_list = page.SearchResultPage.get_image_links(self)

    #Test to create a pd dataframe of product information
    def est_create_pd_dataframe(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = page.SearchResultPage.get_href_List(self)
        product_page = page.ProductPage(self.driver)
        product_page.scrape_links(self.href_list)

    #Test to create a product dictionaries aquired from multiple product page types
    def test_create_dicts_on_dif_prod_pages(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = page.SearchResultPage.get_href_List(self)
        product_page = page.ProductPage(self.driver)
        product_page.scrape_links_on_multiple_product_pages(self.href_list)

    #Method to close the webdriver    
    def tearDown(self):
        self.driver.close


if __name__ == "__main__":
    unittest.main()
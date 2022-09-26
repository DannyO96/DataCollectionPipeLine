import data_storage
import json
import page
import unittest
from fp.fp import FreeProxy
from selenium import webdriver

#Scraper class
class AsosScraper(unittest.TestCase):

    #Method to initialize the chromedriver
    def setUp(self):
        #proxy = FreeProxy(country_id=['IRE']).get()
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
        options = webdriver.ChromeOptions()

        #option.add_argument('--proxy-server=%s' % proxy)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-forms')
        options.add_argument('--disable-scripts')
        options.add_argument('--disable-secure-containers')
        options.add_argument('--disable-same-origin')
        options.add_argument('--disable-secure-scripts')
        options.add_argument('-window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  

        self.driver = webdriver.Chrome("/home/danny/chromedriver",options = options)#/home/danny/chromedriver   /usr/local/bin/chromedriver
        self.driver.get("https://www.asos.com/")

        #JSON file for s3 bucket credentials
        #f = open('my.secrets.AWSbucket.json', "r")
        #self.s3_params = json.loads(f.read())
        #JSON file for RDS credentials
        #f = open('my.secrets.RDSdb.json', "r")
        #self.rds_params = json.loads(f.read())
            
    #Test that we are on the webpage
    def est_title(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.does_title_match()

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
        self.image_link_list = search_result_page.get_image_links()
        print(self.image_link_list)

    #Test to create a pd dataframe of product information
    def est_create_pd_dataframe(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = search_result_page.get_href_list()
        product_page = page.ProductPage(self.driver)
        product_page.scrape_prod_pages(self.href_list)

    #Test to locally save the dataframes in the raw data folder with their corresponding images
    def est_locally_save_dataframes_and_images(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.navigate_to_women()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = search_result_page.get_href_list()
        product_page = page.ProductPage(self.driver)
        prods_frame = product_page.scrape_prod_pages(self.href_list)
        data_store = data_storage.StoreData()
        self.engine = data_store.create_engine()
        data_store.save_locally(prods_frame, self.engine)

    #Test to scrape multiple pages of products and upload the product data to s3 and rds
    def est_scrape_lots_of_prods(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.navigate_to_men()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = search_result_page.get_href_list()
        while True:
            search_result_page.load_more_results()
            thisl = search_result_page.get_href_list()
            self.href_list += thisl
            if len(thisl) > 200:
                break
        product_page = page.ProductPage(self.driver)
        prods_frame = product_page.scrape_prod_pages(self.href_list)
        data_store = data_storage.StoreData()
        self.engine = data_store.create_engine()
        data_store.process_data(prods_frame, self.engine)

    #Test to upload and image data scraped into an amazon s3 bucket
    def est_upload_img_data_to_s3(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = search_result_page.get_href_list()
        product_page = page.ProductPage(self.driver)
        prods_frame = product_page.scrape_prod_pages(self.href_list)
        store_data = data_storage.StoreData()
        self.engine = store_data.create_engine()
        store_data.save_images_to_s3(prods_frame, self.engine)

    #test to upload 1 search result page of scraped data to my relational database
    def est_upload_dataframe_to_rds(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.navigate_to_men()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = search_result_page.get_href_list()
        product_page = page.ProductPage(self.driver)
        prods_frame = product_page.scrape_prod_pages(self.href_list)
        data_store = data_storage.StoreData()
        self.engine = data_store.create_engine()
        data_store.send_dataframe_to_rds(prods_frame, self.engine)

    #This test consitutes the final scraper it scrapes product information then uploads it to cloud storage    
    def test_upload_to_rds_and_upload_to_s3(self):
        mainpage = page.MainPage(self.driver)
        #mainpage.print_page_source()
        mainpage.accept_cookies()
        mainpage.navigate_to_women()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = search_result_page.get_href_list()
        product_page = page.ProductPage(self.driver)
        prods_frame = product_page.scrape_prod_pages(self.href_list)
        data_store = data_storage.StoreData()
        self.engine = data_store.create_engine()
        data_store.save_images_to_s3(prods_frame, self.engine)
        data_store.send_dataframe_to_rds(prods_frame, self.engine)

    def est_upload_single_frame(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.navigate_to_women()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = search_result_page.get_href_list()
        product_page = page.ProductPage(self.driver)
        prods_frame = product_page.scrape_prod_page(self.href_list)
        data_store = data_storage.StoreData() #self.rds_params, self.s3_params
        self.engine = data_store.create_engine()
        data_store.save_images_to_s3(prods_frame, self.engine)
        data_store.send_dataframe_to_rds(prods_frame, self.engine)

    def est_multithread_scraping(self):
        mainpage = page.MainPage(self.driver)
        mainpage.accept_cookies()
        mainpage.navigate_to_women()
        mainpage.search_asos()
        search_result_page = page.SearchResultPage(self.driver)
        self.href_list = search_result_page.get_href_list()
        product_page = page.ProductPage(self.driver)
        product_page.multithreading(self.href_list)


    #Method to close the webdriver    
    def tearDown(self):
        self.driver.close

if __name__ == "__main__":
    unittest.main()
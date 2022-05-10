import unittest
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
from tqdm import tqdm
import os



class ASOSScraper(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("/home/danny/chromedriver")
        self.driver.get("https://www.asos.com/")

    def accept_cookies(self):
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located ((By.ID, "onetrust-accept-btn-handler")))
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        

    def search_asos(self,):
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)

    def load_more_results(self):
        self.search_asos()
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located ((By.CLASS_NAME, "_39_qNys")))
        self.driver.find_element(By.CLASS_NAME, "_39_qNys").click()
        

    def find_container(self):
        self.accept_cookies()
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)
        self.container = self.driver.find_element(By.CLASS_NAME, '_3YREj-P')
        self.products = self.driver.find_elements(By.CLASS_NAME, "_2qG85dG")
        prod_list = []
        for products in tqdm(self.products):
            prod_list.append(products.find_elements(By.TAG_NAME, 'a'))
            print(prod_list)
        return prod_list

    def obtain_product_href(self):
        self.search_asos()
        href_list = []
        product_container_class = '_3YREj-P'
        product_container =  self.driver.find_element(By.CLASS_NAME, product_container_class)
        products = product_container.find_elements(By.CLASS_NAME, "_2qG85dG")

        for product in products:
            a_tag = product.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')

            if href in href_list:
                pass
            else:
                href_list.append(href)
        print(href_list)
        return(href_list)

    def test_obtain_product_info(self):
        self.search_asos()
        aria_list = []
        product_container_class = '_3YREj-P'
        product_container =  self.driver.find_element(By.CLASS_NAME, product_container_class)
        products = product_container.find_elements(By.CLASS_NAME, "_2qG85dG")

        for product in products:
            a_tag = product.find_element(By.TAG_NAME, 'a')
            aria = a_tag.get_attribute('aria-label')

            if aria in aria_list:
                pass
            else:
                aria_list.append(aria)
        print(aria_list)
        return(aria_list)

        

    def create_folder(self, raw_data):
        if not os.path.exists(raw_data):
            os.makedirs(raw_data)


    def tearDown(self):
            self.driver.close()


if __name__ == "__main__":
    unittest.main()

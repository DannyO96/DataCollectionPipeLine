import unittest
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from tqdm import tqdm
import os



class ASOSScraper(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("/home/danny/chromedriver")
        self.driver.get("https://www.asos.com/")

    def est_accept_cookies(self):
        #self.driver.get("https://www.asos.com/")
        WebDriverWait(self.driver, 100).until(
            self.driver.find_element(By.ID, "onetrust-accept-btn-handler"))
        cookie = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookie.click()

    def search_asos(self,):
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)

    def test_find_container(self):
        self.est_accept_cookies()
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)
        self.container = self.driver.find_element(By.XPATH, '//*[@id="plp"]/div/div[3]/div/div[1]/section')
        self.products = self.driver.find_elements(By.XPATH, "//*[@data-auto-id='productTile']/a")
        prod_list = []
        for products in tqdm(self.products):
            prod_list.append(products.find_elements(By.TAG_NAME, 'aria-label'))
            print(prod_list)
        return prod_list

    def create_folder(self, raw_data):
        if not os.path.exists(raw_data):
            os.makedirs(raw_data)


    def tearDown(self):
            self.driver.close()


if __name__ == "__main__":
    unittest.main()

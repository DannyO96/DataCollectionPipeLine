
import unittest
import selenium
import pandas as pd
import numpy as np
import re
import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class ASOSScraper(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("/home/danny/chromedriver")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        driver = webdriver.Chrome("/home/danny/chromedriver", chrome_options=options)
        self.driver.get("https://www.asos.com/") 
    
    def test_accept_cookies(self):
        self.driver.get("https://www.asos.com/")
        WebDriverWait(self.driver, 100).until(
            self.driver.find_element(By.ID, "onetrust-accept-btn-handler"))
        cookie = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookie.click()

    def est_load_more_results(self):
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)
        WebDriverWait(self, 100).until(
            self.driver.find_element(By.CLASS_NAME, "_39_qNys"))
        load_more = self.driver.find_element(By.CLASS_NAME, "_39_qNys")
        load_more.click()
    
    def search_asos(self):
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)

    def est_scrape_asos(self):
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)
        continue_link = self.driver.find_element_by_tag_name('a')
        elems = self.driver.find_elements_by_xpath("//*[@href]")
        for elem in elems:
            print(elem.get_attribute("href"))

    def _print_prodid_list(self):
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)
        prodIds = self.driver.find_elements(By.ID, 'product-')
        for prod in prodIds:
            print(prod.get_attribute("id"))

    def est_print_prodid_list(self):
        products = ["product-"]
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)
        prodIds = self.driver.find_elements_by_xpath("//*[@id]")
        for prod in prodIds:
            print(prod.get_attribute("id"))


    def est_print_prodid_list(self):
        products = {}
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)
        prodIds = self.driver.find_elements_by_xpath("//*[@data-auto-id='productTile']/a")  # data-auto-id="productTile"
        for prod in prodIds:
            id = prod.get_attribute("id")
            products[id]={}
            #print("Aria label is " + prod.get_attribute("aria-label"))
            #print("prod.text is " + prod.text)
            m = re.match(r"(.*); (Original price|Price): (.*), current price: (.*); Discount: (.*)",prod.get_attribute("aria-label"))
            #print(m.group(0))
            products[id]['desc'] = m.group(1)
            products[id]['price'] = m.group(3)
            products[id]['cp'] = m.group(4)
            products[id]['disc'] = m.group(5)
            print("Price" + id + " - " + products[id]['price'])
            print()

    def est_find_container(self):
        self.container = self.driver.find_element(By.XPATH,'//*[@id="chrome-app-container')
        self.products = self.container.find_elements(By.XPATH, "//*[@data-auto-id='productTile']/a")
        prod_list = []
        for items in tqdm(self.products):
            prod_list.append(items.find_elements(By.TAG_NAME, 'a').get_attribute('href'))
            print(prod_list)
        return prod_list

    def est_print_prodid_list(self):
        products = {}
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)
        prodIds = self.driver.find_elements_by_xpath("//*[@data-auto-id='productTile']/a")  # data-auto-id="productTile"
        for prod in prodIds:
            id = prod.get_attribute("id")
            products[id]={}
            #print("Aria label is " + prod.get_attribute("aria-label"))
            #print("prod.text is " + prod.text)
            try:
                m = re.match(r"(.*);\s*(.*)",prod.get_attribute("aria-label"))
            except Exception as E:
                print("WARN: Cannot get description for id:"+id+",aria-label="+prod.get_attribute("aria-label")+" : "+repr(E))
                products[id]['desc']=repr(E)
                next
            #print(m.group(0))
            products[id]['desc'] = m.group(1)
            products[id]['about'] = m.group(2)
            #try:
            pricing = products[id]['about'].split(';')[0]
            #except Exception as E:
            #    print("WARN: Cannot get pricing for id:"+id+",aria-label="+prod.get_attribute("aria-label")+" : "+repr(E))
            kv=[x.strip() for x in pricing.split(',')]

            for (k,v) in split(':',kv):
                if k == "current price":
                   k="Price"
                products[id][k] = v
            print()


    #def

    def filter_prod_id(self):
        pass

    def tearDown(self):
            self.driver.close

if __name__ == "__main__":
    unittest.main()

    
#//*[@id="product-200826600"]/a/div[1]/img
#//*[@id="product-203028176"]/a
#aria-label="Simply Be 3/4 sleeve ribbed tshirt midi dress with side split detail in chocolate; Price: £24.00"
#aria-label="ASOS Actual Athleisure co-ord oversized t-shirt with logo print in frappe; Price: £8.00; MIX & MATCH"
#aria-label="ASOS DESIGN oversized t-shirt with Ibiza Amnesia print in yellow; Price: £22.00"
#aria-label="Simply Be 3/4 sleeve ribbed tshirt midi dress with side split detail in chocolate; Original price: £24.00, current price: £19.25; Discount: -19%"

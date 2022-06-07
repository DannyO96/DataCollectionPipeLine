
import unittest
import selenium
import numpy as np
import pandas as pd
import os
import re
import uuid
import time
from ast import Assign
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from datetime import datetime, timedelta

#class for the methods of the asos scraper
class ASOSScraper(unittest.TestCase):

    def setUp(self):
        # vein attempts to block asos's pop ups which are making manipulation of my datafram so so easy !!!!!!
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-notifications')
        option.add_argument('--disable-forms')
        option.add_argument('--disable-scripts')
        #option.add_argument('--headless')
        #option.add_argument('--disable-gpu')  
        self.driver = webdriver.Chrome("/home/danny/chromedriver",chrome_options = option)
        self.driver.get("https://www.asos.com/")

    # simple funtion to accept cookies after loading the webpage
    def accept_cookies(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located ((By.ID, "onetrust-accept-btn-handler")))
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        
    #function to close the student discount pop up
    def close_discount(self):
        try: 
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located ((By.XPATH, '//*[@id="att_lightbox_close"]/svg/path')))
            self.driver.find_element(By.XPATH, '//*[@id="att_lightbox_close"]/svg/path').click()
            print('discount closed')
        except TimeoutError:
            print('no discounts yet')
            
    #function to search the website
    def search_asos(self,):
        self.driver.get("https://www.asos.com/")
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys("T Shirt")
        search.send_keys(Keys.RETURN)

    #function to load more search results after the initial search
    def load_more_results(self):
        self.search_asos()
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located ((By.CLASS_NAME, "_39_qNys")))
        self.driver.find_element(By.CLASS_NAME, "_39_qNys").click()

    #function to create a unique user ID for products found in the search
    def create_uuid(self):
        UUID = str(uuid.uuid4())
        return UUID
        
    #function to locate the container that contains the search results
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

    #function to obtain a list of links from the search results page
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
        return(href_list)

    #function to obtain product info via product aria labels
    def est_obtain_product_info(self):
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

    #function  to obtain a dictionary of product information
    def est_obtain_product_info_dict(self):
        self.search_asos()
        aria_list = []
        prods = {}
        product_container_class = '_3YREj-P'
        product_container =  self.driver.find_element(By.CLASS_NAME, product_container_class)
        products = product_container.find_elements(By.CLASS_NAME, "_2qG85dG")
        # this loop will do something heklpful
        for product in products:
            a_tag = product.find_element(By.TAG_NAME, 'a')
            aria = a_tag.get_attribute('aria-label')
            m = re.match(r"(.*); (Original price|Price): (.*), Original price: (.*); Discount: (.*)",product.get_attribute("aria-label"))
            print(m.group(0))
            prods[id]['desc'] = m.group(1)
            prods[id]['price'] = m.group(3)
            prods[id]['op'] = m.group(4)
            prods[id]['disc'] = m.group(5)
            print("Price" + id + " - " + prods[id]['price'])
            pricing = prods[id]['about'].split(';')[0]
            #except Exception as E:
            #    print("WARN: Cannot get pricing for id:"+id+",aria-label="+prod.get_attribute("aria-label")+" : "+repr(E))
            kv=[x.strip() for x in pricing.split(',')]

            for (k,v) in split(':',kv):
                if k == "current price":
                   k="Price"
                products[id][k] = v
            print()
        
    def tst_scrape_links(self):

        self.accept_cookies()
        href_list = self.obtain_product_href()

        for href in href_list:
            self.driver.get(href)
            self.driver.find_element(By.XPATH,'//*[@id="product-details-container"]/div[4]/div/a[1]').click()

    def est_scrape_links(self):

        self.accept_cookies()
        href_list = self.obtain_product_href()

        #product_data = ProductData(
        #    prodcode_list = [],
        #    sizeinfo_list = [],
        #    imginfo_list = [],
        #    proddetails_list = [],
        #    aboutprod_list = [],
        #    priceinfo_list = [],
        #    href_list = None)

        #df = pd.DataFrame((72, 6), index = uuid, columns = ('details', 'about', 'pricing', 'imginfo', 'prodcode', 'sizeoinfo'))

        # got list of hrefs from the product grabber. So onow we are going to fethch these & dump them in a nested dict.
        # then we get a new panda which is compriosed of that dict. (Idealls we would add a new panbda dataframe for each href and save the dict memory, gut I don;t know how to add panda dataframe to the existing dataframe thing.
        # )

        for href in href_list:
            #UUID = str(uuid.uuid4())
            UUID=self.create_uuid()
            #hprd={'UUID': [{'prodcodef':}]}
            self.driver.get(href)
            print("DBG: Clicking dets container")
            self.driver.find_element(By.XPATH,'//*[@id="product-details-container"]/div[4]/div/a[1]').click()
            hprd['prodcode'] = self.driver.find_element(By.XPATH,'//*[@id="product-details-container"]/div[2]/div[1]/p')
            hprd['sizeinfo'] = self.driver.find_element(By.XPATH, '//*[@id="main-size-select-0"]')
            hprd['imginfo'] = self.driver.find_element(By.XPATH, '//*[@id="product-details-container"]/div[3]/div[1]/p')
            hprd['proddetails'] = self.driver.find_element(By.XPATH, '//*[@id="product-details-container"]/div[1]/div')
            hprd['aboutprod'] = self.driver.find_element(By.XPATH, '//*[@id="product-details-container"]/div[3]/div[2]/p')
            hprd['priceinfo'] = self.driver.find_element(By.XPATH, '//*[@id="product-price"]/div[1]/span[2]')
            print("DEBUG: prodcode " + str(hprd['prodcode']) + " UUID="+UUID)
            #search page for pname  pic
            #hprd['pname'] = pname
            #hprd['pic'] = pic
        #df = pd.DataFrame((len(72), 6), index = uuid, columns = list('details', 'about', 'pricing', 'imginfo', 'prodcode', 'sizeinfo'))
        df = pd.DataFrame(hrefprods)
        df

    #function to visit links in the list open the product details container and store the product information in a pandas dataframe
    def test_scrape_links(self):

        self.accept_cookies()
        href_list = self.obtain_product_href()

        prodcode_list = []
        sizeinfo_list = []
        imginfo_list = []
        proddetails_list = []
        aboutprod_list = []
        priceinfo_list = []
        
        #df = pd.DataFrame((72, 6), index = uuid, columns = ('details', 'about', 'pricing', 'imginfo', 'prodcode', 'sizeoinfo'))
        # got list of hrefs from the product grabber. So onow we are going to fethch these & dump them in a nested dict.
        # then we get a new panda which is compriosed of that dict. (Idealls we would add a new panbda dataframe for each href and save the dict memory, gut I don;t know how to add panda dataframe to the existing dataframe thing.
        # )

        for i in tqdm(href_list):
            
            #UUID = str(uuid.uuid4())
            UUID=self.create_uuid()
            self.driver.get(i)
            print("DBG: Clicking dets container")
            self.close_discount
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located ((By.XPATH,'//*[@id="product-details-container"]/div[4]/div/a[1]')))
                self.driver.find_element(By.XPATH,'//*[@id="product-details-container"]/div[4]/div/a[1]').click()
            except TimeoutError:
                self.close_discount
                print('Discount Closed')

            prodcode = self.driver.find_element(By.XPATH,'//*[@id="product-details-container"]/div[2]/div[1]/p')
            sizeinfo = self.driver.find_element(By.XPATH, '//*[@id="main-size-select-0"]')
            imginfo = self.driver.find_element(By.XPATH, '//*[@id="product-details-container"]/div[3]/div[1]/p')
            proddetails = self.driver.find_element(By.XPATH, '//*[@id="product-details-container"]/div[1]/div')
            aboutprod = self.driver.find_element(By.XPATH, '//*[@id="product-details-container"]/div[3]/div[2]/p')
            priceinfo = self.driver.find_element(By.XPATH, '//*[@id="product-price"]/div[1]/span[2]')

            prodcode_list.append(prodcode.text)
            sizeinfo_list.append(sizeinfo.text)
            imginfo_list.append(imginfo.text)
            proddetails_list.append(proddetails.text)
            aboutprod_list.append(aboutprod.text)
            priceinfo_list.append(priceinfo.text)

        #hprd = {UUID:{'prodcode': prodcode,'sizeinfo': sizeinfo, 'imginfo': imginfo,'proddeatails': proddetails,'aboutprod': aboutprod,'priceinfo': priceinfo}}
        #print("DEBUG: prodcode " + str(hprd['prodcode']) + " UUID="+UUID)
        #search page for pname  pic
        #hprd['pname'] = pname
        #hprd['pic'] = pic
        #df = pd.DataFrame{(72, 6), index == UUID, columns == dict{'details': proddetails, 'about' : aboutprod, 'pricing' : priceinfo, 'imginfo' : imginfo, 'prodcode' : prodcode, 'sizeinfo': sizeinfo,}}
        #df = pd.DataFrame(hprd)    

            prod_dict = { UUID : {'prodcode': prodcode_list, 'sizeinfo' : sizeinfo_list, 'imginfo' : imginfo_list, 'proddetails' : proddetails_list, 'aboutprod' : aboutprod_list, 'priceinfo'  : priceinfo_list}}
        frame = pd.DataFrame(prod_dict)
        print(frame.T)
        

    def create_folder(self, raw_data):
        if not os.path.exists(raw_data):
            os.makedirs(raw_data)


    def tearDown(self):
        self.driver.close()
    

if __name__ == "__main__":
    unittest.main()

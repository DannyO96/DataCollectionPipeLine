import unicodedata
import re
import os
import uuid
import pandas as pd
import urllib.request
import selenium
from slugify import slugify
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from locators import MainPageLocators
from locators import ProductPageLocators
from locators import SearchResultsPageLocators
from element import BasePageElement
from tqdm import tqdm


#The parent Page class containing general page object methods
class BasePage(object):

    def __init__(self, driver):
        self.driver = driver

#The main page class containing methods occuring on the main page of the website
class MainPage(BasePage):

    def does_title_match(self):
        return "ASOS" in self.driver.title

    def click_search_bar(self):
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.click()
    
    def accept_cookies(self):
        self.driver.delete_all_cookies()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((MainPageLocators.ACCEPT_COOKIES)))
        element.click()
        

    def search_asos(self):
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.send_keys("tshirt")
        element.send_keys(Keys.RETURN)

#Search results page class containing methods occuring on the search results page of the website
class SearchResultPage(BasePage):

    def get_image_links(self):
        product_container = self.driver.find_element(*SearchResultsPageLocators.PRODUCT_CONTAINER)
        products = product_container.find_elements(*SearchResultsPageLocators.PRODUCT_LIST)
        image_links = []

        for product in products:
            img_tag = product.find_element(*SearchResultsPageLocators.IMG_TAG)
            image_link = img_tag.get_attribute('src')

            if image_link in image_links:
                pass
            else:
                image_links.append(image_link)
        print(image_links)
        return(image_links)

    #def download_images(url):
    #    name = "no"
        fullname = str(name)+".jpg"
        urllib.request.urlretrieve(url,fullname)     
    #download_images()

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

    def is_results_found(self):
        return "No results found." not in self.driver.page_source

     #function to load more search results after the initial search
    def load_more_results(self):
        element = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located (SearchResultsPageLocators.LOAD_MORE))
        element.click()

#Product page class containing methods occuring on the page of a product 
class ProductPage(BasePage):
    def close_modal_popup(self):
        try: 
            element = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable(ProductPageLocators.STUDENT_DISCOUNT_CLOSE))
            self.driver.execute_script("arguments[0].click();", element)
            print('discount closed')
        except Exception as ex:
            print('no discounts yet')

    def frame_switch(self):
        self.driver.switch_to.frame(ProductPageLocators.STUDENT_DISCOUNT_IFRAME)
        element = self.driver.find_element(*ProductPageLocators.STUDENT_DISCOUNT_CLOSE)
        element.click()
        self.driver.Switch_to.default_content()

    def switch_iframes(self):
        iframes = self.driver.find_elements(*ProductPageLocators.IFRAMES)
        print(len(iframes))
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)        
            self.driver.switch_to.default_content()

    def close_alert(self):
        iframes = self.driver.find_elements(*ProductPageLocators.IFRAMES)
        print(len(iframes))
        for iframe in iframes:
            try:
                self.driver.switch_to.frame()
                element = self.driver.find_element(*ProductPageLocators.STUDENT_DISCOUNT_CLOSE)
                element.click()
            except:
                pass
        self.driver.switch_to.default_content()

    def create_uuid(self):
        UUID = str(uuid.uuid4())
        return UUID

    def scrape_links(self, href_list):
        image_link_list = []
        productname_list = []
        uuid_list = []
        prodcode_list = []
        sizeinfo_list = []
        imginfo_list = []
        proddetails_list = []
        aboutprod_list = []
        priceinfo_list = []
        #frame = pd.DataFrame(prod_dict, index = UUID, columns = list('prodcode', 'sizeinfo', 'imginfo', 'proddetails', 'aboutprod', 'priceinfo'))
        #frame = pd.DataFrame()

        for i in tqdm(href_list):
            self.driver.get(i)
            print("current href is ?", i)
            UUID = self.create_uuid()
            self.switch_iframes()
            element = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS_CONTAINER)
            #self.switch_iframes()
            element.click()
            self.switch_iframes()
            
            
            #(/html/body)

            product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
            product_code = self.driver.find_element(*ProductPageLocators.PRODUCT_CODE)
            size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
            img_info = self.driver.find_element(*ProductPageLocators.IMG_INFO)
            product_details = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS)
            about_product = self.driver.find_element(*ProductPageLocators.ABOUT_PRODUCT)
            price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
            img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
            image_link = img_tag.get_attribute('src')
            
            image_link_list.append(image_link)
            productname_list.append(product_name.text)
            uuid_list.append(UUID)
            prodcode_list.append(product_code.text)
            sizeinfo_list.append(size_info.text)
            imginfo_list.append(img_info.text)
            proddetails_list.append(product_details.text)
            aboutprod_list.append(about_product.text)
            priceinfo_list.append(price_info.text)

            prod_dict = {'product_name': productname_list,'href': i, 'UUID': uuid_list, 'product_code': prodcode_list, 'size_info' : sizeinfo_list, 'img_info' : imginfo_list, 'product_details' : proddetails_list, 'about_product' : aboutprod_list, 'price_info'  : priceinfo_list, 'img_link' : image_link_list}
        frame = pd.DataFrame.from_dict(prod_dict, ignore_index=True)
            #frame.reindex(UUID)
            #frame = frame.append(prod_dict, ignore_index=True)
        print(frame)
        return(frame)
    
    def scrape_links_on_multiple_product_pages(self, href_list):

        for i in tqdm(href_list):
            self.driver.get(i)
            UUID = self.create_uuid()
            while True:
                print("current href is ?", i)
                #self.close_alert()
                try:
                    element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DETAILS_CONTAINER))
                    element.click()
                    print('clicked container')
                    #self.close_alert()
                    #self.switch_iframes()
                
                    product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
                    product_code = self.driver.find_element(*ProductPageLocators.PRODUCT_CODE)
                    size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
                    img_info = self.driver.find_element(*ProductPageLocators.IMG_INFO)
                    product_details = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS)
                    about_product = self.driver.find_element(*ProductPageLocators.ABOUT_PRODUCT)
                    price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
                    img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
                    image_link = img_tag.get_attribute('src')

                    image_link_list = []
                    product_name_list = []
                    uuid_list = []
                    product_code_list = []
                    size_info_list = []
                    imginfo_list = []
                    product_details_list = []
                    about_product_list = []
                    price_info_list = []

                    image_link_list.append(image_link)
                    product_name_list.append(product_name.text)
                    uuid_list.append(UUID)
                    product_code_list.append(product_code.text)
                    size_info_list.append(size_info.text)
                    imginfo_list.append(img_info.text)
                    product_details_list.append(product_details.text)
                    about_product_list.append(about_product.text)
                    price_info_list.append(price_info.text)

                    prod_dict = {'product_name': product_name_list,'href': i, 'UUID': uuid_list, 'product_code': product_code_list, 'size_info' : size_info_list, 'img_info' : img_info, 'product_details' : product_details_list, 'about_product' : about_product_list, 'price_info'  : price_info_list, 'img_link' : image_link}
                    frame = pd.DataFrame.from_dict(prod_dict)
                    print(frame)
                    filename = product_name_list
                    sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
                    os.makedirs("/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
                    folder = (r"/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
                    filepath = os.path.join(folder, f"{filename}{sys_dtime}.json")
                    frame.to_json(filepath, orient = 'table')
                    break
                except:
                    pass
                
                try:
                    product_description_list = []
                    brand_list = []
                    size_and_fit_list = []
                    look_after_me_list = []
                    about_me_list = []

                    self.switch_iframes()
                    element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON))
                    element.click()
                    self.switch_iframes()
                    product_description = self.driver.find_element(*ProductPageLocators.PRODUCT_DESCRIPTION)
                    product_description_list.append(product_description.text)

                    element2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.BRAND_BUTTON))
                    element2.click()
                    brand = self.driver.find_element(*ProductPageLocators.BRAND)
                    brand_list.append(brand.text)
                    self.switch_iframes()
                    try:
                        element3 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.SIZE_AND_FIT_BUTTON))
                        element3.click()
                        size_and_fit = self.driver.find_element(*ProductPageLocators.SIZE_AND_FIT)
                        size_and_fit_list.append(size_and_fit.text)
                    except:
                        pass    
                    self.switch_iframes()
                    element4 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.LOOK_AFTER_ME_BUTTTON))
                    element4.click()
                    look_after_me = self.driver.find_element(*ProductPageLocators.LOOK_AFTER_ME)
                    look_after_me_list.append(look_after_me.text)
                    
                        
                    try:
                        element5 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.ABOUT_ME_BUTTON))
                        element5.click()
                        about_me = self.driver.find_element(*ProductPageLocators.ABOUT_ME)
                        about_me_list.append(about_me.text)
                    except:
                        pass

                    self.switch_iframes()

                    product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
                    size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
                    price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
                    img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
                    image_link = img_tag.get_attribute('src')

                    

                    prod_dict = {'product_name': (product_name.text),'href': i, 'UUID': UUID, 'product_description' : product_description_list, 'brand' : brand_list, 'size_and_fit' : size_and_fit_list, 'look_after_me' : look_after_me_list, 'about_me' : about_me_list, 'price_info' : (price_info.text), 'img_link' : image_link}
                    self.switch_iframes()
                    frame = pd.DataFrame.from_dict(prod_dict)
                    print(frame)
                    filename = product_name.text
                    sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
                    os.makedirs("/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
                    folder = (r"/home/danny/git/DataCollectionPipeline/raw_data/"f"{filename}{sys_dtime}")
                    filepath = os.path.join(folder, f"{filename}{sys_dtime}.json")
                    frame.to_json(filepath, orient = 'table')
                    break
                except:
                    #self.switch_iframes()
                    print('lap')

                #urllib to download image
                #urllib.urlretrieve(src, "captcha.png")

    def assert_prod_page_type(self, UUID, i):
        
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DETAILS_CONTAINER))
            frame, filename = self.scrape_primary_prodpage(UUID, i)
        except:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON))
            try:
                frame, filename = self.scrape_secondary_product_page(UUID, i)
            except:
                frame, filename = self.scrape_tertiary_product_page(UUID, i)
        return(frame, filename)
        

        #number of buttons = sec or tert
    

    def scrape_primary_prodpage(self, i, UUID):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DETAILS_CONTAINER))
        element.click()
        print('clicked container')
        #self.close_alert()
        #self.switch_iframes()
    
        product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
        product_code = self.driver.find_element(*ProductPageLocators.PRODUCT_CODE)
        size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
        img_info = self.driver.find_element(*ProductPageLocators.IMG_INFO)
        product_details = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS)
        about_product = self.driver.find_element(*ProductPageLocators.ABOUT_PRODUCT)
        price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
        img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
        image_link = img_tag.get_attribute('src')

        image_link_list = []
        product_name_list = []
        uuid_list = []
        product_code_list = []
        size_info_list = []
        imginfo_list = []
        product_details_list = []
        about_product_list = []
        price_info_list = []

        image_link_list.append(image_link)
        #product_name_list.append(product_name.text)
        uuid_list.append(UUID)
        product_code_list.append(product_code.text)
        size_info_list.append(size_info.text)
        imginfo_list.append(img_info.text)
        product_details_list.append(product_details.text)
        about_product_list.append(about_product.text)
        price_info_list.append(price_info.text)
        name = (product_name.text)

        prod_dict = {'product_name': name,'href': i, 'UUID': uuid_list, 'product_code': product_code_list, 'size_info' : size_info_list, 'img_info' : img_info, 'product_details' : product_details_list, 'about_product' : about_product_list, 'price_info'  : price_info_list, 'img_link' : image_link}
        frame = pd.DataFrame.from_dict(prod_dict)
        print(frame)
        filename = product_name_list
        return(frame, filename)

    def scrape_secondary_product_page(self, i, UUID):
        product_description_list = []
        brand_list = []
        size_and_fit_list = []
        look_after_me_list = []
        about_me_list = []

        #self.switch_iframes()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON))
        element.click()
        self.switch_iframes()
        product_description = self.driver.find_element(*ProductPageLocators.PRODUCT_DESCRIPTION)
        product_description_list.append(product_description.text)

        element2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.BRAND_BUTTON))
        element2.click()
        brand = self.driver.find_element(*ProductPageLocators.BRAND)
        brand_list.append(brand.text)
        #self.switch_iframes()
        
        element3 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.SIZE_AND_FIT_BUTTON))
        element3.click()
        size_and_fit = self.driver.find_element(*ProductPageLocators.SIZE_AND_FIT)
        size_and_fit_list.append(size_and_fit.text)
      
        #self.switch_iframes()
        element4 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.LOOK_AFTER_ME_BUTTTON))
        element4.click()
        look_after_me = self.driver.find_element(*ProductPageLocators.LOOK_AFTER_ME)
        look_after_me_list.append(look_after_me.text)
        
        element5 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.ABOUT_ME_BUTTON))
        element5.click()
        about_me = self.driver.find_element(*ProductPageLocators.ABOUT_ME)
        about_me_list.append(about_me.text)
        
        #self.switch_iframes()

        product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
        size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
        price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
        img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
        image_link = img_tag.get_attribute('src')

        prod_dict = {'product_name': (product_name.text),'href': i, 'UUID': UUID, 'product_description' : product_description_list, 'brand' : brand_list, 'size_and_fit' : size_and_fit_list, 'look_after_me' : look_after_me_list, 'about_me' : about_me_list, 'price_info' : (price_info.text), 'img_link' : image_link}
        self.switch_iframes()
        frame = pd.DataFrame.from_dict(prod_dict)
        print(frame)
        filename = (product_name.text)
        return(frame, filename)
        

    def scrape_tertiary_product_page(self, i, UUID):
        product_description_list = []
        brand_list = []
        look_after_me_list = []
        about_me_list = []

        #self.switch_iframes()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON))
        element.click()
        self.switch_iframes()
        product_description = self.driver.find_element(*ProductPageLocators.PRODUCT_DESCRIPTION)
        product_description_list.append(product_description.text)

        element2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.BRAND_BUTTON))
        element2.click()
        brand = self.driver.find_element(*ProductPageLocators.BRAND)
        brand_list.append(brand.text)
        #self.switch_iframes()
        
        #self.switch_iframes()
        element3 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.LOOK_AFTER_ME_BUTTTON2))
        element3.click()
        look_after_me = self.driver.find_element(*ProductPageLocators.LOOK_AFTER_ME)
        look_after_me_list.append(look_after_me.text)
        
            
        
        element4 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLocators.ABOUT_ME_BUTTON2))
        element4.click()
        about_me = self.driver.find_element(*ProductPageLocators.ABOUT_ME)
        about_me_list.append(about_me.text)

        #self.switch_iframes()

        prod_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
        size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
        price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
        img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
        image_link = img_tag.get_attribute('src')
        product_name = (prod_name.text)

        prod_dict = {'product_name': product_name,'href': i, 'UUID': UUID, 'product_description' : product_description_list, 'brand' : brand_list, 'look_after_me' : look_after_me_list, 'about_me' : about_me_list, 'price_info' : (price_info.text), 'img_link' : image_link}
        self.switch_iframes()
        frame = pd.DataFrame.from_dict(prod_dict)
        print(frame)
        filename = product_name
        return(frame, filename)
        

    def save_dataframe_locally(self, frame, filename):
        #filename = product_name.text
        new_filename = slugify(filename)
        sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
        os.makedirs("/home/danny/git/DataCollectionPipeline/raw_data/"f"{new_filename}{sys_dtime}")
        folder = (r"/home/danny/git/DataCollectionPipeline/raw_data/"f"{new_filename}{sys_dtime}")
        filepath = os.path.join(folder, f"{new_filename}{sys_dtime}.json")
        frame.to_json(filepath, orient = 'table')

    def scrape_prod_pages(self, href_list):
        for i in tqdm(href_list):
            self.driver.get(i)
            UUID = self.create_uuid()
            frame, filename = self.assert_prod_page_type(i, UUID)
            self.save_dataframe_locally(frame, filename)












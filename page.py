import pandas as pd
import requests
import selenium
import uuid
from datetime import datetime
from locators import MainPageLocators
from locators import ProductPageLocators
from locators import SearchResultsPageLocators
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from slugify import slugify
from threading import Thread
from tqdm import tqdm

"""
I have separated methods for scraping in a page object model meaning each page object contains methods 
relevant to scraping that type of page on my chosen website.
"""
class BasePage(object):
    """
    This is the base page class it instanciates the webdriver and its methods are inherited by every page class in my page object model
    """
    def __init__(self, driver: selenium.webdriver.chrome.webdriver.WebDriver):
        self.driver = driver


#The main page class containing methods occuring on the main page of the website
class MainPage(BasePage):
    """
    This is the main page class its methods concern actions of the webdriver occuring on the asos homepage and it inherits the methods of base page.
    """
    def does_title_match(self):
        """
        This is a function to check is the name of the site is in the title of the webpage.

        Args:
            param1:self 

        Returns:
            Returns a bool for if a phrase is in the title of the webpage in this case ASOS

        Raises:
            Error "ASOS" not in self.driver.title
        """
        return "ASOS" in self.driver.title
    
    def print_page_source(self):
        """
        This is a function to print out the source html of the page im using, essentially its the function that helps to debug 
        issues with headless mode.
        """
        url = ('https://www.asos.com/')
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            'Content-Type': 'text/html',
        }
        response = requests.get(url, headers=headers)
        html = response.text
        print(html)

    def navigate_to_men(self):
        """
        This is a function to check is the name of the site is in the title of the webpage.

        Args:
            param1:self 

        Returns:
            clicks the mens section BUTTON
        Raises:
            
        """
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MainPageLocators.MEN_SECTION))
        element.click()

    def navigate_to_women(self):
        """
        This is a function to navigate to the womens section of asos

        Args:
            param1:self 

        Returns:
            Clicks the womens section button

        Raises:
            Element not found: usually occurs when the locator for the button has changed as the website has been updated.
        """
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MainPageLocators.WOMEN_SECTION))
        element.click()

    def click_search_bar(self):
        """
        This function clicks the searchbar on the website homepage

        Args:
            param1:self
        Returns:

        Raises:
            Element not found if search bar isnt present on the page
        """
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.click()
    
    def accept_cookies(self):
        """
        This is a function to accept cookies after loading the webpage

        Args:
            param1:self

        Returns:
            Clears cookie cache and clicks the accept cookies button

        Raises:
            ElementNotFound: If the presence of the element is not located
        """
        self.driver.delete_all_cookies()
        #self.driver.get_screenshot_as_png("/home/ec2-user/env/screenshot.png")
        #print("screenshot taken")
        element = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((MainPageLocators.ACCEPT_COOKIES)))
        #element = self.driver.execute_script("arguments[0].click();",self.driver.find_element(MainPageLocators.ACCEPT_COOKIES))
        element.click()
        print('Accepted Cookies')

    def search_asos(self):
        """
        This is a function to search asos for t-shirts it clicks the search bar and send the keys of the search term.

        Args:
            param1:self

        Returns:
            Searches a phrase into the searchbar and enters the search results page

        Raises:
            KeyError: Raises an exception.
            elementnotfound error: raised when elements that are interacted with in the function cannot be found

        """
        element = self.driver.find_element(*MainPageLocators.SEARCH_BAR)
        element.send_keys("tshirt")
        element.send_keys(Keys.RETURN)

#Search results page class containing methods occuring on the search results page of the website
class SearchResultPage(BasePage):
    """
    This is the search results page class its methods concern actions of the webdriver occuring on the search results page,
    it inherits methods from the base page.
    """
    def get_image_links(self):
        """
        This function generates a list of image links from the search results page

        Args:
            param1:self

        Returns:
            A list of image links located using the img tag and the src attribute

        Raises:
            KeyError: Raises an exception.
            elementnotfound error: raised when elements that are interacted with in the function cannot be found

        """
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

    def get_href_list(self):
        """
        This is a function to generate a list of products links(hrefs)

        Args:
            param1:self

        Returns:
            Returns a list of links to product pages

        Raises:
            KeyError: Raises an exception.
            elementnotfound error: raised when elements that are interacted with in the function cannot be found

        """
        product_container = self.driver.find_element(*SearchResultsPageLocators.PRODUCT_CONTAINER)
        productive = product_container.find_element(*SearchResultsPageLocators.PRODUCT_LIST)
        products = productive.find_elements(*SearchResultsPageLocators.PRODUCT_TILE)
        href_list = []

        for product in products:
            a_tag = product.find_element(*SearchResultsPageLocators.A_TAG)
            href = a_tag.get_attribute('href')

            if href in href_list:
                pass
            else:
                href_list.append(href)
        return(href_list)

     #function to load more search results after the initial search
    def load_more_results(self):
        """
        This is a function to click the load more button on the search results page

        Args:
            param1: self.

        Returns:
            This returns a search results page with more search results loaded

        Raises:
            KeyError: Raises an exception.
            elementnotfound error: raised when elements that are interacted with in the function cannot be found

        """
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(SearchResultsPageLocators.LOAD_MORE))
        element.click()

#Product page class containing methods occuring on the page of a product 
class ProductPage(BasePage):
    """
    This is the product page class its methods concern webdriver actions occuring on product pages, it inherits methods from the base page.
    """

    def close_modal_popup(self):
        """
        This is a function i created to close the student discount modal popups

        Args:
            param1:self
        Returns:
            This function doesnt return anything it closes a modal pop up

        Raises:
            KeyError: Raises an exception.
            elementnotfound error: raised when elements that are interacted with in the function cannot be found

        """
        try: 
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(ProductPageLocators.STUDENT_DISCOUNT_CLOSE))
            self.driver.execute_script("arguments[0].click();", element)
            print('discount closed')
        except Exception as ex:
            print('no discounts yet')

    def switch_iframes(self):
        """
        This is a funtion to switch the iframe on the open webpage.

        Args:
            param1: Self.

        Returns:
            This funtion switches the frame back to the default content after and iframe pop up occurs

        Raises:
            KeyError:elementnotfound error: raised when elements that are interacted with in the function cannot be found
        """
        iframes = self.driver.find_elements(*ProductPageLocators.IFRAMES)
        print(len(iframes))
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)        
            self.driver.switch_to.default_content()

    def create_uuid(self):
        """
        This function creates a unique user id and returns it.
        Args:
            param1: self.
        Returns:
            A unique user id is created and returned.
        Raises:
            
        """
        UUID = str(uuid.uuid4())
        return UUID

    def assert_prod_page_type(self, UUID, href):
        """
        This is a function to determine the type of product page the webdriver is on.

        Args:
            param1: self.
            param2: i - this is the href of the product.
            param3: UUID the generated unique user id for the product in this instance of scraping.

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        #frame = pd.DataFrame
        #filename = 1
        
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DETAILS_CONTAINER))
            frame, filename = self.scrape_primary_prodpage(UUID, href)
        except Exception as e:
            print("Locator PRODUCT_DETAILS_CONTAINER. Exception:",e," href:",str(href))
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON))
                frame, filename = self.scrape_altprod_pages(UUID, href)
            except Exception as e:
                print("Locator PRODUCT_DESCRIPTION_BUTTON. Exception:",e," href:",str(href))
                return(pd.DataFrame, "FAIL")
                pass
            
        return(frame, filename)

    def scrape_primary_prodpage(self, i, UUID):
        """
        This is a function to scrape the primary product page type for information it clicks the product details container the creates a dataframe 
        of product information

        Args:
            param1: self
            param2: i - this is the href of the product
            param3: UUID the generated unique user id for the product in this instance of scraping

        Returns:
            This function returns the dataframe of product information and the filename which is the full product name
            return(frame, filename)

        Raises:
            KeyError: Raises an exception.
            elementnotfound error: raised when elements that are interacted with in the function cannot be found
        """
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DETAILS_CONTAINER))
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
        galler_img = self.driver.find_element(*ProductPageLocators.GALLERY_IMAGE)
        image_link = galler_img.get_attribute('src')

        image_link_list = []
        product_name_list = []
        uuid_list = []
        product_code_list = []
        size_info_list = []
        img_info_list = []
        product_details_list = []
        about_product_list = []
        price_info_list = []

        image_link_list.append(image_link)
        product_name_list.append(product_name.text)
        uuid_list.append(UUID)
        product_code_list.append(product_code.text)
        size_info_list.append(size_info.text)
        img_info_list.append(img_info.text)
        product_details_list.append(product_details.text)
        about_product_list.append(about_product.text)
        price_info_list.append(price_info.text)
        name = (product_name.text)

        prod_dict = {'product_name': name,'href': i, 'UUID': uuid_list, 'product_code': product_code_list, 'size_info' : size_info_list, 'img_info' : img_info_list, 'product_details' : product_details_list, 'about_product' : about_product_list, 'price_info'  : price_info_list, 'img_link' : image_link}
        frame = pd.DataFrame.from_dict(prod_dict)
        print(str(frame))
        filename = str(name)
        return(frame, filename)

    def scrape_altprod_pages(self, i ,UUID):
        """
        This is a function to scrape the alternate product page type with aria labels for the product details fields
        Args:
            param1: self
            param2: i - this is the href of the product
            param3: UUID the generated unique user id for the product in this instance of scraping

        Returns:
            This function returns the dataframe of product information and the filename which is the full product name the filename has been encoded to ensure it is byte type

        Raises:
            KeyError: Raises an exception.
            elementnotfound error: raised when elements that are interacted with in the function cannot be found
        """
        product_description_list = []
        brand_list = []
        size_and_fit_list = []
        look_after_me_list = []
        about_me_list = []
        
        try:
            product_description = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(ProductPageLocators.PRODUCT_DESCRIPTION))
            product_description_list.append(product_description.get_attribute("textContent"))
        except:
            product_description_list.append("NULL")
        try:
            brand = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(ProductPageLocators.BRAND))
            brand_list.append(brand.get_attribute("textContent"))
        except:
            brand_list.append('NULL')
        try:
            size_and_fit = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(ProductPageLocators.SIZE_AND_FIT))
            size_and_fit_list.append(size_and_fit.get_attribute("textContent"))
        except:
            size_and_fit_list.append('NULL')
        try:
            look_after_me = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(ProductPageLocators.LOOK_AFTER_ME))
            look_after_me_list.append(look_after_me.get_attribute("textContent"))
        except:
            look_after_me_list.append('NULL')
        try:
            about_me = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(ProductPageLocators.ABOUT_ME))
            about_me_list.append(about_me.get_attribute("textContent"))
        except:
            about_me_list.append('NULL')

        product_name = self.driver.find_element(*ProductPageLocators.PRODUCT_NAME)
        size_info = self.driver.find_element(*ProductPageLocators.SIZE_INFO)
        price_info = self.driver.find_element(*ProductPageLocators.PRICE_INFO)
        img_tag = self.driver.find_element(*SearchResultsPageLocators.IMG_TAG)
        image_link = img_tag.get_attribute('src')

        prod_dict = {'product_name': (product_name.text),'href': i, 'UUID': UUID, 'product_description' : product_description_list, 'brand' : brand_list, 'size_and_fit' : size_and_fit_list, 'look_after_me' : look_after_me_list, 'about_me' : about_me_list, 'price_info' : (price_info.text), 'img_link' : image_link}
        self.switch_iframes()
        frame = pd.DataFrame.from_dict(prod_dict)
        print(str(frame))
        filename = str(product_name.text)
        #filename_bytes = str(filename).encode()
        return(frame, filename)

    def format_filename(self, filename):
        """
        This is a function to turn the name of the file in to a system date time stamped slug ready to be save locally or on the cloud

        Args:
            param1: self
            param2: filename - this is the name of the product file before processing

        Returns:
            This function reeturns the filename ready to be save locally or on the cloud without issues

        Raises:
            TypeError: decoding to str: need a bytes-like object, int found. occurs when attempting to slugify file this occurs because the type of the filename is and int
        
        """
        new_filename = slugify(filename)
        return(new_filename)

    def init_driver_worker(self, href_list): #create new instace of chrome then make it do its job
        ##### init driver
        options = webdriver.ChromeOptions
        #you can't run multible instances of chrome
        #  with the same profile being used,
        #  so either create new profile for each instance or use incognito mode
        #options.add_argument("--incognito")
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
        option = webdriver.ChromeOptions()
        #option.add_argument('--proxy-server=%s' % proxy)
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--allow-running-insecure-content')
        option.add_argument('--disable-notifications')
        option.add_argument('--disable-forms')
        option.add_argument('--disable-scripts')
        option.add_argument('--disable-secure-containers')
        option.add_argument('--disable-same-origin')
        option.add_argument('--disable-secure-scripts')
        option.add_argument('-window-size=1920,1080')
        option.add_argument('--no-sandbox')
        option.add_argument(f'user-agent={user_agent}')
        option.add_argument('--disable-dev-shm-usage')
        #option.add_argument('--headless')
        option.add_argument('--disable-gpu')  

        self.driver = webdriver.Chrome("/home/danny/chromedriver",options = option)
        ##### do the task
        prods_frame = pd.DataFrame()
        
        for href in tqdm(href_list):
            self.driver.get(href)
            self.accept_cookie()
            try:
                try:
                    out_of_stock = self.driver.find_element(*ProductPageLocators.OUT_OF_STOCK)
                    oos = WebElement.is_displayed(out_of_stock)
                except selenium.common.exceptions.NoSuchElementException:
                    oos=False
                try:
                    something_gone_wrong = self.driver.find_element(*ProductPageLocators.SOMETHING_GONE_WRONG)
                    sgw = WebElement.is_displayed(something_gone_wrong)
                except selenium.common.exceptions.NoSuchElementException:
                    sgw=False
                try:
                    container = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS_CONTAINER)
                    pdc = WebElement.is_displayed(container)
                except selenium.common.exceptions.NoSuchElementException:
                    pdc = False
                try:
                    desc_button = self.driver.find_element(*ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON)
                    pdb = WebElement.is_displayed(desc_button)
                except selenium.common.exceptions.NoSuchElementException:
                    pdb = False
                scrapable = pdc or pdb 
            except Exception as E:
                print('Exception: ', E)
            print("oos=",oos," sgw=",sgw," scrapable=",scrapable)    

            if oos == True or sgw == True or scrapable == False:
                print('something wrong')
                continue
            
            else:
                UUID = self.create_uuid()
                print('uuid created')
                frame, self.filename = self.assert_prod_page_type(href, UUID)
                try:
                    filename = self.format_filename(self.filename)
                except Exception as e:
                    print("cant slug filename its got an int in it... Exception:",e," filename:",str(filename))
                    continue
                sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
                print("filename:",str(filename))
                try:
                    frame.insert(0, "filename", filename)
                except Exception as e:
                    print("Cannot add filename to frame. Exception:",e," filename:",str(filename))
                    continue
                frame.insert(0, "date_time", sys_dtime)
                prods_frame = pd.concat([prods_frame,frame])
        print("scrape_prod_pages.prods_frame=",prods_frame)
        return(prods_frame)    
        exit() #close the thread

    def split_range(self, _range, parts): 
        #split a range to chunks
        chunk_size = int(len(_range)/parts)
        chunks = [_range[x:x+chunk_size] for x in range(0, len(_range), chunk_size)]
        return chunks
    
    def multithreading(self, href_list):
        chunks = self.split_range(href_list, 4) # split the task to 9 instances of chrome
        thread_workers = []
        for chunk in chunks:
            t = Thread(target=self.init_driver_worker, args=(chunk,))
            thread_workers.append(t)
            t.start()    
        # wait for the thread_workers to finish
        for t in thread_workers:
            t.join()

    def accept_cookie(self):
        """
        This is a function to accept cookies after loading the webpage

        Args:
            param1:self

        Returns:
            Clears cookie cache and clicks the accept cookies button

        Raises:
            ElementNotFound: If the presence of the element is not located
        """
        self.driver.delete_all_cookies()
        element = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((MainPageLocators.ACCEPT_COOKIES)))
        element.click()

    def scrape_prod_pages(self, href_list):
        """
        This is a function to scrape multiple product page types

        Args:
            param1: self.
            param2: href_list, this is a list of links to product pages returned from the function get href list.

        Returns:
            This function iterates through every link in the href list, checks for know exceptions then 
            creates a UUID for the product asserts the type of product page then creates a dataframe which has two collumns added for date time and 
            the slugifyed filename. This dataframe for a single product is then concatenated to the dataframe of all the products which is returned 
            after all the products have been scraped.

        Raises:
            TypeError: decoding to str: this occurs when the dataframe has not been created correctly usually due to an unhandled out of stock label or a something gone wrong label although try and accept blocks 
            have now been implemented to avoid this error.
        """
        prods_frame = pd.DataFrame()
        
        for href in tqdm(href_list):
            self.driver.get(href)
            self.accept_cookie()
            try:
                try:
                    out_of_stock = self.driver.find_element(*ProductPageLocators.OUT_OF_STOCK)
                    oos = WebElement.is_displayed(out_of_stock)
                except selenium.common.exceptions.NoSuchElementException:
                    oos=False
                try:
                    something_gone_wrong = self.driver.find_element(*ProductPageLocators.SOMETHING_GONE_WRONG)
                    sgw = WebElement.is_displayed(something_gone_wrong)
                except selenium.common.exceptions.NoSuchElementException:
                    sgw=False
                try:
                    container = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS_CONTAINER)
                    pdc = WebElement.is_displayed(container)
                except selenium.common.exceptions.NoSuchElementException:
                    pdc = False
                try:
                    desc_button = self.driver.find_element(*ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON)
                    pdb = WebElement.is_displayed(desc_button)
                except selenium.common.exceptions.NoSuchElementException:
                    pdb = False
                scrapable = pdc or pdb 
            except Exception as E:
                print('Exception: ', E)
            print("oos=",oos," sgw=",sgw," scrapable=",scrapable)    

            if oos == True or sgw == True or scrapable == False:
                print('something wrong')
                continue
            
            else:
                UUID = self.create_uuid()
                print('uuid created')
                frame, self.filename = self.assert_prod_page_type(href, UUID)
                try:
                    filename = self.format_filename(self.filename)
                except Exception as e:
                    print("cant slug filename its got an int in it... Exception:",e," filename:",str(filename))
                    continue
                sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
                print("filename:",str(filename))
                try:
                    frame.insert(0, "filename", filename)
                except Exception as e:
                    print("Cannot add filename to frame. Exception:",e," filename:",str(filename))
                    continue
                frame.insert(0, "date_time", sys_dtime)
                prods_frame = pd.concat([prods_frame,frame])
        print("scrape_prod_pages.prods_frame=",prods_frame)
        return(prods_frame)
            
    def scrape_prod_page(self, href_list):
        """
        This is a function to scrape multiple product page types

        Args:
            param1: self.
            param2: href_list, this is a list of links to product pages returned from the function get href list.

        Returns:
            This function iterates through every link in the href list, checks for know exceptions then 
            creates a UUID for the product asserts the type of product page then creates a dataframe which has two collumns added for date time and 
            the slugifyed filename. This dataframe for a single product is then concatenated to the dataframe of all the products which is returned 
            after all the products have been scraped.

        Raises:
            TypeError: decoding to str: this occurs when the dataframe has not been created correctly usually due to an unhandled out of stock label or a something gone wrong label although try and accept blocks 
            have now been implemented to avoid this error.
        """
        prods_frame = pd.DataFrame()
        
        for href in tqdm(href_list):
            self.driver.get(href)
            try:
                try:
                    out_of_stock = self.driver.find_element(*ProductPageLocators.OUT_OF_STOCK)
                    oos = WebElement.is_displayed(out_of_stock)
                except selenium.common.exceptions.NoSuchElementException:
                    oos=False
                try:
                    something_gone_wrong = self.driver.find_element(*ProductPageLocators.SOMETHING_GONE_WRONG)
                    sgw = WebElement.is_displayed(something_gone_wrong)
                except selenium.common.exceptions.NoSuchElementException:
                    sgw=False
                try:
                    container = self.driver.find_element(*ProductPageLocators.PRODUCT_DETAILS_CONTAINER)
                    pdc = WebElement.is_displayed(container)
                except selenium.common.exceptions.NoSuchElementException:
                    pdc = False
                try:
                    desc_button = self.driver.find_element(*ProductPageLocators.PRODUCT_DESCRIPTION_BUTTON)
                    pdb = WebElement.is_displayed(desc_button)
                except selenium.common.exceptions.NoSuchElementException:
                    pdb = False
                scrapable = pdc or pdb 
            except Exception as E:
                print('Exception: ', E)
            print("oos=",oos," sgw=",sgw," scrapable=",scrapable)    

            if oos == True or sgw == True or scrapable == False:
                print('something wrong')
                continue
            
            else:
                UUID = self.create_uuid()
                print('uuid created')
                frame, self.filename = self.assert_prod_page_type(href, UUID)
                try:
                    filename = self.format_filename(self.filename)
                except:
                    print("cant slug filename its got an int in it...")
                    continue
                sys_dtime = datetime.now().strftime("%d_%m_%Y-%H%M")
                frame.insert(0, "filename", filename)
                frame.insert(0, "date_time", sys_dtime)
                prods_frame = pd.concat([prods_frame,frame])
                break
        print("scrape_prod_pages.prods_frame=",prods_frame)
        return(prods_frame)






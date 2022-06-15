from selenium.webdriver.common.by import By

class MainPageLocators(object):

    SEARCH_BAR = (By.NAME, "q")
    ACCEPT_COOKIES = (By.ID, "onetrust-accept-btn-handler")

class SearchResultsPageLocators(object):

    PRODUCT_CONTAINER = (By.CLASS_NAME, '_3YREj-P')
    PRODUCT_LIST = (By.CLASS_NAME, "_2qG85dG")
    A_TAG = (By.TAG_NAME, 'a')

class ProductPageLocators(object):

    PRODUCT_DETAILS_CONTAINER = (By.XPATH,'//*[@id="product-details-container"]/div[4]/div/a[1]')
    PRODUCT_CODE = (By.XPATH,'//*[@id="product-details-container"]/div[2]/div[1]/p')
    SIZE_INFO = (By.XPATH, '//*[@id="main-size-select-0"]')
    IMG_INFO = (By.XPATH, '//*[@id="product-details-container"]/div[3]/div[1]/p')
    PRODUCT_DETAILS = (By.XPATH, '//*[@id="product-details-container"]/div[1]/div')
    ABOUT_PRODUCT = (By.XPATH, '//*[@id="product-details-container"]/div[3]/div[2]/p')
    PRICE_INFO = (By.XPATH, '//*[@id="product-price"]/div[1]/span[2]')
    STUDENT_DISCOUNT = (By.XPATH, '//*[@id="att_lightbox_close"]/svg/path')

   

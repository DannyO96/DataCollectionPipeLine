from selenium.webdriver.common.by import By

class MainPageLocators(object):

    SEARCH_BAR = (By.NAME, "q")
    ACCEPT_COOKIES = (By.ID, "onetrust-accept-btn-handler")

class SearchResultsPageLocators(object):

    PRODUCT_CONTAINER = (By.CLASS_NAME, '_3YREj-P')
    PRODUCT_LIST = (By.CLASS_NAME, "_2qG85dG")
    A_TAG = (By.TAG_NAME, 'a')
    IMG_TAG = (By.TAG_NAME, 'img')

class ProductPageLocators(object):
#primary product page locator
    PRODUCT_NAME = (By.TAG_NAME, 'h1')
    PRODUCT_DETAILS_CONTAINER = (By.XPATH,'//*[@id="product-details-container"]/div[4]/div/a[1]')
    PRODUCT_CODE = (By.XPATH,'//*[@id="product-details-container"]/div[2]/div[1]/p')
    SIZE_INFO = (By.XPATH, '//*[@id="main-size-select-0"]')
    IMG_INFO = (By.XPATH, '//*[@id="product-details-container"]/div[3]/div[1]/p')
    PRODUCT_DETAILS = (By.XPATH, '//*[@id="product-details-container"]/div[1]/div')
    ABOUT_PRODUCT = (By.XPATH, '//*[@id="product-details-container"]/div[3]/div[2]/p')
    PRICE_INFO = (By.XPATH, '//*[@id="product-price"]/div[1]/span[2]')
    STUDENT_DISCOUNT_IFRAME = (By.ID, 'secure-script-container')
    IFRAMES = (By.TAG_NAME,"iframe")
    STUDENT_DISCOUNT_CLOSE = (By.XPATH, '//*[@id="att_lightbox_close"]/svg/path')
    STUDENT_DISC_IFRAME = (By.XPATH, '//*[@id="chrome-main-content"]')
#secondary product page locators    
    PRODUCT_DESCRIPTION_BUTTON = (By.XPATH, '//*[@id="pdp-ssr-product-description"]/div/ul/li[1]/div/h3/button')
    PRODUCT_DESCRIPTION = (By.XPATH, '//*[@id="productDescriptionDetails"]/div/div')
    BRAND_BUTTON = (By.XPATH, '//*[@id="pdp-ssr-product-description"]/div/ul/li[2]/div/h3/button')
    BRAND = (By.XPATH, '//*[@id="productDescriptionBrand"]')
    SIZE_AND_FIT_BUTTON = (By.XPATH, '//*[@id="pdp-ssr-product-description"]/div/ul/li[3]/div/h3/button')
    SIZE_AND_FIT = (By.XPATH, '//*[@id="productDescriptionSizeAndFit"]')
    LOOK_AFTER_ME_BUTTTON = (By.XPATH, '//*[@id="pdp-ssr-product-description"]/div/ul/li[4]/div/h3/button')
    LOOK_AFTER_ME = (By.XPATH, '//*[@id="productDescriptionCareInfo"]')
    ABOUT_ME_BUTTON = (By.XPATH, '//*[@id="pdp-ssr-product-description"]/div/ul/li[5]/div/h3')
    ABOUT_ME = (By.XPATH, '//*[@id="productDescriptionAboutMe"]')

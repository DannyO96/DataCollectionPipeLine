from selenium.webdriver.common.by import By

class MainPageLocators(object):

    SEARCH_BAR = (By.NAME, "q")
    ACCEPT_COOKIES = (By.ID, "onetrust-accept-btn-handler")

class SearchResultsPageLocators(object):

    PRODUCT_CONTAINER = (By.CLASS_NAME, '_3YREj-P')
    PRODUCT_LIST = (By.CLASS_NAME, "_2qG85dG")
    A_TAG = (By.TAG_NAME, 'a')



   

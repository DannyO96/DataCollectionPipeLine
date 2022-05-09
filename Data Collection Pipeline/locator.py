from selenium.webdriver.common.by import By

class MainPageLocators(object):
    GO_BUTTON = (By.ID, "search-icon")

    ACCEPT_COOKIES = (By.ID, "onetrust-accept-btn-handler")

class SearchResultsPageLocators(object):

    PRODUCT_LIST = (By.XPATH, "/html/body/div[1]/div/main/div/div/div[3]/div/div[1]")




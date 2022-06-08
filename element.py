from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class BasePageElement(object):
    def __set__(self, obj, value):
        driver = obj.driver
        print (self.locator)
        WebDriverWait(driver, 100).until(
            driver.find_element_by_name(self.locator))
        driver.find_element_by_name(self.locator).clear()
        driver.find_element_by_name(self.locator).send_keys(value)

    def __get__(self, obj, owner):
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            driver.find_element_by_name(self.locator))
        element = driver.find_element_by_name(self.locator)
        return element.get_attribute("value")
    
    def wait_to_locate(self, obj):
        driver = obj.driver
        WebDriverWait(driver, 100).until(EC.presence_of_element_located(self.locator))
        
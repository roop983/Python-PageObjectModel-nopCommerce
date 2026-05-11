from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select


from configuratation.config import TestData
import math
import time

from utilities.cookie_utility import CookieManager
from utilities.read_configs_properties import ReadConfig


class BasePage():
    """ Constructor of the Base page class"""
    def __init__(self, driver):
        self.driver = driver
        # self.driver.get(TestData.BASE_URL)
        self.driver.implicitly_wait(5)
        self.driver.get(ReadConfig.get_base_url())
        # CookieManager.save_cookies(driver)
        # driver.get("https://admin-demo.nopcommerce.com")
        # CookieManager.load_cookies(driver)
        # driver.refresh()

    def do_click(self, by_locator):
        wait = WebDriverWait(self.driver, 10)
        # Re-locate element at click time due to stale element exception
        for _ in range(3): # _ → a throwaway variable (we don’t care about the value)
            try:
                ele = wait.until(ec.element_to_be_clickable(by_locator))
                ele.click()
                time.sleep(5)
                return
            except StaleElementReferenceException:
                print("Retrying due to stale element...")

    # text=None: Means: “input is optional”. if text is not None: Only sends keys when text is provided, Skips typing if None
    # def do_send_keys(self, by_locator, text=None, clear_first = True):
    #     element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator))
    #     if clear_first:
    #         element.click()
    #         element.clear()
    #         element.send_keys(Keys.CONTROL + "a")
    #         element.send_keys(Keys.DELETE)
    #         time.sleep(5)
    #     if text is None:
    #         return
    #
    #     if isinstance(text, float) and math.isnan(text):
    #         return
    #
    #     text = str(text).strip()
    #     if text is not None:
    #         element.send_keys(text)

    def do_send_keys(self, by_locator, text=None):
        element = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(by_locator)
        )

        # Strong clear
        element.click()
        element.clear()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

        # Handle empty values
        if text is None:
            return

        import math
        if isinstance(text, float) and math.isnan(text):
            return

        text = str(text).strip()

        if text:
            element.send_keys(text)

    def get_element_text(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator))
        return element.text

    def is_visible(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator))
        return bool(element)

    def is_displayed(self, by_locator):
        try:
            element = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(by_locator))
            return element.is_displayed()
        except:
            return False

    def is_enabled(self, by_locator):
        try:
            element = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(by_locator))
            return element.is_enabled()
        except:
            return False

    def get_title(self):
        # WebDriverWait(self.driver, 10).until(ec.title_is((title))) # waiting to check whether title exists in the page
        return self.driver.title

    def select_dropdown_visible_text(self,by_locator,text):
        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator))
        select_element = Select(element)
        select_element.select_by_visible_text(text)




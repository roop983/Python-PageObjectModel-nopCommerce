from selenium.webdriver.common.by import By

from configuratation.config import TestData
from pages.BasePage import BasePage
from pages.CustomersPage import CustomersPage
from utilities.read_configs_properties import ReadConfig
import time

class LoginAdminPage(BasePage):
    EMAIL = (By.NAME, "Email")
    PASSWORD = (By.CSS_SELECTOR, "input[id='Password']")
    LOGIN_BTN = (By.CSS_SELECTOR, "button.login-button")
    DASHBOARD_HEADER_TEXT = (By.CSS_SELECTOR, "div.content-header > h1")
    NO_CUSTOMER_ACCOUNT_ERROR_MESSAGE = (By.CSS_SELECTOR, "div.message-error > ul > li")
    LOGOUT_BTN = (By.XPATH, "//a[normalize-space()='Logout']")

    def __init__(self, driver):
        super().__init__(driver)
        # self.driver.get(TestData.BASE_URL)


    def get_login_page_title(self):
        return self.get_title()


    def do_Login(self, username, password):
        self.do_send_keys(self.EMAIL,username)
        self.do_send_keys(self.PASSWORD, password)
        self.do_click(self.LOGIN_BTN)
        return CustomersPage(self.driver)

    def get_dahboard_header_text(self):
        dashboard_header_text = self.get_element_text(self.DASHBOARD_HEADER_TEXT).strip()
        return dashboard_header_text

    def get_error_message_text(self):
        invalid_customer_account_error_text = self.get_element_text(self.NO_CUSTOMER_ACCOUNT_ERROR_MESSAGE).strip()
        return invalid_customer_account_error_text

    def do_Logout(self):
        self.do_click(self.LOGOUT_BTN)
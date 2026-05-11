import pytest

from configuratation.config import TestData
from pages.LoginAdminPage import LoginAdminPage
from tests.test_Base import BaseTest
from utilities.custom_logger import Log_maker
import allure


# from selenium.webdriver.remote.webdriver import WebDriver

@allure.feature("Login")
class Test_AdminLogin(BaseTest):
    logger = Log_maker.log_gen()


    @allure.story("Verify Login Page Title")
    def test_login_page_title(self):
        self.logger.info("****************Test_Verification_Login_Page_Title**************")
        with allure.step("Open Login Page"):
            self.loginPage = LoginAdminPage(self.driver) # LoginAdminPage class constructor expects driver, hence driver needs to be passed
        actual_title = self.loginPage.get_login_page_title()
        with allure.step("Validate Login Page Title"):
            assert actual_title == TestData.LOGINPAGE_TITLE

    @allure.story("Verify Login Page")
    def test_Login(self):
        self.logger.info("****************Test_Verification_Login_Page**************")
        with allure.step("Open Login Page"):
            self.loginPage = LoginAdminPage(self.driver)
        with allure.step("Enter Login credentials"):
            self.loginPage.do_Login(TestData.EMAIL, TestData.PASSWORD)
        with allure.step("Logout"):
            self.loginPage.do_Logout()

    @allure.story("Verify Header Text in Home Page")
    def test_Dashboardheader_text(self):
        self.logger.info("****************Test_Verification_Dashboard_Header**************")
        with allure.step("Open Login Page"):
            self.loginPage = LoginAdminPage(self.driver)
        with allure.step("Enter Login credentials"):
            self.loginPage.do_Login(TestData.EMAIL, TestData.PASSWORD)
        actual_header_text = self.loginPage.get_dahboard_header_text()
        with allure.step("Validate Home Page Dashboard Header Text"):
            assert actual_header_text == TestData.DASHBOARD_HEADER_TEXT
        with allure.step("Logout"):
            self.loginPage.do_Logout()

    @allure.story("Verify Invalid Login")
    def test_InvalidLogin(self):
        self.logger.info("****************Test_Verification_Invalid_Login_Credentials**************")
        with allure.step("Open Login Page"):
            self.loginPage = LoginAdminPage(self.driver)
        with allure.step("Enter Invalid Login credentials"):
            self.loginPage.do_Login(TestData.INVALID_EMAIL, TestData.PASSWORD)
        actual_error_text = self.loginPage.get_error_message_text()
        with allure.step("Validate Error for Invalid credentials"):
            assert actual_error_text == TestData.INVALID_EMAIL_ERROR_TEXT



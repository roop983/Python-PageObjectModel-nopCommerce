import pytest
import pandas as pd
from configuratation.config import TestData
from pages.LoginAdminPage import LoginAdminPage
from tests.test_Base import BaseTest
from utilities import excel_utils
from utilities.custom_logger import Log_maker
import allure

from utilities.read_configs_properties import ReadConfig


# from selenium.webdriver.remote.webdriver import WebDriver

class Test_AdminLogin_data_driven(BaseTest):
    logger = Log_maker.log_gen()
    # admin_login_file_path = ReadConfig.get_admin_login_file()

    # Grouping Testcases
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_Login_data_driven(self):
        self.logger.info("****************Test_Verification_Login_Page_Data_Driven**************")
        # admin_login_file = ReadConfig.get_admin_login_file()
        excel_data = excel_utils.read_data_pandas()
        if "result" in excel_data.columns:
            excel_data["result"] = ""
        else:
            excel_data["result"] = ""
        try:
            for index, row in excel_data.iterrows():
                self.loginPage = LoginAdminPage(self.driver)
                self.userName = row["username"]
                self.passWord = row["password"]
                self.expected_login = row["exp_login"]
                self.error_text_message = row["error_message"]
                self.loginPage.do_Login(self.userName, self.passWord)
                if self.expected_login == "Yes":
                    actual_header_text = self.loginPage.get_dahboard_header_text()
                    expected_header_text = TestData.DASHBOARD_HEADER_TEXT
                    assert actual_header_text == TestData.DASHBOARD_HEADER_TEXT
                    excel_data.loc[index, "result"] = "PASS"
                    self.logger.info("Test data is passed")
                    self.loginPage.do_Logout()
                elif self.expected_login == "No":
                    self.logger.info("Negative Test data is passed")
                    actual_error_text = self.loginPage.get_error_message_text()
                    print("Actual Error Text: ", actual_error_text)
                    print("Expected Error Text: ", self.loginPage.get_error_message_text())
                    assert actual_error_text == self.error_text_message
                    excel_data.loc[index, "result"] = "PASS"
        except Exception as e:
            excel_data.loc[index, "result"] = "FAIL"
            print("Exception Occured")
            self.logger.error(f"Testcase failed for row {index}: {e}")
            raise
        excel_utils.write_data_pandas(excel_data)

    # def test_Login_data_driven(self):
    #     self.logger.info("****************Test_Verification_Login_Page_Data_Driven**************")
    #     self.loginPage = LoginAdminPage(self.driver)
    #     admin_login_file = ReadConfig.get_admin_login_file()
    #     print("Admin Login file", admin_login_file)
    #     excel_data = excel_utils.read_data_pandas()









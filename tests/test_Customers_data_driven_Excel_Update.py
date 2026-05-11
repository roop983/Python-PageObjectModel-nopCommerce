import time

import pytest
import pandas as pd
from configuratation.config import TestData
from pages.CustomersPage import CustomersPage
from pages.LoginAdminPage import LoginAdminPage
from tests.test_Base import BaseTest
from utilities import excel_utils
from utilities.custom_logger import Log_maker
from selenium.webdriver.remote.webdriver import WebDriver
import allure

from utilities.excel_utils import get_customers_data
from utilities.read_configs_properties import ReadConfig


# from selenium.webdriver.remote.webdriver import WebDriver

class Test_Customers_data_driven(BaseTest):
    logger = Log_maker.log_gen()

    @pytest.mark.parametrize("data", get_customers_data())
    def test_Customers_data_driven(self, data):
        customers_excel_data = pd.read_excel(
                    ReadConfig.get_customers_data_file(),
                    sheet_name="Sheet1",
                    engine="openpyxl"
                    )
        self.logger.info("****************Test_Verification_Customers_Page_Data_Driven**************")
        # self.driver: WebDriver
        self.loginPage = LoginAdminPage(self.driver)
        self.loginPage.do_Login(ReadConfig.get_username(),ReadConfig.get_password())
        if "result" in customers_excel_data.columns:
            customers_excel_data["result"] = ""
        else:
            customers_excel_data["result"] = ""

        self.CustomersPage = CustomersPage(self.driver)
        # self.CustomersPage.add_comment
        self.CustomersPage.do_click(self.CustomersPage.customers_menu)


        for index, row in customers_excel_data.iterrows():
            try:
                self.CustomersPage.do_click(self.CustomersPage.customers_submenu)
                self.CustomersPage.do_click(self.CustomersPage.add_new_customer)
                self.CustomersPage.do_send_keys(self.CustomersPage.add_email, data["email"])
                # time.sleep(3)
                self.CustomersPage.do_send_keys(self.CustomersPage.add_password, data["password"])
                self.CustomersPage.do_send_keys(self.CustomersPage.add_firstname, data["firstname"])
                self.CustomersPage.do_send_keys(self.CustomersPage.add_lastname, data["lastname"])
                # time.sleep(5)
                if data["gender"] == 'female':
                    self.CustomersPage.do_click(self.CustomersPage.add_gender_female)
                elif data["gender"] == 'male':
                    self.CustomersPage.do_click(self.CustomersPage.add_gender_male)
                # time.sleep(5)
                self.CustomersPage.do_send_keys(self.CustomersPage.add_company_name, data["company_name"])
                if data["is_tax_exempt"] == 'yes':
                    self.CustomersPage.do_click(self.CustomersPage.add_tax_exempt)
                # time.sleep(5)
                if "," in str(data["customer_roles"]):
                    list_customer_roles = str(data["customer_roles"]).split(",")
                    if "Registered" not in list_customer_roles:
                        self.CustomersPage.do_click(self.CustomersPage.default_customer_role_registered_deselect)
                    for ele in list_customer_roles:
                        self.CustomersPage.do_select_customer_role_from_dropdown(ele.strip())
                # time.sleep(5)
                self.CustomersPage.do_select_vendor_from_dropdown(data["manager_vendor"])
                # time.sleep(5)
                self.CustomersPage.do_send_keys(self.CustomersPage.add_comment, data["admin_comment"])
                self.CustomersPage.do_click(self.CustomersPage.save_button)
                customers_excel_data.loc[index, "result"] = "PASS" #This line only updates data in memory, but doesnt write to excel file
                if "Not Applicable" not in str(data["error_message"]):
                    assert data["error_message"] == self.CustomersPage.get_element_text(self.CustomersPage.error_message_customer_roles)
                    customers_excel_data.loc[index, "result"] = "PASS"
                    continue
            except Exception as e:
                customers_excel_data.loc[index, "result"] = "FAIL"
                print("Exception Occured")
                self.logger.exception(f"Testcase failed for row {index}")
                raise # With this statement, the test case will fail whenever there is a exception. Without this, even if there is exception, the test case will be marked Passed.
            finally:
                customers_excel_data.to_excel(
                    ReadConfig.get_customers_data_file(),
                    sheet_name="Sheet1",
                    index=False,
                    engine="openpyxl"
                )









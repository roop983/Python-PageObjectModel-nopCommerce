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
from selenium import webdriver
import allure
import random

from utilities.custom_utility import generate_unique_email
from utilities.excel_utils import get_customers_data
from utilities.read_configs_properties import ReadConfig

# This  is a class fixture. Run once for this class only
@pytest.mark.usefixtures("login","navigate_to_customers")
class Test_Customers_data_driven(BaseTest):
    logger = Log_maker.log_gen()

    # Grouping Testcases
    @pytest.mark.regression
    @pytest.mark.parametrize("data", get_customers_data()) # Parametrize is similar to Dataprovider in TestNG, where testcases is taken from excel sheet
    def test_Customers_data_driven(self, data):
        self.logger.info("****************Test_Verification_Customers_Page_Data_Driven**************")
        customersPage = CustomersPage(self.driver)

        try:
            customersPage.do_click(customersPage.add_new_customer)
            if not(data["email"] == 'admin@yourstore.com'):
                new_email = generate_unique_email(data["email"])
                customersPage.do_send_keys(customersPage.add_email, new_email)
            else:
                customersPage.do_send_keys(customersPage.add_email, data["email"])
            # time.sleep(3)
            customersPage.do_send_keys(customersPage.add_password, data["password"])
            customersPage.do_send_keys(customersPage.add_firstname, data["firstname"])
            customersPage.do_send_keys(customersPage.add_lastname, data["lastname"])
            # time.sleep(5)
            if data["gender"] == 'female':
                customersPage.do_click(customersPage.add_gender_female)
            elif data["gender"] == 'male':
                customersPage.do_click(customersPage.add_gender_male)
            # time.sleep(5)
            customersPage.do_send_keys(customersPage.add_company_name, data["company_name"])
            if data["is_tax_exempt"] == 'yes':
                customersPage.do_click(customersPage.add_tax_exempt)
            # time.sleep(5)
            if "," in str(data["customer_roles"]):
                list_customer_roles = str(data["customer_roles"]).split(",")
                if "Registered" not in list_customer_roles:
                    customersPage.do_click(customersPage.default_customer_role_registered_deselect)
                for ele in list_customer_roles:
                    customersPage.do_select_customer_role_from_dropdown(ele.strip())
            # time.sleep(5)
            customersPage.do_select_vendor_from_dropdown(data["manager_vendor"])
            # time.sleep(5)
            customersPage.do_send_keys(customersPage.add_comment, data["admin_comment"])
            customersPage.do_click(customersPage.save_button)
            if "Not Applicable" not in str(data["error_message"]):
                actual_error = customersPage.get_element_text(customersPage.error_message_customer_roles)
                assert  actual_error == data["error_message"]
            else:
                assert True # or validate success message if available
            customersPage.do_click(customersPage.customers_submenu)
        except Exception:
            self.logger.exception("Test failed")
            self.driver.save_screenshot(f"screenshots/fail_{data['email']}.png")
            raise # With this statement, the test case will fail whenever there is a exception. Without this, even if there is exception, the test case will be marked Passed.









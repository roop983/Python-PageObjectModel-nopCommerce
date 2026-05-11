import base64
import allure
import pytest
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import WebDriver
from pytest_metadata.plugin import metadata_key
import pytest_html
import os

from pages.CustomersPage import CustomersPage
from pages.LoginAdminPage import LoginAdminPage
from utilities.custom_utility import generate_unique_email
from utilities.excel_utils import get_customers_data
from utilities.read_configs_properties import ReadConfig


# This function will enable to add the CLI command-line option --browser using pytest_addoption function. The default value is set to chrome.
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Specify the browser to run tests: chrome or firefox"
    )

# This fixture is to obtain the value of the command-line option --browser, passed from the above function
# It is then used as a parameter in the below init_driver fixture, to determine which browser to run for the test
@pytest.fixture(scope = 'class')
def init_driver(request):
    browser_name = request.config.getoption("browser")
    if browser_name == "chrome":
        options = uc.ChromeOptions()
        # options.add_argument("--headless=new") -- Headless Support
        driver: WebDriver = uc.Chrome(options=options, version_main=146)
    elif browser_name == "firefox":
        driver: WebDriver = webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    request.cls.driver = driver
    print(f"---------- Running tests on {browser_name} ----------")
    yield
    driver.quit()


    # def setup_method(self):
    #     self.driver: WebDriver
    #     self.driver = WebDriver.Chrome()


@pytest.fixture(scope="class")
def login(request):
    driver: WebDriver = request.cls.driver
    loginPage = LoginAdminPage(driver)
    loginPage.do_Login(
        ReadConfig.get_username(),
        ReadConfig.get_password()
    )
    yield

@pytest.fixture(scope="class")
def navigate_to_customers(request):
    driver: WebDriver = request.cls.driver
    customersPage = CustomersPage(driver)
    customersPage.do_click(customersPage.customers_menu)
    customersPage.do_click(customersPage.customers_submenu)

    yield

@pytest.fixture(scope="class")
def customers_email_test_data(request):
    data_list = get_customers_data()
    updated_data = []

    for data in data_list:
        new_email = generate_unique_email(data["email"])
        data["generated_unique_email"] = new_email # modify the dictionary to append a new item
        updated_data.append(data) # Originally data = {"email": "test_admin@yourstore.com","password": "123",}. Now data becomes:{  "email": "test_admin@yourstore.com",  "password": "123",   "generated_email": "test_admin_45678@yourstore.com}
    return updated_data


# Hooks are for customizing the code
# This configuration will run after every test and is for saving screenshot automatically whenever the testcase fails. hookwrapper=True → allows you to run code before AND after the test
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # Exact Hook name to be given here : pytest_runtest_makereport
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", []) # getattr(obj, "attr_name", default_value)
    if report.when == 'call' and report.failed:
        # driver = item.cls.driver
        driver: WebDriver = getattr(item.cls, "driver", None)
        if driver:
            # Capture screenshot as binary (no file needed)
            screenshot = driver.get_screenshot_as_png()
            # Convert to base64
            encoded = base64.b64encode(screenshot).decode("utf-8")
            # Attach to HTML report, Screenshot is embedded directly
            extra.append(pytest_html.extras.image(encoded, mime_type="image/png"))  # Command needed for pytest html report
            # Command needed for Allure report
            allure.attach(
                screenshot,
                name="Screenshot on Failure",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                driver.page_source,
                name="Page Source",
                attachment_type=allure.attachment_type.HTML
            )
            allure.attach(
                "Some debug info",
                name="Logs",
                attachment_type=allure.attachment_type.TEXT
            )
    report.extra = extra # Command needed only for pytest html report



# This Hook is to customize the environment information in a pytest-html report using the pytest-metadata plugin.
# It involves two main steps: adding custom data and removing unwanted default data like the environment info
def pytest_configure(config):
    config.stash[metadata_key]['Project Name'] = 'Ecommerce Project, nopcommerce' # This detail will be added to the report
    config.stash[metadata_key]['Test Module Name'] = 'Admin Login Tests'
    config.stash[metadata_key]['Tester Name'] = 'QA Tester'

# Hook for delete/modify environment info in html report
@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop('JAVA_HOME', None) # This removes specific entries if they exist.JAVA_HOME info will be removed from the report
    metadata.pop('Plugins', None) # This removes specific entries if they exist. Plugins info will be removed
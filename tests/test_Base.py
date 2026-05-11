import pytest
from selenium.webdriver.remote.webdriver import WebDriver
import pytest

# This  is a global fixture. Run for every tests defined in the test class
@pytest.mark.usefixtures("init_driver")
class BaseTest:
    driver: WebDriver
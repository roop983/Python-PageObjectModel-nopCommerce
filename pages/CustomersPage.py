from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.BasePage import BasePage


class CustomersPage(BasePage):

    def __init__(self, driver):
        self.driver = driver
        # self.driver.get(TestData.BASE_URL)

    EMAIL = (By.NAME, "Email")
    PASSWORD = (By.CSS_SELECTOR, "input[id='Password']")
    LOGIN_BTN = (By.CSS_SELECTOR, "button.login-button")

    customers_menu = (By.XPATH, "//a[@class='nav-link' and @href='#']/p[normalize-space()='Customers']")
    customers_submenu = (By.XPATH, "//a[contains(@class,'nav-link') and @href='/Admin/Customer/List']/p[normalize-space()='Customers']")
    add_new_customer = (By.XPATH, "//a[@href='/Admin/Customer/Create' and normalize-space()='Add new']")
    add_email = (By.CSS_SELECTOR, "input[id='Email']")
    add_password = (By.CSS_SELECTOR, "input[id='Password']")
    add_firstname = (By.CSS_SELECTOR, "input[id='FirstName']")
    add_lastname = (By.CSS_SELECTOR, "input[id='LastName']")
    add_gender_female = (By.CSS_SELECTOR, "input[id='Gender_Female']")
    add_gender_male = (By.CSS_SELECTOR, "input[id='Gender_Male']")
    add_company_name = (By.CSS_SELECTOR, "input[id='Company']")
    add_tax_exempt = (By.CSS_SELECTOR, "input[id='IsTaxExempt']")
    customer_roles = (By.CSS_SELECTOR, "ul[class='select2-selection__rendered']")
    default_customer_role_registered_deselect = (By.CSS_SELECTOR, "li[title='Registered'] > span")
    customer_roles_select = (By.CSS_SELECTOR, "select[id='SelectedCustomerRoleIds']")
    add_vendor = (By.CSS_SELECTOR, "ul[class='select2-selection__rendered']")
    select_vendor = (By.CSS_SELECTOR, "select[id='VendorId']")
    add_comment = (By.CSS_SELECTOR, "textarea[id='AdminComment']")
    save_button = (By.XPATH, "//button[@name='save']")
    error_message_customer_roles = (By.CSS_SELECTOR, "div.validation-summary-errors > ul > li")
    customers_header_text = (By.CSS_SELECTOR, "div.content-header")


    def do_select_customer_role_from_dropdown(self, text):
        self.select_dropdown_visible_text(self.customer_roles_select, text)
        self.do_click(self.customer_roles)

    def do_select_vendor_from_dropdown(self, text):
        self.do_click(self.add_vendor)
        self.select_dropdown_visible_text(self.select_vendor, text)










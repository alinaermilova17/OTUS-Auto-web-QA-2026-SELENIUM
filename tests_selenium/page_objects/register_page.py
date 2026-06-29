from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage:
    FIRSTNAME_INPUT = (By.ID, "field-firstname")
    LASTNAME_INPUT = (By.ID, "field-lastname")
    EMAIL_INPUT = (By.ID, "field-email")
    PASSWORD_INPUT = (By.ID, "field-password")
    REGISTER_FORM = (By.CSS_SELECTOR, "#content > section")
    SAVE_BUTTON = (By.CSS_SELECTOR, "#customer-form > footer > button")
    FEMALE_GENDER = (By.CSS_SELECTOR, "#field-id_gender-2")
    BIRTH_DATE_INPUT = (By.CSS_SELECTOR, "#field-birthday")
    AGREEMENT_CHECKBOX = (By.XPATH, "(//*[@id='customer-form']//input[@type='checkbox'])[2]")
    CUSTOMER_PRIVACY = (By.XPATH, "//*[@id='customer-form']/div/div[10]/div[1]/span/label/input")

    def __init__(self, browser):
        self.browser= browser
        self.wait = WebDriverWait(browser, 15)

    def open_register_form(self, base_url: str):
        self.browser.get(f'{base_url}/registration')
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        return self

    def email_input(self, email: str ):
        self.browser.find_element(*RegisterPage.EMAIL_INPUT).send_keys(email)
        return self

    def password_input(self, password: str):
        self.browser.find_element(*RegisterPage.PASSWORD_INPUT).send_keys(password)
        return self

    def firstname_input(self, firstname: str):
        self.browser.find_element(*RegisterPage.FIRSTNAME_INPUT).send_keys(firstname)
        return self

    def lastname_input(self, lastname: str):
        self.browser.find_element(*RegisterPage.LASTNAME_INPUT).send_keys(lastname)
        return self

    def save_button(self):
        self.browser.find_element(*RegisterPage.SAVE_BUTTON).click()

    def female_gender_input(self):
        self.browser.find_element(*RegisterPage.FEMALE_GENDER).click()

    def birth_date_input(self,birthdate: str ):
        self.browser.find_element(*RegisterPage.BIRTH_DATE_INPUT).send_keys(birthdate)
        return self
    def agreement_privacy(self):
        self.browser.find_element(*RegisterPage.AGREEMENT_CHECKBOX).click()

    def customer_privacy(self):
        self.browser.find_element(*RegisterPage.CUSTOMER_PRIVACY).click()

    def register(self, user_data: dict):
        self.firstname_input(user_data['firstname'])
        self.lastname_input(user_data['lastname'])
        self.email_input(user_data['email'])
        self.password_input(user_data['password'])
        self.firstname_input(user_data['firstname'])
        self.birth_date_input(user_data['birthdate'])
        self.female_gender_input()
        self.agreement_privacy()
        self.customer_privacy()
        self.save_button()
        return self


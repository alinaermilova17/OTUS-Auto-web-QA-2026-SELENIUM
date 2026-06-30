from selenium.webdriver.common.by import By
from tests_selenium.page_objects.base_page import BasePage


class RegisterPage(BasePage):
    FIRSTNAME_INPUT = (By.ID, 'field-firstname')
    LASTNAME_INPUT = (By.ID, 'field-lastname')
    EMAIL_INPUT = (By.ID, 'field-email')
    PASSWORD_INPUT = (By.ID, 'field-password')
    REGISTER_FORM = (By.CSS_SELECTOR, '#content > section')
    SAVE_BUTTON = (By.CSS_SELECTOR, '#customer-form > footer > button')
    FEMALE_GENDER = (By.XPATH, "//input[@id='field-id_gender-2']")
    BIRTH_DATE_INPUT = (By.CSS_SELECTOR, '#field-birthday')
    AGREEMENT_CHECKBOX = (By.XPATH, "(//*[@id='customer-form']//input[@type='checkbox'])[2]")
    CUSTOMER_PRIVACY = (By.XPATH, "//*[@id='customer-form']/div/div[10]/div[1]/span/label/input")

    def email_input(self, email: str ):
        return self.find(self.EMAIL_INPUT).send_keys(email)

    def password_input(self, password: str):
        return self.find(self.PASSWORD_INPUT).send_keys(password)

    def firstname_input(self, firstname: str):
        return self.find(self.FIRSTNAME_INPUT).send_keys(firstname)

    def lastname_input(self, lastname: str):
        return self.find(self.LASTNAME_INPUT).send_keys(lastname)

    def save_button(self):
        self.click(self.SAVE_BUTTON)

    def female_gender_input(self):
        self.find(self.FEMALE_GENDER).click()

    def birth_date_input(self,birthdate: str ):
        return self.find(self.BIRTH_DATE_INPUT).send_keys(birthdate)

    def agreement_privacy(self):
        self.find(self.AGREEMENT_CHECKBOX).click()

    def customer_privacy(self):
        self.find(self.CUSTOMER_PRIVACY).click()

    def register(self, user_data: dict):
        self.female_gender_input()
        self.firstname_input(user_data['firstname'])
        self.lastname_input(user_data['lastname'])
        self.email_input(user_data['email'])
        self.password_input(user_data['password'])
        self.birth_date_input(user_data['birthdate'])
        self.agreement_privacy()
        self.customer_privacy()
        self.save_button()
        return self


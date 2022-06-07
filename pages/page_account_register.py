from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class PageRegisterLocator:
    CONTINUE = (By.CSS_SELECTOR, '[value = "Continue"]')


class PageRegister(BasePage):
    def fill_in_the_fields(self, firstname, lastname, email, telephone, password, confirm):
        with allure.step("Заполнение полей"):
            self.find_element((By.CSS_SELECTOR, '[name="firstname"]')).send_keys(firstname)
            self.find_element((By.CSS_SELECTOR, '[name="lastname"]')).send_keys(lastname)
            self.find_element((By.CSS_SELECTOR, '[name="email"]')).send_keys(email)
            self.find_element((By.CSS_SELECTOR, '[name="telephone"]')).send_keys(telephone)
            self.find_element((By.CSS_SELECTOR, '[name="password"]')).send_keys(password)
            self.find_element((By.CSS_SELECTOR, '[name="confirm"]')).send_keys(confirm)

    def click_continue_button(self):
        with allure.step("Нажимаем кнопку продолжить"):
            self.find_element(PageRegisterLocator.CONTINUE).click()

    def click_checkbox_privacy_policy(self):
        with allure.step("Кликаем на чекбокс"):
            self.find_element((By.CSS_SELECTOR, '[name="agree"]')).click()

    def get_text_alert_null__privacy_policy(self):
        with allure.step("Получаем текст аллерта"):
            return self.find_element((By.CSS_SELECTOR, '[class="alert alert-danger alert-dismissible"]')).text

    def get_text_error_null_name(self):
        with allure.step("Получаем ошибку незаполненного поля"):
            return self.find_elements((By.CSS_SELECTOR, '[class="text-danger"]'))[0].text

    def get_count_error_null_fields(self):
        with allure.step("Считаем количество незаполненных полей"):
            return len(self.find_elements((By.CSS_SELECTOR, '[class="text-danger"]')))

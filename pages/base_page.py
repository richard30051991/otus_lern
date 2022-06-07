from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import allure


class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def find_element(self, locator, time=8):
        return WebDriverWait(self.browser, time).until(EC.presence_of_element_located(locator),
                                                       message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=6):
        return WebDriverWait(self.browser, time).until(EC.presence_of_all_elements_located(locator),
                                                       message=f"Can't find elements by locator {locator}")

    def search_by_text(self, text):
        with allure.step(f"ищем на странице {text}"):
            try:
                self.find_element((By.XPATH, f"//*[contains(text(), '{text}')]"))
                return True
            except TimeoutException:
                return False

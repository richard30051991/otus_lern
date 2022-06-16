from pages.page_account_register import PageRegister
from pages.base_page import BasePage
from pages.page_home_opencard import PageHomeShop
from pages.page_catalog_opencard import PageCatalogShop
from pages.page_card_apple_cinema import PageCardShop
import allure
import uuid


@allure.feature('Тест магазина опенкард')
@allure.story('Регистрация нового пользователя')
def test_add_new_user(browser, url):
    browser.get(url + "/index.php?route=account/register")
    email = str(uuid.uuid1()) + "@test.ru"
    PageRegister(browser).fill_in_the_fields(firstname="Имя",
                                             lastname="Фамилия",
                                             email=email,
                                             telephone="123456798",
                                             password="12345",
                                             confirm="12345")
    PageRegister(browser).click_checkbox_privacy_policy()
    PageRegister(browser).click_continue_button()
    assert BasePage(browser).search_by_text("Your Account Has Been Created!")
    assert BasePage(browser).search_by_text("Congratulations! Your new account has been successfully created!")


@allure.feature('Тест магазина опенкард')
@allure.story('Смена валюты оплаты')
def test_change_currency(browser, url):
    browser.get(url)
    PageHomeShop(browser).click_menu_change_currency()
    PageHomeShop(browser).change_currency('EUR')
    assert PageHomeShop(browser).get_text_icon_currency() == "€"
    assert PageHomeShop(browser).get_price_macbook() == "472.33€\nEx Tax: 392.30€"
    PageHomeShop(browser).click_menu_change_currency()
    PageHomeShop(browser).change_currency('GBP')
    assert PageHomeShop(browser).get_text_icon_currency() == "£"
    assert PageHomeShop(browser).get_price_macbook() == "£368.73\nEx Tax: £306.25"
    PageHomeShop(browser).click_menu_change_currency()
    PageHomeShop(browser).change_currency('USD')
    assert PageHomeShop(browser).get_text_icon_currency() == "$"
    assert PageHomeShop(browser).get_price_macbook() == "$602.00\nEx Tax: $500.00"


@allure.feature('Тест магазина опенкард')
@allure.story('Проверка домашней страница магазина')
def test_home_page(browser, url):
    browser.get(url)
    assert PageHomeShop(browser).get_count_product_by_page() == 4
    assert PageHomeShop(browser).get_text_footer() == "Powered By OpenCart Your Store © 2022"
    PageHomeShop(browser).click_menu_change_currency()
    assert PageHomeShop(browser).count_currency() == 3

    assert PageHomeShop(browser).get_text_by_search_placeholder() == "Search"
    assert " item(s) - $" in PageHomeShop(browser).get_text_by_button_basket()


@allure.feature('Тест магазина опенкард')
@allure.story('Проверка страницы каталога')
def test_catalog(browser, url):
    browser.get(url+"index.php?route=product/category&path=20")
    assert PageCatalogShop(browser).check_input_limit() == "15"
    assert PageCatalogShop(browser).get_input_sort() == "Default"
    assert PageCatalogShop(browser).get_new_price_apple_cinema() == "$110.00"
    assert PageCatalogShop(browser).get_old_price_apple_cinema() == "$122.00"


@allure.feature('Тест магазина опенкард')
@allure.story('Карточка товара Apple Cinema')
def test_card_apple_cinema(browser, url):
    browser.get(url+"index.php?route=product/product&product_id=42")
    assert PageCardShop(browser).get_count_image_product() == 5
    assert PageCardShop(browser).get_styles_price() == "text-decoration: line-through;"
    assert PageCardShop(browser).get_name_product() == 'Apple Cinema 30"'


@allure.feature('Тест магазина опенкард')
@allure.story('Страница регистрации нового пользователя')
def test_page_registration(browser, url):
    browser.get(url + "index.php?route=account/register")
    PageRegister(browser).click_continue_button()
    assert PageRegister(browser).get_text_alert_null__privacy_policy() == \
           'Warning: You must agree to the Privacy Policy!'
    assert PageRegister(browser).get_text_error_null_name() == "First Name must be between 1 and 32 characters!"
    assert PageRegister(browser).get_count_error_null_fields() == 5

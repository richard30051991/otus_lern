from pages.page_admin_home_page import PageHomeAdmin
from pages.page_admin_add_product import PageAddProduct
from pages.page_autorization import PageAuthorizationAdmin
import allure


@allure.feature('Тест Админка')
@allure.story('Добавление нового товара')
def test_add_product(browser, authorization_admin):
    PageHomeAdmin(browser).open_page_products()
    count_product = PageHomeAdmin(browser).count_product()
    PageHomeAdmin(browser).open_menu_add_product()
    PageAddProduct(browser).fill_name_title_model(name="Название товара",
                                                  title="Описание товара",
                                                  model="С3РО")
    PageAddProduct(browser).click_save_product_button()
    assert PageHomeAdmin(browser).text_alert() == "Success: You have modified products!\n×"
    assert count_product + 1 == PageHomeAdmin(browser).count_product()


@allure.feature('Тест Админка')
@allure.story('Удаление товара')
def test_delete_product(browser, authorization_admin):
    name = "1ый товар на удаление"
    PageHomeAdmin(browser).open_page_products()
    PageHomeAdmin(browser).open_menu_add_product()
    PageAddProduct(browser).fill_name_title_model(name=name,
                                                  title="Описание товара",
                                                  model="С3РО")
    PageAddProduct(browser).click_save_product_button()
    count_product = PageHomeAdmin(browser).count_product()
    PageHomeAdmin(browser).change_checkbox_by_name_product(name)
    PageHomeAdmin(browser).click_delete_button()
    assert PageHomeAdmin(browser).text_alert() == "Success: You have modified products!\n×"
    assert count_product - 1 == PageHomeAdmin(browser).count_product()


@allure.feature('Тест Админка')
@allure.story('Страница авторизации')
def test_page_authorization(browser, url):
    browser.get(url + "admin/")
    assert PageAuthorizationAdmin(browser).get_text_title() == "Please enter your login details."
    assert PageAuthorizationAdmin(browser).get_text_by_button_submit() == "Login"
    assert PageAuthorizationAdmin(browser).get_text_by_error_authorization() ==\
           'No match for Username and/or Password.\n×'
    assert PageAuthorizationAdmin(browser).get_text_placeholder("username") == "Username"
    assert PageAuthorizationAdmin(browser).get_text_placeholder("password") == "Password"


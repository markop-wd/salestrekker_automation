"""
When something out of the ordinary has to be done
Instead of programming in the main business logic just implement it here and import it there
"""
import random
import traceback
import string
from time import sleep

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from selenium.webdriver import Firefox
from webdriver_manager.firefox import GeckoDriverManager

from main.Permanent.login import LogIn
from main.mail import mail_get


def random_string_create(char_nums: int = 10):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(char_nums))
    return result_str


def password_string_create(char_nums: int = 10):
    result_str = ''

    result_str += random.choice(string.ascii_lowercase)
    result_str += random.choice(string.ascii_uppercase)
    result_str += random.choice(string.digits)
    result_str += random.choice(string.punctuation)

    result_str += ''.join(random.choice(string.printable[:-6]) for i in range(char_nums))
    return result_str


def user_setup_raw(driver: Firefox, ent: str):
    """
    This is a basic version of setting up a user for the first time
    # TODO Improve this version and connect it to the LogIn class
    :param driver:
    :param ent:
    :return:
    """
    driver.maximize_window()
    mail_dict = mail_get(ent)
    if mail_dict['email'] and mail_dict['password']:
        LogIn(driver, ent, mail_dict['email'], mail_dict['password']).log_in()
        print(f'Logged into - {ent}')
        try:
            driver.find_element(by=By.CSS_SELECTOR, value='input[name="phoneNumber"]')

        except exceptions.NoSuchElementException:
            pass
        else:
            WdWait(driver, 10).until(
                ec.visibility_of_element_located((
                    By.CSS_SELECTOR, 'input[name="phoneNumber"]'))).send_keys('123456789')

            WdWait(driver, 10).until(
                ec.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    'input[ng-model="CurrentAccount.user.address.street"]'))) \
                .send_keys('street')

            driver.find_element(by=By.CSS_SELECTOR,
                                value='a[ui-sref=".password-and-security"]').click()

        WdWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
        new_password = password_string_create()
        print(new_password)
        for element in driver.find_elements_by_css_selector('input[type="password"]'):
            if element.get_attribute('ng-model') == 'Model.oldPassword':
                element.send_keys(mail_dict['password'])
            else:
                element.send_keys(new_password)
            sleep(1)

        WdWait(driver, 10).until(ec.element_to_be_clickable((
            By.CSS_SELECTOR, 'button[ng-click="changePassword()"]'))).click()

        WdWait(driver, 10).until(ec.element_to_be_clickable
                                 ((By.CSS_SELECTOR,
                                   'div[ng-if="Model.AUTH.isPasswordChangeRequired()"] button'))) \
            .click()

        WdWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'board#board')))
        input(f'{ent} finish')
    else:
        print('Oj dios mio no email information')


def md_toast_waiter(driver: Firefox):
    try:
        driver.find_element(by=By.TAG_NAME, value='md-toast')
    except exceptions.NoSuchElementException:
        try:
            WdWait(driver, 3).until(ec.invisibility_of_element_located((By.TAG_NAME, 'md-toast')))
        except exceptions.TimeoutException:
            md_toast_waiter(driver)
    else:
        while True:
            try:
                md_toast = driver.find_element(by=By.TAG_NAME, value='md-toast')
            except exceptions.NoSuchElementException:
                break
            else:
                driver.execute_script("arguments[0].remove();", md_toast)
                try:
                    md_toast2 = driver.find_element(by=By.TAG_NAME, value='md-toast')
                except exceptions.NoSuchElementException:
                    break
                else:
                    driver.execute_script("arguments[0].remove();", md_toast2)
                sleep(3)


def element_clicker(driver: Firefox, web_element: WebElement = None, css_selector: str = ''):
    if css_selector:
        try:
            element = WdWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        except exceptions.TimeoutException:
            raise exceptions.ElementNotInteractableException(
                'Element not clickable after 10 seconds')
        except exceptions.NoSuchElementException:
            raise exceptions.NoSuchElementException(
                f'No element found with css selector: {css_selector}')
        except Exception as e:
            print(traceback.format_exc())
            raise e
        else:
            try:
                element.click()
            except exceptions.ElementClickInterceptedException:
                md_toast_waiter(driver)
                driver.execute_script('arguments[0].click();', element)
            except Exception as e:
                print(traceback.format_exc())
                raise e
    elif web_element:
        try:
            web_element.click()
        except exceptions.ElementClickInterceptedException:
            md_toast_waiter(driver)
            driver.execute_script('arguments[0].click();', web_element)
        except Exception as e:
            print(traceback.format_exc())
            raise e


if __name__ == '__main__':
    # user_setup_raw(Firefox(executable_path=GeckoDriverManager().install()), ent='dev')
    print(password_string_create())

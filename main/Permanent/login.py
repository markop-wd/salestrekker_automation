from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait

# TODO - Add assertions that certain elements are in place - this is a good starting point for tests
from main.Permanent.helper_funcs import element_waiter


def run(driver: Chrome, ent: str, email: str, password: str, two_fact: str = ''):
    auth_url = "https://" + ent + '.salestrekker.com/authenticate'

    driver.get(auth_url)
    element_waiter(driver=driver, css_selector="form#auth", url=auth_url)

    driver.find_element(by=By.CSS_SELECTOR,
                        value='input[name="email"]').send_keys(email)

    driver.find_element(by=By.CSS_SELECTOR,
                        value='input[ng-model="password"]').send_keys(password)
    driver.find_element(by=By.TAG_NAME, value='button').click()

    try:
        WdWait(driver, 5).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'span > span.mr1')))
    except exceptions.TimeoutException:
        pass
    else:
        # TODO - custom exception, remove the try except pass block
        print('Incorrect login information')
        raise exceptions.TimeoutException

    try:
        WdWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'navBar')))
    except exceptions.TimeoutException:
        if driver.current_url == auth_url:
            try:
                WdWait(driver, 5).until(
                    ec.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'input[ng-model="twoFactorCode"]')))
            except exceptions.TimeoutException:
                try:
                    WdWait(driver, 10).until(
                        ec.visibility_of_element_located((By.ID, 'navBar')))
                except exceptions.TimeoutException:
                    raise exceptions.TimeoutException

            else:
                # TODO - Writer a leaner implementation, add a custom exception
                if not two_fact:
                    raise ValueError('No two factor code provided')

                driver.find_element(By.CSS_SELECTOR,
                                    value='input[ng-model="twoFactorCode"]').send_keys(two_fact)
                driver.find_element(by=By.TAG_NAME, value='button').click()
                element_waiter(driver, css_selector='#navBar')



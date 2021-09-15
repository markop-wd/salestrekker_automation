"""
Client portal login function
"""
from time import sleep

from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait

from main.Permanent.helper_funcs import element_clicker, element_waiter


def _log_in_helper(driver: Chrome, link: str, pin: str, ent: str):
    assert driver.title == 'Authenticate | Salestrekker Client Portal'
    element_waiter(driver, css_selector='input', url=link)

    driver.find_element(by=By.CSS_SELECTOR,
                        value='input[placeholder="PIN code"]').send_keys(pin)
    element_clicker(driver=driver, css_selector='button')

    try:
        WdWait(driver, 5).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.bp3-intent-danger')))
    except exceptions.TimeoutException:
        pass
    else:
        print('Incorrect login information')
        raise exceptions.TimeoutException

    try:
        WdWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'dashboard')))
    except exceptions.TimeoutException:
        if driver.current_url != f'https://{ent}-cp.salestrekker.com/dashboard':
            WdWait(driver, 15).until(
                ec.visibility_of_element_located((By.CLASS_NAME, 'dashboard')))
            # TODO - Privacy YES/NO handler


def log_in(driver: Chrome, link: str, pin: str):
    """

    Args:
        driver ():
        link ():
        pin ():

    Returns:

    """
    ent = link.split('-')[0].split('/')[-1]

    driver.get(link)
    try:
        WdWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'div#root')))
    except exceptions.TimeoutException as exc:
        time_increment = 0
        while True:
            driver.get(link)

            if "Authenticate" in driver.title:
                break

            if time_increment > 13:
                print('Salestrekker unresponsive, manual checkup needed')
                raise exceptions.TimeoutException from exc

            sleep(time_increment)
            try:
                WdWait(driver, time_increment).until(
                    ec.visibility_of_element_located((By.TAG_NAME, 'div#root')))
            except exceptions.TimeoutException:
                time_increment += 2
    finally:
        _log_in_helper(driver=driver, ent=ent, link=link, pin=pin)

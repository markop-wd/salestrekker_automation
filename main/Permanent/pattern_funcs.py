from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from selenium.webdriver import Firefox

from time import sleep


def css_element_click(driver: Firefox, css_selector: str, refresh=True):
    try:
        WdWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, css_selector))).click()
    except exceptions.ElementNotInteractableException:
        # TODO - Handler for the element not interactable exception
        driver.execute_script(f"document.querySelector('{css_selector}').click();")
    except exceptions.ElementClickInterceptedException:
        driver.execute_script(f"document.querySelector('{css_selector}').click();")
    except exceptions.TimeoutException:
        if refresh:
            driver.refresh()
            try:
                WdWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, str(css_selector)))).click()
            except exceptions.ElementNotInteractableException:
                driver.execute_script(f"document.querySelector('{css_selector}').click();")
            except exceptions.ElementClickInterceptedException:
                driver.execute_script(f"document.querySelector('{css_selector}').click();")
            except exceptions.TimeoutException:
                driver.refresh()
    except Exception as exc:
        print('Unkown exception')


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

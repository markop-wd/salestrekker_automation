from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def css_element_click(driver, element, refresh=True):
    try:
        WdWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, str(element)))).click()
    except exceptions.ElementNotInteractableException:
        driver.execute_script(f"document.querySelector('{element}').click();")
    except exceptions.ElementClickInterceptedException:
        driver.execute_script(f"document.querySelector('{element}').click();")
    except exceptions.TimeoutException:
        if refresh:
            driver.refresh()
            try:
                WdWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, str(element)))).click()
            except exceptions.ElementNotInteractableException:
                driver.execute_script(f"document.querySelector('{element}').click();")
            except exceptions.ElementClickInterceptedException:
                driver.execute_script(f"document.querySelector('{element}').click();")
            except exceptions.TimeoutException:
                driver.refresh()
    except Exception as exc:
        print('Unkown exception')


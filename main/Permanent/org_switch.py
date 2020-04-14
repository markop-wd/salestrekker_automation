from selenium.webdriver.support.wait import WebDriverWait as wd_wait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


def org_changer(driver, org_name):
    assert "salestrekker" in driver.current_url, 'invalid url'
    assert "authenticate" not in driver.current_url, 'you are at a login page'
    try:
        wd_wait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME,'st-toolbar')))
    except exceptions.TimeoutException:
        driver.refresh()
        try:
            wd_wait(driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-toolbar')))
        except exceptions.TimeoutException:
            driver.quit()
            # TODO - Cleanup

    try:
        driver.execute_script('document.querySelector("body > div > md-menu-content > md-menu-item > button").click();')
    except exceptions.JavascriptException:
        try:
            driver.refresh()
            wd_wait(driver, 15).until(ec.presence_of_element_located((By.CSS_SELECTOR, '#navBar > div > md-menu > a')))
        except exceptions.TimeoutException:
            driver.quit()
            # --TODO - Custom error here
            # TODO - Cleanup
        else:
            driver.execute_script(
                'document.querySelector("body > div > md-menu-content > md-menu-item > button").click();')

    #
    # try:
    #     wd_wait(driver, 10).until(ec.presence_of_element_located(
    #         (By.CSS_SELECTOR, 'body > div > md-menu-content > md-menu-item > button')))
    # except exceptions.ElementClickInterceptedException:
    #     driver.execute_script('document.querySelector("body > div > md-menu-content > '
    #                           'md-menu-item:nth-child(3) > button").click();')

    wd_wait(driver, 15).until(
        ec.presence_of_element_located((By.XPATH, "//md-dialog[@aria-label='Switch organization']")))
    driver.find_element_by_xpath("//input[@placeholder='Search for an organization']").send_keys(
        org_name)

    # TODO - REWRITE
    try:
        organisation_names = driver.find_elements_by_css_selector('div > small')
        for element in organisation_names:
            if element.text.lower() == str(org_name).lower():
                element.find_element_by_xpath("./..").click()
                print('found and clicked', org_name)
                break
            else:
                print('passing over')
                pass
    except exceptions.NoSuchElementException:
        print('No organisation with such name')
        driver.quit()
        # TODO - Cleanup

    # TODO - Cleanup

    try:
        wd_wait(driver, 80).until(ec.title_contains(org_name))
    except exceptions.TimeoutException:
        driver.quit()
        # TODO - Cleanup
    print('Org Changer Finished')

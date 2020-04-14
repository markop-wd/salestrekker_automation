from selenium.webdriver.support.wait import WebDriverWait as wd_wait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
from contextlib import contextmanager


def log_in_helper(driver, email, password):
    try:
        wd_wait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
    except exceptions.TimeoutException:
        driver.refresh()
        try:
            wd_wait(driver, 15).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
        except exceptions.TimeoutException:
            driver.refresh()
            try:
                wd_wait(driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
            except exceptions.TimeoutException:
                print('Salestrekker unresponsive, manual checkup needed')
                driver.quit()
                # TODO - Check Availability and Cleanup

    # TODO - Unknown exception^

    else:
        input_elements = driver.find_elements_by_tag_name('input')
        for log_input in input_elements:
            if log_input.get_attribute('placeholder') == 'Your E-Mail':
                log_input.send_keys(email)
                continue
            elif log_input.get_attribute('placeholder') == 'Your Password':
                log_input.send_keys(password)
                continue
            else:
                continue

        driver.find_element_by_tag_name('button').click()


def log_in(driver, ent, email, password):
    driver.get("https://" + ent + '.salestrekker.com/authenticate')
    try:
        wd_wait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'sign-in')))
    except exceptions.TimeoutException:
        time_increment = 0
        while True:
            driver.get("https://" + ent + '.salestrekker.com/authenticate')
            if "Authentication" in driver.title:
                break
            elif time_increment > 13:
                print('Salestrekker unresponsive, manual checkup needed')
                driver.quit()
                # TODO - Check Availability and Cleanup

            time.sleep(time_increment)
            try:
                wd_wait(driver, time_increment).until(ec.presence_of_element_located((By.TAG_NAME, 'sign-in')))
            except exceptions.TimeoutException:
                time_increment += 2

    log_in_helper(driver, email, password)

    try:
        wd_wait(driver, 15).until(ec.presence_of_element_located((By.ID, 'board')))
    except exceptions.TimeoutException:
        while True:
            log_in_helper(driver, email, password)
            wd_wait(driver, 15).until(By.ID, 'board')

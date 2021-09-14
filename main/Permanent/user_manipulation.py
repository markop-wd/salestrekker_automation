from time import sleep

from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait


# TODO move this to API
def add_user(driver: Chrome, ent: str, email: str, username: str, broker: bool = True,
             admin: bool = True, mentor: bool = False):
    main_url = "https://" + ent + ".salestrekker.com"
    first_name = username.split(' ')[0]
    try:
        last_name = username.split(' ')[1]
    except IndexError:
        last_name = 'Surname'
        username = first_name + ' Surname'

    try:
        WdWait(driver, 5).until(ec.visibility_of_element_located((By.TAG_NAME, 'st-accounts-list')))
    except exceptions.TimeoutException:
        driver.get(main_url + '/settings/users')
        try:
            WdWait(driver, 10).until(
                ec.visibility_of_element_located((By.TAG_NAME, 'st-accounts-list')))
        except exceptions.TimeoutException:
            driver.get(main_url + '/settings/users')
            WdWait(driver, 15).until(
                ec.visibility_of_element_located((By.TAG_NAME, 'st-accounts-list')))

    driver.find_element(by=By.CSS_SELECTOR, value='span > button').click()
    WdWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'span > button')))

    def send_text_to_element(css_input, input_value):
        driver.find_element(by=By.CSS_SELECTOR, value=css_input).send_keys(input_value)
        sleep(0.5)
        try:
            WdWait(driver, 1).until(
                ec.text_to_be_present_in_element_value((By.CSS_SELECTOR, css_input),
                                                       input_value))
        except exceptions.TimeoutException:
            driver.find_element(by=By.CSS_SELECTOR, value=css_input).send_keys(
                Keys.CONTROL + "a")
            driver.find_element(by=By.CSS_SELECTOR, value=css_input).send_keys(input_value)

    send_text_to_element('div:nth-child(1) > md-input-container > input', email)

    send_text_to_element('div:nth-child(2) > md-input-container > input', first_name)

    send_text_to_element('div:nth-child(3) > md-input-container > input', last_name)

    try:
        WdWait(driver, 10).until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR, 'md-dialog-actions > button:nth-child(2)'))).click()
    except exceptions.ElementClickInterceptedException:
        driver.execute_script(
            'document.querySelector("md-dialog-actions > button:nth-child(2)").click();')

    WdWait(driver, 10).until(
        ec.text_to_be_present_in_element((By.CSS_SELECTOR, 'span.md-toast-text > span:first-child'),
                                         'User'))
    WdWait(driver, 10).until(
        ec.invisibility_of_element_located(
            (By.CSS_SELECTOR, 'span.md-toast-text > span:first-child')))
    user = return_user(driver, username, email)
    # TODO - Make a validation first before clicking it and make better checks that it's done
    if broker:
        mortgage_broker_switch = user.find_element(by=By.CSS_SELECTOR,
                                                   value='md-switch[aria-label="User is Mortgage Broker"]')

        try:
            mortgage_broker_switch.click()
        except exceptions.ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", mortgage_broker_switch)

        try:
            user.find_element(by=By.CSS_SELECTOR,
                              value='a:nth-child(7) > md-switch[aria-checked="true"]')
        except exceptions.NoSuchElementException:
            print(username, 'Broker Click Error')

    if mentor:
        mentor_switch = user.find_element(by=By.CSS_SELECTOR,
                                          value='md-switch[aria-label="User is Mentor"]')

        try:
            mentor_switch.click()
        except exceptions.ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", mentor_switch)

        try:
            user.find_element(by=By.CSS_SELECTOR,
                              value='a:nth-child(6) > md-switch[aria-checked="true"]')
        except exceptions.NoSuchElementException:
            print(username, 'Mentor Click Error')

    if admin:
        admin_switch = user.find_element(by=By.CSS_SELECTOR,
                                         value='md-switch[aria-label="User is System Admin"]')

        try:
            admin_switch.click()
        except exceptions.ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", admin_switch)

        try:
            user.find_element(by=By.CSS_SELECTOR,
                              value='a:nth-child(8) > md-switch[aria-checked="true"]')
        except exceptions.NoSuchElementException:
            print(username, 'Admin Click Error')


def return_user(driver, username, email):
    # assert "Users : Settings" in driver.title
    main_documents = driver.find_element(by=By.CSS_SELECTOR, value='body > md-content')
    last_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)
    sleep(0.2)
    while True:
        driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
        sleep(3)
        new_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)

        if new_height == last_height:
            break
        last_height = new_height

    users = driver.find_elements(by=By.TAG_NAME, value='st-list-item')
    for user in users:
        if user.find_element(by=By.CSS_SELECTOR,
                             value='a:first-of-type > content > span').text == username:
            if user.find_element(by=By.CSS_SELECTOR,
                                 value='a:first-of-type > content > sub-content > em').text.lower() == email.lower():
                return user


# TODO Move this to API
def return_all_users(driver: Chrome, ent):
    if driver.current_url != f"https://{ent}.salestrekker.com/settings/users":
        driver.get("https://" + ent + ".salestrekker.com/settings/users")

    try:
        WdWait(driver, 15).until(
            ec.visibility_of_element_located((By.TAG_NAME, "st-accounts-list")))
    except exceptions.TimeoutException:
        driver.refresh()
        WdWait(driver, 30).until(
            ec.visibility_of_element_located((By.TAG_NAME, "st-accounts-list")))

    main_documents = driver.find_element(by=By.CSS_SELECTOR, value='body > md-content')
    last_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)
    sleep(0.2)
    while True:
        driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
        sleep(3)
        new_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)

        if new_height == last_height:
            break
        last_height = new_height

    users = [user.text for user in driver.find_elements(by=By.CSS_SELECTOR,
                                                        value='a:first-of-type > content > span')]

    return users


def get_current_username(driver):
    try:
        return driver.find_element(by=By.CSS_SELECTOR,
                                   value='md-menu > a > st-avatar > img').get_property('alt')
    except exceptions.NoSuchElementException:
        return driver.find_element(by=By.CSS_SELECTOR,
                                   value='st-avatar[account="$ctrl.currentAccount"] > img').get_property(
            'alt')

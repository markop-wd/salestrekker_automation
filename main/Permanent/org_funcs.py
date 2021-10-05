from datetime import date
from time import sleep

from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait

from main.Permanent.helper_funcs import element_clicker, element_waiter
from main.Permanent.user_manipulation import get_current_username


# TODO - Rewrite and ensure more stability on this one
# TODO - Write custom exceptions on this one
def org_changer(driver: Chrome, org_name):
    assert "salestrekker" in driver.current_url, 'invalid url'
    assert "authenticate" not in driver.current_url, 'you are at a login page'

    # toolbar_check(driver)

    if not _check_current_org(driver, org_name):
        element_clicker(driver, css_selector='#navBar > div > md-menu > a')
        # TODO - Sandwich click handler (if the screen is narrow)
        element_clicker(driver,
                        css_selector='button[ng-click="::$ctrl.organizationChange($event)"]')

        try:
            WdWait(driver, 15).until(
                ec.visibility_of_element_located(
                    (By.CSS_SELECTOR, "md-dialog[aria-label='Switch organization']")))
        except exceptions.TimeoutException:
            WdWait(driver, 10).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, "body > div > md-dialog")))

        try:
            # TODO - Two sleeps here, find a way to bypass them
            sleep(1)
            driver.find_element(by=By.CSS_SELECTOR,
                                value="input[placeholder='Search for an organization']").send_keys(
                str(org_name))
            sleep(1)

        except exceptions.ElementNotInteractableException:
            # TODO - research alternate way to input the search value here
            # I won't raise the exception because there is a chance to find the organisation
            pass
        except exceptions.NoSuchElementException:
            # If the search input is missing just find it manually
            print('No input search box for Switch Organisation', org_name)

        # TODO - REWRITE
        organisation_names = driver.find_elements(by=By.CSS_SELECTOR,
                                                  value='md-content > div > div > div')
        if not organisation_names:
            print(
                'No organisation with such a name')
            raise ValueError
            # TODO - sensible concurrent agnostic org name picker
            # new_org_name = input("organisation name")
            # if new_org_name.lower() == 'q':
            #     raise Exception
            # else:
            #     org_changer(driver, new_org_name)

        try:
            org_el = driver.find_element(by=By.XPATH,
                                         value=f'//small[text()="{org_name}"]/ancestor::*[position()=1]')
        except exceptions.NoSuchElementException:
            print('No organisation with that exact name', org_name)
            for organisation in organisation_names:
                if str(organisation.find_element(by=By.TAG_NAME,
                                                 value='small').text).lower() == org_name.lower():
                    print('Found the organisation element')
                    _organization_change(driver, organisation, org_name)
                    break
                else:
                    # TODO
                    print('No element with that name')
                    raise ValueError
                    # new_org_name = input("Organisation name")
                    #
                    # if new_org_name.lower() == 'q':
                    #     raise Exception
                    # else:
                    #     org_changer(driver, new_org_name)
        else:
            _organization_change(driver, org_el, org_name)

    # else:
    # print('Already in that organisation, moving on')


def _organization_change(driver: Chrome, org_el: WebElement, org_name: str):
    """
    when the organisation is found click the element and wait for the new organisation to appear
    :return:
    """
    try:
        org_el.click()
    except exceptions.ElementClickInterceptedException:
        driver.execute_script('arguments[0].click();', org_el)
    finally:
        try:
            WdWait(driver, 5).until(ec.title_contains('Organization switch in progress'))
        except exceptions.TimeoutException:
            if not _check_current_org(driver, org_name):
                if input('Failed - do you want to re-initialize the search').lower() in ['yes',
                                                                                         'y']:
                    org_changer(driver, org_name)
                else:
                    raise Exception
                    # driver.quit()
        else:
            # TODO - Add a proper way to wait for the org change instead of the single name wait
            try:
                WdWait(driver, 20).until(ec.title_contains(org_name))
            except exceptions.TimeoutException:
                if not _check_current_org(driver, org_name):
                    org_changer(driver, org_name)


def _check_current_org(driver: Chrome, org_name: str) -> bool:
    element_waiter(driver=driver, css_selector='#navBar', url=driver.current_url)

    try:
        search_input = driver.find_element(by=By.CSS_SELECTOR,
                                           value='md-autocomplete-wrap > input').get_attribute('aria-label')
    except exceptions.NoSuchElementException:
        try:
            driver.find_element(by=By.CSS_SELECTOR, value='button.md-icon-button').click()
        except exceptions.NoSuchElementException:
            raise exceptions.NoSuchElementException(
                'Tried to check the current org, couldnt find the alternative '
                'sandwich clicker.')
        else:
            search_input = driver.find_element(by=By.CSS_SELECTOR,
                                               value='md-autocomplete-wrap > input').get_attribute(
                'aria-label')

    # TODO - Redo this check for organisation names
    first = str("Search " + org_name + " ...").lower()
    second = search_input.lower()
    if first != second:
        return False
    else:
        return True


def organization_create(driver: Chrome, ent, parent_group, ent_group,
                        new_org=f'Test Organization {date.today()}'):
    main_url = "https://" + ent + ".salestrekker.com"
    groups_and_branches_url = main_url + '/settings/groups-and-branches'
    # Go to the main enterprise group
    org_changer(driver, ent_group)

    driver.get(main_url + "/settings/groups-and-branches")
    element_waiter(driver=driver, css_selector='st-organization-groups-and-branches-list > main > md-content > st-list',
                   url=groups_and_branches_url)

    current_user_name = get_current_username(driver)

    add_new_org_button = WdWait(driver, 30).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.primary.md-button.md-ink-ripple')))

    try:
        add_new_org_button.click()
    except exceptions.ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", add_new_org_button)

    WdWait(driver, 20).until(ec.visibility_of_element_located((By.TAG_NAME, 'md-dialog-content')))
    WdWait(driver, 20).until(
        ec.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div > md-input-container > input'))).send_keys(
        new_org)
    WdWait(driver, 20).until(
        ec.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'div > div > md-autocomplete > md-autocomplete-wrap > input'))).send_keys(
        str(current_user_name) + Keys.ENTER)
    # wd_wait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME,
    # 'md-contact-suggestion'))).click()
    driver.find_element(by=By.CSS_SELECTOR, value='md-input-container > md-select').click()
    parent_group_selector = WdWait(driver, 5).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, 'md-select-menu > md-content')))
    sleep(0.1)
    for elemento in parent_group_selector.find_elements(by=By.TAG_NAME,
                                                        value='md-option > div > span'):
        if elemento.text == parent_group:
            elemento.click()

    # input('Test')
    try:
        WdWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'md-dialog-actions > '
                                                                              'button:nth-child(2)'))).click()
    except exceptions.ElementClickInterceptedException:
        driver.execute_script(
            "document.querySelector('md-dialog-actions > button:nth-child(2)').click();")

    WdWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))
    WdWait(driver, 10).until(
        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))

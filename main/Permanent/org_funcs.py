from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from datetime import date
from time import sleep


# TODO - Rewrite and ensure more stability on this one
from main.Permanent.user_manipulation import get_current_username


def org_changer(driver, org_name):
    assert "salestrekker" in driver.current_url, 'invalid url'
    assert "authenticate" not in driver.current_url, 'you are at a login page'

    toolbar_check(driver)

    if not check_current_org(driver, org_name):

        try:
            WdWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#navBar > div > md-menu > a'))).click()

        except exceptions.ElementNotInteractableException:
            driver.execute_script("document.querySelector('#navBar > div > md-menu > a').click();")
        except exceptions.ElementClickInterceptedException:
            driver.execute_script('document.querySelector("#navBar > div > md-menu > a").click();')

        try:
            WdWait(driver, 10).until(ec.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[ng-click="::$ctrl.organizationChange($event)"]'))).click()
        except exceptions.ElementClickInterceptedException:
            driver.execute_script(
                'document.querySelector(\'button[ng-click="::$ctrl.organizationChange($event)"]\').click();')

        try:
            WdWait(driver, 15).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "md-dialog[aria-label='Switch organization']")))
        except exceptions.TimeoutException:
            WdWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "body > div > md-dialog")))
        try:
            # TODO - Two sleeps here, find a way to bypass them
            sleep(1)
            driver.find_element_by_css_selector("input[placeholder='Search for an organization']").send_keys(
                str(org_name))
            sleep(1)

        except exceptions.ElementNotInteractableException:
            # TODO - research alternate way to input the search value here
            pass
            # I won't raise the exception because there is a chance to find the organisation
        except exceptions.NoSuchElementException:
            # If the search input is missing just find it manually
            print('No input search box for Switch Organisation')
            pass

        # TODO - REWRITE
        organisation_names = driver.find_elements_by_css_selector('md-content > div > div > div')
        if not organisation_names:
            print('No organisation with such a name please input the correct name or press Q to quit')

            new_org_name = input("organisation name")
            if new_org_name.lower() == 'q':
                driver.quit()
            else:
                # org_name = new_org_name
                org_changer(driver, new_org_name)
        for element in organisation_names:
            if element.find_element_by_tag_name('small').text.lower() == str(org_name).lower():
                element.click()
                # print('Moving to ', org_name)
                try:
                    WdWait(driver, 5).until(ec.title_contains(('Organization switch in progress')))
                    sleep(2)
                    break
                except exceptions.TimeoutException:
                    if check_current_org(driver, org_name):
                        break
                    else:
                        if input('Failed - do you want to re-initialize the search').lower() == 'yes':
                            org_changer(driver, org_name)
                        else:
                            driver.quit()

            else:
                pass

        # TODO - Cleanup

        try:
            WdWait(driver, 80).until(ec.title_contains(org_name))
            sleep(1)
        except exceptions.TimeoutException:
            driver.quit()
            # TODO - Cleanup
        # print('Org Changer Finished')
    else:
        # print('Already in that organisation, moving on')
        pass


def check_current_org(driver, org_name):

    toolbar_check(driver)

    try:
        search_input = driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
            'aria-label')
    except exceptions.NoSuchElementException:
        try:
            driver.find_element_by_css_selector('button.md-icon-button').click()
        except exceptions.NoSuchElementException:
            raise exceptions.NoSuchElementException('Tried to check the current org, couldnt find the alternative '
                                                    'sandwich clicker.')
        else:
            search_input = driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute('aria-label')

    # TODO - Redo this check for organisation names
    if ("Search " + org_name + " ...") != search_input:
        return False
    else:
        return True


def toolbar_check(driver, wait_time=30):

    # TODO - Tidy this one

    # small function to split nums. into two parts i.e. - 30 into 23 and 7
    longer = wait_time - (wait_time // 4)
    shorter = wait_time - longer

    try:
        WdWait(driver, shorter).until(ec.presence_of_element_located((By.ID, 'navBar')))
    except exceptions.TimeoutException:
        driver.refresh()
        try:
            WdWait(driver, longer).until(ec.presence_of_element_located((By.ID, 'navBar')))
        except exceptions.TimeoutException:
            raise exceptions.TimeoutException('Could not find the navbar via the toolbar_checker')
            # TODO - Cleanup


def organization_create(driver, ent, parent_group, ent_group, new_org=f'Test Organization {date.today()}'):
    from selenium.webdriver.common.keys import Keys

    main_url = "https://" + ent + ".salestrekker.com"

    # Go to the main enterprise group
    org_changer(driver, ent_group)

    driver.get(main_url + "/settings/groups-and-branches")
    try:
        WdWait(driver, 60).until(
            ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))
    except exceptions.TimeoutException:
        driver.get(main_url + "/settings/groups-and-branches")
        try:
            WdWait(driver, 30).until(
                ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))
        except exceptions.TimeoutException:
            driver.get(main_url + "/settings/groups-and-branches")
            try:
                WdWait(driver, 50).until(
                    ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))
            except exceptions.TimeoutException:
                driver.get(main_url + "/settings/groups-and-branches")
                WdWait(driver, 50).until(ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))

    current_user_name = get_current_username(driver)
    WdWait(driver, 30).until(
        ec.element_to_be_clickable((By.CLASS_NAME, 'primary.md-button.md-ink-ripple'))).click()
    WdWait(driver, 20).until(ec.visibility_of_element_located((By.TAG_NAME, 'md-dialog-content')))
    WdWait(driver, 20).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'div > md-input-container > input'))).send_keys(
        new_org)
    WdWait(driver, 20).until(
        ec.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div > div > md-autocomplete > md-autocomplete-wrap > input'))).send_keys(
        str(current_user_name) + Keys.ENTER)
    # wd_wait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME,
    # 'md-contact-suggestion'))).click()
    driver.find_element_by_css_selector('md-input-container > md-select').click()
    parent_group_selector = WdWait(driver, 5).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, 'md-select-menu > md-content')))
    sleep(0.1)
    for elemento in parent_group_selector.find_elements_by_tag_name('md-option > div > span'):
        if elemento.text == parent_group:
            elemento.click()

    # input('Test')
    try:
        WdWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'md-dialog-actions > '
                                                                              'button:nth-child(2)'))).click()
    except exceptions.ElementClickInterceptedException:
        driver.execute_script("document.querySelector('md-dialog-actions > button:nth-child(2)').click();")

    WdWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))
    WdWait(driver, 10).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))

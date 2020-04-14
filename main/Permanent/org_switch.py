from time import sleep
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as wd_wait
from selenium.common import exceptions
from selenium.webdriver.common.by import By


def org_changer(self, org_name):
    sleep(5)
    wd_wait(self.driver, 15).until(ec.visibility_of_element_located((By.TAG_NAME, 'md-content')))
    try:
        self.driver.find_element_by_css_selector('#navBar > div > md-menu > a').click()
    except exceptions.NoSuchElementException:
        self.driver.refresh()
        sleep(15)
        try:
            self.driver.find_element_by_css_selector('#navBar > div > md-menu > a').click()

            self.driver.execute_script('document.querySelector("#navBar > div > md-menu > a").click();')
        except exceptions.NoSuchElementException:
            self.driver.refresh()
            sleep(15)
            self.driver.find_element_by_css_selector('#navBar > div > md-menu > a').click()

        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('document.querySelector("#navBar > div > md-menu > a").click();')

    except exceptions.ElementClickInterceptedException:
        self.driver.execute_script('document.querySelector("#navBar > div > md-menu > a").click();')

    pass
    # TODO - Write a nice exit function here

    try:
        wd_wait(self.driver, 10).until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR, 'body > div > md-menu-content > md-menu-item > button'))).click()
    except exceptions.ElementClickInterceptedException:
        self.driver.execute_script('document.querySelector("body > div > md-menu-content > '
                                   'md-menu-item:nth-child(3) > button").click();')

    wd_wait(self.driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//md-dialog[@aria-label='Switch organization']")))
    self.driver.find_element_by_xpath("//input[@placeholder='Search for an organization']").send_keys(
        org_name)

    sleep(2)
    # TODO - REWRITE
    for element in self.driver.find_elements_by_css_selector('div > small'):
        if element.text.lower() == str(org_name).lower():
            element.find_element_by_xpath("./..").click()
            print('found and clicked', org_name)
            break
        else:
            print('passing over')
            pass
    # self.driver.find_element_by_css_selector('md-content > div > div.layout-wrap.layout-row > div').click()

    # TODO - Write a nice exit function here

    try:
        wd_wait(self.driver, 80).until(ec.title_contains(org_name))
    except exceptions.TimeoutException:
        self.driver.quit()
        # TODO
        # Better exit, find a way to cleanup the Selenium functions
        # Also consider re-running and getting the current position and based on that
    print('Org Changer Finished')

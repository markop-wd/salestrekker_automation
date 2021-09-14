from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait


# TODO - Add assertions that certain elements are in place - this is a good starting point for tests
# TODO - Switch the element clicker for the one in the pattern funcs
# TODO - Make custom exceptions for handling the below

class LogIn:

    def __init__(self, driver: Chrome, ent, email, password):
        self.driver = driver
        self.ent = ent
        self.email = email
        self.password = password
        self.retries = 0

    def log_in_helper(self):
        assert self.driver.current_url == f'https://{self.ent}.salestrekker.com/authenticate'

        try:
            WdWait(self.driver, 15).until(ec.visibility_of_element_located((By.TAG_NAME, "input")))
        except exceptions.TimeoutException:
            self.driver.refresh()
            try:
                WdWait(self.driver, 20).until(
                    ec.visibility_of_element_located((By.TAG_NAME, "input")))
            except exceptions.TimeoutException:
                self.driver.refresh()
                try:
                    WdWait(self.driver, 25).until(
                        ec.visibility_of_element_located((By.TAG_NAME, "input")))
                except exceptions.TimeoutException:
                    print('Salestrekker unresponsive, manual checkup needed')
                    raise exceptions.TimeoutException
                    # self.driver.quit()
                    # TODO - Check Availability and Cleanup

        else:
            try:
                self.driver.find_element(by=By.CSS_SELECTOR,
                                         value='input[ng-model="email"]').send_keys(self.email)
            except exceptions.NoSuchElementException:
                print('No email element?')
            else:
                try:
                    self.driver.find_element(by=By.CSS_SELECTOR,
                                             value='input[ng-model="password"]').send_keys(
                        self.password)
                except exceptions.NoSuchElementException:
                    print('No password elemento?')
                else:
                    self.driver.find_element(by=By.TAG_NAME, value='button').click()

            try:
                WdWait(self.driver, 5).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'span > span.mr1')))
            except exceptions.TimeoutException:
                pass
            else:
                print('Incorrect login information')
                raise exceptions.TimeoutException
                # self.driver.quit()

            try:
                WdWait(self.driver, 10).until(ec.visibility_of_element_located((By.ID, 'navBar')))
            except exceptions.TimeoutException:
                if self.driver.current_url == f'https://{self.ent}.salestrekker.com/authenticate':
                    try:
                        WdWait(self.driver, 5).until(
                            ec.visibility_of_element_located(
                                (By.CSS_SELECTOR, 'input[ng-model="twoFactorCode"]')))
                    except exceptions.TimeoutException:
                        try:
                            WdWait(self.driver, 10).until(
                                ec.visibility_of_element_located((By.ID, 'navBar')))
                        except exceptions.TimeoutException:
                            print('Test')
                            if not self.retries > 1:
                                self.retries += 1
                                self.log_in()
                            else:
                                raise exceptions.TimeoutException
                                # self.driver.quit()
                    else:
                        self.driver.find_element(By.CSS_SELECTOR,
                                                 value='input[ng-model="twoFactorCode"]').send_keys(
                            input(f'Enter the two factor for {self.email} on {self.ent}: '))
                        self.driver.find_element(by=By.TAG_NAME, value='button').click()
                        try:
                            WdWait(self.driver, 15).until(
                                ec.visibility_of_element_located((By.ID, 'navBar')))
                        except exceptions.TimeoutException:
                            if not self.retries > 1:
                                self.retries += 1
                                self.log_in()
                            else:
                                raise exceptions.TimeoutException
                                # self.driver.quit()

    def log_in(self):
        self.driver.get("https://" + self.ent + '.salestrekker.com/authenticate')
        try:
            WdWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.TAG_NAME, 'sign-in')))
        except exceptions.TimeoutException:
            time_increment = 0
            while True:
                self.driver.get("https://" + self.ent + '.salestrekker.com/authenticate')
                if "Authentication" in self.driver.title:
                    break
                elif time_increment > 13:
                    print('Salestrekker unresponsive, manual checkup needed')
                    raise exceptions.TimeoutException
                    # self.driver.quit()
                    # TODO - Check Availability

                # sleep(time_increment)
                try:
                    WdWait(self.driver, time_increment).until(
                        ec.visibility_of_element_located((By.TAG_NAME, 'sign-in')))
                except exceptions.TimeoutException:
                    time_increment += 2
        finally:
            self.log_in_helper()

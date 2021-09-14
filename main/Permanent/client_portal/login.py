from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait


# TODO - Add assertions that certain elements are in place - this is a good starting point for tests
# TODO - Switch the element clicker for the one in the pattern funcs
# TODO - Make custom exceptions for handling the below

class LogIn:

    def __init__(self, driver: Chrome, link: str, pin: str):
        self.driver = driver
        self.link = link
        self.ent = link.split('-')[0].split('/')[-1]
        self.pin = pin
        self.retries = 0

    def log_in_helper(self):
        assert self.driver.title == f'Authenticate | Salestrekker Client Portal'

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

        finally:
            try:
                self.driver.find_element(by=By.CSS_SELECTOR,
                                         value='input[placeholder="PIN code"]').send_keys(self.pin)
            except exceptions.NoSuchElementException:
                print('No PIN element?')
            else:
                self.driver.find_element(by=By.TAG_NAME, value='button').click()

            try:
                WdWait(self.driver, 5).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.bp3-intent-danger')))
            except exceptions.TimeoutException:
                pass
            else:
                print('Incorrect login information')
                raise exceptions.TimeoutException
                # self.driver.quit()

            try:
                WdWait(self.driver, 10).until(
                    ec.visibility_of_element_located((By.CLASS_NAME, 'dashboard')))
            except exceptions.TimeoutException:
                if self.driver.current_url != f'https://{self.ent}-cp.salestrekker.com/dashboard':

                    try:
                        WdWait(self.driver, 15).until(
                            ec.visibility_of_element_located((By.CLASS_NAME, 'dashboard')))
                    except exceptions.TimeoutException:
                        # TODO - Privacy YES/NO handler
                        print('No dashboard')
                        if not self.retries > 1:
                            self.retries += 1
                            self.log_in()
                        else:
                            raise exceptions.TimeoutException
                            # self.driver.quit()

    def log_in(self):
        self.driver.get(self.link)
        # self.driver.get("https://" + self.ent + '-cp.salestrekker.com/authenticate')
        try:
            WdWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, 'div#root')))
        except exceptions.TimeoutException:
            time_increment = 0
            while True:
                self.driver.get(self.link)
                if "Authenticate" in self.driver.title:
                    break
                elif time_increment > 13:
                    print('Salestrekker unresponsive, manual checkup needed')
                    raise exceptions.TimeoutException
                    # TODO - Check Availability

                # sleep(time_increment)
                try:
                    WdWait(self.driver, time_increment).until(
                        ec.visibility_of_element_located((By.TAG_NAME, 'div#root')))
                except exceptions.TimeoutException:
                    time_increment += 2
        finally:
            self.log_in_helper()

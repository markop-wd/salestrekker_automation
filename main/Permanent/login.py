from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from time import sleep


class LogIn:

    def __init__(self, driver, ent, email, password):
        self.driver = driver
        self.ent = ent
        self.email = email
        self.password = password
        self.retries = 0
        pass

    def log_in_helper(self):
        try:
            WdWait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
        except exceptions.TimeoutException:
            self.driver.refresh()
            try:
                WdWait(self.driver, 15).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
            except exceptions.TimeoutException:
                self.driver.refresh()
                try:
                    WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
                except exceptions.TimeoutException:
                    print('Salestrekker unresponsive, manual checkup needed')
                    self.driver.quit()
                    # TODO - Check Availability and Cleanup

        # TODO - Unknown exception^

        else:
            input_elements = self.driver.find_elements_by_tag_name('input')
            for log_input in input_elements:
                if log_input.get_attribute('placeholder') == 'Your E-Mail':
                    log_input.send_keys(self.email)
                    continue
                elif log_input.get_attribute('placeholder') == 'Your Password':
                    log_input.send_keys(self.password)
                    continue
                else:
                    continue

            self.driver.find_element_by_tag_name('button').click()

    def log_in(self):
        self.driver.get("https://" + self.ent + '.salestrekker.com/authenticate')
        try:
            WdWait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'sign-in')))
        except exceptions.TimeoutException:
            time_increment = 0
            while True:
                self.driver.get("https://" + self.ent + '.salestrekker.com/authenticate')
                if "Authentication" in self.driver.title:
                    break
                elif time_increment > 13:
                    print('Salestrekker unresponsive, manual checkup needed')
                    self.driver.quit()
                    # TODO - Check Availability and Cleanup

                sleep(time_increment)
                try:
                    WdWait(self.driver, time_increment).until(ec.presence_of_element_located((By.TAG_NAME, 'sign-in')))
                except exceptions.TimeoutException:
                    time_increment += 2

        self.log_in_helper()

        try:
            WdWait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'navBar')))
        except exceptions.TimeoutException:
            if not self.retries > 1:
                self.log_in()
            else:
                self.driver.quit()


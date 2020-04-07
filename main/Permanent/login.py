from selenium.webdriver.support.wait import WebDriverWait as wd_wait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
import time


def login(self, email, password):
    try:
        wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "input_0"))).send_keys(email)
    # TODO - REWRITE SO HE CAN RECOGNIZE IF ANYTHING IS LOADED AND THEN PROCEED - RATHER THAN WAITING AROUND FOR A
    #  SPECIFIC AND IF NOT THEN PROCEEDING
    except exceptions.TimeoutException:
        inputs = self.driver.find_elements_by_tag_name('input')
        for element in inputs:
            if element.get_attribute('placeholder') == 'Your E-Mail':
                element.send_keys(email)
            elif element.get_attribute('placeholder') == 'Your Password':
                element.send_keys(password)
            else:
                continue
        self.driver.find_element_by_tag_name('button').click()
        time.sleep(5)
    else:
        self.driver.find_element_by_id('input_1').send_keys(password)
        self.driver.find_element_by_tag_name('button').click()


def main_func(self):
    self.driver.get(self.main_url + '/authenticate')

    try:
        assert "Authentication" in self.driver.title
    except AssertionError:
        time_increment = 0
        while True:
            self.driver.get(self.main_url + '/authenticate')
            time.sleep(time_increment)
            time_increment += 1
            if "Authentication" in self.driver.title:
                break
            elif time_increment > 8:
                # find a way to check the availability of the service in this case
                print('Salestrekker unresponsive, manual checkup needed')
                self.driver.quit()

    self.login(self.email, self.password)

    try:
        wd_wait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'board')))
    except exceptions.TimeoutException:
        while True:
            self.driver.get(self.main_url + '/authenticate')
            try:
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "input_0"))).send_keys(
                    self.email)
            except exceptions.TimeoutException:
                inputs = self.driver.find_elements_by_tag_name('input')
                for element in inputs:
                    if element.get_attribute('placeholder') == 'Your E-Mail':
                        element.send_keys(self.email)
                    elif element.get_attribute('placeholder') == 'Your Password':
                        element.send_keys(self.password)
                    else:
                        continue
            self.driver.find_element_by_id('input_1').send_keys(self.password)
            self.driver.find_element_by_tag_name('button').click()
            wd_wait(self.driver, 15).until(By.ID, 'board')

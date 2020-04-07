from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as wd_wait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import time
import random
import datetime

ents = ['vownet', 'ioutsource', 'ynet', 'nlgconnect', 'platform', 'chief', 'sfg']
dev_main_org = '# Salestrekker Enterprise'
vow_main_org = 'Vow Financial Pty Ltd'
iot_main_org = 'outsource financial pty ltd'
ynet_main_org = 'Yellow Brick Road Finance Pty Limited'
nlg_main_org = '# NLG Connect'
ptf_main_org = '# Platform Connect'
chief_main_org = 'Chief'
gem_main_org = 'Astute Financial Management Pty Ltd'
gemnz_main_org = 'Gem New Zealand'
sfg_main_org = 'Specialist Finance Group'
app_main_org = '3 Demo N Co'
user = 'matthew+0406@salestrekker.com'
options = Options()
# options.headless = True

print(time.time())


class TestInitializer:

    def __init__(self, ent='dev', email='matthew@salestrekker.com', password='',
                 new_org_name=f'Test Organisation {datetime.date.today()}', group=''):
        self.ent = ent
        self.main_url = 'https://' + ent + '.salestrekker.com'
        self.driver = Firefox(executable_path=GeckoDriverManager().install(), options=options)
        # self.driver = Chrome(ChromeDriverManager().install())
        self.email = email
        self.password = password
        self.new_org_name = new_org_name
        self.document_list = []
        self.workflow_list = []
        self.current_user_name = ''
        self.group = group
        self.hl_workflow_name = 'Test Automation Workflow'

    def login(self, email, password):
        try:
            wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "input_0"))).send_keys(email)
            self.driver.find_element_by_id('input_1').send_keys(password)
            self.driver.find_element_by_tag_name('button').click()
        # TODO - REWRITE SO HE CAN RECOGNIZE IF ANYTHING IS LOADED
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
        self.go_to_main_org()

#TODO - Rewrite so that there is only one function taking in the self.ent parameter

    def go_to_main_org(self):

        if self.ent == 'vownet':
            if 'Vow Financial Pty Ltd' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in_main_org')
            else:
                self.org_changer(vow_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(vow_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif self.ent == 'ynet':
            if 'Yellow Brick Road Finance Pty Limited' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(ynet_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(ynet_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif self.ent == 'gem':
            if 'Astute Financial Management Pty Ltd' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(gem_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(gem_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif self.ent == 'gemnz':
            if 'Yellow Brick Road Finance Pty Limited' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(gemnz_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(gemnz_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif self.ent == 'app':
            if '3 Demo N Co' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(app_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(app_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif self.ent == 'nlgconnect':
            if '# NLG Connect' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(nlg_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(nlg_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif self.ent == 'platform':
            if '# Platform Connect' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(ptf_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(ptf_main_org)

            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif self.ent == 'chief':
            if 'Chief' in str(self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                    'aria-label')):
                print('in main org')
            else:
                self.org_changer(chief_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(chief_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif self.ent == 'ioutsource':
            if 'outsource financial pty ltd' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(iot_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(iot_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif self.ent == 'sfg':
            if 'Specialist Finance Group' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(sfg_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(sfg_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

        elif 'dev' in self.driver.current_url:
            if dev_main_org in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(dev_main_org)

            self.document_get()
            self.workflow_get()
            self.org_changer(dev_main_org)
            self.organization_create(group=self.group, new_org=self.new_org_name)
            self.driver.get(self.main_url + '/authenticate')
            wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
            self.login(self.email, self.password)
            self.org_changer(self.new_org_name)
            self.document_compare()
            self.workflow_compare()
            self.add_user()
            self.add_hl_workflow()

    def org_changer(self, org_name):
        time.sleep(5)
        wd_wait(self.driver, 15).until(ec.visibility_of_element_located((By.TAG_NAME, 'md-content')))
        try:
            self.driver.find_element_by_css_selector('#navBar > div > md-menu > a').click()
        except exceptions.NoSuchElementException:
            self.driver.refresh()
            time.sleep(15)
            try:
                self.driver.find_element_by_css_selector('#navBar > div > md-menu > a').click()

                self.driver.execute_script('document.querySelector("#navBar > div > md-menu > a").click();')
            except exceptions.NoSuchElementException:
                self.driver.refresh()
                time.sleep(15)
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

        time.sleep(2)
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

    def document_get(self):
        # TODO - LABEL

        if self.group in self.driver.current_url:
            pass
        else:
            self.org_changer(self.group)

        self.document_list = []
        self.driver.get(self.main_url + '/settings/documents')
        try:
            wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        except exceptions.TimeoutException:
            self.driver.get(self.main_url + '/settings/documents')
            try:
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
            except exceptions.TimeoutException:
                self.driver.get(self.main_url + '/settings/documents')
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))

        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        # print(last_height)
        time.sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            time.sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            self.document_list.append(document.find_element_by_css_selector('a > content > span').text)

        time.sleep(8)

    def document_compare(self):
        new_org_document_list = []
        self.driver.get(self.main_url + '/settings/documents')
        wd_wait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        # print('before compare scrolling')
        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        # print(last_height)
        time.sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            time.sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            new_org_document_list.append(document.find_element_by_css_selector('a > content > span').text)

        if new_org_document_list == self.document_list:
            print('Documents good')
        else:
            print("Following documents weren't inherited")
            [print(documentino) for documentino in self.document_list if documentino not in new_org_document_list]
        time.sleep(8)

    def workflow_get(self):

        if self.group in self.driver.current_url:
            pass
        else:
            self.org_changer(self.group)

        self.driver.get(self.main_url + '/settings/workflows')
        wd_wait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        # print('before scrolling')
        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        # print(last_height)
        time.sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            time.sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            self.workflow_list.append(document.find_element_by_css_selector('a > span').text)

    def workflow_compare(self):
        new_workflow_list = []
        self.driver.get(self.main_url + '/settings/workflows')
        wd_wait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        # print('before compare scrolling')
        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        # print(last_height)
        time.sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            time.sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            new_workflow_list.append(document.find_element_by_css_selector('a > span').text)

        if not bool(set(self.workflow_list).difference(new_workflow_list)):
            print('Workflows good')
        else:
            print("Following workflows weren't inherited")
            [print(workflowino) for workflowino in self.workflow_list if workflowino not in new_workflow_list]
        time.sleep(8)

    def add_hl_workflow(self):
        self.driver.get(self.main_url + "/settings/workflow/0")
        try:
            wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
        except exceptions.TimeoutException:
            self.driver.get(self.main_url + "/settings/workflow/0")
            try:
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
            except exceptions.TimeoutException:
                self.driver.get(self.main_url + "/settings/workflow/0")
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))

        self.current_user_name = self.driver.find_element_by_css_selector('div > st-avatar > img').get_attribute('alt')
        for count, input_el in enumerate(
                self.driver.find_elements_by_css_selector('st-block-form-content > div input')):
            if count == 0:
                input_el.send_keys(self.hl_workflow_name)
            if count == 1:
                input_el.send_keys('AutoTest WF')
            if count == 2:
                input_el.send_keys(self.current_user_name + Keys.ENTER)
                time.sleep(1)
                input_el.send_keys('Test Surname' + Keys.ENTER)

        self.driver.find_element_by_css_selector('st-block-form-content >div >div:nth-child(4)').click()

        type_list = wd_wait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'body > div > md-select-menu '
                                                             '> md-content')))

        for wf_type in type_list.find_elements_by_tag_name('md-option'):
            if wf_type.find_element_by_css_selector('div > span').text == 'Home Loan':
                wf_type.click()
                time.sleep(5)
                break

        new_stages = random.randint(0, 5)
        while new_stages > 0:
            self.driver.find_element_by_css_selector('span > button').click()
            new_stages -= 1

        number_of_stages = len(self.driver.find_elements_by_css_selector('st-block:nth-child(2) > '
                                                                         'st-block-form-content main'))

        time.sleep(5)

        self.driver.get(self.main_url + "/settings/workflows")

        try:
            wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
        except exceptions.TimeoutException:
            self.driver.get(self.main_url + "/settings/workflow/0")
            try:
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
            except exceptions.TimeoutException:
                self.driver.get(self.main_url + "/settings/workflow/0")
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))

        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        print(last_height)
        time.sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            time.sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for elel in self.driver.find_elements_by_css_selector('st-list-item > a > span'):
            if elel.text == self.hl_workflow_name:
                nav_url = self.main_url + "/board/" + \
                          str(elel.find_element_by_xpath('./..').get_attribute('href')).split('/')[-1]
                self.driver.get(nav_url)
                break

        try:
            wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.ID, 'board')))
        except exceptions.TimeoutException:
            self.driver.get(nav_url)
            try:
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.ID, 'board')))
            except exceptions.TimeoutException:
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.ID, 'board')))

        if number_of_stages == len(self.driver.find_elements_by_css_selector('#board > stage ')):
            print('all good with stage and HL WF adding')
        else:
            print('diff between expected and actual is ',
                  number_of_stages - len(self.driver.find_elements_by_css_selector('#board > stage')))

    def add_user(self):
        self.driver.get(self.main_url + '/settings/users')
        try:
            wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-accounts-list')))
        except exceptions.TimeoutException:
            self.driver.get(self.main_url + '/settings/users')
            wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-accounts-list')))

        self.driver.find_element_by_css_selector('span > button').click()
        wd_wait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'span > button')))
        self.driver.find_element_by_css_selector('div:nth-child(1) > md-input-container > input').send_keys(user)
        self.driver.find_element_by_css_selector(
            'div:nth-child(2) > md-input-container:nth-child(1) > input').send_keys('Test')
        self.driver.find_element_by_css_selector(
            'div:nth-child(2) > md-input-container:nth-child(2) > input').send_keys('Surname')

        try:
            wd_wait(self.driver, 10).until(ec.element_to_be_clickable(
                (By.CSS_SELECTOR, 'md-dialog-actions > button:nth-child(2)'))).click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('document.querySelector("md-dialog-actions > button:nth-child(2)").click();')
        time.sleep(5)
        print('add user good')
        pass

    def duplicate_hl_wf(self):
        self.driver.get(self.main_url + "/settings/workflows")
        try:
            wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
        except exceptions.TimeoutException:
            self.driver.get(self.main_url + "/settings/workflows")
            try:
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
            except exceptions.TimeoutException:
                self.driver.get(self.main_url + "/settings/workflows")
                wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))

        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        # print(last_height)
        time.sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            time.sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for elel in self.driver.find_elements_by_css_selector('st-list-item > a > span'):
            if elel.text == self.hl_workflow_name:
                elel.find_element_by_xpath('')
                nav_url = self.main_url + "/board/" + \
                          str(elel.find_element_by_xpath('./..').get_attribute('href')).split('/')[-1]

                break

        # self.hl_workflow_name
        pass

    def organization_create(self, group, new_org='Test Organization 2020-03-31'):
        self.driver.get(self.main_url + "/settings/groups-and-branches")
        try:
            wd_wait(self.driver, 60).until(
                ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))
        except exceptions.TimeoutException:
            self.driver.get(self.main_url + "/settings/groups-and-branches")
            try:
                wd_wait(self.driver, 30).until(
                    ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))
            except exceptions.TimeoutException:
                self.driver.get(self.main_url + "/settings/groups-and-branches")
                try:
                    wd_wait(self.driver, 50).until(
                        ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))
                except exceptions.TimeoutException:
                    self.driver.get(self.main_url + "/settings/groups-and-branches")
                    wd_wait(self.driver, 50).until(ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))

        self.current_user_name = self.driver.find_element_by_css_selector('div > st-avatar > img').get_attribute('alt')
        print(self.current_user_name)
        wd_wait(self.driver, 30).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'primary.md-button.md-ink-ripple'))).click()
        wd_wait(self.driver, 20).until(ec.visibility_of_element_located((By.TAG_NAME, 'md-dialog-content')))
        wd_wait(self.driver, 20).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'div > md-input-container > input'))).send_keys(
            new_org)
        wd_wait(self.driver, 20).until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div > div > md-autocomplete > md-autocomplete-wrap > input'))).send_keys(
            str(self.current_user_name) + Keys.ENTER)
        # wd_wait(self.driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME,
        # 'md-contact-suggestion'))).click()
        self.driver.find_element_by_css_selector('md-input-container > md-select').click()
        wd_wait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'md-select-menu > md-content')))
        for elemento in self.driver.find_elements_by_tag_name('md-option'):
            if elemento.find_element_by_tag_name(
                    'span').text == group:
                elemento.click()
        wd_wait(self.driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'md-dialog-actions > '
                                                                                    'button:nth-child(2)'))).click()
        time.sleep(10)
        pass

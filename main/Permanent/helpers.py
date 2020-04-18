from selenium.webdriver.support.wait import WebDriverWait as wd_wait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from time import sleep

from datetime import date


def org_changer(driver, org_name):
    assert "salestrekker" in driver.current_url, 'invalid url'
    assert "authenticate" not in driver.current_url, 'you are at a login page'

    toolbar_check(driver)

    if not check_current_org(driver, org_name):

        try:
            driver.find_element_by_css_selector('#navBar > div > md-menu > a').click()
        except exceptions.NoSuchElementException:
            # At this point there is no reason that the profile icon isn't there except that the screen is narrow
            # TODO - Write a sandwich clicker and org changer from there
            pass

        except exceptions.ElementClickInterceptedException:
            driver.execute_script('document.querySelector("#navBar > div > md-menu > a").click();')

        try:
            wd_wait(driver, 10).until(ec.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[ng-click="::$ctrl.organizationChange($event)"]'))).click()
        except exceptions.ElementClickInterceptedException:
            driver.execute_script(
                'document.querySelector(\'button[ng-click="::$ctrl.organizationChange($event)"]\').click();')

        try:
            wd_wait(driver, 15).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "md-dialog[aria-label='Switch organization']")))
        except exceptions.TimeoutException:
            wd_wait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "body > div > md-dialog")))
        try:
            driver.find_element_by_css_selector("input[placeholder='Search for an organization']").send_keys(
                org_name)
        except exceptions.ElementNotInteractableException:
            # No idea what to do here
            # TODO - research alternate way to input the search value here
            pass
            # I won't raise the exception because there is a chance to find the organization
        except exceptions.NoSuchElementException:
            # If the search input is missing just find it manually
            print('No input search box for Switch organization')
            pass

        # TODO - REWRITE
        organization_names = driver.find_elements_by_css_selector('md-content > div > div > div')
        if not organization_names:
            print('No organization with such a name please input the correct name or press Q to quit')

            new_org_name = input("organization name")
            if new_org_name.lower() == 'q':
                driver.quit()
            else:
                # org_name = new_org_name
                org_changer(driver, new_org_name)

        for element in organization_names:
            if element.find_element_by_tag_name('small').text.lower() == str(org_name).lower():
                element.click()
                print('found and clicked', org_name)

                osidjfoiajdsoifadsf
                # TODO - Fix the organisation checker

                sdnjoafijsdiofjoiasdjfoi
                try:
                    wd_wait(driver, 10).until(ec.title_contains(('organization switch in progress')))
                except exceptions.TimeoutException:
                    if check_current_org(driver, org_name):
                        break
                    else:
                        if input('Failed - do you want to re-initialize the search').lower() == 'yes':
                            org_changer(driver, org_name)
                        else:
                            driver.quit()

            else:
                print('passing over')

        # TODO - Cleanup

        try:
            wd_wait(driver, 80).until(ec.title_contains(org_name))
        except exceptions.TimeoutException:
            driver.quit()
            # TODO - Cleanup
        print('Org Changer Finished')
    else:
        print('Already in that organization, moving on')
        pass


# helper for OrgChanger to check if you are already in that organization
def check_current_org(driver, org_name):
    try:
        search_input = driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
            'aria-label')
    except exceptions.NoSuchElementException:
        driver.refresh()
        try:
            wd_wait(driver, 15).until(ec.presence_of_element_located((By.TAG_NAME, 'st-toolbar')))
        except exceptions.TimeoutException:
            raise exceptions.TimeoutException
        else:
            search_input = driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                'aria-label')

    if (org_name not in search_input) or (org_name not in driver.title):
        return False
    else:
        return True


def toolbar_check(driver, wait_time=30):
    # TODO - Tidy this one

    # small function to split nums. into two parts i.e. - 30 into 23 and 7
    longer = wait_time - (wait_time // 4)

    try:
        wd_wait(driver, wait_time - longer).until(ec.presence_of_element_located((By.TAG_NAME, 'st-toolbar')))
    except exceptions.TimeoutException:
        driver.refresh()
        try:
            wd_wait(driver, longer).until(ec.presence_of_element_located((By.TAG_NAME, 'st-toolbar')))
        except exceptions.TimeoutException:
            raise exceptions.TimeoutException
            # driver.quit()
            # TODO - Cleanup


class LogIn:

    def __init__(self, driver, ent, email, password):
        self.driver = driver
        self.ent = ent
        self.email = email
        self.password = password
        pass

    def log_in_helper(self):
        try:
            wd_wait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
        except exceptions.TimeoutException:
            self.driver.refresh()
            try:
                wd_wait(self.driver, 15).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
            except exceptions.TimeoutException:
                self.driver.refresh()
                try:
                    wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
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
            wd_wait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'sign-in')))
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
                    wd_wait(self.driver, time_increment).until(ec.presence_of_element_located((By.TAG_NAME, 'sign-in')))
                except exceptions.TimeoutException:
                    time_increment += 2

        self.log_in_helper()

        try:
            wd_wait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'board')))
        except exceptions.TimeoutException:
            while True:
                self.log_in_helper()
                wd_wait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'board')))
                self.driver.quit()
                # TODO - Create an exit function out of here


class DocumentCheck:

    def __init__(self, driver, ent):
        self.driver = driver
        self.document_list = []
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.parent_org = ''
        self.child_org = ''

    def document_get(self, org):
        # TODO - LABEL

        self.parent_org = org

        if org in self.driver.title:
            pass
        else:
            org_changer(self.driver, org)

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
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            self.document_list.append(document.find_element_by_css_selector('a > content > span').text)

    def document_compare(self, org):

        self.child_org = org

        if org in self.driver.title:
            pass
        else:
            org_changer(self.driver, org)

        new_document_list = []
        self.driver.get(self.main_url + '/settings/documents')
        wd_wait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        # print('before compare scrolling')
        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        # print(last_height)
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            new_document_list.append(document.find_element_by_css_selector('a > content > span').text)

        if not bool(set(self.document_list).difference(new_document_list)):
            print(f'Documents good from {self.parent_org} >> {self.child_org}')
        else:
            print(f'Documents bad from {self.parent_org} >> {self.child_org}')
            not_inherited = []
            for documentino in self.document_list:
                if documentino not in new_document_list:
                    not_inherited.append(('  ' + documentino + '\n'))

            with open(f"document_inheritance {date.today()}.txt", "a+") as doc_inherit:
                doc_inherit.write(
                    'From >> ' + self.parent_org + ' >> to >> ' + self.child_org + ' the following document weren\'t inherited \n')
                doc_inherit.writelines(not_inherited)
                doc_inherit.write('\n')
        sleep(8)


class WorkflowCheck:

    def __init__(self, driver, ent):
        self.driver = driver
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.parent_org = ''
        self.child_org = ''
        self.workflow_list = []

    def workflow_get(self, org):

        self.parent_org = org

        if org in self.driver.title:
            pass
        else:
            org_changer(self.driver, org)

        self.driver.get(self.main_url + '/settings/workflows')
        wd_wait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        # print('before scrolling')
        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        # print(last_height)
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            self.workflow_list.append(document.find_element_by_css_selector('a > span').text)

    def workflow_compare(self, org):

        if org in self.driver.title:
            pass
        else:
            org_changer(self.driver, org)

        new_workflow_list = []
        self.driver.get(self.main_url + '/settings/workflows')
        wd_wait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        # print('before compare scrolling')
        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        # print(last_height)
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            new_workflow_list.append('  ' + document.find_element_by_css_selector('a > span').text + '\n')

        if not bool(set(self.workflow_list).difference(new_workflow_list)):
            print(f'Workflows good from {self.parent_org} >> {self.child_org}')
        else:
            print(f'Workflows bad from {self.parent_org} >> {self.child_org}')
            not_inherited = []
            for workflow in self.workflow_list:
                if workflow not in new_workflow_list:
                    not_inherited.append(('  ' + workflow + '\n'))

            with open(f"workflow_inheritance {date.today()}.txt", "a+") as wf_inherit:
                wf_inherit.write(
                    'From >> ' + self.parent_org + ' >> to >> ' + self.child_org + ' the following workflows weren\'t inherited \n')
                wf_inherit.writelines(not_inherited)
                wf_inherit.write('\n')
        sleep(8)


def organization_create(driver, ent, group, new_org_name=f'Test organization {date.today()}'):
    from selenium.webdriver.common.keys import Keys

    main_url = "https://" + ent + ".salestrekker.com"

    driver.get(main_url + "/settings/groups-and-branches")
    try:
        wd_wait(driver, 60).until(
            ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))
    except exceptions.TimeoutException:
        driver.get(main_url + "/settings/groups-and-branches")
        try:
            wd_wait(driver, 30).until(
                ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))
        except exceptions.TimeoutException:
            driver.get(main_url + "/settings/groups-and-branches")
            try:
                wd_wait(driver, 50).until(
                    ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))
            except exceptions.TimeoutException:
                driver.get(main_url + "/settings/groups-and-branches")
                wd_wait(driver, 50).until(ec.invisibility_of_element_located((By.TAG_NAME, 'st-progressbar')))

    current_user_name = driver.find_element_by_css_selector('div > st-avatar > img').get_attribute('alt')
    print(current_user_name)
    wd_wait(driver, 30).until(
        ec.element_to_be_clickable((By.CLASS_NAME, 'primary.md-button.md-ink-ripple'))).click()
    wd_wait(driver, 20).until(ec.visibility_of_element_located((By.TAG_NAME, 'md-dialog-content')))
    wd_wait(driver, 20).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'div > md-input-container > input'))).send_keys(
        new_org_name)
    wd_wait(driver, 20).until(
        ec.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div > div > md-autocomplete > md-autocomplete-wrap > input'))).send_keys(
        str(current_user_name) + Keys.ENTER)
    # wd_wait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME,
    # 'md-contact-suggestion'))).click()
    driver.find_element_by_css_selector('md-input-container > md-select').click()
    wd_wait(driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'md-select-menu > md-content')))
    for elemento in driver.find_elements_by_tag_name('md-option'):
        if elemento.find_element_by_tag_name(
                'span').text == group:
            elemento.click()
    wd_wait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'md-dialog-actions > '
                                                                           'button:nth-child(2)'))).click()
    sleep(10)
    pass


def add_hl_workflow(self):
    import random
    from selenium.webdriver.common.keys import Keys

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
            sleep(1)
            input_el.send_keys('Test Surname' + Keys.ENTER)

    self.driver.find_element_by_css_selector('st-block-form-content >div >div:nth-child(4)').click()

    type_list = wd_wait(self.driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'body > div > md-select-menu '
                                                         '> md-content')))

    for wf_type in type_list.find_elements_by_tag_name('md-option'):
        if wf_type.find_element_by_css_selector('div > span').text == 'Home Loan':
            wf_type.click()
            sleep(5)
            break

    new_stages = random.randint(0, 5)
    while new_stages > 0:
        self.driver.find_element_by_css_selector('span > button').click()
        new_stages -= 1

    number_of_stages = len(self.driver.find_elements_by_css_selector('st-block:nth-child(2) > '
                                                                     'st-block-form-content main'))

    sleep(5)

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
    sleep(1)
    while True:
        self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
        sleep(3)
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

# def add_user(self):
#     self.driver.get(self.main_url + '/settings/users')
#     try:
#         wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-accounts-list')))
#     except exceptions.TimeoutException:
#         self.driver.get(self.main_url + '/settings/users')
#         wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-accounts-list')))
#
#     self.driver.find_element_by_css_selector('span > button').click()
#     wd_wait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'span > button')))
#     self.driver.find_element_by_css_selector('div:nth-child(1) > md-input-container > input').send_keys(user)
#     self.driver.find_element_by_css_selector(
#         'div:nth-child(2) > md-input-container:nth-child(1) > input').send_keys('Test')
#     self.driver.find_element_by_css_selector(
#         'div:nth-child(2) > md-input-container:nth-child(2) > input').send_keys('Surname')
#
#     try:
#         wd_wait(self.driver, 10).until(ec.element_to_be_clickable(
#             (By.CSS_SELECTOR, 'md-dialog-actions > button:nth-child(2)'))).click()
#     except exceptions.ElementClickInterceptedException:
#         self.driver.execute_script('document.querySelector("md-dialog-actions > button:nth-child(2)").click();')
#     sleep(5)
#     print('add user good')
#     pass


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
    sleep(1)
    while True:
        self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
        sleep(3)
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

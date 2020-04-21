from selenium.webdriver.support.wait import WebDriverWait as wd_wait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from time import sleep


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
            sleep(1)
            driver.find_element_by_css_selector("input[placeholder='Search for an organization']").send_keys(
                str(org_name))
            sleep(1)

        except exceptions.ElementNotInteractableException:
            # No idea what to do here
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
                print('Moving to ', org_name)
                try:
                    wd_wait(driver, 5).until(ec.title_contains(('Organization switch in progress')))
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
            wd_wait(driver, 80).until(ec.title_contains(org_name))
        except exceptions.TimeoutException:
            driver.quit()
            # TODO - Cleanup
        # print('Org Changer Finished')
    else:
        print('Already in that organisation, moving on')
        pass


# helper for OrgChanger to check if you are already in that organisation
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
                wd_wait(self.driver, 15).until(By.ID, 'board')
                self.driver.quit()
                # TODO - Create an exit function out of here


class DocumentCheck:

    def __init__(self, driver, ent, time):
        self.ent = ent
        self.driver = driver
        self.document_list = []
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.parent_org = ''
        self.child_org = ''
        self.time = time

    def document_get(self, org):
        # TODO - LABEL

        self.parent_org = org

        if org in self.driver.current_url:
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

        if org in self.driver.current_url:
            pass
        else:
            org_changer(self.driver, org)

        new_org_document_list = []
        self.driver.get(self.main_url + '/settings/documents')
        wd_wait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        md_content = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", md_content)
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", md_content)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", md_content)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            new_org_document_list.append(document.find_element_by_css_selector('a > content > span').text)

        # This got really convoluted in order to account for both from parent to child and reverse cases.
        # TODO - Check if there is an easier way to handle this
        if not set(new_org_document_list).symmetric_difference(set(self.document_list)):
            with open(f"InfoFolder/{self.ent} {self.time} document_inheritance.txt", "a+") as doc_inherit:
                doc_inherit.write(
                    'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' no disrepancies noted between documents\n')
        else:
            not_inherited = []

            for documentino in self.document_list:
                if documentino not in new_org_document_list:
                    not_inherited.append('  ' + documentino + '\n')

            if not_inherited:
                with open(f"InfoFolder/{self.ent} {self.time} document_inheritance.txt", "a+") as doc_inherit:
                    doc_inherit.write(
                        'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' the following wasn\'t inherited\n')
                    doc_inherit.writelines(not_inherited)

            not_inherited = []

            for documentino in new_org_document_list:
                if documentino not in self.document_list:
                    not_inherited.append(' ' + documentino + '\n')

            if not_inherited:
                with open(f"InfoFolder/{self.ent} {self.time} document_inheritance.txt", "a+") as doc_inherit:
                    doc_inherit.write(self.main_url + ' - ' + "Documents are present in the child org " + self.child_org + ' that are not present in the parent org ' + self.parent_org + ' the following is \'extra\'\n')
                    doc_inherit.writelines(not_inherited)

        sleep(8)


class WorkflowCheck:

    def __init__(self, driver, ent, time):
        self.driver = driver
        self.ent = ent
        self.workflow_list = []
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.parent_org = ''
        self.child_org = ''
        self.time = time

    def workflow_get(self, org):

        self.parent_org = org

        if org in self.driver.current_url:
            pass
        else:
            org_changer(self.driver, org)

        self.driver.get(self.main_url + '/settings/workflows')
        wd_wait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        md_content = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", md_content)
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", md_content)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", md_content)

            if new_height == last_height:
                break
            last_height = new_height

        for document in self.driver.find_elements_by_tag_name('st-list-item'):
            self.workflow_list.append(document.find_element_by_css_selector('a > span').text)

    def workflow_compare(self, org):

        self.child_org = org

        if org in self.driver.current_url:
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
            new_workflow_list.append(document.find_element_by_css_selector('a > span').text)

        if not set(self.workflow_list).symmetric_difference(set(new_workflow_list)):
            with open(f"InfoFolder/{self.ent} {self.time} workflow_inheritance.txt", "a+") as wf_inherit:
                wf_inherit.write(
                    'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' no disrepancies noted between workflows\n')
        else:
            not_inherited = []
            for workflowino in self.workflow_list:
                if workflowino not in new_workflow_list:
                    not_inherited.append('  ' + workflowino + '\n')

            if not_inherited:
                with open(f"InfoFolder/{self.ent} {self.time} workflow_inheritance.txt", "a+") as wf_inherit:
                    wf_inherit.write('From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' the following wasn\'t inherited\n')
                    wf_inherit.writelines(not_inherited)

            not_inherited = []

            for worklofino in new_workflow_list:
                if worklofino not in self.workflow_list:
                    not_inherited.append(' ' + worklofino + '\n')

            if not_inherited:
                with open(f"InfoFolder/{self.ent} {self.time} workflow_inheritance.txt", "a+") as wf_inherit:
                    wf_inherit.write(self.main_url + ' - ' + "Workflows are present in the child org " + self.child_org + ' that are not present in the parent org ' + self.parent_org + ' the following is \'extra\'\n')
                    wf_inherit.writelines(not_inherited)
        sleep(8)

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
            driver.find_element_by_css_selector("input[placeholder='Search for an organization']").send_keys(
                org_name)
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
                print('found and clicked', org_name)
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
                print('passing over')

        # TODO - Cleanup

        try:
            wd_wait(driver, 80).until(ec.title_contains(org_name))
        except exceptions.TimeoutException:
            driver.quit()
            # TODO - Cleanup
        print('Org Changer Finished')
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

    def __init__(self, driver, ent):
        self.driver = driver
        self.document_list = []
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.parent_org = ''
        self.child_org = ''

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
            new_org_document_list.append(document.find_element_by_css_selector('a > content > span').text)

        if new_org_document_list == self.document_list:
            print('Documents good')
        else:
            not_inherited = []
            for documentino in self.document_list:
                if documentino not in new_org_document_list:
                    not_inherited.append(('  ' + documentino + '\n'))

            with open("document_inheritance.txt", "rw+") as doc_inherit:
                doc_inherit.write(
                    'From ' + self.parent_org + ' to ' + self.child_org + ' the following wasn\'t inherited')
                doc_inherit.writelines(not_inherited, )
        sleep(8)

# def workflow_get(driver, org, ent):
#
#     workflow_list = []
#     main_url = "https://" + ent + ".salestrekker.com"
#
#     if org in driver.current_url:
#         pass
#     else:
#         org_changer(driver,org)
#
#     driver.get(main_url + '/settings/workflows')
#     wd_wait(driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
#     # print('before scrolling')
#     main_documents = driver.find_element_by_css_selector('body > md-content')
#
#     last_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)
#     # print(last_height)
#     sleep(1)
#     while True:
#         driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
#         sleep(3)
#         new_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)
#
#         if new_height == last_height:
#             break
#         last_height = new_height
#
#     for document in driver.find_elements_by_tag_name('st-list-item'):
#         workflow_list.append(document.find_element_by_css_selector('a > span').text)
#
#     return workflow_list
#
#
# def workflow_compare(driver, org, ent, workflow_list):
#
#     main_url = "https://" + ent + ".salestrekker.com"
#
#     if org in driver.current_url:
#         pass
#     else:
#         org_changer(driver,org)
#
#     new_workflow_list = []
#     driver.get(main_url + '/settings/workflows')
#     wd_wait(driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
#     # print('before compare scrolling')
#     main_documents = driver.find_element_by_css_selector('body > md-content')
#
#     last_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)
#     # print(last_height)
#     sleep(1)
#     while True:
#         driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
#         sleep(3)
#         new_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)
#
#         if new_height == last_height:
#             break
#         last_height = new_height
#
#     for document in driver.find_elements_by_tag_name('st-list-item'):
#         new_workflow_list.append(document.find_element_by_css_selector('a > span').text)
#
#     if not bool(set(workflow_list).difference(new_workflow_list)):
#         print('Workflows good')
#     else:
#         print("Following workflows weren't inherited")
#         [print(workflowino) for workflowino in workflow_list if workflowino not in new_workflow_list]
#     sleep(8)

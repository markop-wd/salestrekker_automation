from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from datetime import date, datetime

from time import sleep


# TODO - Rewire what needs to  be rewired this is a mess
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


# helper for OrgChanger to check if you are already in that organisation
def check_current_org(driver, org_name):
    try:
        search_input = driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
            'aria-label')
    except exceptions.NoSuchElementException:
        driver.refresh()
        try:
            WdWait(driver, 15).until(ec.presence_of_element_located((By.TAG_NAME, 'st-toolbar')))
        except exceptions.TimeoutException:
            raise exceptions.TimeoutException
        else:
            search_input = driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                'aria-label')

    # TODO - Redo this check for organisation names
    if (("Search " + org_name + " ...") != search_input) or (org_name not in driver.title):
        return False
    else:
        return True


def toolbar_check(driver, wait_time=30):
    # TODO - Tidy this one

    # small function to split nums. into two parts i.e. - 30 into 23 and 7
    longer = wait_time - (wait_time // 4)

    try:
        WdWait(driver, wait_time - longer).until(ec.presence_of_element_located((By.TAG_NAME, 'st-toolbar')))
    except exceptions.TimeoutException:
        driver.refresh()
        try:
            WdWait(driver, longer).until(ec.presence_of_element_located((By.TAG_NAME, 'st-toolbar')))
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
            WdWait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'board')))
        except exceptions.TimeoutException:
            while True:
                self.log_in_helper()
                WdWait(self.driver, 15).until(By.ID, 'board')
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
            WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        except exceptions.TimeoutException:
            self.driver.get(self.main_url + '/settings/documents')
            try:
                WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
            except exceptions.TimeoutException:
                self.driver.get(self.main_url + '/settings/documents')
                WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))

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

        writer_time = str(datetime.today())

        self.child_org = org

        if org in self.driver.current_url:
            pass
        else:
            org_changer(self.driver, org)

        new_org_document_list = []
        self.driver.get(self.main_url + '/settings/documents')
        WdWait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
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
        if set(new_org_document_list).symmetric_difference(set(self.document_list)):
            not_inherited = []

            for documentino in self.document_list:
                if documentino not in new_org_document_list:
                    not_inherited.append('  ' + documentino + '\n')

            if not_inherited:
                with open(f"Reports/{self.time}/{self.ent} document_inheritance.txt", "a+") as doc_inherit:
                    doc_inherit.write(writer_time +
                                      'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' the following wasn\'t inherited\n')
                    doc_inherit.writelines(not_inherited)
                    doc_inherit.write('\n')

            not_inherited = []

            for documentino in new_org_document_list:
                if documentino not in self.document_list:
                    not_inherited.append(' ' + documentino + '\n')

            if not_inherited:
                with open(f"Reports/{self.time}/{self.ent} document_inheritance.txt", "a+") as doc_inherit:
                    doc_inherit.write(writer_time +
                                      self.main_url + ' - ' + "Documents are present in the child org " + self.child_org + ' that are not present in the parent org ' + self.parent_org + ' the following is \'extra\'\n')
                    doc_inherit.writelines(not_inherited)
                    doc_inherit.write('\n')

        else:
            with open(f"Reports/{self.time}/{self.ent} document_inheritance.txt", "a+") as doc_inherit:
                doc_inherit.write(
                    'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' no disrepancies noted between documents\n')

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
        WdWait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
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
        writer_time = str(datetime.today().time())

        if org in self.driver.current_url:
            pass
        else:
            org_changer(self.driver, org)

        new_workflow_list = []
        self.driver.get(self.main_url + '/settings/workflows')
        WdWait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        main_documents = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
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
            with open(f"Reports/{self.time}/{self.ent} workflow_inheritance.txt", "a+") as wf_inherit:
                wf_inherit.write(
                    'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' no disrepancies noted between workflows\n')
        else:
            not_inherited = []
            for workflowino in self.workflow_list:
                if workflowino not in new_workflow_list:
                    not_inherited.append('  ' + workflowino + '\n')

            if not_inherited:
                with open(f"Reports/{self.time}/{self.ent} workflow_inheritance.txt", "a+") as wf_inherit:
                    wf_inherit.write(writer_time +
                                     'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' the following wasn\'t inherited\n')
                    wf_inherit.writelines(not_inherited)
                    wf_inherit.write('\n')

            not_inherited = []

            for worklofino in new_workflow_list:
                if worklofino not in self.workflow_list:
                    not_inherited.append(' ' + worklofino + '\n')

            if not_inherited:
                with open(f"Reports/{self.time}/{self.ent} workflow_inheritance.txt", "a+") as wf_inherit:
                    wf_inherit.write(
                        writer_time + self.main_url + ' - ' + "Workflows are present in the child org " + self.child_org + ' that are not present in the parent org ' + self.parent_org + ' the following is \'extra\'\n')
                    wf_inherit.writelines(not_inherited)
                    wf_inherit.write('\n')

        sleep(8)


def user_extraction(driver, ent):
    main_url = "https://" + ent + ".salestrekker.com"
    driver.get(main_url + "/settings/users")

    WdWait(driver, 15).until(ec.presence_of_element_located((By.TAG_NAME, "st-accounts-list")))
    main_documents = driver.find_element_by_css_selector('body > md-content')
    last_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)
    sleep(1)
    while True:
        driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
        sleep(3)
        new_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)

        if new_height == last_height:
            break
        last_height = new_height

    users = []
    for user in driver.find_elements_by_css_selector('a:first-of-type > content > span'):
        users.append(user.text)

    return users


def get_current_username(driver):
    try:
        return driver.find_element_by_css_selector('md-menu > a > st-avatar > img').get_property('alt')
    except exceptions.NoSuchElementException:
        return driver.find_element_by_css_selector('st-avatar[account="CurrentAccount"] > img').get_property('alt')
        pass


class WorkflowManipulation:

    def __init__(self, driver, ent):
        self.ent = ent
        self.driver = driver
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.num_of_created_stages = 0
        self.all_users = []

    # def workflow_name_convert(self,wf_name):
    #     if wf_name == 'homeloan' or 'hl'

    def add_workflow(self, workflow_type='Home Loan',
                     all_users=True, wf_owner=''):

        valid_wfs = ["None", "Asset Finance", "Commercial Loan", "Conveyancing", "Home Loan", "Insurance",
                     "Personal Loan", "Real Estate"]

        import random
        from selenium.webdriver.common.keys import Keys
        while workflow_type not in valid_wfs:
            print('Valid options are\n')
            for wf in valid_wfs:
                print(wf + '\n')
            workflow_type = input("Please enter a valid wf type")

        workflow_name = f'Test WF - {workflow_type} - {date.today()}'
        sleep(0.1)

        assert "salestrekker" in self.driver.current_url, 'invalid url'
        assert "authenticate" not in self.driver.current_url, 'you are at a login page'

        # TODO - Assert that you ar at a correct position

        # TODO-- Write a way to convert workflow name values to the system values
        # self.workflow_name_convert(workflow_name)

        self.driver.get(self.main_url + "/settings/workflow/0")
        try:
            WdWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-block.mb0')))
        except exceptions.TimeoutException:
            self.driver.get(self.main_url + "/settings/workflow/0")
            try:
                WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-block.mb0')))
            except exceptions.TimeoutException:
                self.driver.get(self.main_url + "/settings/workflow/0")
                WdWait(self.driver, 20).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-block.mb0')))

        if all_users:
            if not bool(self.all_users):
                self.all_users = user_extraction(self.driver, self.ent)
                self.driver.get(self.main_url + "/settings/workflow/0")
                for user in self.all_users:
                    self.driver.find_element_by_css_selector('div:nth-child(6) input').send_keys(user + Keys.ENTER)
                    sleep(0.1)
            else:
                for user in self.all_users:
                    self.driver.find_element_by_css_selector('div:nth-child(6) input').send_keys(user + Keys.ENTER)
                    sleep(0.1)
        else:
            user = get_current_username(self.driver)
            self.driver.find_element_by_css_selector('div:nth-child(6) input').send_keys(user + Keys.ENTER)

        # This is the workflow type selector

        wf_select_id = str(self.driver.find_element_by_css_selector(
            'st-block-form-content >div >div:nth-child(4) > md-input-container > md-select').get_attribute('id'))
        wf_select_container_id = str(int(wf_select_id.split("_")[-1]) + 1)

        self.driver.find_element_by_css_selector('st-block-form-content > div > div:nth-child(4)').click()
        # don't look at me like that, this was the safer route... I think

        WdWait(self.driver, 10).until(ec.element_to_be_clickable((By.ID, "select_container_" + wf_select_container_id)))

        workflow_types = self.driver.find_elements_by_css_selector(
            "div#select_container_" + wf_select_container_id + " > md-select-menu > md-content > md-option > div > span")
        sleep(0.1)
        for wf_type in workflow_types:
            wf_el_text = wf_type.text
            # TODO
            if wf_el_text == workflow_type:
                try:
                    wf_type.click()
                except:
                    self.driver.execute_script("arguments[0].click()", wf_type.find_element_by_tag_name('span'))
                break

        # This is the workflow owner selector

        try:
            self.driver.find_element_by_css_selector('st-block-form-content > div > div:nth-child(3)').click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script(
                "document.querySelector('st-block-form-content > div > div:nth-child(3)').click();")

        owner_select_id = str(self.driver.find_element_by_css_selector(
            'st-block-form-content >div >div:nth-child(3) > md-input-container > md-select').get_attribute('id'))

        owner_select_container_id = str(int(owner_select_id.split("_")[-1]) + 1)

        WdWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.ID, "select_container_" + owner_select_container_id)))
        deal_owners = self.driver.find_elements_by_css_selector(
            "div#select_container_" + owner_select_container_id + " md-option")
        if not wf_owner:
            user = get_current_username(self.driver)
            sleep(0.1)
            for deal_owner in deal_owners:
                span = deal_owner.find_element_by_tag_name('span')
                if span.text == user:
                    deal_owner.click()
                    break
        else:
            user = wf_owner
            owners = []
            sleep(0.1)
            for deal_owner in deal_owners:
                loop_owner = deal_owner.find_element_by_tag_name('span').text
                owners.append(loop_owner)
                if loop_owner == user:
                    deal_owner.click()
                    break
            else:
                print('No deal owner with name ', wf_owner)
                print('Here are the available workflow owners\n')
                for name in owners:
                    print(name + '\n')

                wf_owner = input('Please re-input the workflow owner name')
                user = wf_owner
                owners = []
                sleep(0.1)
                for deal_owner in deal_owners:
                    loop_owner = deal_owner.find_element_by_tag_name('span').text
                    owners.append(loop_owner)
                    if loop_owner == user:
                        deal_owner.click()
                        break
                else:
                    print('No user with that name - either something is wrong and I didn\'t write this out')

        # From here

        new_stages = random.randint(0, 5)
        while new_stages > 0:
            try:
                self.driver.find_element_by_css_selector('span > button').click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script("document.querySelector('span > button').click();")

            new_stages -= 1

        sleep(1)
        self.driver.find_element_by_css_selector('st-block-form-content > div > div:first-child > md-input-container '
                                                 '> input').send_keys(workflow_name)

        # number_of_stages = len(self.driver.find_elements_by_css_selector('workflow-stages > workflow-stage'))

        WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))
        WdWait(self.driver, 10).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))

        # TODO - Confirm that the workflow exists

        # self.driver.get(self.main_url + "/settings/workflows")
        #
        # try:
        #     wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
        # except exceptions.TimeoutException:
        #     self.driver.get(self.main_url + "/settings/workflow/0")
        #     try:
        #         wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
        #     except exceptions.TimeoutException:
        #         self.driver.get(self.main_url + "/settings/workflow/0")
        #         wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
        #
        # main_documents = self.driver.find_element_by_css_selector('body > md-content')
        #
        # last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        # print(last_height)
        # sleep(1)
        # while True:
        #     self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
        #     sleep(3)
        #     new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
        #
        #     if new_height == last_height:
        #         break
        #     last_height = new_height
        #
        # for elel in self.driver.find_elements_by_css_selector('st-list-item > a > span'):
        #     if elel.text == workflow_name:
        #         nav_url = self.main_url + "/board/" + \
        #                   str(elel.find_element_by_xpath('./..').get_attribute('href')).split('/')[-1]
        #         self.driver.get(nav_url)
        #         break
        #
        # try:
        #     wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.ID, 'board')))
        # except exceptions.TimeoutException:
        #     self.driver.get(nav_url)
        #     try:
        #         wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.ID, 'board')))
        #     except exceptions.TimeoutException:
        #         wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.ID, 'board')))
        #
        # if number_of_stages == len(self.driver.find_elements_by_css_selector('#board > stage ')):
        #     print('all good with stage and HL WF adding')
        # else:
        #     print('diff between expected and actual is ',
        #           number_of_stages - len(self.driver.find_elements_by_css_selector('#board > stage')))

    # def duplicate_hl_wf(self):
    #     self.driver.get(self.main_url + "/settings/workflows")
    #     try:
    #         wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
    #     except exceptions.TimeoutException:
    #         self.driver.get(self.main_url + "/settings/workflows")
    #         try:
    #             wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
    #         except exceptions.TimeoutException:
    #             self.driver.get(self.main_url + "/settings/workflows")
    #             wd_wait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'md-content')))
    #
    #     main_documents = self.driver.find_element_by_css_selector('body > md-content')
    #
    #     last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
    #     # print(last_height)
    #     sleep(1)
    #     while True:
    #         self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
    #         sleep(3)
    #         new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_documents)
    #
    #         if new_height == last_height:
    #             break
    #         last_height = new_height
    #
    #     for elel in self.driver.find_elements_by_css_selector('st-list-item > a > span'):
    #         if elel.text == self.hl_workflow_name:
    #             elel.find_element_by_xpath('')
    #             nav_url = self.main_url + "/board/" + \
    #                       str(elel.find_element_by_xpath('./..').get_attribute('href')).split('/')[-1]
    #
    #             break
    #
    #     # self.hl_workflow_name
    #     pass
    #


# TODO - Re-write to allow adding multiple users
def add_user(driver, ent, email, username='Test Surname'):
    from selenium.webdriver.common.keys import Keys

    main_url = "https://" + ent + ".salestrekker.com"
    first_name = username.split(' ')[0]
    try:
        last_name = username.split(' ')[1]
    except IndexError:
        last_name = 'Surname'

    try:
        WdWait(driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-accounts-list')))
    except exceptions.TimeoutException:
        driver.get(main_url + '/settings/users')
        WdWait(driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-accounts-list')))

    driver.find_element_by_css_selector('span > button').click()
    WdWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'span > button')))

    # TODO - All the three Try Excepts below are of the same pattern and just require the css element selector as input - maybe this can be turn into a general pattern for a checker, input details assert it's there etc.
    driver.find_element_by_css_selector('div:nth-child(1) > md-input-container > input').send_keys(email)
    try:
        WdWait(driver, 1).until(
            ec.text_to_be_present_in_element_value((By.CSS_SELECTOR, 'div:nth-child(1) > md-input-container > input'),
                                                   email))
    except exceptions.TimeoutException:
        driver.find_element_by_css_selector('div:nth-child(1) > md-input-container > input').send_keys(
            Keys.CONTROL + "a")
        driver.find_element_by_css_selector('div:nth-child(1) > md-input-container > input').send_keys(email)

    sleep(0.1)
    driver.find_element_by_css_selector(
        'div:nth-child(2) > md-input-container:nth-child(1) > input').send_keys(first_name)
    try:
        WdWait(driver, 1).until(
            ec.text_to_be_present_in_element_value((By.CSS_SELECTOR, 'div:nth-child(2) > md-input-container > input'),
                                                   first_name))
    except exceptions.TimeoutException:
        driver.find_element_by_css_selector(
            'div:nth-child(2) > md-input-container:nth-child(1) > input').send_keys(Keys.CONTROL + 'a')
        driver.find_element_by_css_selector(
            'div:nth-child(2) > md-input-container:nth-child(1) > input').send_keys(first_name)

    sleep(0.1)
    driver.find_element_by_css_selector(
        'div:nth-child(2) > md-input-container:nth-child(2) > input').send_keys(last_name)
    try:
        WdWait(driver, 1).until(ec.text_to_be_present_in_element_value(
            (By.CSS_SELECTOR, 'div:nth-child(2) > md-input-container:nth-child(2) > input'), last_name))
    except exceptions.TimeoutException:
        driver.find_element_by_css_selector(
            'div:nth-child(2) > md-input-container:nth-child(2) > input').send_keys(Keys.CONTROL + 'a')
        driver.find_element_by_css_selector(
            'div:nth-child(2) > md-input-container:nth-child(2) > input').send_keys(last_name)

    sleep(0.1)
    # input('Add user test')
    try:
        WdWait(driver, 10).until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR, 'md-dialog-actions > button:nth-child(2)'))).click()
    except exceptions.ElementClickInterceptedException:
        driver.execute_script('document.querySelector("md-dialog-actions > button:nth-child(2)").click();')

    WdWait(driver, 10).until(
        ec.text_to_be_present_in_element((By.CSS_SELECTOR, 'span.md-toast-text > span:first-child'), 'User'))
    WdWait(driver, 10).until(
        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'span.md-toast-text > span:first-child')))


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

from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from datetime import date

from time import sleep

from main.Permanent.user_manipulation import return_all_users, get_current_username
from selenium.webdriver.common.keys import Keys


class WorkflowManipulation:

    def __init__(self, driver, ent):
        self.ent = ent
        self.driver = driver
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.num_of_created_stages = 0
        self.all_users = []

    def add_workflow(self, workflow_type='Home Loan',
                     add_all_users=True, wf_owner=''):

        valid_wfs = ["None", "Asset Finance", "Commercial Loan", "Conveyancing", "Home Loan", "Insurance",
                     "Personal Loan", "Real Estate"]

        import random
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

        if add_all_users:
            if not bool(self.all_users):
                self.add_users_to_workflow()
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

    def workflow_users(self, workflow_id):
        self.driver.get(self.main_url + '/settings/workflow/' + workflow_id)
        WdWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-block.mb0')))
        try:
            return_list = [user.text for user in
                           self.driver.find_elements_by_css_selector('md-chip div.md-contact-name')]
        except exceptions.NoSuchElementException:
            return_list = []

        return return_list

    def add_users_to_workflow(self, worklfow_id='New', users="All"):

        if users == 'All':
            self.all_users = return_all_users(self.driver, self.ent)
        else:
            self.all_users = users.split('-')

        if worklfow_id == 'New':
            self.driver.get(self.main_url + "/settings/workflow/0")
        else:
            self.driver.get(self.main_url + "/settings/workflow/" + worklfow_id)
        for user in self.all_users:
            WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div:nth-child(6) input')))
            self.driver.find_element_by_css_selector('div:nth-child(6) input').send_keys(user + Keys.ENTER)
            sleep(0.1)

        WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.md-toast-content')))
        WdWait(self.driver, 10).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.md-toast-content')))


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

    def get_all_workflows(self):
        """
        Returns full href of the workflows - example https://dev.salestrekker.com/board/jaoj0342-joadf203-wraf
        :return:
        """
        self.driver.get(self.main_url)
        WdWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Deals"]'))).click()
        workflow_container = WdWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'md-menu-content.sub-menu > section')))
        workflows = workflow_container.find_elements_by_css_selector('md-menu-item > a')
        workflow_list = [workflow.get_attribute('href') for workflow in workflows]
        return workflow_list

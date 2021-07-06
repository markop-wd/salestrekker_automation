"""
Main business logic.
This is where you call all of the modules/functions and organize them. 

Once there is a GUI this should be repurposed so that buttons call their respective functions.
"""
import os
import random
from datetime import date, datetime
import json
import concurrent.futures
from time import sleep

from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import Permanent.client_portal.login
from Permanent.client_portal.portal_fill import PortalFill

from Permanent.login import LogIn
from Permanent.deal_create import EditDeal
from Permanent.deal_fill import MultipleDealCreator
from Permanent.document_comparator import DocumentCheck
from Permanent.workflow_comparator import WorkflowCheck
from Permanent import org_funcs, user_manipulation, helper_funcs, workflow_manipulation
from mail import mail_get
import filelock

# This is the worker that I modify to fit special scenarios - e.g. when I want to create 10 empty deals I write the logic here
from main.Permanent.deal_manipulation import Screenshot
from main.Permanent.helper_funcs import md_toast_remover


class Test:

    def __init__(self, driver, org_name):
        self.driver = driver
        self.org_name = org_name

    def screenshot_helper(self, element_with_scroll, org_name, sub_section_name, button_count):
        scroll_total = self.driver.execute_script(f"return arguments[0].scrollHeight", element_with_scroll)
        content = self.driver.execute_script(f"return arguments[0].clientHeight", element_with_scroll)

        scroll_new = 0
        count = 1
        while scroll_new < (scroll_total - 100):

            md_toast_remover(self.driver)

            self.driver.execute_script(f"arguments[0].scroll(0,{scroll_new});", element_with_scroll)

            self.driver.get_screenshot_as_file(
                f'SettingsScreenshots/{org_name}/{button_count}. {sub_section_name} no. {count}.png')
            scroll_new += (content - 120)
            count += 1
            if content == scroll_total:
                break

    def main(self):
        from selenium.webdriver.support.wait import WebDriverWait as WdWait
        from selenium.webdriver.support import expected_conditions as ec

        self.driver.get('https://dev.salestrekker.com/settings')
        if not os.path.exists('SettingsScreenshots'):
            os.mkdir('SettingsScreenshots')
        if not os.path.exists(f'SettingsScreenshots/{self.org_name}'):
            os.mkdir(f'SettingsScreenshots/{self.org_name}')
        sleep(10)

        buttons = self.driver.find_elements(by=By.CSS_SELECTOR, value='st-sidebar-block div > a')

        for count, el in enumerate(buttons, start=1):
            try:
                el.click()
            except exceptions.ElementNotInteractableException:
                self.driver.execute_script('arguments[0].click();', el)
            try:
                WdWait(self.driver, 10).until(ec.visibility_of_element_located((By.TAG_NAME, 'main')))
            except exceptions.TimeoutException:
                pass
            scroll_el = self.driver.find_element(by=By.CSS_SELECTOR, value='body > md-content')
            setting_name = el.find_element(by=By.TAG_NAME, value='span').text
            self.screenshot_helper(element_with_scroll=scroll_el, org_name=self.org_name,
                                   sub_section_name=setting_name, button_count=count)


def worker(driver: Chrome, ent: str, password: str, runner_main_org: str,
           runner_learn_org: str, email: str = 'helpdesk@salestrekker.com'):
    with open("perm_vars.json", "r") as perm_json:
        perm_vars = json.load(perm_json)

    test_users = perm_vars['test_users']
    allowed_workflows = perm_vars['workflows'].split('-')

    # LogIn(driver, ent, email, password).log_in()

    # org_funcs.organization_create(driver, ent, runner_learn_org, runner_main_org)
    LogIn(driver, ent, email, password).log_in()
    # org_funcs.org_changer(driver, '# Enterprise')
    # org_funcs.org_changer(driver, 'Test Organization 2021-03-10 Test')

    # org_funcs.org_changer(driver, runner_main_org)
    orgi_name = 'New Zealand Test'
    org_funcs.org_changer(driver, orgi_name)

    # org_funcs.org_changer(driver, f'Test Organization {date.today()}')
    # org_funcs.org_changer(driver, 'New Zealand Test')

    # sleep(5000)
    # matthew_user = test_users['matthew']
    # email_split = matthew_user['email'].split('@')
    # email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    # user_manipulation.add_user(driver, ent, email=email,
    #                            username=matthew_user['username'])

    # for name, values in test_users.items():
    #     # First split the email then append the current date to before the @ - so instead of phillip@salestrekker.com this will create phillip+240321@salestrekker.com
    #     email_split = values['email'].split('@')
    #     email_with_date = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    #
    #     user_manipulation.add_user(driver, ent,
    #                                email=email_with_date, username=values['username'],
    #                                broker=False, admin=False,
    #                                mentor=False)
    #
    # for name, values in test_users.items():
    #
    #     user_manipulation.add_user(driver, ent,
    #                                email=values['email'], username=values['username'],
    #                                broker=True, admin=True,
    #                                mentor=False)

    # user_manipulation.add_user(driver, ent, email=matthew_user['email'],
    #                            username=matthew_user['username'])
    # hl_workflow = ''
    # for workflow in allowed_workflows:
    #     workflow_manipulation.add_workflow(driver=driver, ent=ent, workflow_type=workflow, wf_owner='Phillip Djukanovic')

    af_workflow = 'https://dev.salestrekker.com/board/592111a5-b638-41c5-bf09-92b6a9b0c9e5'
    hl_workflow = 'https://dev.salestrekker.com/board/9a2d3ca1-5cd3-4cf2-8d32-1f0f2fae710d'
    # wff = 'https://dev.salestrekker.com/board/d016d318-0d3c-48cb-9fe5-0f9d238e9ab9'
    # deal_create = EditDeal(ent, driver)
    # deal_fill = MultipleDealCreator(driver)
    #
    # link = deal_create.run(workflow=wff, deal_owner_name='Marko P',
    #                        client_email='matthew@salestrekker.com')
    # deal_fill.client_profile_input(link)

    # for workflow in workflow_manipulation.get_all_workflows(driver, ent):
    #     if "Test WF - Asset Finance" in workflow['name']:
    #         af_workflow = workflow['link']
    #     if "Test WF - Home Loan" in workflow['name']:
    #         hl_workflow = workflow['link']
    #
    if af_workflow or hl_workflow:
        deal_create = EditDeal(ent, driver)
        deal_fill = MultipleDealCreator(driver)
        # hd_username = user_manipulation.get_current_username(driver)

        if af_workflow:
            link = deal_create.run(workflow=af_workflow, deal_owner_name='Marko P', af_type='cons')
            deal_fill.client_profile_input(link)

            link = deal_create.run(workflow=af_workflow, deal_owner_name='Marko P', af_type='comm')
            deal_fill.client_profile_input(link)
        if hl_workflow:
            link = deal_create.run(workflow=hl_workflow, deal_owner_name='Marko P')
            deal_fill.client_profile_input(link)

    # new_email, new_password = helper_funcs.user_setup_raw(driver, ent)
    # with open('details.json', 'r') as details:
    #     json_details = json.load(details)
    #     json_details[
    #     ent][new_email] = new_password
    # with open('details.json', 'w') as details:
    #     json.dump(json_details, details)

    # helper_funcs.accreditation_fill(driver, ent)

    # org_funcs.org_changer(driver, f'Test Organization {date.today()}')

    # driver.get(f"https://{ent}.salestrekker.com/settings/import-data")

    # input("Heyo")

    # hl_workflow = hl_workflows[ent]
    # hl_workflow = 'https://dev.salestrekker.com/board/de975f9c-e6db-42d3-99e9-c9c4e77b11f5'

    # workflows = ['https://dev.salestrekker.com/settings/workflow/64c691a1-14a9-4552-a4f8-bc21cdfffee6',
    #              'https://dev.salestrekker.com/settings/workflow/d61756d6-2572-4f10-86ae-7560dc040a4d']
    # owners = ['Maya Test', 'Matthew Test', 'Zac Test', 'Phillip Test']
    # af_workflow = 'https://dev.salestrekker.com/board/30b94e85-3d1f-491e-a558-6172c618451d'
    # for workflow in workflows:
    #     workflow_manipulation.add_users_to_workflow(driver, ent, workflow, owners)
    #
    # deal_create = EditDeal(ent, driver)
    # deal_fill = MultipleDealCreator(driver)
    # deal_link = deal_create.run(workflow=hl_workflow, deal_owner_name='Marko P')
    # deal_fill.client_profile_input(deal_link)

    # for _ in range(3):
    #     new_deal_hl = deal_create.run(workflow=hl_workflow.split('/')[-1], deal_owner_name='Marko P')
    #     deal_fill.client_profile_input(new_deal_hl)

    # for _ in range(5):
    #     new_deal_hl = deal_create.run(workflow=af_workflow.split('/')[-1], deal_owner_name='Matthew Test')
    #     if random.choice([1, 2, 3, 4]) == 2:
    #         deal_fill.client_profile_input(new_deal_hl)

    # deal_create.run(workflow=hl_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test')

    # # new_deal_af = deal_create.run(workflow=af_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test')
    # deal_create.run(workflow=af_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test', af_type='comm')

    # # print(hl, new_deal)

    # deal_fill.client_profile_input("https://dev.salestrekker.com/fact-find/58b2bcee-d020-4beb-a2fb-326def7b5a48/198c95c7-b607-45b0-abef-8404825e8483")
    # new_email, new_password = helper_funcs.user_setup_raw(driver, ent)
    # with open('details.json', 'r') as details:
    #     json_details = json.load(details)
    #     json_details[ent][new_email] = new_password
    # with open('details.json', 'w') as details:
    #     json.dump(json_details, details)

    sleep(5)
    print(f'finished {ent}')


# The logic here is mostly static and includes the main rundown. Login, create an organization, add users, the workflows, add all types of deals
def worker_main(driver: Chrome, ent: str, password: str, runner_main_org: str,
                runner_learn_org: str, email: str = 'helpdesk@salestrekker.com'):
    # The workflows here just serve as a placeholder
    # hl_workflows = {
    #     "gem": "https://gem.salestrekker.com/board/ba299909-8eb3-4f72-803e-809ee5197e15",
    #     "ynet": "https://ynet.salestrekker.com/board/c1e72ff3-70a3-4425-a7e4-9dc3a15d0f9f",
    #     "vownet": "https://vownet.salestrekker.com/board/67e4c833-c232-4cb0-9069-01ddab1b0fde",
    #     "gemnz": "https://gemnz.salestrekker.com/board/fc760400-f16d-4637-a91d-47af13872b8d",
    #     "platform": "https://platform.salestrekker.com/board/04454b28-33a6-46c8-bc92-8bb1b1eb06ef",
    #     "nlgconnect": "https://nlgconnect.salestrekker.com/board/e1d9450f-14eb-4081-8c45-5e6f74834688",
    #     "app": "https://app.salemailestrekker.com/board/0e192f77-4ff4-4ec9-9daf-7ca6f25a6fd1",
    #     "ioutsource": "https://ioutsource.salestrekker.com/board/f749f86b-07d2-404e-aabe-509c8a7578b7",
    #     "sfg": "https://sfg.salestrekker.com/board/cf28e583-0033-4efe-82f1-a31158baa4e2",
    #     "chief": "https://chief.salestrekker.com/board/50894293-ddef-4cd1-84a2-f490ee5f80df"}

    # Perm vars contain all the main and learn organization names, types of workflows, which users to add and with which permissions
    with open("perm_vars.json", "r") as perm_json:
        perm_vars = json.load(perm_json)

    test_users = perm_vars['test_users']
    allowed_workflows = perm_vars['workflows'].split('-')

    driver.implicitly_wait(20)

    LogIn(driver, ent, email, password).log_in()

    org_funcs.organization_create(driver, ent, runner_learn_org, runner_main_org)

    document_check = DocumentCheck(driver, ent)
    workflow_check = WorkflowCheck(driver, ent)

    # Gets the names of the documents and workflows in the Learn organization (as that is the main group and everything in the new org is inherited from it.
    document_check.document_get(runner_learn_org)
    workflow_check.workflow_get(runner_learn_org)

    # Sleep here is as the document inheritance is not instant, but takes some time
    sleep(160)

    # org_funcs.org_changer(driver, f'Test Organization {date.today()}')

    # Compare the document and workflow names in the new organization with the ones from Learn (that you extracted previously)
    document_check.document_compare(f'Test Organization {date.today()}')
    workflow_check.workflow_compare(f'Test Organization {date.today()}')

    # This is if I only want to add myself to the organization
    # matthew_user = test_users['matthew']
    # email_split = matthew_user['email'].split('@')
    # email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    # user_manipulation.add_user(driver, ent, email=email,
    #                            username=matthew_user['username'])
    #

    # Add all users defined in perm_var.json to the organization you are currently in (new org by the current logic)
    email_spli = test_users['matthew']['email'].split('@')
    date_email = email_spli[0] + f'+{date.today().strftime("%d%m%y")}@' + email_spli[1]
    user_manipulation.add_user(driver, ent,
                               email=date_email, username=test_users['matthew']['username'],
                               broker=False, admin=False,
                               mentor=False)

    # for name, values in test_users.items():
    #     # First split the email then append the current date to before the @ - so instead of phillip@salestrekker.com this will create phillip+240321@salestrekker.com
    #     email_split = values['email'].split('@')
    #     email_with_date = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    # 
    #     user_manipulation.add_user(driver, ent,
    #                                email=email_with_date, username=values['username'],
    #                                broker=False, admin=False,
    #                                mentor=False)

    # driver.refresh()
    sleep(5)
    user_manipulation.add_user(driver, ent,
                               email=test_users['matthew']['email'], username='Marko P',
                               broker=test_users['matthew']['broker'], admin=test_users['matthew']['admin'],
                               mentor=test_users['matthew']['mentor'])

    user_manipulation.add_user(driver, ent,
                               email=test_users['phillip']['email'], username='Phillip Djukanovic',
                               broker=test_users['phillip']['broker'], admin=test_users['phillip']['admin'],
                               mentor=test_users['phillip']['mentor'])

    # for name, values in test_users.items():
    #     user_manipulation.add_user(driver, ent,
    #                                email=values['email'], username=values['username'],
    #                                broker=values['broker'], admin=values['admin'],
    #                                mentor=values['mentor'])

    # Add all workflows defined in perm_vars.json
    for workflow in allowed_workflows:
        workflow_manipulation.add_workflow(driver=driver, ent=ent, workflow_type=workflow,
                                           wf_owner='Phillip Djukanovic')

    sleep(10)
    driver.refresh()
    hl_workflow = ''
    af_workflow = ''
    for workflow in workflow_manipulation.get_all_workflows(driver, ent):
        if "Test WF - Home Loan" in workflow['name']:
            hl_workflow = workflow['link']
        if "Test WF - Asset Finance" in workflow['name']:
            af_workflow = workflow['link']

    if hl_workflow or af_workflow:
        deal_create = EditDeal(ent, driver)
        deal_fill = MultipleDealCreator(driver)
        # hd_username = user_manipulation.get_current_username(driver)
        if hl_workflow:
            deal_link = deal_create.run(workflow=hl_workflow, deal_owner_name='Phillip Djukanovic')
            deal_fill.client_profile_input(deal_link)
        if af_workflow:
            deal_link = deal_create.run(workflow=af_workflow, deal_owner_name='Phillip Djukanovic', af_type='cons')
            deal_fill.client_profile_input(deal_link)

            deal_link = deal_create.run(workflow=af_workflow, deal_owner_name='Phillip Djukanovic', af_type='comm')
            deal_fill.client_profile_input(deal_link)

    # Navigate to the st.receive@gmail.com (to which I set a forwarding of new user emails to) and get the username and password and store those in details.json
    # new_email, new_password = helper_funcs.user_setup_raw(driver, ent)
    # with open('details.json', 'r') as details:
    #     json_details = json.load(details)
    #     json_details[ent][new_email] = new_password
    # with open('details.json', 'w') as details:
    #     json.dump(json_details, details)

    # Fill in new accrediations - this needs to be fixed as it's not working anymore
    # helper_funcs.accreditation_fill(driver, ent)

    sleep(5)


def cp_worker(driver: Chrome, pin: str, link: str):
    # Client portal handling logic
    driver.implicitly_wait(10)

    Permanent.client_portal.login.LogIn(driver, link, pin).log_in()
    driver.get(link.split('authenticate')[0])
    portal_runner = PortalFill(driver)
    portal_runner.main()
    driver.refresh()
    sleep(20)
    portal_runner.screenshot()


def api(driver: Chrome, ent: str, password: str, email: str = 'helpdesk@salestrekker.com'):
    # Create an API that you can access online and give it commands instead of running the app on your computer - still in testing phase.
    LogIn(driver, ent, email, password).log_in()

    print(f'finished {ent}')

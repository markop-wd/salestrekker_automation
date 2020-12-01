from main.Permanent import document_comparator, workflow_comparator, workflow_manipulation, user_manipulation, \
    org_funcs, login, deal_create, deal_manipulation, groups_and_branches_manipulation

from selenium.webdriver import Chrome
from selenium.webdriver import Firefox

from selenium.webdriver.firefox.options import Options as f_fox_options
from selenium.webdriver.chrome.options import Options as chr_options

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from datetime import date, datetime
import json
import time
from random import randrange
import traceback


# chrome_options = chr_options()
# # chrome_options.add_argument('--headless')
# chrome_options.add_argument('start-maximized')


# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument(
#     "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.39 Safari/537.36")


class WorkerInitializer:

    def __init__(self, start_time, ent='dev', email='matthew@salestrekker.com', password='',
                 new_org_name=f'Test Organisation {date.today()}', group='Default'):
        self.ent = ent
        self.main_url = 'https://' + ent + '.salestrekker.com'
        self.driver = Firefox(executable_path=GeckoDriverManager().install())
        # self.driver = Firefox(ChromeDriverManager().install(), chrome_options=chrome_options)
        # self.driver.set_window_size(1920, 1080)
        self.driver.maximize_window()
        self.email = email
        self.password = password
        self.new_org_name = new_org_name
        self.main_org = ''
        self.group = group
        self.hl_workflow_name = 'Automation Workflow Name'
        with open("perm_vars", "r") as perm_json:
            perm_vars = json.load(perm_json)
        self.allowed_workflows = perm_vars['workflows'].split('-')
        self.test_users = perm_vars['test_users']
        self.log_helper = login.LogIn(self.driver, self.ent, self.email, self.password)
        self.doc_helper = document_comparator.DocumentCheck(self.driver, self.ent, start_time)
        self.wf_helper = workflow_comparator.WorkflowCheck(self.driver, self.ent, start_time)
        self.wf_manipulate = workflow_manipulation.WorkflowManipulation(self.driver, self.ent)
        self.deal_create = deal_create.EditDeal(self.ent, self.driver)
        self.deal_fill = deal_create.MultipleDealCreator(self.ent, self.driver)
        self.deal_manipulation = deal_manipulation.Screenshot(self.driver)
        self.groups_and_branches = groups_and_branches_manipulation.GroupsAndBranches(self.driver, self.ent)

    def deployment_logic(self, runner_main_org, runner_learn_org):

        contact_types = ["string:018a40bf-027a-4a08-9910-a0cbb058ddab", "string:ef8154b0-7bda-4d1e-a87e-f286c06f7d94",
                         "string:d583957c-3ee9-4ec2-b041-efa0f8d41875", "string:e542c9e7-ba5c-4ac3-9234-52263b157271",
                         "string:5fc8a573-5d6f-427e-acd8-a435dff25fd6", "string:2ad70288-34e7-4fb1-9662-fa101389870f",
                         "string:e7e0844e-af08-4734-9182-cd10d118eaaa", "string:0b39633b-24a8-40e9-b3a5-934538c3cf57",
                         "string:f017b136-6988-46a8-8a2d-e29e8033673f", "string:90f14042-9110-445e-8e6e-4417bedf06f4",
                         "string:5772ddbb-f89a-48e4-843b-0cf7d041f785", "string:1c671835-7241-46d0-beaa-de1d7f613d96",
                         "string:6cd3e44c-6b2c-426f-a4f7-079405a74107", "string:2ed149c6-2b4e-4f28-a6bd-fe7708331b5b",
                         "string:c2babc6c-a4c5-4deb-99fc-b0780e7b35c1", "string:a181539e-e964-4d67-b3d9-da4b9fdee312",
                         "string:07c75870-0e66-4b61-b56f-770ccaa551bd", "string:a91d6341-5372-475b-841d-b89c5998ac66",
                         "string:804b1680-eeaf-4154-aacb-865641000405", "string:1a8a91f8-5666-4ce6-9a78-5cf9a49b5367",
                         "string:fa625960-e2ab-4699-bab3-57a721f8bce0", "string:a8b080e6-6041-43a2-bce3-b50503019504",
                         "string:91ca1a29-6fdb-4b65-bcec-fab85892ed56", "string:5ba8db09-da48-4b26-8766-05a8e1d09c88",
                         "string:f298fa78-3991-4e8c-9319-c14ee9b5c9d1", "string:d24fefd4-ad7d-4d69-a35d-4b1f84bb1b30",
                         "string:78edd653-2bf9-4a78-8cb9-15f0e44928d9", "string:a8bcbee4-8471-4b51-94e9-b6afbfbe06b2",
                         "string:30aa7c93-a721-45cc-a4a6-01e16feffff4", "string:489f97cf-2952-4bda-8c0a-8e24856315a8",
                         "string:91014368-29c2-4a66-8d36-b88f50b70da3", "string:6176d6ef-faec-427a-b52d-da92df39ada6",
                         "string:67da720d-b94d-4f74-ab29-e109bd780b33", "string:f589a325-f614-4a59-ab49-5720a4fd6756",
                         "string:dc0947fa-cc42-4504-87f7-f320618e2e3b", "string:4f96e10f-49f5-4634-9af6-e28544e300a8",
                         "string:748417ed-4f58-46d0-aaac-1a01c072f70b", "string:58ac3382-83c8-4b80-9c96-5eb5be9e604a",
                         "string:41674e36-4b27-4e77-914e-e9e39d188263", "string:86ecc076-a2cc-46e8-a64c-edddd29ba3fa",
                         "string:64d5a6dc-e308-476a-8a9f-66f85ac7318f", "string:e2cd11d9-7c67-4e2b-b3f5-5cdcac08ace7",
                         "string:603d1ca5-82e7-48d2-98b6-885a57315f9e", "string:434ca1cb-edf2-4448-8cb9-bff59f22f6f8",
                         "string:1f72f021-59be-40cd-8494-30f1c979273b", "string:e8f5dce4-e663-4e77-96ec-08f015f4ca91",
                         "string:3ac4e392-f4c5-4d1b-b10f-c86692781ca7"]

        self.log_helper.log_in()
        print(f'Logged into - {self.ent}')

        hl_workflow = 'https://dev.salestrekker.com/board/179e90ab-ccde-41b3-bbe5-935dc87482eb'
        af_workflow = 'https://dev.salestrekker.com/board/0d0b2524-c365-4d03-acb4-8d4728596a61'

        # org_funcs.organization_create(self.driver, self.ent, runner_learn_org, runner_main_org)

        # self.doc_helper.document_get(runner_learn_org)
        # self.wf_helper.workflow_get(runner_learn_org)

        org_funcs.org_changer(self.driver, '# Salestrekker Enterprise')

        created_url = self.deal_create.create_deal(workflow=hl_workflow.split('/')[-1], contact_type='string:018a40bf-027a-4a08-9910-a0cbb058ddab')
        self.deal_fill.client_profile_input(created_url)

    # print(f'finished {self.ent}')

        # for user in self.test_users:
        #     test_list = user['email'].split('@')
        #     email = test_list[0] + f'+{date.today().strftime("%d%m%y")}@' + test_list[1]
        #     user_manipulation.add_user(self.driver, self.ent, email=email, username=user['username'],
        #                                broker=user['broker'], admin=user['admin'], mentor=user['mentor'])
        #
        # self.doc_helper.document_compare(f'Test Organization {date.today()}')
        # self.wf_helper.workflow_compare(f'Test Organization {date.today()}')

        # for workflow in self.allowed_workflows:
        #     self.wf_manipulate.add_workflow(workflow_type=workflow)

    def test_logic(self, runner_main_org, runner_learn_org, new_org=f'Test Organization {date.today()}'):
        print('start:', datetime.now())

        # from time import sleep
        from random import choice
        # import traceback
        # screenshots = False

        self.log_helper.log_in()
        # org_funcs.organization_create(self.driver, self.ent, runner_learn_org, runner_main_org, new_org=new_org)
        # self.log_helper.log_in()
        # org_funcs.org_changer(self.driver, new_org)

        # self.driver.get(f'https://{self.ent}.salestrekker.com/settings/groups-and-branches')
        # try:
        #     WdWait(self.driver, 40).until(ec.presence_of_element_located(
        #         (By.CSS_SELECTOR, 'st-organization-groups-and-branches-list > main > md-content > st-list')))
        # except exceptions.TimeoutException:
        #     self.driver.get(f'https://{self.ent}.salestrekker.com/settings/groups-and-branches')
        #     WdWait(self.driver, 40).until(ec.presence_of_element_located(
        #         (By.CSS_SELECTOR, 'st-organization-groups-and-branches-list > main > md-content > st-list')))
        #
        # content = self.driver.find_element(by=By.CSS_SELECTOR,value='body > md-content')
        # self.groups_and_branches.group_and_branches_scroller(content)
        # organizations = self.driver.find_elements(by=By.CSS_SELECTOR,value='st-list-item a:first-child')
        # count = 0
        #
        # if self.ent == 'ynet':
        #     for row in csv_reader.ynet_csv_reader():
        #         print(f'start {row[2]} loop: ', datetime.now())
        #         if count > 10:
        #             self.driver.get(f'https://{self.ent}.salestrekker.com/settings/groups-and-branches')
        #             try:
        #                 WdWait(self.driver, 40).until(ec.presence_of_element_located(
        #                     (
        #                         By.CSS_SELECTOR,
        #                         'st-organization-groups-and-branches-list > main > md-content > st-list')))
        #             except exceptions.TimeoutException:
        #                 self.driver.get(f'https://{self.ent}.salestrekker.com/settings/groups-and-branches')
        #                 WdWait(self.driver, 40).until(ec.presence_of_element_located(
        #                     (
        #                         By.CSS_SELECTOR,
        #                         'st-organization-groups-and-branches-list > main > md-content > st-list')))
        #
        #             content = self.driver.find_element(by=By.CSS_SELECTOR,value='body > md-content')
        #             self.groups_and_branches.group_and_branches_scroller(content)
        #             organizations = self.driver.find_elements(by=By.CSS_SELECTOR,value='st-list-item a:first-child')
        #             self.groups_and_branches.organisations = []
        #             count = 0
        #
        #         try:
        #             self.groups_and_branches.groups_and_branches_main(organizations, row[0].rstrip().lstrip(),
        #                                                               row[1].rstrip().lstrip(),
        #                                                               row[2].rstrip().lstrip(), row[3])
        #
        #         except:
        #             self.driver = None
        #             self.driver = Firefox(executable_path=GeckoDriverManager().install())
        #
        #             self.driver.maximize_window()
        #
        #             self.log_helper.log_in()
        #             # org_funcs.organization_create(self.driver, self.ent, runner_learn_org, runner_main_org, new_org=new_org)
        #             # self.log_helper.log_in()
        #             org_funcs.org_changer(self.driver, runner_main_org)
        #
        #             self.driver.get(f'https://{self.ent}.salestrekker.com/settings/groups-and-branches')
        #             try:
        #                 WdWait(self.driver, 40).until(ec.presence_of_element_located(
        #                     (
        #                         By.CSS_SELECTOR,
        #                         'st-organization-groups-and-branches-list > main > md-content > st-list')))
        #             except exceptions.TimeoutException:
        #                 self.driver.get(f'https://{self.ent}.salestrekker.com/settings/groups-and-branches')
        #                 WdWait(self.driver, 40).until(ec.presence_of_element_located(
        #                     (
        #                         By.CSS_SELECTOR,
        #                         'st-organization-groups-and-branches-list > main > md-content > st-list')))
        #
        #             content = self.driver.find_element(by=By.CSS_SELECTOR,value='body > md-content')
        #             self.groups_and_branches.group_and_branches_scroller(content)
        #             organizations = self.driver.find_elements(by=By.CSS_SELECTOR,value='st-list-item a:first-child')
        #             count = 0
        #             self.groups_and_branches.groups_and_branches_main(organizations, row[0].rstrip().lstrip(),
        #                                                               row[1].rstrip().lstrip(),
        #                                                               row[2].rstrip().lstrip(), row[3])
        #
        #         count += 1
        #         print(f'end {row[2]} loop: ', datetime.now())
        #
        # if self.ent == 'vownet':
        #     for row in csv_reader.vow_csv_reader():
        #         print(f'start {row[2]} loop: ', datetime.now())
        #         if count > 50:
        #             print('reset')
        #             self.driver.get(f'https://{self.ent}.salestrekker.com/settings/groups-and-branches')
        #             try:
        #                 WdWait(self.driver, 40).until(ec.presence_of_element_located(
        #                     (
        #                         By.CSS_SELECTOR,
        #                         'st-organization-groups-and-branches-list > main > md-content > st-list')))
        #             except exceptions.TimeoutException:
        #                 self.driver.get(f'https://{self.ent}.salestrekker.com/settings/groups-and-branches')
        #                 WdWait(self.driver, 40).until(ec.presence_of_element_located(
        #                     (
        #                         By.CSS_SELECTOR,
        #                         'st-organization-groups-and-branches-list > main > md-content > st-list')))
        #
        #             content = self.driver.find_element(by=By.CSS_SELECTOR,value='body > md-content')
        #             self.groups_and_branches.group_and_branches_scroller(content)
        #             organizations = self.driver.find_elements(by=By.CSS_SELECTOR,value='st-list-item a:first-child')
        #             self.groups_and_branches.organisations = []
        #             count = 0
        #
        #         self.groups_and_branches.groups_and_branches_main(organizations, row[0].rstrip().lstrip(),
        #                                                           row[1].rstrip().lstrip(),
        #                                                           row[2].rstrip().lstrip(), row[3])
        #
        #         count += 1
        #         print(f'end {row[2]} loop: ', datetime.now())
        #
        #
        # self.doc_helper.document_get(runner_learn_org)
        # self.wf_helper.workflow_get(runner_learn_org)

        # org_funcs.org_changer(self.driver, '0.Learn Ynet 2.0')

        # org_funcs.org_changer(self.driver, new_org)
        if self.ent == 'nlgconnect':
            org_funcs.org_changer(self.driver, 'Z. Learn NLG Connect')
            workflows = ['https://nlgconnect.salestrekker.com/board/01d32a4b-819e-4d4d-bcfd-4ab245706d60']

            for workflow in workflows:
                created_url = self.deal_create.create_deal(workflow=workflow.split('/')[-1])
                self.deal_fill.client_profile_input(created_url)

        elif self.ent == 'chief':
            org_funcs.org_changer(self.driver, 'ZZZ Learn Chief')
            workflows = ['https://chief.salestrekker.com/board/2cf949d8-339c-4be6-94dd-450896bf1faa']

            for workflow in workflows:
                created_url = self.deal_create.create_deal(workflow=workflow.split('/')[-1])
                self.deal_fill.client_profile_input(created_url)

        elif self.ent == 'vownet':
            org_funcs.org_changer(self.driver, 'Learn Vownet')
            workflows = ['https://vownet.salestrekker.com/board/008a9205-ef53-4842-bcbe-3dae0178609c']

            for workflow in workflows:
                created_url = self.deal_create.create_deal(workflow=workflow.split('/')[-1])
                self.deal_fill.client_profile_input(created_url)

        elif self.ent == 'sfg':
            org_funcs.org_changer(self.driver, '0 - Learn SFGconnect')
            workflows = ['https://sfg.salestrekker.com/board/67c68515-e3b1-45b7-9f98-3c276629bf85']

            for workflow in workflows:
                created_url = self.deal_create.create_deal(workflow=workflow.split('/')[-1])
                self.deal_fill.client_profile_input(created_url)

        elif self.ent == 'platform':
            org_funcs.org_changer(self.driver, 'Z. Learn Platform Connect')
            workflows = ['https://platform.salestrekker.com/board/81e50a6c-abe3-4917-91ef-b2ba3b40b962']

            for workflow in workflows:
                created_url = self.deal_create.create_deal(workflow=workflow.split('/')[-1])
                self.deal_fill.client_profile_input(created_url)

        elif self.ent == 'dev':

            # org_funcs.org_changer(self.driver, '# Salestrekker Enterprise')
            hl_workflow = 'https://dev.salestrekker.com/board/179e90ab-ccde-41b3-bbe5-935dc87482eb'
            af_workflow = 'https://dev.salestrekker.com/board/0d0b2524-c365-4d03-acb4-8d4728596a61'

            # created_url = self.deal_create.create_deal(workflow=hl_workflow.split('/')[-1])
            # self.deal_fill.client_profile_input(created_url)

        # org_funcs.org_changer(self.driver, '3 Demo N Co')

        # for user in self.test_users:
        #     user_manipulation.add_user(self.driver, self.ent, user['email'], username=user['username'],
        #                                broker=user['broker'], admin=user['admin'], mentor=user['mentor'])
        #

        # email_split = user['email'].split('@')
        # email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
        # user_manipulation.add_user(self.driver, self.ent, email=user['email'], username=user['username'], broker=user['broker'], admin=user['admin'], mentor=user['mentor'])
        # user_manipulation.add_user(self.driver, self.ent, email='matthew@salestrekker.com', username='Matthew Test',
        #                            broker=True, admin=True, mentor=False)

        # user_manipulation.add_user(self.driver, self.ent, email=self.test_users[0]['email'], username=self.test_users[0]['username'], broker=self.test_users[0]['broker'], admin=self.test_users[0]['admin'], mentor=self.test_users[0]['mentor'])

        # for i in range(60):
        #     user_manipulation.add_user(self.driver, self.ent, email=f'testfirst{i}@kikik.com', username=f'testfirst{i}', mentor=choice([True,False]), broker=choice([True,False]), admin=choice([True,False]))

        # allowed_workflows = [{'name': 'Flex', 'type': 'Home Loan'}, {'name': 'Mercury', 'type': 'Home Loan'},
        #                      {'name': 'AOL', 'type': 'Home Loan'}, {'name': 'LoanApp', 'type': 'Home Loan'},
        #                      {'name': 'Flex', 'type': 'Asset Finance'},
        #                      {'name': 'Mercury', 'type': 'Asset Finance'}, {'name' : 'LoanApp', 'type': 'Asset Finance'}]

        # workflow_types.split('')
        # workflow_types = ("Flex, Mercury, Simpology-LoanApp, AOL, DriveOnline, Equifax").split(', ')
        # # workflow_types =
        #
        # for workflow in workflow_types:
        #     if workflow in ['Flex', 'Mercury', 'Simpology-LoanApp', 'AOL']:
        #         self.wf_manipulate.add_workflow(workflow_name=str('0409 - ') + str(workflow) + str(' - HL'), workflow_type='Home Loan')
        #     elif workflow in ['DriveOnline']:
        #         self.wf_manipulate.add_workflow(workflow_name=str('0409 - ') + str(workflow) + str(' - AF'), workflow_type='Asset Finance')
        #     else:
        #         self.wf_manipulate.add_workflow(workflow_name=str('0409 - ') + str(workflow) + str(' - AF'), workflow_type='Asset Finance')
        #         self.wf_manipulate.add_workflow(workflow_name=str('0409 - ') + str(workflow) + str(' - HL'), workflow_type='Home Loan')

        # workflows = self.wf_manipulate.get_all_workflows()
        #
        # workflows = ['https://app.salestrekker.com/board/3235f045-376c-4c66-a795-ca1869ffe7d9']
        #
        # for workflow in workflows:
        #     created_url = self.deal_create.create_deal(workflow=workflow.split('/')[-1])
        #     self.deal_fill.client_profile_input(created_url)
        #     # created_url = self.deal_create.create_deal(workflow='https://dev.salestrekker.com/board/ceda438a-1da8-4356-9518-ac7c3bc7823f'.split('/')[-1])

        # if screenshots:
        #     # all_deals = ['https://platform.salestrekker.com/deal/81e50a6c-abe3-4917-91ef-b2ba3b40b962/8d58ae8b-5c24-446d-b11b-40195aa1e649', 'https://platform.salestrekker.com/deal/81e50a6c-abe3-4917-91ef-b2ba3b40b962/2a70601d-83bf-4093-ad57-f8f644d3e5bc']
        #     all_deals = self.wf_manipulate.get_deals()
        #     for deal in all_deals:
        #         try:
        #             self.deal_manipulation.screenshot(deal)
        #         except Exception as test:
        #
        # self.doc_helper.document_compare(new_org)
        # self.wf_helper.workflow_compare(new_org)

        print('end:', datetime.now())

        input('Good?')

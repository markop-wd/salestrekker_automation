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
        with open("perm_vars", "r") as perm_vars_json:
            perm_vars = json.load(open("perm_vars", "r"))
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

        self.log_helper.log_in()
        org_funcs.organization_create(self.driver, self.ent, runner_learn_org, runner_main_org)
        self.doc_helper.document_get(runner_learn_org)
        self.wf_helper.workflow_get(runner_learn_org)
        # org_funcs.org_changer(self.driver, runner_learn_org)
        # org_funcs.org_changer(self.driver, f'Test Organization {date.today()}')

        # for user in self.test_users:
        #     test_list = self.test_users[user].split('@')
        #     email = test_list[0] + f'+{date.today().strftime("%d%m%y")}@' + test_list[1]
        #     user_manipulation.add_user(self.driver, self.ent, email=email, username=user['username'],
        #                                broker=user['broker'], admin=user['admin'], mentor=user['mentor'])

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

            created_url = self.deal_create.create_deal(workflow=hl_workflow.split('/')[-1])
            self.deal_fill.client_profile_input(created_url)

            # self.driver.get(
            #     'https://dev.salestrekker.com/deal/home-loan/179e90ab-ccde-41b3-bbe5-935dc87482eb/d0f3fd00-ecce-4a17-a55d-4c6f31085e1e')
            # assets_button = WdWait(self.driver, 20).until(
            #     ec.visibility_of_element_located((By.XPATH, '//span[text()="Assets"]')))
            # assets_button.click()
            # for i in [1, 21, 31, 32, 33, 34, 35, 68, 84, 95, 109, 131, 134, 138, 139, 141, 148, 155, 185, 199, 208, 230,
            #           255, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329,
            #           330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348,
            #           349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367,
            #           368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386,
            #           387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405,
            #           406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424,
            #           425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443,
            #           444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462,
            #           463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481,
            #           482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500,
            #           501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519,
            #           520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538,
            #           539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557,
            #           558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576,
            #           577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595,
            #           596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614,
            #           615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633,
            #           634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 659, 675, 740, 747, 749, 751, 798, 802, 831]:
            #     try:
            #         new_oo_button = self.driver.find_element(by=By.CSS_SELECTOR,
            #                                      value='button[aria-label="Owner occupier property address"]')
            #         try:
            #             new_oo_button.click()
            #         except exceptions.ElementNotInteractableException:
            #             time.sleep(2)
            #             self.driver.execute_script('arguments[0].click();', new_oo_button)
            #
            #         input_el = self.driver.find_element(By.CSS_SELECTOR,
            #                                              'input[aria-label="Search Property (eg. 1 Walker Avenue)"]')
            #         ul_el_id = 'ul-' + str(input_el.get_attribute('id')).split('-')[-1]
            #         input_el.send_keys(f'{i} address')
            #         WdWait(self.driver, 15).until(ec.visibility_of_element_located((By.ID, ul_el_id)))
            #         li_els = self.driver.find_element(By.ID, ul_el_id).find_elements(by=By.CSS_SELECTOR,
            #                                                                          value='li span')
            #
            #         if len(li_els) == 0:
            #             input_el.send_keys(Keys.CONTROL + 'a')
            #             time.sleep(1)
            #             input_el.send_keys(Keys.DELETE)
            #
            #         else:
            #             self.driver.execute_script("arguments[0].click();", li_els[randrange(0, len(li_els))])
            #             time.sleep(5)
            #     except Exception as exc:
            #         print('address num: ', i)
            #         traceback.print_exc()
            #         print(exc)
            #     finally:
            #         asset_delete = self.driver.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Remove "]')
            #         try:
            #             asset_delete.click()
            #         except exceptions.ElementClickInterceptedException:
            #             self.driver.execute_script("arguments[0].click();", asset_delete)

            # created_url = self.deal_create.create_deal(workflow=af_workflow.split('/')[-1], af_type='comm')
            # self.deal_fill.client_profile_input(created_url)
            #
            # created_url = self.deal_create.create_deal(workflow=af_workflow.split('/')[-1],af_type='cons')
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

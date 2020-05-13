from main.Permanent import document_comparator, workflow_comparator, workflow_manipulation, user_manipulation, \
    org_funcs, login, deal_create, deal_manipulation

from selenium.webdriver import Chrome
from selenium.webdriver import Firefox

from selenium.webdriver.firefox.options import Options as f_fox_options
from selenium.webdriver.chrome.options import Options as chr_options

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from datetime import date, datetime
import json

chrome_options = chr_options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('start-maximized')


class WorkerInitializer:

    def __init__(self, start_time, ent='dev', email='matthew@salestrekker.com', password='',
                 new_org_name=f'Test Organisation {date.today()}', group='Default'):
        self.ent = ent
        self.main_url = 'https://' + ent + '.salestrekker.com'
        # self.driver = Firefox(executable_path=GeckoDriverManager().install(), options=options)
        self.driver = Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.driver.set_window_size(1920, 1080)
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
        self.deal_create = deal_create.MultipleDealCreator(self.ent, self.driver)
        self.deal_manipulate = deal_manipulation.DealManipulation(self.driver, self.ent)

    def deployment_logic(self, runner_main_org, runner_learn_org):

        self.log_helper.log_in()
        org_funcs.organization_create(self.driver, self.ent, runner_learn_org, runner_main_org)
        self.doc_helper.document_get(runner_learn_org)
        self.wf_helper.workflow_get(runner_learn_org)
        org_funcs.org_changer(self.driver, runner_learn_org)
        org_funcs.org_changer(self.driver, f'Test Organization {date.today()}')

        for user in self.test_users:
            test_list = self.test_users[user].split('@')
            email = test_list[0] + f'+{date.today().strftime("%d%m%y")}@' + test_list[1]
            user_manipulation.add_user(self.driver, self.ent, email=email, username=user['username'], broker=user['broker'], admin=user['admin'], mentor=user['mentor'])

        self.doc_helper.document_compare(f'Test Organization {date.today()}')
        self.wf_helper.workflow_compare(f'Test Organization {date.today()}')
        for workflow in self.allowed_workflows:
            self.wf_manipulate.add_workflow(workflow_type=workflow)

    def test_logic(self, runner_main_org, runner_learn_org, new_org=f'Test Organization {date.today()}'):
        # from time import sleep
        # from random import choice
        from selenium.webdriver.support.wait import WebDriverWait as WdWait
        from selenium.webdriver.support import expected_conditions as ec
        from selenium.webdriver.common.by import By
        from selenium.common import exceptions
        screenshots = True

        self.log_helper.log_in()
        # org_funcs.org_changer(self.driver, new_org)
        # org_funcs.organization_create(self.driver, self.ent, runner_learn_org, runner_main_org, new_org)
        # self.log_helper.log_in()
        # self.doc_helper.document_get(runner_learn_org)
        # self.wf_helper.workflow_get(runner_learn_org)
        org_funcs.org_changer(self.driver, new_org)
        # org_funcs.org_changer(self.driver, 'Test Organization 2020-05-12')

        # for user in self.test_users:
        #     # email_split = user['email'].split('@')
        #     # email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
        #     user_manipulation.add_user(self.driver, self.ent, email=user['email'], username=user['username'], broker=user['broker'], admin=user['admin'], mentor=user['mentor'])

        # user_manipulation.add_user(self.driver, self.ent, email=self.test_users[0]['email'], username=self.test_users[0]['username'], broker=self.test_users[0]['broker'], admin=self.test_users[0]['admin'], mentor=self.test_users[0]['mentor'])

        # for i in range(60):
        #     user_manipulation.add_user(self.driver, self.ent, email=f'testfirst{i}@kikik.com', username=f'testfirst{i}', mentor=choice([True,False]), broker=choice([True,False]), admin=choice([True,False]))
        #
        # for workflow in self.allowed_workflows:
        #     self.wf_manipulate.add_workflow(workflow_type=workflow)
        # self.driver.refresh()

        workflows = self.wf_manipulate.get_all_workflows()
        while True:
            try:
                for workflow in workflows:
                        print(datetime.now())
                        print(workflow)
                        self.deal_create.create_deal(workflow=workflow.split('/')[-1])
            except:
                continue


        # if screenshots:
        #     all_deals = self.deal_manipulate.get_deals()
        #     for deal in all_deals:
        #         self.driver.get(deal)
        #         WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > md-content')))
        #         WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR,'st-sidebar-block button:nth-child(2)')))
        #         test = self.driver.find_elements_by_css_selector('st-sidebar-block button')
        #         test[-1].click()
        #         WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-contact')))
        #         deal_name = self.driver.find_element_by_css_selector('div > header-title > h1 > small').text
        #         # seleniumself.driver.find_element().
        #         for button_count, button in enumerate(
        #                 self.driver.find_elements_by_css_selector('st-sidebar-content > st-sidebar-block > div button'),
        #                 start=1):
        #             current_separator = button.find_element_by_css_selector('span.truncate').text
        #
        #             if current_separator in ['Connect to Mercury', 'Connect to Flex']:
        #                 continue
        #             elif current_separator == 'First Surname':
        #                 current_separator_text = f'{button_count}. Client'
        #             elif current_separator == 'Company Name':
        #                 current_separator_text = f'{button_count}. Company'
        #             else:
        #                 current_separator_text = f'{button_count}. {current_separator}'
        #
        #             try:
        #                 button.click()
        #             except exceptions.ElementClickInterceptedException:
        #                 self.driver.execute_script('arguments[0].click();', button)
        #
        #             content = WdWait(self.driver, 10).until(
        #                 ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))
        #             self.deal_manipulate.screenshot(element_with_scroll=content,sub_section_name=current_separator_text,deal_name=deal_name)

        # self.doc_helper.document_compare(new_org)
        # self.wf_helper.workflow_compare(new_org)

        input('Good?')

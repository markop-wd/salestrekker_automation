from main.Permanent import document_comparator, workflow_comparator, workflow_manipulation, user_manipulation, \
    org_funcs, login, deal_create

from selenium.webdriver import Chrome
from selenium.webdriver import Firefox

from selenium.webdriver.firefox.options import Options as f_fox_options
from selenium.webdriver.chrome.options import Options as chr_options

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from datetime import date
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
        perm_vars = json.load(open("perm_vars", "r"))
        self.allowed_workflows = perm_vars['workflows'].split('-')
        self.test_users = perm_vars['test_users']
        self.log_helper = login.LogIn(self.driver, self.ent, self.email, self.password)
        self.doc_helper = document_comparator.DocumentCheck(self.driver, self.ent, start_time)
        self.wf_helper = workflow_comparator.WorkflowCheck(self.driver, self.ent, start_time)
        self.wf_manipulate = workflow_manipulation.WorkflowManipulation(self.driver, self.ent)
        self.deal_manipulate = deal_create.MultipleDealCreator(self.ent, self.driver)

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
            user_manipulation.add_user(self.driver, self.ent, email=email, username=user)

        self.doc_helper.document_compare(f'Test Organization {date.today()}')
        self.wf_helper.workflow_compare(f'Test Organization {date.today()}')
        for workflow in self.allowed_workflows:
            self.wf_manipulate.add_workflow(workflow_type=workflow)

    def test_logic(self, runner_main_org, runner_learn_org):

        self.log_helper.log_in()
        org_funcs.org_changer(self.driver,'Test Organization 2020-05-01')
        self.deal_manipulate.create_deal()
        # org_funcs.organization_create(self.driver, self.ent, runner_learn_org, runner_main_org)
        # self.log_helper.log_in()
        # self.doc_helper.document_get(runner_learn_org)
        # self.wf_helper.workflow_get(runner_learn_org)
        # org_funcs.org_changer(self.driver, f'Test Organization {date.today()}')

        # for user in self.test_users:
        #     email_split = self.test_users[user].split('@')
        #     email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
        #     user_manipulation.add_user(self.driver, self.ent, email=email, username=user)

        # self.doc_helper.document_compare(f'Test Organization {date.today()}')
        # self.wf_helper.workflow_compare(f'Test Organization {date.today()}')
        #
        # for workflow in self.allowed_workflows:
        #     self.wf_manipulate.add_workflow(workflow_type=workflow)

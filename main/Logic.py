from main.Permanent import Helpers

from selenium.webdriver import Chrome
from selenium.webdriver import Firefox

from selenium.webdriver.firefox.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from datetime import date
import json

# user = 'matthew+0406@salestrekker.com'
options = Options()


# with open("main/perm_vars") as perm_json:
#     perm_vars = json.load(perm_json)
#     orgs_info = perm_vars['orgs_info']
#     all_orgs = [org for org in perm_vars['orgs_info']]

class TestInitializer:

    def __init__(self, start_time, ent='dev', email='matthew@salestrekker.com', password='',
                 new_org_name=f'Test Organisation {date.today()}', group='Default'):
        self.ent = ent
        self.main_url = 'https://' + ent + '.salestrekker.com'
        # self.driver = Firefox(executable_path=GeckoDriverManager().install(), options=options)
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        # self.driver.find_element().get_attribute('id')
        self.email = email
        self.password = password
        self.new_org_name = new_org_name
        self.main_org = ''
        self.group = group
        self.hl_workflow_name = 'Automation Workflow Name'
        self.log_helper = Helpers.LogIn(self.driver, self.ent, self.email, self.password)
        self.doc_helper = Helpers.DocumentCheck(self.driver, self.ent, start_time)
        self.wf_helper = Helpers.WorkflowCheck(self.driver, self.ent, start_time)
        self.wf_manipulate = Helpers.WorkflowManipulation(self.driver, self.ent)
        # self.driver.find_element().get_property('')

    def deployment_logic(self, runner_main_org, runner_learn_org):
        today = date.today().strftime('%d%m%y')
        self.log_helper.log_in()
        Helpers.organization_create(self.driver, self.ent, runner_learn_org, runner_main_org)
        self.doc_helper.document_get(runner_learn_org)
        self.wf_helper.workflow_get(runner_learn_org)
        Helpers.org_changer(self.driver, f'Test Organization {today}')
        Helpers.add_user(self.driver, self.ent, f'zac+{today}@salestrekker.com','Zac Test')
        Helpers.add_user(self.driver, self.ent, f'matthew+{today}@salestrekker.com', 'Matthew Test')
        Helpers.add_user(self.driver, self.ent, f'maya+{today}@salestrekker.com', 'Maya Test')
        Helpers.add_user(self.driver, self.ent, f'phillip+{today}@salestrekker.com', 'Phillip Test')
        self.doc_helper.document_compare(f'Test Organization {today}')
        self.wf_helper.workflow_compare(f'Test Organization {today}')
        self.wf_manipulate.add_workflow(workflow_type='None')
        self.wf_manipulate.add_workflow(workflow_type='Asset Finance')
        self.wf_manipulate.add_workflow(workflow_type='Commercial Loan')
        self.wf_manipulate.add_workflow(workflow_type='Conveyancing')
        self.wf_manipulate.add_workflow(workflow_type='Home Loan')
        self.wf_manipulate.add_workflow(workflow_type='Insurance')
        self.wf_manipulate.add_workflow(workflow_type='Personal Loan')
        self.wf_manipulate.add_workflow(workflow_type='Real Estate')

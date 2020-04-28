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

    def test_logic(self, runner_main_org, runner_learn_org):
        self.log_helper.log_in()
        # helpers.org_changer(self.driver, runner_learn_org)
        self.doc_helper.document_get(runner_main_org)
        self.wf_helper.workflow_get(runner_main_org)
        self.doc_helper.document_compare(runner_learn_org)
        self.wf_helper.workflow_compare(runner_learn_org)
        self.wf_manipulate.add_workflow()
        # helpers.add_hl_workflow()
        # self.org_changer(runner_main_org)
        # self.organization_create(group=self.group, new_org=self.new_org_name)
        # self.driver.get(self.main_url + '/authenticate')
        # wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
        # self.login(self.email, self.password)
        # self.org_changer(runner_main_org)
        # self.document_compare()
        # self.workflow_compare()
        # self.add_user()
        # self.add_hl_workflow()



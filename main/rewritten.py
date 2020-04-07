from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as wd_wait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import time
from datetime import date

# ents = ['vownet', 'ioutsource', 'ynet', 'nlgconnect', 'platform', 'chief', 'sfg']
dev_main_org = '# Salestrekker Enterprise'
vow_main_org = 'Vow Financial Pty Ltd'
iot_main_org = 'outsource financial pty ltd'
ynet_main_org = 'Yellow Brick Road Finance Pty Limited'
nlg_main_org = '# NLG Connect'
ptf_main_org = '# Platform Connect'
chief_main_org = 'Chief'
gem_main_org = 'Astute Financial Management Pty Ltd'
gemnz_main_org = 'Gem New Zealand'
sfg_main_org = 'Specialist Finance Group'
app_main_org = '3 Demo N Co'
user = 'matthew+0406@salestrekker.com'
options = Options()
# options.headless = True

print(time.time())


class TestInitializer:

    def __init__(self, ent='dev', email='matthew@salestrekker.com', password='',
                 new_org_name=f'Test Organisation {date.today()}', group='Default'):
        self.ent = ent
        self.main_url = 'https://' + ent + '.salestrekker.com'
        self.driver = Firefox(executable_path=GeckoDriverManager().install(), options=options)
        # self.driver = Chrome(ChromeDriverManager().install())
        self.email = email
        self.password = password
        self.new_org_name = new_org_name
        self.document_list = []
        self.workflow_list = []
        self.current_user_name = ''
        self.runner_main_org = ''
        self.group = group
        self.hl_workflow_name = 'Automation Workflow Name'

    def go_to_main_org(self):

        if self.ent == 'vownet':
            self.runner_main_org = vow_main_org
            if 'Vow Financial Pty Ltd' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in_main_org')
            else:
                self.org_changer(vow_main_org)

            self.test_logic()

        elif self.ent == 'ynet':
            self.runner_main_org = ynet_main_org
            if 'Yellow Brick Road Finance Pty Limited' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(ynet_main_org)

            self.test_logic()


        elif self.ent == 'gem':
            self.runner_main_org = gem_main_org
            if 'Astute Financial Management Pty Ltd' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(gem_main_org)

            self.test_logic()


        elif self.ent == 'gemnz':
            self.runner_main_org = gemnz_main_org
            if 'Yellow Brick Road Finance Pty Limited' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(gemnz_main_org)

            self.test_logic()


        elif self.ent == 'app':
            self.runner_main_org = app_main_org
            if '3 Demo N Co' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(app_main_org)

            self.test_logic()


        elif self.ent == 'nlgconnect':
            self.runner_main_org = nlg_main_org
            if '# NLG Connect' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(nlg_main_org)

            self.test_logic()


        elif self.ent == 'platform':
            self.runner_main_org = ptf_main_org
            if '# Platform Connect' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(ptf_main_org)

            self.test_logic()


        elif self.ent == 'chief':
            self.runner_main_org = chief_main_org
            if 'Chief' in str(self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                    'aria-label')):
                print('in main org')
            else:
                self.org_changer(chief_main_org)

            self.test_logic()


        elif self.ent == 'ioutsource':
            self.runner_main_org = iot_main_org
            if 'outsource financial pty ltd' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(iot_main_org)

            self.test_logic()


        elif self.ent == 'sfg':
            self.runner_main_org = sfg_main_org
            if 'Specialist Finance Group' in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(sfg_main_org)

            self.test_logic()


        elif 'dev' in self.driver.current_url:
            self.runner_main_org = dev_main_org
            if dev_main_org in str(
                    self.driver.find_element_by_css_selector('md-autocomplete-wrap > input').get_attribute(
                        'aria-label')):
                print('in main org')
            else:
                self.org_changer(dev_main_org)

            self.test_logic()

    def test_logic(self, main_org):

        self.document_get()
        self.workflow_get()
        self.org_changer(main_org)
        self.organization_create(group=self.group, new_org=self.new_org_name)
        self.driver.get(self.main_url + '/authenticate')
        wd_wait(self.driver, 10).until(ec.title_contains(('Authentication')))
        self.login(self.email, self.password)
        self.org_changer(main_org)
        self.document_compare()
        self.workflow_compare()
        self.add_user()
        self.add_hl_workflow()

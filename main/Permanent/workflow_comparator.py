from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from datetime import datetime

from time import sleep

from main.Permanent.org_funcs import org_changer


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

        org_changer(self.driver, org)

        self.driver.get(self.main_url + '/settings/workflows')
        WdWait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        main_content = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_content)
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_content)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_content)

            if new_height == last_height:
                break
            last_height = new_height

        self.workflow_list = [workflow.text for workflow in
                              self.driver.find_elements_by_css_selector('st-list-item a > span')]

    # TODO - Make an incrementer list for workflow get, and workflow compare would actually just compare without
    #  doing the get for the second list
    def workflow_compare(self, org):

        self.child_org = org
        writer_time = str(datetime.today().time())

        org_changer(self.driver, org)

        self.driver.get(self.main_url + '/settings/workflows')
        WdWait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        main_content = self.driver.find_element_by_css_selector('body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_content)
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_content)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_content)

            if new_height == last_height:
                break
            last_height = new_height

        new_workflow_list = [workflow.text for workflow in
                             self.driver.find_elements_by_css_selector('st-list-item a > span')]

        # TODO - Check if there is an easier way to handle this

        #  First check the symmetric difference if it returns false (meaning that there isn't a single
        #  differing element) it will check the difference both ways from new org to group and vice versa
        if not set(self.workflow_list).symmetric_difference(set(new_workflow_list)):
            with open(f"Reports/{self.time}/{self.ent} workflow_inheritance.txt", "a+") as wf_inherit:
                wf_inherit.write(writer_time +
                                 'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' no disrepancies noted between workflows\n')
        else:
            not_inherited = [(' ' + workflowino + '\n') for workflowino in self.workflow_list if
                             workflowino not in new_workflow_list]

            if not_inherited:
                with open(f"Reports/{self.time}/{self.ent} workflow_inheritance.txt", "a+") as wf_inherit:
                    wf_inherit.write(writer_time +
                                     'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' the following wasn\'t inherited\n')
                    wf_inherit.writelines(not_inherited)
                    wf_inherit.write('\n')

            not_inherited = [(' ' + workflowino + '\n') for workflowino in new_workflow_list if
                             workflowino not in self.workflow_list]

            if not_inherited:
                with open(f"Reports/{self.time}/{self.ent} workflow_inheritance.txt", "a+") as wf_inherit:
                    wf_inherit.write(
                        writer_time + self.main_url + ' - ' + "Workflows are present in the child org " + self.child_org + ' that are not present in the parent org ' + self.parent_org + ' the following is \'extra\'\n')
                    wf_inherit.writelines(not_inherited)
                    wf_inherit.write('\n')

        sleep(1)

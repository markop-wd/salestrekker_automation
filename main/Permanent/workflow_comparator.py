from datetime import datetime, date
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
# from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait

from main.Permanent.org_funcs import org_changer


class WorkflowCheck:
    def __init__(self, driver: Chrome, ent):
        self.driver = driver
        self.ent = ent
        self.workflow_list = []
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.parent_org = ''
        self.child_org = ''

    def workflow_get(self, org):

        self.parent_org = org

        org_changer(self.driver, org)

        self.driver.get(self.main_url + '/settings/workflows')
        WdWait(self.driver, 30).until(
            ec.visibility_of_element_located((By.TAG_NAME, 'st-list')))
        main_content = self.driver.find_element(by=By.CSS_SELECTOR,
                                                value='body > md-content')

        last_height = self.driver.execute_script(
            "return arguments[0].scrollHeight", main_content)
        sleep(1)
        while True:
            self.driver.execute_script(
                f"arguments[0].scroll(0,{last_height});", main_content)
            sleep(3)
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", main_content)

            if new_height == last_height:
                break
            last_height = new_height

        self.workflow_list = [
            workflow.text for workflow in self.driver.find_elements(
                by=By.CSS_SELECTOR, value='st-list-item a > span')
        ]

    # TODO - Make an incrementer list for workflow get, and workflow compare would actually just compare without
    #  doing the get for the second list
    def workflow_compare(self, org):

        self.child_org = org
        writer_time = str(datetime.today().time())

        org_changer(self.driver, org)

        self.driver.get(self.main_url + '/settings/workflows')
        self.driver.refresh()
        WdWait(self.driver, 30).until(
            ec.visibility_of_element_located((By.TAG_NAME, 'st-list')))
        main_content = self.driver.find_element(by=By.CSS_SELECTOR,
                                                value='body > md-content')

        last_height = self.driver.execute_script(
            "return arguments[0].scrollHeight", main_content)
        sleep(1)
        while True:
            self.driver.execute_script(
                f"arguments[0].scroll(0,{last_height});", main_content)
            sleep(3)
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", main_content)

            if new_height == last_height:
                break
            last_height = new_height

        new_workflow_list = [
            workflow.text for workflow in self.driver.find_elements(
                by=By.CSS_SELECTOR, value='st-list-item a > span')
        ]

        # TODO - Check if there is an easier way to handle this

        #  First check the symmetric difference if it returns false (meaning that there isn't a single
        #  differing element) it will check the difference both ways from new org to group and vice versa
        list_difference = set(self.workflow_list).symmetric_difference(
            set(new_workflow_list))
        if not list_difference:
            with open(f"Reports/{date.today()}/workflow_inheritance.txt",
                      "a+") as wf_inherit:
                wf_inherit.write(self.ent + " - " + writer_time + " - From " + self.parent_org +
                                 " to " + self.child_org +
                                 " no disrepancies noted between workflows\n")
        else:
            not_inherited = [('\t' + workflowino + '\n')
                             for workflowino in self.workflow_list
                             if workflowino not in new_workflow_list]

            if not_inherited:
                with open(f"Reports/{date.today()}/workflow_inheritance.txt",
                          "a+") as wf_inherit:
                    wf_inherit.write(self.ent + " - " + writer_time +
                                     " - From " + self.parent_org + ' to ' +
                                     self.child_org +
                                     " the following wasn't inherited\n")
                    wf_inherit.writelines(not_inherited)
                    wf_inherit.write('\n')

            extra_wfs = [('\t' + workflowino + '\n')
                         for workflowino in new_workflow_list
                         if workflowino not in self.workflow_list]

            if extra_wfs:
                with open(f"Reports/{date.today()}/workflow_inheritance.txt",
                          "a+") as wf_inherit:
                    wf_inherit.write(self.ent + " - " +
                                     writer_time +
                                     " - Following workflows are present in the child org " +
                                     self.child_org +
                                     " that are not present in the parent org " +
                                     self.parent_org + "\n")
                    wf_inherit.writelines(extra_wfs)
                    wf_inherit.write('\n')

        sleep(1)

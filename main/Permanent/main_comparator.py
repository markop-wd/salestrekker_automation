from time import sleep
from datetime import datetime, date

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from main.Permanent.helper_funcs import element_waiter
from main.Permanent.org_funcs import org_changer


def run(driver: Chrome, parent_org: str, child_org: str, wait: bool):
    # Instantiates comparator classes with orgs
    dc = DocumentComparator(driver=driver, child_org=child_org, parent_org=parent_org)
    wf = WorkflowComparator(driver=driver, child_org=child_org, parent_org=parent_org)

    # get the docs/wfs (just calling it with the appropriate org)
    # the result is stored within the class based on which org was given
    dc.document_get(dc.parent_org)
    wf.workflow_get(wf.parent_org)
    if wait:
        sleep(320)
    dc.document_get(dc.child_org)
    wf.workflow_get(wf.child_org)

    # this needs to be called at the end
    # I didn't find a different solutiion at the moment as sleep is between these two classes
    # maybe in the future I can merge them
    wf.wf_comparison_report()
    dc.doc_comparison_report()


class DocumentComparator:

    def __init__(self, driver: Chrome, child_org: str, parent_org: str):
        self.driver = driver
        self.child_org = child_org
        self.parent_org = parent_org
        self.child_list = []
        self.parent_list = []
        self.ent = self.driver.current_url.split('.')[0].split('/')[-1]

    def document_get(self, org):
        if org != self.child_org or org != self.parent_org:
            raise InvalidOrganisationNameException

        org_changer(self.driver, org)
        documents_url = "https://" + self.ent + '.salestrekker.com/settings/documents'

        self.driver.get(documents_url)
        element_waiter(self.driver, css_selector='st-list', url=documents_url)

        main_content = self.driver.find_element(by=By.CSS_SELECTOR,
                                                value='body > md-content')

        last_height = self.driver.execute_script(
            "return arguments[0].scrollHeight", main_content)
        sleep(1)

        while True:
            self.driver.execute_script(
                f"arguments[0].scroll(0,{last_height});", main_content)
            # TODO - remove manual sleep
            sleep(3)
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", main_content)

            if new_height == last_height:
                break
            last_height = new_height

        document_list = [
            document.text for document in self.driver.find_elements(
                by=By.CSS_SELECTOR, value='st-list-item a > content > span')
        ]
        if org == self.child_org:
            self.child_list = document_list
        else:
            self.parent_list = document_list

    def doc_comparison_report(self):

        writer_time = str(datetime.today())

        #  First check the symmetric difference if it returns false (meaning that there isn't a single
        #  differing element) it will check the difference both ways from new org to group and vice versa

        list_difference = set(self.child_list).symmetric_difference(
            set(self.parent_list))
        if not list_difference:
            with open(f"Reports/{date.today()}/document_inheritance.txt",
                      "a+") as doc_inherit:
                doc_inherit.write(self.ent + " - " + writer_time + ' - From ' +
                                  self.parent_org + ' to ' + self.child_org +
                                  ' no disrepancies noted between documents\n')

        else:
            not_inherited = [('\t' + documentino + '\n')
                             for documentino in self.parent_list
                             if documentino not in self.child_list]

            if not_inherited:
                with open(f"Reports/{date.today()}/document_inheritance.txt",
                          "a+") as doc_inherit:
                    doc_inherit.write(self.ent + " - " + writer_time + ' - From ' +
                                      self.parent_org + ' to ' +
                                      self.child_org +
                                      " the following wasn't inherited\n")
                    doc_inherit.writelines(not_inherited)
                    doc_inherit.write('\n')

            extra_docs = [('\t' + documentino + '\n')
                          for documentino in self.child_list
                          if documentino not in self.parent_list]

            if extra_docs:
                with open(f"Reports/{date.today()}/document_inheritance.txt",
                          "a+") as doc_inherit:
                    doc_inherit.write(self.ent + " - " +
                                      writer_time +
                                      " - Documents are present in the child org " +
                                      self.child_org +
                                      ' that are not present in the parent org ' +
                                      self.parent_org + '\n')
                    doc_inherit.writelines(not_inherited)
                    doc_inherit.write('\n')


class WorkflowComparator:

    def __init__(self, driver: Chrome, child_org, parent_org):
        self.driver = driver
        self.child_org = child_org
        self.parent_org = parent_org
        self.child_list = []
        self.parent_list = []
        self.ent = self.driver.current_url.split('.')[0].split('/')[-1]

    def workflow_get(self, org: str):

        if org != self.child_org or org != self.parent_org:
            raise InvalidOrganisationNameException

        org_changer(self.driver, org)
        workflow_url = 'https://' + self.ent + '.salestrekker.com/settings/workflows'

        self.driver.get(workflow_url)
        element_waiter(self.driver, css_selector='st-list', url=workflow_url)

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

        workflow_list = [
            workflow.text for workflow in self.driver.find_elements(
                by=By.CSS_SELECTOR, value='st-list-item a > span')
        ]
        if org == self.child_org:
            self.child_list = workflow_list
        else:
            self.parent_list = workflow_list

    def wf_comparison_report(self):

        writer_time = str(datetime.today())

        #  First check the symmetric difference if it returns false (meaning that there isn't a single
        #  differing element) it will check the difference both ways from new org to group and vice versa

        list_difference = set(self.parent_list).symmetric_difference(
            set(self.child_list))
        if not list_difference:
            with open(f"Reports/{date.today()}/workflow_inheritance.txt",
                      "a+") as wf_inherit:
                wf_inherit.write(self.ent + " - " + writer_time + " - From " + self.parent_org +
                                 " to " + self.child_org +
                                 " no disrepancies noted between workflows\n")
        else:
            not_inherited = [('\t' + workflowino + '\n')
                             for workflowino in self.parent_list
                             if workflowino not in self.child_list]

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
                         for workflowino in self.child_list
                         if workflowino not in self.parent_list]

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


class InvalidOrganisationNameException(Exception):
    """
    Inner exception in case anyone tampers with the main_comparator
    A different not runtime solution should be found
    """
    def __init__(self, message="Organisation name provided to the comparator is not valid"):
        super().__init__(message)

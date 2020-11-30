from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from datetime import datetime

from time import sleep

from main.Permanent.org_funcs import org_changer


class DocumentCheck:

    def __init__(self, driver, ent, time):
        self.ent = ent
        self.driver = driver
        self.document_list = []
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.parent_org = ''
        self.child_org = ''
        self.time = time

    def document_get(self, org):
        # TODO - LABEL

        self.parent_org = org

        org_changer(self.driver, org)

        self.driver.get(self.main_url + '/settings/documents')
        try:
            WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        except exceptions.TimeoutException:
            self.driver.get(self.main_url + '/settings/documents')
            try:
                WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
            except exceptions.TimeoutException:
                self.driver.get(self.main_url + '/settings/documents')
                WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))

        main_content = self.driver.find_element(by=By.CSS_SELECTOR,value='body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_content)
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_content)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_content)

            if new_height == last_height:
                break
            last_height = new_height

        self.document_list = [document.text for document in
                              self.driver.find_elements(by=By.CSS_SELECTOR,value='st-list-item a > content > span')]

    def document_compare(self, org):

        writer_time = str(datetime.today())

        self.child_org = org

        org_changer(self.driver, org)

        self.driver.get(self.main_url + '/settings/documents')
        WdWait(self.driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'st-list')))
        main_content = self.driver.find_element(by=By.CSS_SELECTOR,value='body > md-content')

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", main_content)
        sleep(1)
        while True:
            self.driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_content)
            sleep(3)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", main_content)

            if new_height == last_height:
                break
            last_height = new_height

        new_org_document_list = [document.text for document in
                                 self.driver.find_elements(by=By.CSS_SELECTOR,value='st-list-item a > content > span')]

        # TODO - Check if there is an easier way to handle this

        #  First check the symmetric difference if it returns false (meaning that there isn't a single
        #  differing element) it will check the difference both ways from new org to group and vice versa
        if not set(new_org_document_list).symmetric_difference(set(self.document_list)):
            with open(f"Reports/{self.time}/{self.ent} document_inheritance.txt", "a+") as doc_inherit:
                doc_inherit.write(writer_time +
                                  'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' no disrepancies noted between documents\n')

        else:
            not_inherited = [(' ' + documentino + '\n') for documentino in self.document_list if
                             documentino not in new_org_document_list]

            if not_inherited:
                with open(f"Reports/{self.time}/{self.ent} document_inheritance.txt", "a+") as doc_inherit:
                    doc_inherit.write(writer_time +
                                      'From ' + self.main_url + ' - ' + self.parent_org + ' to ' + self.child_org + ' the following wasn\'t inherited\n')
                    doc_inherit.writelines(not_inherited)
                    doc_inherit.write('\n')

            not_inherited = [(' ' + documentino + '\n') for documentino in new_org_document_list if
                             documentino not in self.document_list]

            if not_inherited:
                with open(f"Reports/{self.time}/{self.ent} document_inheritance.txt", "a+") as doc_inherit:
                    doc_inherit.write(writer_time +
                                      self.main_url + ' - ' + "Documents are present in the child org " + self.child_org + ' that are not present in the parent org ' + self.parent_org + ' the following is \'extra\'\n')
                    doc_inherit.writelines(not_inherited)
                    doc_inherit.write('\n')

        sleep(1)

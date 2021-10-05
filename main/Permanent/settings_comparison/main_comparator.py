from selenium.webdriver import Chrome
from time import sleep

from .workflow_comparator import workflow_get, wf_comparison_report
from .document_comparator import document_get, doc_comparison_report


def run(driver: Chrome, parent_org: str, child_org: str, wait: bool):
    parent_wf_list = workflow_get(driver=driver, org=parent_org)
    parent_doc_list = document_get(driver=driver, org=parent_org)
    if wait:
        sleep(320)
    child_wf_list = workflow_get(driver=driver, org=child_org)
    child_doc_list = document_get(driver=driver, org=child_org)

    ent = driver.current_url.split('.')[0].split('/')[-1]

    wf_comparison_report(ent=ent, child_org=child_org, parent_org=parent_org,
                         child_list=child_wf_list, parent_list=parent_wf_list)

    doc_comparison_report(ent=ent, child_org=child_org, parent_org=parent_org,
                          child_list=child_doc_list, parent_list=parent_doc_list)

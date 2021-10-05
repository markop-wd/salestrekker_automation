from datetime import datetime, date
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from main.Permanent.helper_funcs import element_waiter
from main.Permanent.org_funcs import org_changer


def document_get(driver: Chrome, org: str):

    org_changer(driver, org)
    ent = driver.current_url.split('.')[0].split('/')[-1]
    documents_url = "https://" + ent + '.salestrekker.com/settings/documents'

    driver.get(documents_url)
    element_waiter(driver, css_selector='st-list', url=documents_url)

    main_content = driver.find_element(by=By.CSS_SELECTOR,
                                       value='body > md-content')

    last_height = driver.execute_script(
        "return arguments[0].scrollHeight", main_content)
    sleep(1)

    while True:
        driver.execute_script(
            f"arguments[0].scroll(0,{last_height});", main_content)
        # TODO - remove manual sleep
        sleep(3)
        new_height = driver.execute_script(
            "return arguments[0].scrollHeight", main_content)

        if new_height == last_height:
            break
        last_height = new_height

    document_list = [
        document.text for document in driver.find_elements(
            by=By.CSS_SELECTOR, value='st-list-item a > content > span')
    ]
    return document_list


def doc_comparison_report(ent: str, child_org: str, parent_org: str, child_list: list[str], parent_list: list[str]):

    writer_time = str(datetime.today())

    #  First check the symmetric difference if it returns false (meaning that there isn't a single
    #  differing element) it will check the difference both ways from new org to group and vice versa

    list_difference = set(child_list).symmetric_difference(
        set(parent_list))
    if not list_difference:
        with open(f"Reports/{date.today()}/document_inheritance.txt",
                  "a+") as doc_inherit:
            doc_inherit.write(ent + " - " + writer_time + ' - From ' +
                              parent_org + ' to ' + child_org +
                              ' no disrepancies noted between documents\n')

    else:
        not_inherited = [('\t' + documentino + '\n')
                         for documentino in parent_list
                         if documentino not in child_list]

        if not_inherited:
            with open(f"Reports/{date.today()}/document_inheritance.txt",
                      "a+") as doc_inherit:
                doc_inherit.write(ent + " - " + writer_time + ' - From ' +
                                  parent_org + ' to ' +
                                  child_org +
                                  " the following wasn't inherited\n")
                doc_inherit.writelines(not_inherited)
                doc_inherit.write('\n')

        extra_docs = [('\t' + documentino + '\n')
                      for documentino in child_list
                      if documentino not in parent_list]

        if extra_docs:
            with open(f"Reports/{date.today()}/document_inheritance.txt",
                      "a+") as doc_inherit:
                doc_inherit.write(ent + " - " +
                                  writer_time +
                                  " - Documents are present in the child org " +
                                  child_org +
                                  ' that are not present in the parent org ' +
                                  parent_org + '\n')
                doc_inherit.writelines(not_inherited)
                doc_inherit.write('\n')

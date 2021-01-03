"""
Main business logic
"""
from datetime import date, datetime
import json
import concurrent.futures
from time import sleep

from selenium.common import exceptions
from selenium.webdriver import Chrome,Chrome
from selenium.webdriver.common.by import By

from Permanent.login import LogIn
from Permanent.deal_create import EditDeal
from Permanent.deal_fill import MultipleDealCreator
from Permanent.document_comparator import DocumentCheck
from Permanent.workflow_comparator import WorkflowCheck
from Permanent import org_funcs, user_manipulation, helper_funcs, workflow_manipulation
from mail import mail_get
import filelock


def worker(driver: Chrome, ent: str, email: str = 'matthew@salestrekker.com', password: str = '',
           runner_main_org: str = '',
           runner_learn_org: str = ''):
    with open("perm_vars.json", "r") as perm_json:
        perm_vars = json.load(perm_json)

    test_users = perm_vars['test_users']
    allowed_workflows = perm_vars['workflows'].split('-')


    # hl_workflows = {
    #     "gem": "https://gem.salestrekker.com/board/ba299909-8eb3-4f72-803e-809ee5197e15",
    #     "ynet": "https://ynet.salestrekker.com/board/c1e72ff3-70a3-4425-a7e4-9dc3a15d0f9f",
    #     "vownet": "https://vownet.salestrekker.com/board/67e4c833-c232-4cb0-9069-01ddab1b0fde",
    #     "gemnz": "https://gemnz.salestrekker.com/board/fc760400-f16d-4637-a91d-47af13872b8d",
    #     "platform": "https://platform.salestrekker.com/board/04454b28-33a6-46c8-bc92-8bb1b1eb06ef",
    #     "nlgconnect": "https://nlgconnect.salestrekker.com/board/e1d9450f-14eb-4081-8c45-5e6f74834688",
    #     "app": "https://app.salemailestrekker.com/board/0e192f77-4ff4-4ec9-9daf-7ca6f25a6fd1",
    #     "ioutsource": "https://ioutsource.salestrekker.com/board/f749f86b-07d2-404e-aabe-509c8a7578b7",
    #     "sfg": "https://sfg.salestrekker.com/board/cf28e583-0033-4efe-82f1-a31158baa4e2",
    #     "chief": "https://chief.salestrekker.com/board/50894293-ddef-4cd1-84a2-f490ee5f80df"}

    driver.implicitly_wait(35)
    #
    # new_email, new_password = helper_funcs.user_setup_raw(driver, ent)
    # with open('details.json', 'r') as details:
    #     json_details = json.load(details)
    #     json_details[ent][new_email] = new_password
    # with open('details.json', 'w') as details:
    #     json.dump(json_details, details)

    LogIn(driver, ent, email, password).log_in()
    driver.get("https://dev.salestrekker.com/settings/my-accreditations")

    # # TODO
#     driver.get("https://" + ent + ".salestrekker.com/settings/my-accreditations")
#     # WdWait(driver, 50).until(ec.visibility_of_element_located((By.TAG_NAME, 'st-block-form-content')))

#     try:
#         for delete_button in driver.find_elements(by=By.CSS_SELECTOR, value='button.delete'):
#             try:
#                 driver.execute_script("arguments[0].click();", delete_button)
#             except exceptions.ElementClickInterceptedException:
#                 helper_funcs.element_clicker(driver=driver,web_element=delete_button)
#                 # driver.execute_script("arguments[0].click();", delete_button)
#     except exceptions.NoSuchElementException:
#         pass

#     add_new = driver.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Add new lender accreditation"]')
#     helper_funcs.element_clicker(driver=driver, web_element=add_new)
#     md_select = driver.find_element(by=By.CSS_SELECTOR, value='md-select[ng-change="pickLender(lenderAccreditation)"]')
#     helper_funcs.element_clicker(driver=driver, web_element=md_select)
#     md_select_id = str(md_select.get_attribute('id'))
#     md_select_container_id = str(int(md_select_id.split("_")[-1]) + 1)

#     all_els = driver.find_elements(by=By.CSS_SELECTOR, value=f'#select_container_{md_select_container_id} md-option')
#
#     helper_funcs.element_clicker(driver=driver, web_element=all_els[0])
#
#     # number_els = range(len(all_els) - 1)
#
#     number_els = range(10)
#
#     for _ in number_els:
#         driver.execute_script("arguments[0].click();", add_new)
#         # helper_funcs.element_clicker(driver=driver, web_element=add_new)
#
#     for element in driver.find_elements(by=By.CSS_SELECTOR, value='input[ng-model="lenderAccreditation.brokerIdPrimary"]'):
#         try:
#             driver.execute_script("arguments[0].value=1234;", element)
#             sleep(1)
#
#         except exceptions.ElementClickInterceptedException:
#             element.send_keys('1234')
#
#     all_bre = driver.find_elements(by=By.CSS_SELECTOR,
#                                    value='md-select[ng-change="pickLender(lenderAccreditation)"]')
#
#     for count, element in enumerate(all_bre):
#         if count == 0:
#             continue
#         elif count == 11:
#             break
#
#         # driver.execute_script("arguments[0].click();", element)
#         helper_funcs.element_clicker(driver=driver, web_element=element)
#         md_select_id = str(element.get_attribute('id'))
#         md_select_container_id = str(int(md_select_id.split("_")[-1]) + 1)
#         to_click = driver.find_elements(by=By.CSS_SELECTOR, value=f'#select_container_{md_select_container_id} md-option')[count]
#         driver.execute_script("arguments[0].click();", to_click)
#         # helper_funcs.element_clicker(driver=driver, web_element=to_click)
#
#     helper_funcs.md_toast_wait(driver=driver)

    # sleep(20)


    # new_email, new_password = helper_funcs.user_setup_raw(driver, ent)
    # with open('details.json', 'r') as details:
    #     json_details = json.load(details)
    #     json_details[ent][new_email] = new_password
    # with open('details.json', 'w') as details:
    #     json.dump(json_details, details)

# TODO

    # org_funcs.organization_create(driver, ent, runner_learn_org, runner_main_org)

    # # # TODO - just run documentcheck and give it the the learn org and the new org name at same time
    # document_check = DocumentCheck(driver, ent)
    # workflow_check = WorkflowCheck(driver, ent)
    # document_check.document_get(runner_learn_org)
    # workflow_check.workflow_get(runner_learn_org)

    # sleep(60)

    # org_funcs.org_changer(driver, runner_learn_org)
    # org_funcs.org_changer(driver, f'Test Organization {date.today()}')

    # document_check.document_compare(f'Test Organization {date.today()}')
    # workflow_check.workflow_compare(f'Test Organization {date.today()}')

    # matthew_user = test_users['matthew']
    # email_split = matthew_user['email'].split('@')
    # email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    # user_manipulation.add_user(driver, ent, email=email,
    #                            username=matthew_user['username'])

    # # for user in test_users:
    # #     test_list = user['email'].split('@')
    # #     email = test_list[0] + f'+{date.today().strftime("%d%m%y")}@' + test_list[1]
    # #     user_manipulation.add_user(driver, ent,
    # #                                email=email, username=user['username'],
    # #                                broker=user['broker'], admin=user['admin'],
    # #                                mentor=user['mentor'])

    # for workflow in allowed_workflows:
    #     workflow_manipulation.add_workflow(driver=driver,ent=ent, workflow_type=workflow, wf_owner='Matthew Test')

    # hl_workflow = hl_workflows[ent]
    hl_workflow = 'https://dev.salestrekker.com/board/5041acbd-a041-4d7e-ae1b-2e2a4fa5fe45'

    #
    # deal_create = EditDeal(ent, driver)
    #
    # deal_fill = MultipleDealCreator(ent, driver)
    #
    # new_deal = deal_create.run(workflow=hl_workflow.split('/')[-1], deal_owner_name='Matthew Test')
    #
    # deal_fill.client_profile_input(new_deal)

    print(f'finished {ent}')


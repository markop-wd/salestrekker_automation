"""
Main business logic
"""
from datetime import date, datetime
import json
import concurrent.futures
from time import sleep

from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

import Permanent.client_portal.login
from Permanent.client_portal.portal_fill import PortalFill

from Permanent.login import LogIn
from Permanent.deal_create import EditDeal
from Permanent.deal_fill import MultipleDealCreator
from Permanent.document_comparator import DocumentCheck
from Permanent.workflow_comparator import WorkflowCheck
from Permanent import org_funcs, user_manipulation, helper_funcs, workflow_manipulation
from mail import mail_get
import filelock


def worker(driver: Chrome, ent: str, password: str, runner_main_org: str,
           runner_learn_org: str, email: str = 'helpdesk@salestrekker.com'):
    with open("perm_vars.json", "r") as perm_json:
        perm_vars = json.load(perm_json)

    test_users = perm_vars['test_users']
    allowed_workflows = perm_vars['workflows'].split('-')

    LogIn(driver, ent, email, password).log_in()

    # org_funcs.organization_create(driver, ent, runner_learn_org, runner_main_org)
    # LogIn(driver, ent, email, password).log_in()
    # org_funcs.org_changer(driver, f'Test Organization {date.today()}')
    #
    # matthew_user = test_users['matthew']
    # email_split = matthew_user['email'].split('@')
    # email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    # user_manipulation.add_user(driver, ent, email=email,
    #                            username=matthew_user['username'])
    #
    # user_manipulation.add_user(driver, ent, email=matthew_user['email'],
    #                            username=matthew_user['username'])
    #
    # for workflow in allowed_workflows:
    #     workflow_manipulation.add_workflow(driver=driver, ent=ent, workflow_type=workflow, wf_owner='Matthew Test')
    #
    # new_email, new_password = helper_funcs.user_setup_raw(driver, ent)
    # with open('details.json', 'r') as details:
    #     json_details = json.load(details)
    #     json_details[
    #     ent][new_email] = new_password
    # with open('details.json', 'w') as details:
    #     json.dump(json_details, details)
    #
    # helper_funcs.accreditation_fill(driver, ent)

    # org_funcs.org_changer(driver, f'Test Organization {date.today()}')

    # driver.get(f"https://{ent}.salestrekker.com/settings/import-data")

    # input("Heyo")

    # hl_workflow = hl_workflows[ent]
    workflow = 'https://dev.salestrekker.com/board/ceda438a-1da8-4356-9518-ac7c3bc7823f'

    deal_create = EditDeal(ent, driver)
    deal_fill = MultipleDealCreator(ent, driver)

    # new_deal_hl = deal_create.run(workflow=workflow.split('/')[-1], deal_owner_name='Salestrekker Help Desk')
    new_deal_hl = deal_create.run(workflow=workflow.split('/')[-1], deal_owner_name='Matthew Test', af_type='cons')
    deal_fill.client_profile_input(new_deal_hl)

    new_deal_af = deal_create.run(workflow=workflow.split('/')[-1], deal_owner_name='Matthew Test', af_type='comm')
    deal_fill.client_profile_input(new_deal_af)


    # new_deal_hl = deal_create.run(workflow=hl_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test')
    # deal_create.run(workflow=hl_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test')

    # # new_deal_af = deal_create.run(workflow=af_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test')
    # deal_create.run(workflow=af_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test', af_type='comm')

    # # print(hl, new_deal)

    # deal_fill.client_profile_input("https://dev.salestrekker.com/fact-find/58b2bcee-d020-4beb-a2fb-326def7b5a48/198c95c7-b607-45b0-abef-8404825e8483")

    print(f'finished {ent}')


def worker_main(driver: Chrome, ent: str, password: str, runner_main_org: str,
                runner_learn_org: str, email: str = 'helpdesk@salestrekker.com'):
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
    with open("perm_vars.json", "r") as perm_json:
        perm_vars = json.load(perm_json)

    test_users = perm_vars['test_users']
    allowed_workflows = perm_vars['workflows'].split('-')

    driver.implicitly_wait(20)

    LogIn(driver, ent, email, password).log_in()

    org_funcs.organization_create(driver, ent, runner_learn_org, runner_main_org)

    document_check = DocumentCheck(driver, ent)
    workflow_check = WorkflowCheck(driver, ent)

    document_check.document_get(runner_learn_org)
    workflow_check.workflow_get(runner_learn_org)

    sleep(90)
    # org_funcs.org_changer(driver, f'Test Organization {date.today()}')

    document_check.document_compare(f'Test Organization {date.today()}')
    workflow_check.workflow_compare(f'Test Organization {date.today()}')

    matthew_user = test_users['matthew']
    email_split = matthew_user['email'].split('@')
    email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    user_manipulation.add_user(driver, ent, email=email,
                               username=matthew_user['username'])

    # phillip_user = test_users['phillip']
    # email_split = phillip_user['email'].split('@')
    # email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    # user_manipulation.add_user(driver, ent, email=email,
    #                            username=phillip_user['username'])

    # # for user in test_users:
    # #     test_list = user['email'].split('@')
    # #     email = test_list[0] + f'+{date.today().strftime("%d%m%y")}@' + test_list[1]
    # #     user_manipulation.add_user(driver, ent,
    # #                                email=email, username=user['username'],
    # #                                broker=user['broker'], admin=user['admin'],
    # #                                mentor=user['mentor'])

    for workflow in allowed_workflows:
        workflow_manipulation.add_workflow(driver=driver, ent=ent, workflow_type=workflow, wf_owner='Matthew Test')

    new_email, new_password = helper_funcs.user_setup_raw(driver, ent)
    with open('details.json', 'r') as details:
        json_details = json.load(details)
        json_details[ent][new_email] = new_password
    with open('details.json', 'w') as details:
        json.dump(json_details, details)

    helper_funcs.accreditation_fill(driver, ent)

    sleep(5)


def cp_worker(driver: Chrome, pin: str, link: str):
    driver.implicitly_wait(10)

    Permanent.client_portal.login.LogIn(driver, link, pin).log_in()
    driver.get(link.split('authenticate')[0])
    portal_runner = PortalFill(driver)
    portal_runner.main()
    driver.refresh()
    sleep(20)
    portal_runner.screenshot()


def api(driver: Chrome, ent: str, password: str, email: str = 'helpdesk@salestrekker.com'):

    LogIn(driver, ent, email, password).log_in()

    print(f'finished {ent}')

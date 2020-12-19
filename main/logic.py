"""
Main business logic
"""
from datetime import date, datetime
import json
import concurrent.futures
from time import sleep

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

from Permanent.login import LogIn
from Permanent.deal_create import EditDeal
from Permanent.deal_fill import MultipleDealCreator
from Permanent.document_comparator import DocumentCheck
from Permanent.workflow_comparator import WorkflowCheck
from Permanent import org_funcs, user_manipulation, helper_funcs, workflow_manipulation
from mail import mail_get
import filelock


def worker(driver: Firefox, ent: str, email: str = 'matthew@salestrekker.com', password: str = '',
           runner_main_org: str = '',
           runner_learn_org: str = '', org_list: list = None):

    # with open("perm_vars.json", "r") as perm_json:
    #     perm_vars = json.load(perm_json)

    # all_orgs = ["**MAKE YOUR OWN** Matt Test Group (QA automation testing)", "10,001 Deals",
    #             "3 Demo N Co", "@Maya test Group", "Access Funds", "Ana Test Branch",
    #             "Ana Test Group", "API Testing", "ATF Wealth Accelerator", "Automated Tests",
    #             "Award Mortgage", "Branch 20042020", "Branch 20042020 2", "Branch 20042020 3",
    #             "branch 2505", "Branch Test 19012020", "branch test new 19012020", "Branchino",
    #             "Branchino2", "Branchino3", "C21 API Test", "Changing name org test",
    #             "Child Service Testing", "CommsTest", "CungaLunga", "Deploy 1805", "Deploy 3006",
    #             "Dinar Playground", "Dinar Test", "Dinar Test Branch", "Doc labels test branch",
    #             "Finance Service Testing", "Finding Nemo", "Group 12/10", "Group 20042020 2",
    #             "group 2801", "Group MTFK", "Group Test 14012020", "Group Test 19012020",
    #             "Group Test No2", "Groupino", "Groupino2", "Hello ma BEJbi", "I-BRANCH", "I-GROUP",
    #             "Import Test", "INHERIT branch", "inherit branch", "inherit group",
    #             "INHERIT group test", "inheritance test org 27/03", "ioutsource UAT",
    #             "KreativnoIZanimljivoImeOrganizacije.....Test",
    #             "KreativnoIZanimljivoImeOrganizacije.....Test",
    #             "KreativnoIZanimljivoImeOrganizacije.....Test",
    #             "KreativnoIZanimljivoImeOrganizacije.....Test", "Labels TEST",
    #             "Lilly Group Pty Ltd", "Lilly Org", "maya test", "maya test 16/06",
    #             "Maya test branch", "maya test group 16/06", "MlekoISir", "Mobile Apps Test",
    #             "NemamViseIdejaKakoDaNazovemOrganizaciju...Test", "Nemanja's group", "new branch",
    #             "New Branch 13/12/2019", "New Branch Service Testing", "NEW GOD STAGOD",
    #             "New Group 13/12/2019", "new test group", "New Zealand Test",
    #             "newly added test branch", "Nextgen Broking", "NotificationDelaySent", "NZ branch",
    #             "NZ branch 25 05", "NZ branch 2804", "NZ Group", "NZ Group 2804", "NZ Inherit",
    #             "NZ Test", "NZ test 24042020", "NZ test 28042020", "org 07042020",
    #             "org new test 02/04", "organization 12/10", "Organization 12/10 A",
    #             "organization 7/04", "organization A.version dev", "Organization test 26/03",
    #             "Parent Service Testing", "Platform Demo", "QA Team Test Ground", "Ramo Ramo",
    #             "Resolve Finance", "Services testing", "SFG Functionality Testing",
    #             "Short Test Organization 2020-03-31", "Shroogle DEV", "STB", "STB 2", "STB1",
    #             "Stefan Test", "STG", "STG 2", "STG1", "Test", "test 1", "Test Add User",
    #             "Test BOrganisation 2020-04-28", "Test Branch Scott 2", "test change name org",
    #             "Test Group Scott", "test group to be deleted", "Test New Group",
    #             "Test org 23042020", "Test Organization 2020-04-28", "Test Organization 2020-04-28",
    #             "Test Organization 2020-04-29", "Test Organization 2020-04-30",
    #             "Test Organization 2020-05-01", "Test Organization 2020-05-08",
    #             "Test Organization 2020-05-11", "Test Organization 2020-05-12",
    #             "Test Organization 2020-05-29", "Test Organization 2020-06-30",
    #             "Test Organization 2020-07-01", "Test Organization 2020-09-04",
    #             "Test Organization 2020-12-09", "testing brach", "ThisIsTotallyABranch",
    #             "ThisIsTotallyAGroup", "ThisIsTotallyAnotherBranch", "ThisIsTotallyAThirdBranch",
    #             "Ugabuga", "xSource ApplyOnline Training Organisation"]

    LogIn(driver, ent, email, password).log_in()
    # for org in org_list:
    #     org_funcs.org_changer(driver, org)
    #     print('Currently in', org)
    #
    #     try:
    #         all_users = user_manipulation.return_all_users(driver, ent)
    #     except:
    #         continue
    #     else:
    #
    #         org_name = driver.find_element(by=By.CSS_SELECTOR,
    #                                        value='st-avatar[organization] > img').get_attribute('alt')
    #         fl = filelock.FileLock("current_vars.json")
    #         with fl:
    #             with open("current_vars.json", "r") as writing:
    #                 load_dict = json.load(writing)
    #
    #         try:
    #             date_updated = load_dict[ent][org_name]['date']
    #         except KeyError:
    #             load_dict[ent].update({org_name: {"users": all_users, "date": str(datetime.today())}})
    #             with fl:
    #                 with open("current_vars.json", "w") as writing:
    #                     json.dump(load_dict, writing)
    #
    #         else:
    #             dict_date = datetime.strptime(date_updated.split(' ')[0], '%Y-%m-%d').date()
    #             if dict_date < date.today():
    #                 load_dict[ent][org_name].update({"users": all_users, "date": str(datetime.today())})
    #                 with fl:
    #                     with open("current_vars.json", "w") as writing:
    #                         json.dump(load_dict, writing)

    # hl_workflows = {
    #     "gem": "https://gem.salestrekker.com/board/66392b75-efed-4fb5-b250-ae6f8ff117d2",
    #     "ynet": "https://ynet.salestrekker.com/board/053b299d-4e9b-4cf2-9cd2-62565368ceb4",
    #     "vownet": "https://vownet.salestrekker.com/board/9ce60451-ec50-4189-97f3-324a0bda739a",
    #     "gemnz": "https://gemnz.salestrekker.com/board/52a7f2be-5eb1-4f51-a936-25e8cb9ccb41",
    #     "platform": "https://platform.salestrekker.com/board/49501dc2-c191-4bde-8cf7-03470daa77cd",
    #     "nlgconnect": "https://nlgconnect.salestrekker.com/board/cc97584b-6f1c-4aec-aef5-b8910498676f",
    #     "app": "https://app.salestrekker.com/board/ea831fdf-94a8-4f58-9b9d-d14d1b9c9d09",
    #     "ioutsource": "https://ioutsource.salestrekker.com/board/a56877f4-c238-4348-9cad-35b287080a5a",
    #     "sfg": "https://sfg.salestrekker.com/board/23cba2d2-a140-4f91-bb32-a366eaed305e",
    #     "chief": "https://chief.salestrekker.com/board/7fc07c5b-9a54-481b-bb41-09ee6092e8ed"}

    # helper_funcs.user_setup_raw(driver, ent)
    # LogIn(driver, ent, 'matthew+091220@salestrekker.com', "fZ8['G1fB-j_x3").log_in()
    # test_users = perm_vars['test_users']
    # org_funcs.organization_create(driver, ent, runner_learn_org, runner_main_org)

    # # # TODO - just run documentcheck and give it the the learn org and the new org name at same time
    # document_check = DocumentCheck(driver, ent)
    # workflow_check = WorkflowCheck(driver, ent)

    # document_check.document_get(runner_learn_org)
    # workflow_check.workflow_get(runner_learn_org)

    # org_funcs.org_changer(driver, runner_main_org)
    # # org_funcs.org_changer(driver, f'Test Organization {date.today()}')
    #
    # document_check.document_compare(f'Test Organization {date.today()}')
    # workflow_check.workflow_compare(f'Test Organization {date.today()}')
    #
    # matthew_user = test_users['matthew']
    # email_split = matthew_user['email'].split('@')
    # email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    # user_manipulation.add_user(driver, ent, email=email,
    #                            username=matthew_user['username'])
    #
    # # for user in test_users:
    # #     test_list = user['email'].split('@')
    # #     email = test_list[0] + f'+{date.today().strftime("%d%m%y")}@' + test_list[1]
    # #     user_manipulation.add_user(driver, ent,
    # #                                email=email, username=user['username'],
    # #                                broker=user['broker'], admin=user['admin'],
    # #                                mentor=user['mentor'])
    #
    # wf_manipulate = WorkflowManipulation(driver, ent)
    # allowed_workflows = perm_vars['workflows'].split('-')
    # for workflow in allowed_workflows:
    #     wf_manipulate.add_workflow(workflow_type=workflow)

    # hl_workflow = hl_workflows[ent]
    #
    hl_workflow = 'https://dev.salestrekker.com/board/d016d318-0d3c-48cb-9fe5-0f9d238e9ab9'

    # deals = [
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/9809a778-610c-4ccc-85ae-c3263a1b76e1",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/a33674fe-5194-4a34-ba46-496fa5ae1966",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/8fe805a4-7d4d-455a-952b-935d8ce76109",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/7b608635-7c30-4d22-92e0-dcb598112205",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/a30103b1-9761-487f-9454-9148038d7a61",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/ae4f83c7-5a94-47f7-be3e-a539d175b0d5",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/ed71c17c-887f-48bd-a9d7-64eed0e3cad6",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/06d7abe8-91f6-48ec-84a7-2139807cebaa",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/a756fda3-aaa4-4f29-b2f9-dc71bb61b1b4",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/36b9bd1a-7fff-45ba-ac0d-2b872ca703a8",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/946a5b25-ab44-4794-9439-9b8555989a0c",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/e2765306-0cd5-4bb6-862f-336fd9ec802e",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/3ea64bae-893d-4add-bb63-dd009e28d9c3",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/1e5e25fb-db61-4799-8f75-1ce517866be0",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/a3526ac9-f2eb-4ccb-b88b-8a1d107ff063",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/ab9fbe8d-0a7b-4c80-9d6c-53ee58855181",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/d8467704-8a7c-4225-b6cc-c6123324df5a",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/6151a089-bafc-4043-9e5c-39fb23839543",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/786d8a13-23c4-4e34-b809-06099062463a",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/c955e5e3-e1db-4742-ad1e-a7a651f4a584",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/c6cb922e-74d5-454f-97d9-a1bf3db7c2b7",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/7f0909d7-afc2-4f89-bb2a-49d8ea41725e",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/a01c76c3-f595-4320-8365-d16ddfc6be12",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/af202a8c-2ce6-48cc-aa0a-fba10c90c3ea",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/15002f90-3283-47e7-8d9f-478253bd1d92",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/56402e3f-1623-4b58-8a5a-2a52b899f7f8",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/6d67d317-fa83-4962-a032-447ded13e709",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/b8cbc771-26e8-4516-b80b-e0303712c5f4",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/ea782cff-1732-4e13-9240-babd4a4befe7",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/b84fcdb6-adaf-4a5f-96ca-bd3a66e5bd89",
    #     "https://dev.salestrekker.com/deal/850abfe9-c7b7-4f79-9f53-425154be44dc/7dc2ae8d-23ba-44a7-b1db-79467131ff88"]

    deal_create = EditDeal(ent, driver)

    deal_fill = MultipleDealCreator(ent, driver)

    new_deal = deal_create.run(workflow=hl_workflow.split('/')[-1], deal_owner_name='Marko P')

    deal_fill.client_profile_input(new_deal)

    # for i in range(1, 10):
    #     deal_create.create_deal(workflow=hl_workflow.split('/')[-1],
    #                             settlement_date=f'0{i}/12/2020')
    # for i in range(10, 32):
    #     deal_create.create_deal(workflow=hl_workflow.split('/')[-1], settlement_date=f'{i}/12/2020')

    # for count,deal in enumerate(deals):
    #     print(f'{count} started')
    #     deal_fill.client_profile_input(deal)
    #     print(f'{count} finished')

    print(f'finished {ent}')

"""
Main business logic.
This is where you call all of the modules/functions and organize them.

Once there is a GUI this should be repurposed so that buttons call their respective functions.
"""
import json
import os
from datetime import date, datetime
from time import sleep

from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

from main.Permanent import org_funcs, user_manipulation, workflow_manipulation, login
from main.Permanent.deal_create.deal_create import CreateDeal
from Permanent.deal_fill import FillDeal
from main.Permanent import main_comparator


def test_worker(ent: str = 'dev', password: str = "+!'Y$pE+{Bw_oXB.",
                email: str = 'matthew@salestrekker.com'):
    """
    Just a simple test worker, that I call from runner for customized tasks

    Args:
        email:
        password:
        ent (object):
    """
    start_time = datetime.now()
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_PRINT_FIRST_LINE'] = 'False'

    driver = Chrome(executable_path=ChromeDriverManager().install())

    login.run(driver, ent, email, password)
    org_funcs.org_changer(driver, '# Enterprise')

    workflow_manipulation.get_deals(driver, 'dev', all_deals=True)


    sleep(3)
    print(f'finished {ent}', datetime.now() - start_time)


def simple_worker(driver: Chrome, ent: str, password: str, email: str = 'helpdesk@salestrekker.com',
                  con_arg: int = None):
    """
    Just a simple test worker, that I call from runner for customized tasks

    Args:
        con_arg:
        email:
        password:
        driver:
        ent (object):
    """

    start_time = datetime.now()

    login.run(driver, ent, email, password)

    org_funcs.org_changer(driver, 'Test Organization 2021-10-05')

    af_workflow = ''
    for workflow in workflow_manipulation.get_all_workflows(driver, ent):
        if "Test WF - Asset Finance" in workflow['name']:
            af_workflow = workflow['link']

    if af_workflow:
        deal_create = CreateDeal(ent, driver)
        deal_fill = FillDeal(driver)
        # hd_username = user_manipulation.get_current_username(driver)
        if af_workflow:
            deal_link = deal_create.run(workflow=af_workflow, deal_owner_name='Marko P',
                                        af_type='cons',
                                        client_email='matthew@salestrekker.com')
            deal_fill.run(deal_link)

            deal_link = deal_create.run(workflow=af_workflow, deal_owner_name='Marko P',
                                        af_type='comm',
                                        client_email='matthew@salestrekker.com')
            deal_fill.run(deal_link)

    sleep(3)
    print(f'finished {ent}', datetime.now() - start_time)


def worker(driver: Chrome, ent: str, password: str, email: str = 'helpdesk@salestrekker.com',
           con_arg=None):
    """
    Just a simple test worker, that I call from runner for customized tasks

    Args:
        con_arg:
        email:
        password:
        driver:
        ent (object):
    """
    start_time = datetime.now()
    print('start', ent if not con_arg else con_arg)
    # with open("perm_vars.json", "r") as perm_json:
    #     perm_vars = json.load(perm_json)

    # runner_learn_org = perm_vars['ents_info'][ent]['learn']
    # runner_main_org = perm_vars['ents_info'][ent]['main']
    # test_users = perm_vars['test_users']
    # allowed_workflows = perm_vars['workflows'].split('-')

    login.run(driver, ent, email, password)
    # org_funcs.org_changer(driver, 'Dinar Playground')

    # ContactCreate(driver).main_contact_create_logic()

    # deal_create = CreateDeal(ent, driver)
    # url = deal_create.run()
    # FillDeal(driver).run(url)

    #
    # org_funcs.organization_create(driver, ent, runner_learn_org, runner_main_org)
    # LogIn(driver, ent, email, password).log_in()
    #
    # org_funcs.org_changer(driver, f'Test Organization {date.today()}')
    # # org_funcs.org_changer(driver, '# Enterprise')
    #
    # # org_funcs.org_changer(driver, runner_main_org)
    # # orgi_name = '# Enterprise'
    # # org_funcs.org_changer(driver, orgi_name)
    #
    # matthew_user = test_users['matthew']
    # email_split = matthew_user['email'].split('@')
    # email = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    # user_manipulation.add_user(driver, ent, email=email,
    #                            username=matthew_user['username'], broker=False, admin=False)
    #
    # # user_manipulation.add_user(driver, ent, email=matthew_user['email'],
    # #                            username=matthew_user['username'])
    # #
    # for name, values in test_users.items():
    #     # First split the email then append the current date to before the @ - so instead of phillip@salestrekker.com this will create phillip+240321@salestrekker.com
    #     email_split = values['email'].split('@')
    #     email_with_date = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    #
    #     user_manipulation.add_user(driver, ent,
    #                                email=email_with_date, username=values['username'],
    #                                broker=False, admin=False,
    #                                mentor=False)
    #
    # for name, values in test_users.items():
    #     user_manipulation.add_user(driver, ent,
    #                                email=values['email'], username=values['username'],
    #                                broker=True, admin=True,
    #                                mentor=False)
    #
    # hl_workflow = ''
    # af_workflow = ''
    #
    # for workflow in allowed_workflows:
    #     workflow_manipulation.add_workflow(driver=driver, ent=ent, workflow_type=workflow,
    #                                        wf_owner='Marko P')
    #
    # # workflow = 'https://dev.salestrekker.com/board/'
    # # af_wf_id = 'd7eedafa-d622-4ac9-b260-9199237de346'
    # # af_workflow = workflow + af_wf_id
    # hl_workflow = 'https://dev.salestrekker.com/board/24d94478-fe9f-43c8-ad5b-b63227dc5cdf'
    # # wff = 'https://dev.salestrekker.com/board/d016d318-0d3c-48cb-9fe5-0f9d238e9ab9'
    #
    # # config_deal_create(driver, ent, hl_workflow, con_arg)
    #
    # # deal_fill = MultipleDealCreator(driver)
    # # af_types = ['cons', 'comm']
    #
    # #     link = f'https://dev.salestrekker.com/deal/asset-finance/{af_wf_id}/' + link.split('/')[-1]
    # #     glass_test(driver, ent, link)
    #
    # # deal_fill.client_profile_input(link)
    # # driver.refresh()
    # # for workflow in workflow_manipulation.get_all_workflows(driver, ent):
    # #     if "Test WF - Asset Finance" in workflow['name']:
    # #         af_workflow = workflow['link']
    # #     if "Test WF - Home Loan" in workflow['name']:
    # #         hl_workflow = workflow['link']
    #
    # # if af_workflow or hl_workflow:
    # #     deal_create = EditDeal(ent, driver)
    # #     deal_fill = MultipleDealCreator(driver)
    # #     # hd_username = user_manipulation.get_current_username(driver)
    # #
    # #     if af_workflow:
    # #         # deal_link = deal_create.run(workflow=af_workflow, deal_owner_name='Phillip Djukanovic', af_type='comm', client_email='matthew@salestrekker.com')
    # #         # deal_fill.client_profile_input(deal_link)
    #
    # #         deal_link = deal_create.run(workflow=af_workflow, deal_owner_name='Phillip Djukanovic', af_type='cons', client_email='matthew@salestrekker.com')
    # #         deal_fill.client_profile_input(deal_link)
    # #     if hl_workflow:
    # #         deal_link = deal_create.run(workflow=hl_workflow, deal_owner_name='Phillip Djukanovic', client_email='matthew@salestrekker.com')
    # #         deal_fill.client_profile_input(deal_link)
    #
    # # new_email, new_password = helper_funcs.user_setup_raw(driver, ent)
    # # with open('details.json', 'r') as details:
    # #     json_details = json.load(details)
    # #     json_details[
    # #     ent][new_email] = new_password
    # # with open('details.json', 'w') as details:
    # #     json.dump(json_details, details)
    #
    # # helper_funcs.accreditation_fill(driver, ent)
    #
    # # org_funcs.org_changer(driver, f'Test Organization {date.today()}')
    #
    # # driver.get(f"https://{ent}.salestrekker.com/settings/import-data")
    #
    # # input("Heyo")
    #
    # # hl_workflow = hl_workflows[ent]
    # # hl_workflow = 'https://dev.salestrekker.com/board/de975f9c-e6db-42d3-99e9-c9c4e77b11f5'
    #
    # # workflows = ['https://dev.salestrekker.com/settings/workflow/64c691a1-14a9-4552-a4f8-bc21cdfffee6',
    # #              'https://dev.salestrekker.com/settings/workflow/d61756d6-2572-4f10-86ae-7560dc040a4d']
    # # owners = ['Maya Test', 'Matthew Test', 'Zac Test', 'Phillip Test']
    # # af_workflow = 'https://dev.salestrekker.com/board/30b94e85-3d1f-491e-a558-6172c618451d'
    # # for workflow in workflows:
    # #     workflow_manipulation.add_users_to_workflow(driver, ent, workflow, owners)
    #
    # # deal_create = EditDeal(ent, driver)
    # # deal_fill = MultipleDealCreator(driver)
    # # deal_link = deal_create.run(workflow=hl_workflow, deal_owner_name='Marko P')
    # # deal_fill.client_profile_input(deal_link)
    #
    # # for _ in range(3):
    # #     new_deal_hl = deal_create.run(workflow=hl_workflow.split('/')[-1], deal_owner_name='Marko P')
    # #     deal_fill.client_profile_input(new_deal_hl)
    #
    # # for _ in range(5):
    # #     new_deal_hl = deal_create.run(workflow=af_workflow.split('/')[-1], deal_owner_name='Matthew Test')
    # #     if random.choice([1, 2, 3, 4]) == 2:
    # #         deal_fill.client_profile_input(new_deal_hl)
    #
    # # deal_create.run(workflow=hl_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test')
    #
    # # # new_deal_af = deal_create.run(workflow=af_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test')
    # # deal_create.run(workflow=af_workflows[ent].split('/')[-1], deal_owner_name='Matthew Test', af_type='comm')
    #
    # # # print(hl, new_deal)
    #
    # # deal_fill.client_profile_input("https://dev.salestrekker.com/fact-find/58b2bcee-d020-4beb-a2fb-326def7b5a48/198c95c7-b607-45b0-abef-8404825e8483")
    # # new_email, new_password = helper_funcs.user_setup_raw(driver, ent)
    # # with open('details.json', 'r') as details:
    # #     json_details = json.load(details)
    # #     json_details[ent][new_email] = new_password
    # # with open('details.json', 'w') as details:
    # #     json.dump(json_details, details)
    #
    # sleep(5)
    print(f'finished {ent if not con_arg else con_arg}', datetime.now() - start_time)
    # # print(f'finished {ent}')


# The logic here is mostly static and includes the main rundown. Login, create an organization, add users,
# the workflows, add all types of deals
def worker_main(driver: Chrome, ent: str, password: str, email: str = 'helpdesk@salestrekker.com', *args, **kwargs):
    """
    The logic here is mostly static and includes the main rundown.
    Login, create an organization, add users, the workflows, add all types of deals
    """

    # Perm vars contain all the main and learn organization names, types of workflows, which users to add and with
    # which permissions
    with open("perm_vars.json", "r") as perm_json:
        perm_vars = json.load(perm_json)

    test_users = perm_vars['test_users']
    allowed_workflows = perm_vars['workflows'].split('-')
    runner_learn_org = perm_vars['ents_info'][ent]['learn']
    runner_main_org = perm_vars['ents_info'][ent]['main']

    driver.implicitly_wait(20)

    login.run(driver, ent, email, password)

    org_funcs.organization_create(driver, ent, runner_learn_org, runner_main_org)

    # Compares both wfs and docs between two orgs
    main_comparator.run(driver=driver, parent_org=runner_learn_org,
                        child_org=f'Test Organization {date.today()}', wait=True)

    # make sure you are in the proper Test Org
    org_funcs.org_changer(driver=driver, org_name=f'Test Organization {date.today()}')

    # Add all users defined in perm_var.json
    email_spli = test_users['matthew']['email'].split('@')
    date_email = email_spli[0] + f'+{date.today().strftime("%d%m%y")}@' + email_spli[1]
    user_manipulation.add_user(driver, ent,
                               email=date_email, username=test_users['matthew']['username'],
                               broker=False, admin=False,
                               mentor=False)

    # for name, values in test_users.items():
    #     # First split the email then append the current date to before the @ - so instead of phillip@salestrekker.com this will create phillip+240321@salestrekker.com
    #     email_split = values['email'].split('@')
    #     email_with_date = email_split[0] + f'+{date.today().strftime("%d%m%y")}@' + email_split[1]
    #
    #     user_manipulation.add_user(driver, ent,
    #                                email=email_with_date, username=values['username'],
    #                                broker=False, admin=False,
    #                                mentor=False)

    # driver.refresh()
    sleep(5)
    user_manipulation.add_user(driver, ent,
                               email=test_users['matthew']['email'], username='Marko P',
                               broker=test_users['matthew']['broker'],
                               admin=test_users['matthew']['admin'],
                               mentor=test_users['matthew']['mentor'])

    user_manipulation.add_user(driver, ent,
                               email=test_users['phillip']['email'], username='Phillip Djukanovic',
                               broker=test_users['phillip']['broker'],
                               admin=test_users['phillip']['admin'],
                               mentor=test_users['phillip']['mentor'])

    # for name, values in test_users.items():
    #     user_manipulation.add_user(driver, ent,
    #                                email=values['email'], username=values['username'],
    #                                broker=values['broker'], admin=values['admin'],
    #                                mentor=values['mentor'])

    # Add all workflows defined in perm_vars.json
    for workflow in allowed_workflows:
        workflow_manipulation.add_workflow(driver=driver, ent=ent, workflow_type=workflow,
                                           wf_owner='Phillip Djukanovic')

    sleep(5)
    driver.refresh()
    hl_workflow = ''
    af_workflow = ''
    for workflow in workflow_manipulation.get_all_workflows(driver, ent):
        if "Test WF - Home Loan" in workflow['name']:
            hl_workflow = workflow['link']
        if "Test WF - Asset Finance" in workflow['name']:
            af_workflow = workflow['link']

    if hl_workflow or af_workflow:
        deal_create = CreateDeal(ent, driver)
        deal_fill = FillDeal(driver)
        # hd_username = user_manipulation.get_current_username(driver)
        if hl_workflow:
            deal_link = deal_create.run(workflow=hl_workflow, deal_owner_name='Phillip Djukanovic',
                                        client_email='matthew@salestrekker.com')
            deal_fill.run(deal_link)
        if af_workflow:
            deal_link = deal_create.run(workflow=af_workflow, deal_owner_name='Phillip Djukanovic',
                                        af_type='cons',
                                        client_email='matthew@salestrekker.com')
            deal_fill.run(deal_link)

            deal_link = deal_create.run(workflow=af_workflow, deal_owner_name='Phillip Djukanovic',
                                        af_type='comm',
                                        client_email='matthew@salestrekker.com')
            deal_fill.run(deal_link)

    # TODO - new user handling via received e-mail to st.receive@gmail
    # helper_funcs.accreditation_fill(driver, ent)

    sleep(5)


def cp_worker(driver: Chrome, pin: str, link: str):
    from Permanent.client_portal import login, portal_fill
    # Client portal handling logic
    driver.implicitly_wait(10)

    # TODO - Refactor login.log_in call (same with portal_fill)
    login.log_in(driver, link, pin)
    driver.get(link.split('authenticate')[0])
    portal_runner = portal_fill.PortalFill(driver)
    driver.refresh()
    sleep(20)
    portal_runner.screenshot()


if __name__ == "__main__":
    test_worker()

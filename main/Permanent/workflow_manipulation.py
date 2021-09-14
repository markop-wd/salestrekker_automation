import json
from datetime import date, datetime
import random
from time import sleep
from pathlib import Path

from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

from main import filelock
from main.Permanent import user_manipulation
from main.Permanent.helper_funcs import element_waiter, element_clicker, element_dissapear
from main.Permanent.user_manipulation import return_all_users, get_current_username


def get_deals(driver, ent: str, all_deals=True, workflow_id=''):
    all_deals_list = []

    if all_deals:
        all_wfs = get_all_workflows(driver, ent)

        for wf in all_wfs:
            driver.get(wf)
            WdWait(driver, 15).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, 'body > md-content > board')))

            element_with_scroll = WdWait(driver, 15).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, 'body > md-content > board')))

            scroll_height_total = driver.execute_script("return arguments[0].scrollHeight",
                                                        element_with_scroll)
            scroll_height_new = 0
            while scroll_height_total != scroll_height_new:
                driver.execute_script(f"arguments[0].scroll(0,{scroll_height_total});",
                                      element_with_scroll)
                sleep(1)
                # WdWait(driver, 50).until(ec.invisibility_of_element_located((By.TAG_NAME, 'md-progress-linear.ng-scope')))
                scroll_height_new = scroll_height_total
                scroll_height_total = driver.execute_script("return arguments[0].scrollHeight",
                                                            element_with_scroll)

            all_deals_list = [deal.get_attribute('href') for deal in
                              driver.find_elements(by=By.CSS_SELECTOR, value='st-ticket-tile > a')]

    else:
        driver.get(workflow_id)
        WdWait(driver, 15).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'body > md-content > board')))
        element_with_scroll = WdWait(driver, 15).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'body > md-content > board')))

        scroll_height_total = driver.execute_script("return arguments[0].scrollHeight",
                                                    element_with_scroll)
        scroll_height_new = 0
        while scroll_height_total != scroll_height_new:
            driver.execute_script(f"arguments[0].scroll(0,{scroll_height_total});",
                                  element_with_scroll)
            sleep(1)
            scroll_height_new = scroll_height_total
            scroll_height_total = driver.execute_script("return arguments[0].scrollHeight",
                                                        element_with_scroll)

        all_deals_list = [deal.get_attribute('href') for deal in
                          driver.find_elements(by=By.CSS_SELECTOR, value='st-ticket-tile > a')]

    return all_deals_list


def add_workflow(driver: Chrome, ent: str, workflow_type='Home Loan',
                 add_all_users=True, wf_owner='', workflow_name=''):
    """
    adding a workflow to the current organization
    valid_wfs = {'None', 'Asset Finance', 'Commercial Loan', 'Conveyancing', 'Home Loan',
             'Insurance', 'Personal Loan', 'Real Estate'}
    """

    main_url = "https://" + ent + ".salestrekker.com"

    if not workflow_name:
        workflow_name = f'Test WF - {workflow_type} - {date.today()}'

    assert "salestrekker" in driver.current_url, 'invalid url'
    assert "authenticate" not in driver.current_url, 'you are at a login page'

    driver.get(main_url + "/settings/workflow/0")
    element_waiter(driver, css_selector='st-block.mb0', url=f'{main_url}/settings/workflow/0')

    if add_all_users:
        # Lock the file before accessing it (due to multithreading issues)
        all_users = extract_all_users(driver, ent)

        add_users_to_workflow(driver=driver, ent=ent, users=all_users)
    else:
        user = get_current_username(driver)
        driver.find_element(by=By.CSS_SELECTOR, value='div:nth-child(6) input').send_keys(
            user + Keys.ENTER)

    _wf_type(driver, workflow_type)

    _owner_select(driver, wf_owner)

    # From here
    new_stages = random.randint(0, 5)
    while new_stages > 0:
        element_clicker(driver, css_selector='span > button')
        new_stages -= 1

    sleep(1)
    driver.find_element(by=By.CSS_SELECTOR,
                        value='st-block-form-content > div > div:first-child > md-input-container > input').send_keys(
        workflow_name)

    # number_of_stages = len(driver.find_elements(by=By.CSS_SELECTOR,value='workflow-stages > workflow-stage'))
    try:
        WdWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))
    except exceptions.TimeoutException:
        sleep(7)
    else:
        WdWait(driver, 10).until(
            ec.invisibility_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))

    # TODO - Confirm that the workflow exists


def _owner_select(driver: Chrome, wf_owner: str):
    element_clicker(driver, css_selector='st-block-form-content > div > div:nth-child(3)')
    owner_select_id = str(driver.find_element(by=By.CSS_SELECTOR,
                                              value='st-block-form-content >div >div:nth-child(3) > md-input-container > md-select').get_attribute(
        'id'))
    owner_select_container_id = str(int(owner_select_id.split("_")[-1]) + 1)
    WdWait(driver, 10).until(
        ec.element_to_be_clickable((By.ID, "select_container_" + owner_select_container_id)))
    deal_owners = driver.find_elements(by=By.CSS_SELECTOR,
                                       value="div#select_container_" + owner_select_container_id + " md-option")
    if not wf_owner:
        user = get_current_username(driver)
        sleep(0.1)
        for deal_owner in deal_owners:
            span = deal_owner.find_element(by=By.TAG_NAME, value='span')
            if span.text == user:
                element_clicker(driver, web_element=deal_owner)
                break
    else:
        user = wf_owner
        owners = []
        sleep(0.1)
        for deal_owner in deal_owners:
            loop_owner = deal_owner.find_element(by=By.TAG_NAME, value='span').text
            owners.append(loop_owner)
            if loop_owner == user:
                element_clicker(driver, web_element=deal_owner)
                break
        else:
            user = get_current_username(driver)
            sleep(0.1)
            for deal_owner in deal_owners:
                span = deal_owner.find_element(by=By.TAG_NAME, value='span')
                if span.text == user:
                    element_clicker(driver, web_element=deal_owner)
                    break


def _wf_type(driver: Chrome, workflow_type: str):
    wf_select_id = str(driver.find_element(by=By.CSS_SELECTOR,
                                           value='st-block-form-content >div >div:nth-child(4) > md-input-container > md-select').get_attribute(
        'id'))
    wf_select_container_id = str(int(wf_select_id.split("_")[-1]) + 1)
    # don't look at me like that, this was the safer route... I think
    element_clicker(driver=driver, css_selector='st-block-form-content > div > div:nth-child(4)')
    WdWait(driver, 10).until(
        ec.element_to_be_clickable((By.ID, "select_container_" + wf_select_container_id)))
    workflow_types = driver.find_elements(by=By.CSS_SELECTOR,
                                          value="div#select_container_" + wf_select_container_id + " > md-select-menu > md-content > md-option > div > span")
    sleep(0.1)
    for wf_type in workflow_types:
        wf_el_text = wf_type.text
        # TODO
        if wf_el_text == workflow_type:
            element_clicker(driver, web_element=wf_type)
            break


def extract_all_users(driver: Chrome, ent: str):
    org_name = driver.find_element(by=By.CSS_SELECTOR, value='st-avatar[organization] > img').get_attribute('alt')
    # This works as the main runner is started from InitTest/Main
    current_vars_path = Path.cwd() / 'current_vars.json'

    fl = filelock.FileLock(str(current_vars_path.resolve()))

    with fl:
        with open(current_vars_path, "r") as json_file:
            load_dict = json.load(json_file)
            # If we don't have a date we don't have anything and if we do we want to save it
            try:
                date_updated = load_dict[ent][org_name]['date']
            except KeyError:
                # Missing the date and the whole entry get all users and fill them in the dict
                all_users = user_manipulation.return_all_users(driver, ent)
                load_dict[ent].update({org_name: {"users": all_users, "date": str(datetime.today())}})
                to_dump = load_dict
                # json.dump(load_dict, json_file)
                # add_users_to_workflow(driver=driver, ent=ent, users=all_users)

            else:
                # We have the date compare it against today if it's before today get all users again
                # dict_date = datetime.strptime(date_updated, '%Y-%m-%d').date()
                dict_date = datetime.strptime(date_updated.split(' ')[0], '%Y-%m-%d').date()
                if dict_date < date.today():
                    all_users = user_manipulation.return_all_users(driver, ent)
                    load_dict[ent][org_name].update({"users": all_users, "date": str(datetime.today())})
                    to_dump = load_dict
                    # json.dump(load_dict, json_file)
                    # add_users_to_workflow(driver=driver, ent=ent, users=all_users)
                else:
                    # The date is today so just extract the users
                    to_dump = False
                    all_users = load_dict[ent][org_name]['users']

    if to_dump:
        with fl:
            with open('current_vars.json', "w") as json_file:
                json.dump(to_dump, json_file)

    return all_users


def add_users_to_workflow(driver, ent: str, workflow_id='New', users="All"):
    main_url = "https://" + ent + ".salestrekker.com"

    if users == 'All':
        all_users = return_all_users(driver, ent)
    else:
        if isinstance(users, str):
            all_users = users.split('-')
        else:
            all_users = users

    if workflow_id == 'New':
        if driver.current_url != f'{main_url}/settings/workflow/0':
            driver.get(main_url + "/settings/workflow/0")
    else:
        driver.get(main_url + "/settings/workflow/" + workflow_id)
    for user in all_users:
        WdWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'div:nth-child(6) input')))
        driver.find_element(by=By.CSS_SELECTOR, value='div:nth-child(6) input').send_keys(
            user + Keys.ENTER)
        sleep(0.1)

    element_dissapear(driver, 'div.md-toast-content')


def get_all_workflows(driver: Chrome, ent: str):
    """
    Returns list of full hrefs of the workflows - example href https://dev.salestrekker.com/board/jaoj0342-joadf203-wraf
    :return:
    """
    main_url = "https://" + ent + ".salestrekker.com"

    driver.get(main_url)
    # Try finding the main deals button that once clicked will show a list of workflows
    try:
        element_clicker(driver, css_selector='button[aria-label="Deals"]')
    except exceptions.TimeoutException:
        # Except the links are not within the button the deals button is a link for the only wf itself
        workflow = WdWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Deals"]')))
        workflow_list = [{"name": '',
                          "link": workflow.get_attribute('href')}]
    else:
        workflow_container = WdWait(driver, 10).until(
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, 'md-menu-content.sub-menu > section')))
        workflows = workflow_container.find_elements(by=By.CSS_SELECTOR, value='md-menu-item > a')
        workflow_list = [{"name": workflow.find_element(by=By.TAG_NAME, value="span").text,
                          "link": workflow.get_attribute('href')} for workflow in workflows]
    return workflow_list


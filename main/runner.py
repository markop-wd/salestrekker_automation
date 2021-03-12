"""
The background logic of handling reports, threads, exceptions
"""
import concurrent.futures
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from datetime import date, datetime
import json
import traceback
from os import mkdir

from urllib3 import exceptions as http_execs

from logic import worker, cp_worker, worker_main, api
from main.Permanent.login import LogIn

with open("perm_vars.json") as perm_json:
    ents_info = json.load(perm_json)['ents_info']

with open("details.json") as details:
    info = json.load(details)

options = Options()
options.add_experimental_option("detach", True)

all_ents = [
    'ynet', 'vownet', 'gem', 'gemnz', 'platform', 'nlgconnect', 'app',
    'ioutsource', 'chief', 'sfg'
]


# TODO - Extract into a report creating module
def csv_writer(write_dict: dict, ent_name: str):
    """
    Writing the report on what occurred in the driver/ent instance
    :param write_dict:
    :param ent_name:
    :return:
    """
    try:
        mkdir(f'Reports/{date.today()}')
    except FileExistsError:
        pass
    finally:
        file_name = f'Reports/{date.today()}/organization_rundown_{datetime.now().strftime("%H")}.txt'

        with open(f'{file_name}', 'a') as rundown:
            rundown.write(f'{ent_name}\n')
            for key, value in write_dict.items():
                rundown.write(f'\t {key} {value}\n')
            rundown.write('\n')


def main_runner(ent, email="helpdesk@salestrekker.com", cp_pin: str = '', cp_link: str = ''):
    try:
        mkdir(f'Reports/{date.today()}')
    except FileExistsError:
        pass
    finally:
        try:
            mkdir(f'Reports/{date.today()}/Screenshots')
        except FileExistsError:
            pass

    completed = {}

    driver = Chrome(executable_path=ChromeDriverManager().install())

    # driver_ids = {"url": driver.command_executor._url, "id": driver.session_id}
    # with open("new_session.json", "w") as new:
    #     json.dump(driver_ids, new)

    driver.maximize_window()

    try:
        if bool(cp_pin) and bool(cp_link):
            ent = cp_link.split('-')[0].split('/')[-1]
            cp_worker(driver=driver, pin=cp_pin, link=cp_link)
        else:
            worker_main(driver=driver, ent=ent, password=info[ent][email], runner_main_org=ents_info[ent]['main'],
                   runner_learn_org=ents_info[ent]['learn'], email=email)
            # api(driver=driver, ent=ent, password=info[ent][email], email=email)

    except http_execs.NewConnectionError:
        completed['time'] = datetime.now().strftime('%H:%M:%S')
        completed['completed'] = False
        completed['traceback'] = traceback.format_exc()
        completed['current url'] = driver.current_url
        traceback.print_exc()
    except http_execs.MaxRetryError:
        completed['time'] = datetime.now().strftime('%H:%M:%S')
        completed['completed'] = False
        completed['traceback'] = traceback.format_exc()
        completed['current url'] = driver.current_url
        traceback.print_exc()
    except Exception:
        captured_time = datetime.now().strftime("%H:%M:%S")
        driver.get_screenshot_as_file(
            f'Reports/{date.today()}/Screenshots/{captured_time} {ent}.png')
        completed['time'] = captured_time
        completed['completed'] = False
        completed['traceback'] = traceback.format_exc()
        completed['current url'] = driver.current_url
        traceback.print_exc()
    else:
        completed['time'] = datetime.now().strftime("%H:%M:%S")
        completed['completed'] = True
        completed['traceback'] = ''
        completed['current url'] = ''
        # driver.get_screenshot_as_file("test.png")
    finally:
        driver.quit()
        csv_writer(completed, ent)
        # return completed


if __name__ == '__main__':
    consumer_list = [
        {"ent": "platform", "cp_link": "https://platform-cp.salestrekker.com/authenticate/ZxQ4L3w2Cc6D",
         "cp_pin": "361089"},
        {"ent": "sfg", "cp_link": "https://sfg-cp.salestrekker.com/authenticate/eqDHXfq64AO4", "cp_pin": "061642"},
        {"ent": "nlgconnect", "cp_link": "https://nlgconnect-cp.salestrekker.com/authenticate/RsHs97Fv9HqJ",
         "cp_pin": "358065"}
    ]

    commercial_list = [
        {"ent": "platform", "cp_link": "https://platform-cp.salestrekker.com/authenticate/pdKGdnOInyI0",
         "cp_pin": "045101"},
        {"ent": "sfg", "cp_link": "https://sfg-cp.salestrekker.com/authenticate/1AOFWGF6RW16", "cp_pin": "573635"},
        {"ent": "nlgconnect", "cp_link": "https://nlgconnect-cp.salestrekker.com/authenticate/Ha0ybv-_tjtp",
         "cp_pin": "302847"}
    ]

    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        future_runner = {executor.submit(main_runner, ent): ent for ent in
                         all_ents}

    # import_ents = [
    #     'platform', 'sfg'
    # ]

    # def wrapper(p):
    #     return main_runner(email="matthew+120321@salestrekker.com", ent=p)
    #
    # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
    #     test_runner = {executor.submit(wrapper, 'dev'): i for i in range(3)}

    # main_runner(**consumer_list[2])

    # main_runner(cp_link='https://dev-cp.salestrekker.com/authenticate/E8cia8xfWdjV', cp_pin='538750')

    # email_date = date.today().strftime("%d%m%y")
    # main_runner('dev', email=f'matthew+{email_date}@salestrekker.com')

    # def wrapper(p):
    #     return main_runner(**p)
    #
    # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
    #     test_runner = {executor.submit(wrapper, array): array for array in consumer_list}

    # main_runner(cp_link='https://dev-cp.salestrekker.com/authenticate/lk2Bga1LUxod', cp_pin='800790')

    # main_runner('ioutsource', email='helpdesk@salestrekker.com')
    # main_runner('dev', email='matthew+291220@salestrekker.com')

    # main_runner('dev')

    # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
    #     future_runner = {executor.submit(main_runner, 'dev'): i for i in
    #                      range(3)}

    # email_date = date.today().strftime("%d%m%y")
    # for ent in import_ents:
    #     main_runner(ent, email=f'matthew+{email_date}@salestrekker.com')

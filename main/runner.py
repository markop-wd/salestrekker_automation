"""
This encapsulatese the logic.py with the reports, threads and exceptions.
"""
import concurrent.futures
import json
import os
import traceback
from datetime import date, datetime
from os import mkdir
from pathlib import Path

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from urllib3 import exceptions as http_execs
from webdriver_manager.chrome import ChromeDriverManager

from logic import cp_worker, simple_worker, worker_main, worker

# Details are the logins stored
with open("details.json") as details:
    info = json.load(details)


# TODO - Extract into a report creating module
def csv_writer(write_dict: dict, ent_name: str):
    """
    Writing the report on what occurred in the driver/ent instance
    :param write_dict:
    :param ent_name:
    :return:
    """
    todays_report_path = f"Reports/{date.today()}"
    todays_screenshots_path = f"{todays_report_path}/Screenshots"
    with Path(todays_report_path) as report_path:
        if not report_path.exists():
            mkdir(report_path)

    with Path(todays_screenshots_path) as screenshots_path:
        if not screenshots_path.exists():
            mkdir(screenshots_path)

    final_csv_report_path = f'Reports/{date.today()}/organization_rundown_{datetime.now().strftime("%H")}.txt'
    csv_path = Path(final_csv_report_path)

    with open(csv_path, 'a') as rundown_report:
        rundown_report.write(f'{ent_name}\n')
        for key, value in write_dict.items():
            rundown_report.write(f'\t {key} {value}\n')
        rundown_report.write('\n')


def main_runner(ent='gemnz', email="helpdesk@salestrekker.com", cp_pin: str = '', cp_link: str = '',
                conccurent_arg=None):
    """
    This is the wrapper for the caller
    Also handler for the exceptions, if any it will store them in a report
    """

    completed = {
        'completed': False,
        'time': '',
        'traceback': '',
        'current_url': ''
    }

    os.environ['WDM_LOG_LEVEL'] = '0'
    options = Options()
    options.headless = True
    # Detach it so the program can end but the Chrome will remain open until you close it manually
    # options.add_experimental_option("detach", True)
    service = Service(executable_path=ChromeDriverManager(log_level=0, print_first_line=False).install())
    driver = Chrome(service=service, options=options)

    # driver_ids = {"url": driver.command_executor._url, "id": driver.session_id}
    # with open("new_session.json", "w") as new:
    #     json.dump(driver_ids, new)

    if options.headless:
        driver.set_window_size(1920, 1080)
    driver.maximize_window()

    try:
        # If I give him a client portal pin and link it is obvious I should call cp_worker instead of main worker
        if bool(cp_pin) and bool(cp_link):
            ent = cp_link.split('-')[0].split('/')[-1]
            cp_worker(driver=driver, pin=cp_pin, link=cp_link)
        else:
            # If no cp link or pin then call the main worker with parameters you get from perm vars and details
            # worker_main(driver=driver, ent=ent, password=info[ent][email], email=email,
            #             con_arg=conccurent_arg)
            worker(driver=driver, ent=ent, password=info[ent][email], email=email, con_arg=conccurent_arg)

    # Exception catching and storing the exceptions, time when it happened and the traceback for reporting and also include a screenshot.
    except http_execs.NewConnectionError:
        completed['time'] = datetime.now().strftime('%H:%M:%S')
        completed['traceback'] = traceback.format_exc()
        completed['current url'] = driver.current_url
        traceback.print_exc()
    except http_execs.MaxRetryError:
        completed['time'] = datetime.now().strftime('%H:%M:%S')
        completed['traceback'] = traceback.format_exc()
        completed['current url'] = driver.current_url
        traceback.print_exc()
    except Exception:
        captured_time = datetime.now().strftime("%H:%M:%S")
        driver.get_screenshot_as_file(
            f'Reports/{date.today()}/Screenshots/{captured_time} {ent}.png')
        completed['time'] = captured_time
        completed['traceback'] = traceback.format_exc()
        completed['current url'] = driver.current_url
        traceback.print_exc()
    else:
        completed['time'] = datetime.now().strftime("%H:%M:%S")
        completed['completed'] = True
    finally:
        # Finally quit the driver and write the report
        driver.quit()
        csv_writer(completed, ent)
        # return completed


if __name__ == '__main__':
    # This is what gets called first and then calls the runner function

    # consumer_list = [
    #     {"ent": "platform", "cp_link": "https://platform-cp.salestrekker.com/authenticate/ZxQ4L3w2Cc6D",
    #      "cp_pin": "361089"},
    #     {"ent": "sfg", "cp_link": "https://sfg-cp.salestrekker.com/authenticate/eqDHXfq64AO4", "cp_pin": "061642"},
    #     {"ent": "nlgconnect", "cp_link": "https://nlgconnect-cp.salestrekker.com/authenticate/RsHs97Fv9HqJ",
    #      "cp_pin": "358065"}
    # ]
    #
    # commercial_list = [
    #     {"ent": "platform", "cp_link": "https://platform-cp.salestrekker.com/authenticate/pdKGdnOInyI0",
    #      "cp_pin": "045101"},
    #     {"ent": "sfg", "cp_link": "https://sfg-cp.salestrekker.com/authenticate/1AOFWGF6RW16", "cp_pin": "573635"},
    #     {"ent": "nlgconnect", "cp_link": "https://nlgconnect-cp.salestrekker.com/authenticate/Ha0ybv-_tjtp",
    #      "cp_pin": "302847"}
    # ]

    # cp_list = [
    #     {"ent": "sfg", "cp_link": "https://sfg-cp.salestrekker.com/authenticate/z5gG8DXyT0w7",
    #      "cp_pin": "125005"},
    #     {"ent": "sfg", "cp_link": "https://sfg-cp.salestrekker.com/authenticate/Btg7PnH-0UOE", "cp_pin": "874198"},
    #     {"ent": "sfg", "cp_link": "https://sfg-cp.salestrekker.com/authenticate/o0b8tw3ShvWu",
    #      "cp_pin": "464358"},
    #     {"ent": "platform", "cp_link": "https://platform-cp.salestrekker.com/authenticate/ebrRu5pwxzVf",
    #     "cp_pin": "184025"},
    #     {"ent": "platform", "cp_link": "https://platform-cp.salestrekker.com/authenticate/aAwI2Hpmtz6k",
    #      "cp_pin": "479620"},
    #     {"ent": "platform", "cp_link": "https://platform-cp.salestrekker.com/authenticate/vt2zy3SznD4x",
    #     "cp_pin": "958749"},
    #     {"ent": "nlgconnect", "cp_link": "https://nlgconnect-cp.salestrekker.com/authenticate/M0UlvEZb926b",
    #      "cp_pin": "863857"},
    #     {"ent": "nlgconnect", "cp_link": "https://nlgconnect-cp.salestrekker.com/authenticate/oRiZbp6WRtRl",
    #     "cp_pin": "658114"},
    #     {"ent": "nlgconnect", "cp_link": "https://nlgconnect-cp.salestrekker.com/authenticate/bx61k5KHK7UR",
    #      "cp_pin": "268132"}
    # ]

    # my_test_ents = ['nlgconnect', 'platform', 'sfg']
    # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
    #     future_runner = {executor.submit(main_runner, ent): ent for ent in
    #                      my_test_ents}
    main_runner('dev')
    #
    # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
    #     future_runner = {executor.submit(main_runner, 'dev'): _ for _ in
    #                      range(3)}

    # import_ents = [
    #     'platform', 'sfg'
    # ]

    # def wrapper(p):
    #     return main_runner(email="matthew@salestrekker.com", ent='dev', stuff=p)
    #
    #
    # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
    #     test_runner = {executor.submit(wrapper, i): i for i in range(3)}
    
    # main_runner(**consumer_list[2])

    # main_runner(cp_link='https://dev-cp.salestrekker.com/authenticate/E8cia8xfWdjV', cp_pin='538750')

    # email_date = date.today().strftime("%d%m%y")
    # main_runner('dev', email=f'matthew+{email_date}@salestrekker.com')

    # def wrapper(p):
    #     return main_runner(**p)
    #
    # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
    #     test_runner = {executor.submit(wrapper, array): array for array in cp_list}

    # main_runner(cp_link='https://dev-cp.salestrekker.com/authenticate/lk2Bga1LUxod', cp_pin='800790')

    # main_runner('ioutsource', email='helpdesk@salestrekker.com')
    # main_runner('dev', email='matthew+291220@salestrekker.com')

    # main_runner('dev')

    # start_time = datetime.now()
    # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
    #     future_runner = {executor.submit(main_runner, conccurent_arg=i): i for i in
    #                      range(1, 4)}
    # print('end:', datetime.now() - start_time)
    #
    # email_date = date.today().strftime("%d%m%y")
    # for ent in import_ents:
    #     main_runner(ent, email=f'matthew+{email_date}@salestrekker.com')

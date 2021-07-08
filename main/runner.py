"""
The background logic of handling reports, threads, exceptions
"""
import concurrent.futures
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from datetime import date, datetime
import json
import traceback
from os import mkdir

from urllib3 import exceptions as http_execs

from logic import worker_main

with open("details.json") as details:
    info = json.load(details)

all_ents = [
    'ynet', 'vownet', 'gem', 'gemnz', 'platform', 'nlgconnect', 'app',
    'ioutsource', 'chief', 'sfg', 'dev'
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


def main_runner(ent, headless):
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

    options = Options().add_argument('--headless')

    driver = Chrome(executable_path=ChromeDriverManager().install(), options=options)

    driver.maximize_window()

    try:
        worker_main(driver=driver, ent=ent, password="login@LOGIN1234", email="matthew+login@salestrekker.com")
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


if __name__ == "__main__":
    headless_input = input('Headless? (y/n): ')
    num_of_proc_input = int(input('Num of processes (min 1, max 12): '))

    ents = ((headless_input, ent) for ent in all_ents)

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_of_proc_input) as executor:
        future_runner = executor.submit(lambda p: main_runner(*p), ())



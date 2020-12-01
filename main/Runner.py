import threading

from main import Logic
from datetime import date, datetime
from urllib3 import exceptions
import json
import csv
import traceback
from os import mkdir

from time import sleep

with open("perm_vars") as perm_json:
    perm_vars = json.load(perm_json)
    ents_info = perm_vars['ents_info']
    all_ents = [ent for ent in perm_vars['ents_info']]


with open("details.json") as details:
    info = json.load(details)


class Runners:

    def __init__(self):
        self.completed = {}
        self.test = False
        self.folder_name = f'Reports/{date.today()}'

    def main_runner(self, ent):

        try:
            mkdir(self.folder_name)
        except FileExistsError:
            pass

        current_runner = Logic.WorkerInitializer(start_time=date.today(), email='matthew@salestrekker.com',
                                                 password=info[ent]['pass'],
                                                 group=ents_info[ent]['learn'], ent=ent)

        try:
            current_runner.deployment_logic(ents_info[ent]['main'], ents_info[ent]['learn'])
        except exceptions.NewConnectionError:
            # TODO - Find a way to go back to the line where he was after encountering either of the two errors
            self.completed[ent] = (datetime.now().strftime('%H %M %S'), False, traceback.format_exc(), current_runner.driver.current_url)
            self.csv_writer()
            traceback.print_exc()
            current_runner.driver.quit()
        except exceptions.MaxRetryError:
            # TODO - Find a way to go back to the line where he was after encountering either of the two errors
            self.completed[ent] = (datetime.now().strftime('%H %M %S'), False, traceback.format_exc(), current_runner.driver.current_url)
            self.csv_writer()
            traceback.print_exc()
            current_runner.driver.quit()
        except Exception:
            captured_time = datetime.now().strftime("%H:%M:%S")
            current_runner.driver.get_screenshot_as_file(
                f'{self.folder_name}/{captured_time} {ent}.png')
            self.completed[ent] = (captured_time, False, traceback.format_exc(), current_runner.driver.current_url)
            self.csv_writer()
            traceback.print_exc()
            current_runner.driver.quit()
        else:
            self.completed[ent] = (datetime.now().strftime("%H:%M:%S"), True, '')
            current_runner.driver.quit()
        finally:
            self.csv_writer()

    def test_runner(self):
        self.test = True

        try:
            mkdir(self.folder_name + '/Test')
        except FileExistsError:
            pass
        except FileNotFoundError:
            mkdir(self.folder_name)
            mkdir(self.folder_name + '/Test')

        for ent in all_ents:

            if ent not in ['dev']:
                continue

            current_runner = Logic.WorkerInitializer(start_time=date.today(), email='matthew@salestrekker.com',
                                                     password=info[ent]['pass'],
                                                     group=ents_info[ent]['learn'], ent=ent)

            try:
                current_runner.test_logic(ents_info[ent]['main'], ents_info[ent]['learn'])
            except exceptions.NewConnectionError:
                # TODO - Find a way to go back to the line where he was after encountering either of the two errors
                captured_time = datetime.now().strftime("%H:%M:%S")
                self.completed[ent] = (captured_time, False, traceback.format_exc(), current_runner.driver.current_url)
                traceback.print_exc()
                current_runner.driver.quit()
                continue

            except exceptions.MaxRetryError:
                # TODO - Find a way to go back to the line where he was after encountering either of the two errors
                captured_time = datetime.now().strftime("%H:%M:%S")
                self.completed[ent] = (captured_time, False, traceback.format_exc(), current_runner.driver.current_url)
                traceback.print_exc()
                current_runner.driver.quit()
                continue

            except Exception:
                captured_time = datetime.now().strftime("%H:%M:%S")
                current_runner.driver.get_screenshot_as_file(
                    f'{self.folder_name}/Test/{captured_time} {ent}.png')
                self.completed[ent] = (captured_time, False, traceback.format_exc(), current_runner.driver.current_url)
                traceback.print_exc()
                current_runner.driver.quit()
                continue

            else:
                captured_time = datetime.now().strftime("%H:%M:%S")
                self.completed[ent] = (captured_time, True, '', '')
                current_runner.driver.quit()

        self.csv_writer()

    def csv_writer(self):

        if self.test:
            file_name = f'{self.folder_name}/Test/organization_rundown.csv'
        else:
            file_name = f'{self.folder_name}/organization_rundown.csv'

        with open(f'{file_name}', 'a') as rundown:
            writer = csv.writer(rundown)

            for key, value in self.completed.items():
                writer.writerow([key, value])


if __name__ == '__main__':
    test = Runners()
    test.main_runner('dev')

    #
    # thread_list = []
    #
    # test_ents = ['app','sfg','gemnz','ioutsource']
    #
    # for ent in test_ents:
    #     if ent == 'dev':
    #         continue
    #     t = threading.Thread(name=f'Thread {ent}', target=test.main_runner, args=(ent,))
    #     t.start()
    #     sleep(1)
    #     print(t.name + " starting")
    #     thread_list.append(t)
    #
    # for thread in thread_list:
    #     thread.join()
    #

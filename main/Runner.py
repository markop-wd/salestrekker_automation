from main import Logic
from datetime import date
from urllib3 import exceptions
import json
import csv
import traceback
import datetime

# file_to_open = Path("main") / "perm_vars"

with open("perm_vars") as perm_json:
    perm_vars = json.load(perm_json)
    ents_info = perm_vars['ents_info']
    all_ents = [ent for ent in perm_vars['ents_info']]

with open("details") as details:
    info = json.load(details)

init_list = []
completed = {}

for count, ent in enumerate(all_ents):
    #
    # if count > 0:
    #     break

    currentDT = datetime.datetime.now().strftime("%Y-%m-%d")

    init_list.append(Logic.TestInitializer(start_time=currentDT, email='helpdesk@salestrekker.com', password=info[ent]['pass'], group=ents_info[ent]['learn'], ent=ent))
    current_runner_instance = init_list[count]

    try:
        current_runner_instance.test_logic(ents_info[ent]['main'], ents_info[ent]['learn'])
    except exceptions.NewConnectionError:
        # TODO - Find a way to go back to the line where he was after encountering either of the two errors

        traceback.print_exc()
        current_runner_instance.driver.refresh()
        current_runner_instance.driver.quit()
        completed[ent] = False
    except exceptions.MaxRetryError:
        # TODO - Find a way to go back to the line where he was after encountering either of the two errors
        traceback.print_exc()
        current_runner_instance.driver.refresh()
        current_runner_instance.driver.quit()
        completed[ent] = False
    except:
        traceback.print_exc()
        current_runner_instance.driver.quit()
        completed[ent] = False
    else:
        current_runner_instance.driver.quit()
        completed[ent] = True


with open(f'InfoFolder/{date.today()} organization_rundown.csv', 'a') as rundown:
    writer = csv.writer(rundown)

    for key, value in completed.items():
        writer.writerow([key, value])

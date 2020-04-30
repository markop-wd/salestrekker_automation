from main import Logic
from datetime import date, datetime
from urllib3 import exceptions
import json
import csv
import traceback
from os import mkdir

# file_to_open = Path("main") / "perm_vars"

with open("perm_vars") as perm_json:
    perm_vars = json.load(perm_json)
    ents_info = perm_vars['ents_info']
    all_ents = [ent for ent in perm_vars['ents_info']]

with open("details") as details:
    info = json.load(details)

init_list = []
completed = {}
folder_name = f'Reports/{date.today()}'
file_name = f'{folder_name}/organization_rundown.csv'
try:
    mkdir(folder_name)
except FileExistsError:
    pass

for count, ent in enumerate(all_ents):

    init_list.append(
        Logic.TestInitializer(start_time=date.today(), email='helpdesk@salestrekker.com', password=info[ent]['pass'],
                              group=ents_info[ent]['learn'], ent=ent))
    current_runner_instance = init_list[count]

    try:
        current_runner_instance.deployment_logic(ents_info[ent]['main'], ents_info[ent]['learn'])
    except exceptions.NewConnectionError:
        # TODO - Find a way to go back to the line where he was after encountering either of the two errors
        traceback.print_exc()
        current_runner_instance.driver.quit()
        completed[ent] = (False, traceback.format_exc())
    except exceptions.MaxRetryError:
        # TODO - Find a way to go back to the line where he was after encountering either of the two errors
        traceback.print_exc()
        current_runner_instance.driver.quit()
        completed[ent] = (False, traceback.format_exc())
    except:
        traceback.print_exc()
        current_runner_instance.driver.quit()
        completed[ent] = (False, traceback.format_exc())
    else:
        current_runner_instance.driver.quit()
        completed[ent] = (True, '')

with open(f'{file_name}', 'a') as rundown:
    writer = csv.writer(rundown)

    for key, value in completed.items():
        writer.writerow([datetime.today(), key, value])

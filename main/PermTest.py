from main import rewritten
from pathlib import Path
from urllib3 import exceptions
import json
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
completed = []

for count, ent in enumerate(all_ents):

    # if count > 0:
    #     break

    currentDT = datetime.datetime.now()

    init_list.append(rewritten.TestInitializer(start_time=currentDT.strftime("%Y-%m-%d %H.%M.%S"), email='helpdesk@salestrekker.com', password=info[ent]['pass'], group=ents_info[ent]['learn'], ent=ent))
    current_runner_instance = init_list[count]
    try:
        current_runner_instance.test_logic(ents_info[ent]['main'], ents_info[ent]['learn'])
    except exceptions.NewConnectionError:
        traceback.print_exc()
        current_runner_instance.driver.refresh()
        current_runner_instance.driver.quit()
        completed.append(ent + ' - Not Completed\n')
    except exceptions.MaxRetryError:
        traceback.print_exc()
        current_runner_instance.driver.refresh()
        current_runner_instance.driver.quit()
        completed.append(ent + ' - Not Completed\n')
        # TODO - Find a way to go back to the line where he was after encountering either of the two errors
    except:
        traceback.print_exc()
        current_runner_instance.driver.quit()
        completed.append(ent + ' - Not Completed\n')
    else:
        current_runner_instance.driver.quit()
        completed.append(ent + '\n')

with open('completed.txt', 'a') as compl:
    compl.writelines(completed)

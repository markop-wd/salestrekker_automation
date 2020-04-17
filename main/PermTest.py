from main import rewritten
from pathlib import Path
from urllib3 import exceptions
import json
import traceback

# file_to_open = Path("main") / "perm_vars"

with open("perm_vars") as perm_json:
    perm_vars = json.load(perm_json)
    orgs_info = perm_vars['orgs_info']
    all_orgs = [org for org in perm_vars['orgs_info']]

with open("details") as details:
    info = json.load(details)

init_list = []
completed = []

for count, org in enumerate(all_orgs):
    if count > 1:
        break
    init_list.append(rewritten.TestInitializer(email='helpdesk@salestrekker.com', password=info[org]['pass'], group=orgs_info[org]['learn'],ent=org))
    current_runner_instance = init_list[count]
    try:
        current_runner_instance.test_logic(orgs_info[org]['main'],orgs_info[org]['learn'])
    except exceptions.NewConnectionError:
        current_runner_instance.driver.refresh()
    except exceptions.MaxRetryError:
        current_runner_instance.driver.refresh()
    except:
        traceback.print_exc()
        current_runner_instance.driver.quit()
    else:
        completed.append(org + '\n')
        current_runner_instance.driver.quit()

with open('completed.txt', 'a') as compl:
    compl.writelines(completed)

# print(init_list)
#
# init_test = rewritten.TestInitializer(email='matthew@salestrekker.com',password='tQ9^8K3HZsml9bKCuYme2u')
# try:
#     init_test.test_logic('test_org')
#     # login.log_in(driver, "dev", "matthew@salestrekker.com", "tQ9^8K3HZsml9bKCuYme2u")
#     # org_switch.org_changer(driver, "NOTANACTUALORGANISATION")
#     # driver.quit()
#
# except:
#
#     init_test.driver.quit()

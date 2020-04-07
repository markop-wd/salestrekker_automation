from play import test
import traceback
from time import sleep

init_test = test.TestInitializer(ent='dev', email='matthew@salestrekker.com', password='', new_org_name='Yet Another Test Organization 2020-03-31', group='**MAKE YOUR OWN** Matt Test Group (QA automation testing)')
try:
    init_test.main_func()
    sleep(15)
    init_test.driver.quit()
    print('success')
except:
    traceback.print_exc()
    init_test.driver.quit()


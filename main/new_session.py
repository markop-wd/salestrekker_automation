from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from Permanent.helper_funcs import accreditation_fill

with open("new_session.json", "r") as fajlino:
    json_fajlino = json.load(fajlino)

options = Options()

driver = webdriver.Remote(command_executor=json_fajlino['url'], options=options)
# prevent annoying empty chrome windows
driver.close()
driver.session_id = json_fajlino['id']

accreditation_fill(driver, 'dev')

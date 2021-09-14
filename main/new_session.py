"""
If a function exits this is the function that should take the browser back.
Not finished yet.
"""

import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    with open("new_session.json", "r") as fajlino:
        json_fajlino = json.load(fajlino)

    options = Options()

    driver_r = webdriver.Remote(command_executor=json_fajlino['url'], options=options)
    # prevent annoying empty chrome windows
    driver_r.close()
    driver_r.session_id = json_fajlino['id']
    yup = False

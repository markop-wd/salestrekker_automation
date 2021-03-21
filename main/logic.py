"""
Main business logic
"""
from time import sleep

from selenium.webdriver import Chrome

from Permanent.login import LogIn


def worker_main(driver: Chrome, ent: str, password: str,
                email: str = 'helpdesk@salestrekker.com'):
    LogIn(driver, ent, email, password).log_in()
    sleep(5)


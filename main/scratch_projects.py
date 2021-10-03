"""
Just some unclean hacky projects that yet to need to be reformatted, finished and moved to permanent tooling
"""
import copy
import json
import os
import random
import string
import traceback
from datetime import datetime, date
from pathlib import Path
from time import sleep

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.webdriver.support import expected_conditions as ec
import requests

from main.Permanent.deal_create.deal_create import CreateDeal
from main.Permanent.deal_fill import FillDeal
from main.Permanent.helper_funcs import md_toast_remover, random_string_create, AddressInput, element_clicker, selector, \
    element_dissapear, element_waiter
from main.Permanent.deal_fill_selectors import CONTENT, INFO_BUTTONS, ADD_HOUSEHOLD, \
    HOUSEHOLD_PICKER


class Test:

    def __init__(self, driver: Chrome, org_name):
        self.driver = driver
        self.org_name = org_name

    def screenshot_helper(self, element_with_scroll, org_name, sub_section_name, button_count):
        scroll_total = self.driver.execute_script("return arguments[0].scrollHeight",
                                                  element_with_scroll)
        content = self.driver.execute_script("return arguments[0].clientHeight",
                                             element_with_scroll)

        scroll_new = 0
        count = 1
        while scroll_new < (scroll_total - 100):

            md_toast_remover(self.driver)

            self.driver.execute_script(f"arguments[0].scroll(0,{scroll_new});", element_with_scroll)

            self.driver.get_screenshot_as_file(
                f'SettingsScreenshots/{org_name}/{button_count}. {sub_section_name} no. {count}.png')
            scroll_new += (content - 120)
            count += 1
            if content == scroll_total:
                break

    def main(self):
        from selenium.webdriver.support.wait import WebDriverWait as WdWait
        from selenium.webdriver.support import expected_conditions as ec

        self.driver.get('https://dev.salestrekker.com/settings')
        if not os.path.exists('SettingsScreenshots'):
            os.mkdir('SettingsScreenshots')
        if not os.path.exists(f'SettingsScreenshots/{self.org_name}'):
            os.mkdir(f'SettingsScreenshots/{self.org_name}')
        sleep(10)

        buttons = self.driver.find_elements(by=By.CSS_SELECTOR, value='st-sidebar-block div > a')

        for count, el in enumerate(buttons, start=1):
            try:
                el.click()
            except exceptions.ElementNotInteractableException:
                self.driver.execute_script('arguments[0].click();', el)
            try:
                WdWait(self.driver, 10).until(
                    ec.visibility_of_element_located((By.TAG_NAME, 'main')))
            except exceptions.TimeoutException:
                pass
            scroll_el = self.driver.find_element(by=By.CSS_SELECTOR, value='body > md-content')
            setting_name = el.find_element(by=By.TAG_NAME, value='span').text
            self.screenshot_helper(element_with_scroll=scroll_el, org_name=self.org_name,
                                   sub_section_name=setting_name, button_count=count)


def config_deal_create(driver: Chrome, ent: str, hl_workflow: str, con_arg: int):
    with open("deal_config.json") as create_config:
        main_config = json.load(create_config)
    scen_1 = copy.deepcopy(main_config)
    scen_1['contacts']['number_of_contacts']['value'] = 1
    scen_1['contacts']['contact_types']['types'] = 'person'
    scen_2 = copy.deepcopy(main_config)
    scen_2['contacts']['number_of_contacts']['value'] = 2
    scen_2['contacts']['contact_types']['types'] = 'person'
    scen_3 = copy.deepcopy(main_config)
    scen_3['contacts']['contact_types']['types'] = 'custom'
    scen_3['contacts']['contact_types']['custom'] = 'pers,comp'
    scen_4 = copy.deepcopy(main_config)
    scen_4['contacts']['contact_types']['types'] = 'custom'
    scen_4['contacts']['contact_types']['custom'] = 'pers,pers,comp'
    scen_5 = copy.deepcopy(main_config)
    scen_5['contacts']['number_of_contacts']['value'] = 10
    scen_5['contacts']['contact_types']['types'] = 'mixed'
    scen_5['contacts']['non_client']['active'] = True
    scen_5['contacts']['non_client']['no_of_clients'] = 6
    scen_6 = copy.deepcopy(main_config)
    scen_6['contacts']['contact_types']['types'] = 'custom'
    scen_6['contacts']['contact_types']['custom'] = 'comp'
    scen_7 = copy.deepcopy(main_config)
    scen_7['contacts']['contact_types']['types'] = 'custom'
    scen_7['contacts']['contact_types']['custom'] = 'comp,pers,pers'
    scen_8 = copy.deepcopy(main_config)
    scen_8['contacts']['contact_types']['types'] = 'custom'
    scen_8['contacts']['contact_types']['custom'] = 'pers,pers,comp'
    scen_list = [scen_1, scen_2, scen_3, scen_4, scen_5, scen_6, scen_7, scen_8]
    deal = CreateDeal(ent, driver, config=scen_list[con_arg - 1],
                      deal_name=f'Scenario {con_arg} NANOBOT')
    if con_arg <= 5:
        url = deal.run(workflow=hl_workflow, deal_owner_name='Salestrekker Help Desk',
                       af_type="cons")
    else:
        url = deal.run(workflow=hl_workflow, deal_owner_name='Salestrekker Help Desk',
                       af_type="comm")
    with open("edit_config.json") as fill_config:
        edit_config = json.load(fill_config)
    scen1_fill = copy.deepcopy(edit_config)
    scen1_fill['income']['type'] = 'bus'
    scen1_fill['assets']['type'] = 'acc'
    scen2_fill = copy.deepcopy(edit_config)
    scen2_fill['income']['type'] = 'payg,bus,tax,ntax'
    scen3_fill = copy.deepcopy(edit_config)
    scen3_fill['income']['type'] = 'payg,bus,tax'
    scen4_fill = copy.deepcopy(edit_config)
    scen4_fill['income']['type'] = 'bus,payg,tax,rent'
    scen5_fill = copy.deepcopy(edit_config)
    scen5_fill['income']['type'] = 'bus,payg,tax,rent'
    fill_configs = [scen1_fill, scen2_fill, scen3_fill, scen4_fill, scen5_fill]
    if con_arg <= 5:
        FillDeal(driver, config=fill_configs[con_arg - 1]).run(url)
    else:
        FillDeal(driver, config=edit_config).run(url)


class ContactCreate:
    def __init__(self, driver: Chrome):
        self.driver = driver
        self.address_placeholders = ['Search Property (eg. 1 Walker Avenue)',
                                     'Search current address',
                                     'Search employer address', 'Search next of kin address',
                                     'Search mailing address',
                                     'Search previous address',
                                     'Search post settlement address']
        occupation_path = Path('assets/occupations.json')
        with open(occupation_path) as occupation_codes:
            self.occupations = json.load(occupation_codes)

        industry_path = Path('assets/industries.json')
        with open(industry_path, 'r') as industry_codes:
            self.industries = json.load(industry_codes)

    def ul_list_selector(self, input_el, input_text):
        sleep(5)
        input_el.send_keys(input_text)

        # The ul list produced by typing in the input always has the ID inside itself but needs to modified like so
        ul_el_id = 'ul-' + str(input_el.get_attribute('id')).split('-')[-1]
        try:
            WdWait(self.driver, 15).until(ec.visibility_of_element_located((By.ID, ul_el_id)))
        except exceptions.TimeoutException:
            print('No list returned after 15 seconds')

        else:
            li_els = self.driver.find_element(By.ID, ul_el_id).find_elements(by=By.CSS_SELECTOR,
                                                                             value='li span')
            if len(li_els) == 0:
                input_el.send_keys(Keys.CONTROL + 'a')
                sleep(0.1)
                input_el.send_keys(Keys.DELETE)
                sleep(0.2)
            else:
                self.driver.execute_script("arguments[0].click();",
                                           li_els[random.randrange(0, len(li_els))])

    def input_el_handler(self, content):
        input_els = content.find_elements(by=By.TAG_NAME, value='input')
        try:
            for input_el in input_els:

                value_test = input_el.get_attribute('value')

                if value_test == '$0':
                    if input_el.get_attribute('ng-model') == 'householdExpense.value':
                        try:
                            input_el.send_keys(random.randrange(0, 5000))
                        except:
                            print('Expense value error')
                            traceback.print_stack()
                            traceback.print_exc()
                            continue
                    else:
                        value = random.randrange(0, 50000)

                        try:
                            input_el.send_keys(value)
                        except exceptions.ElementNotInteractableException:
                            continue

                elif value_test == '$0.00':
                    value = random.randrange(0, 500000)

                    try:
                        input_el.send_keys(value)
                    except exceptions.ElementNotInteractableException:
                        continue

                elif value_test == '0.00%':
                    value = random.randrange(0, 10000)

                    try:
                        input_el.send_keys(value)
                    except exceptions.ElementNotInteractableException:
                        continue

                elif not value_test or value_test == ' ':
                    ng_model = input_el.get_attribute('ng-model')
                    ng_change = input_el.get_attribute('ng-change')

                    if input_el.get_attribute('class') == 'md-datepicker-input md-input':
                        year = random.randrange(1930, 2010)
                        if input_el.get_attribute('placeholder') == 'MM/YYYY':
                            try:
                                input_el.send_keys(f'01/{year}')
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                input_el.send_keys(f'01/01/{year}')
                            except exceptions.ElementNotInteractableException:
                                continue
                    elif ng_model == 'householdExpense.comments':
                        try:
                            input_el.send_keys(random_string_create())
                        except:
                            traceback.print_stack()
                            traceback.print_exc()
                            continue

                    elif ng_model == '$mdAutocompleteCtrl.scope.searchText':
                        input_aria_label = input_el.get_attribute('aria-label')
                        if input_aria_label in self.address_placeholders:
                            address_input = AddressInput()
                            if not address_input.ul_list_selector(self.driver, input_el,
                                                                  f'{random.randrange(1, 100)} la'):
                                address_input.address_repeat = 0
                                address_input.ul_list_selector(self.driver, input_el,
                                                               f'{random.randrange(1, 50)} te')

                        elif input_aria_label == 'Employer ABN':
                            input_el.send_keys(str(random.randrange(10000000000, 100000000000)))

                        elif input_aria_label == 'Employer ACN':
                            input_el.send_keys(str(random.randrange(100000000, 1000000000)))

                        elif input_aria_label == 'ABS occupation code':
                            occupation = self.occupations[
                                random.randrange(0, len(self.occupations) - 1)]
                            self.ul_list_selector(input_el, occupation['id'])

                        elif input_aria_label == 'ANZSCO industry code':
                            industry = self.industries[
                                random.randrange(0, len(self.industries) - 1)]
                            self.ul_list_selector(input_el, industry['id'])

                        elif input_aria_label == 'Employer name':
                            self.ul_list_selector(input_el, random_string_create(3).lower())

                    elif ng_change == '$ctrl.saveAddress()':
                        continue

                    elif ng_model in ['$ctrl.contact.person.contact.work',
                                      '$ctrl.contact.person.contact.home',
                                      '$ctrl.contact.person.contact.primary']:
                        input_el.send_keys("".join(random.sample(string.digits, 9)))
                    elif ng_model == '$ctrl.contact.person.contact.secondaryEmail':
                        input_el.send_keys('secondary@email.com')
                    else:
                        try:
                            input_el.send_keys(random_string_create())
                        except exceptions.ElementNotInteractableException:
                            continue

        except exceptions.StaleElementReferenceException:
            pass

    def md_select_handler(self, content):
        for md_select in content.find_elements(by=By.TAG_NAME, value='md-select'):
            try:
                if not element_clicker(self.driver, web_element=md_select):
                    continue

                md_select_id = str(md_select.get_attribute('id'))
                md_select_container_id = str(int(md_select_id.split("_")[-1]) + 1)
                WdWait(self.driver, 5).until(
                    ec.element_to_be_clickable(
                        (By.ID, 'select_container_' + md_select_container_id)))
                md_select_container = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                                value='#select_container_' + md_select_container_id + ' md-option')

                try:
                    to_click = random.randrange(0, len(md_select_container))
                except ValueError:
                    continue
                if not element_clicker(self.driver, web_element=md_select_container[to_click]):
                    continue
            except:
                traceback.print_stack()
                traceback.print_exc()
                continue

    def checkbox_handler(self, content):
        checkboxes = content.find_elements(by=By.TAG_NAME, value='md-checkbox')

        for checkbox in checkboxes:
            try:
                if checkbox.get_attribute('ng-change') == '$ctrl.marketingToggle()':
                    continue
                else:
                    if random.randrange(0, 100) > 30:
                        if not element_clicker(self.driver, web_element=checkbox):
                            continue
            except exceptions.NoSuchElementException:
                print('excepted exception but why')
            except exceptions.StaleElementReferenceException:
                continue

    def select_el_handler(self, content):
        selects = content.find_elements(by=By.TAG_NAME, value='select')
        for select_el in selects:
            try:
                ng_model = select_el.get_attribute('ng-model')
                if ng_model == '$ctrl.address.country':
                    selector(self.driver, select_el, index='1')
                elif ng_model in ['$ctrl.employment.isCurrent',
                                  '$ctrl.employment.type',
                                  '$ctrl.employment.status',
                                  '$ctrl.employment.basis']:
                    continue
                elif ng_model in ['$ctrl.contact.person.information.countryOfResidency',
                                  '$ctrl.contact.person.information.countryOfTaxResidence',
                                  '$ctrl.contact.person.information.citizenship',
                                  '$ctrl.contact.person.information.residentialStatus',
                                  '$ctrl.contact.person.information.countryOfBirth']:
                    selector(self.driver, select_el, index='1')
                else:
                    selector(self.driver, select_el)
            except exceptions.StaleElementReferenceException:
                continue

    def md_radio_group(self, content):
        md_radio_group = content.find_elements(by=By.TAG_NAME, value='md-radio-group')
        for group in md_radio_group:
            try:
                md_radio_buttons = group.find_elements(by=By.TAG_NAME,
                                                       value='md-radio-button')
                radio_button_to_click = random.randrange(0, len(md_radio_buttons))
                element_clicker(self.driver, web_element=md_radio_buttons[radio_button_to_click])
            except exceptions.StaleElementReferenceException:
                continue

    def main_contact_create_logic(self):
        # if random.choice([True, False]):
        b = True
        if b:
            self.driver.get('https://sfg.salestrekker.com/contact/edit/person/0')
            WdWait(self.driver, 15).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, 'st-contact[form-name="contactEditForm"]')))

            all_buttons = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                    value='div.group-items > button')

            for count, button in enumerate(all_buttons):
                button.click()
                sleep(5)
                content = WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((eval(CONTENT['by']), CONTENT['value'])))
                if count == 0:
                    self.contact_details()

                    self.select_el_handler(content)
                    self.md_select_handler(content)
                    self.md_radio_group(content)
                    self.checkbox_handler(content)
                    self.input_el_handler(content)
                if count == 1:

                    income_buttons = self.driver.find_elements(by=eval(INFO_BUTTONS['by']),
                                                               value=INFO_BUTTONS['value'])
                    for income_button in income_buttons:

                        if not element_clicker(self.driver, web_element=income_button):
                            continue

                    sleep(0.1)

                    self.md_select_handler(content)

                    self.select_el_handler(content)

                    self.input_el_handler(content)
                    income_buttons = self.driver.find_elements(by=eval(INFO_BUTTONS['by']),
                                                               value=INFO_BUTTONS['value'])
                    for income_button in income_buttons:

                        if not element_clicker(self.driver, web_element=income_button):
                            continue

                    sleep(0.1)

                    self.md_select_handler(content)

                    self.select_el_handler(content)

                    self.input_el_handler(content)
                if count == 2:
                    WdWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.TAG_NAME, 'st-households')))
                    self.driver.find_element(by=eval(ADD_HOUSEHOLD['by']),
                                             value=ADD_HOUSEHOLD['value']).click()

                    household_picker = WdWait(self.driver, 10).until(ec.presence_of_element_located(
                        (eval(HOUSEHOLD_PICKER['by']), HOUSEHOLD_PICKER['value'])))
                    element_clicker(self.driver, web_element=household_picker)

                    sleep(0.5)

                    self.input_el_handler(content)

                    self.select_el_handler(content)

                if count == 3:
                    assets = self.driver.find_elements(by=eval(INFO_BUTTONS['by']),
                                                       value=INFO_BUTTONS['value'])
                    for asset in assets:
                        if not element_clicker(self.driver, web_element=asset):
                            continue
                        if not element_clicker(self.driver, web_element=asset):
                            continue

                    self.checkbox_handler(content)

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    self.md_select_handler(content)

                if count == 4:
                    liabilities = self.driver.find_elements(by=eval(INFO_BUTTONS['by']),
                                                            value=INFO_BUTTONS['value'])

                    for liability in liabilities:
                        if not element_clicker(self.driver, web_element=liability):
                            continue
                        if not element_clicker(self.driver, web_element=liability):
                            continue

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    self.md_select_handler(content)

                if count == 5:
                    insurances = self.driver.find_elements(by=eval(INFO_BUTTONS['by']),
                                                           value=INFO_BUTTONS['value'])
                    for insurance in insurances:
                        if not element_clicker(self.driver, web_element=insurance):
                            continue
                        if not element_clicker(self.driver, web_element=insurance):
                            continue

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    self.md_select_handler(content)

                    element_dissapear(self.driver, 'div.md-toast-content')
                    element_clicker(self.driver, css_selector='button.save')
                    element_dissapear(self.driver, 'div.md-toast-content')
        else:
            self.driver.get('https://sfg.salestrekker.com/contact/edit/company/0')
            WdWait(self.driver, 15).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, 'st-contact[form-name="contactEditForm"]')))

    def contact_details(self):
        first_names = ['Misty', 'Karl', 'Tanisha', 'Jasmin', 'Lexi-Mai', 'Chandni', 'Musab',
                       'Spike', 'Doris',
                       'Dominick', 'Rudi',
                       'Saira', 'Keeleigh', 'Nana', 'Andrew', 'Kirandeep', 'Roland', 'Harry',
                       'Alexie', 'Adelaide',
                       'Finbar', 'Nasir',
                       'Patrycja', 'Nela', 'Belinda', 'Amaya', 'Husnain', 'Tiana', 'Wyatt',
                       'Kenneth', 'April',
                       'Leia',
                       'Bushra',
                       'Levi', 'Keira', 'Amin', 'Samiha', 'Marianne', 'Habib', 'Yousuf', 'Nicola',
                       'Samanta',
                       'Benedict', 'Nikhil',
                       'Aurora', 'Giulia', 'Rosa', 'Alannah', 'Marian', 'Dionne', 'Xanthe',
                       'Anabel', 'Samira',
                       'Mason',
                       'Colleen',
                       'Esther', 'Faheem', 'Rachael', 'Kuba', 'Callam', 'Nick', 'Ayub', 'Esmay',
                       'Aimee', 'Sarah',
                       'Billy', 'Enid',
                       'Katie-Louise', 'Ashlee', 'Tamar', 'Darla', 'Whitney', 'Helena', 'Rachelle',
                       'Maisie',
                       'Julia',
                       'Mandy',
                       'Isaiah', 'Sally', 'Marianna', 'Jasleen', 'Evie-Mae', 'Lana', 'Kiana',
                       'Preston', 'Rae',
                       'Poppy-Rose', 'Lyla',
                       'Christy', 'Maheen', 'Cordelia', 'Mariya', 'Amelia-Grace', 'Kier', 'Sonny',
                       'Alessia',
                       'Inigo',
                       'Hareem',
                       'Caitlyn', 'Ayana', 'Danielle', 'Charlotte', 'Bronwyn', 'Eliot', 'Lesley',
                       'Ada', 'Azra',
                       'Wilbur', 'Lillian',
                       'Yannis', 'Sherri', 'Cosmo', 'Nella', 'Hasan', 'Tyrique', 'Jonah',
                       'Lexi-Mae', 'Nigel',
                       'Zavier',
                       'Bevan',
                       'Leo', 'Israel', 'Sharna', 'Jagoda', 'Deborah', 'Claire', 'Anabelle',
                       'Kobie', 'Nabeel',
                       'Kayley', 'Zahrah',
                       'Beck', 'Kingsley', 'Micah', 'Jerry', 'Haydn', 'Robyn', 'Carwyn', 'Rhys',
                       'Seamus', 'Maia',
                       'Iman', 'Rahul',
                       'Judy', 'Arwa', 'Jeevan', 'Francesco', 'Shyam', 'Amal', 'Gabrielle',
                       'Kellie', 'Derry',
                       'Quentin', 'Hashir',
                       'Alma', 'Rheanna', 'Sebastian', 'Sahara', 'Miriam', 'Debbie', 'Niyah',
                       'Lillie-May', 'Petra',
                       'Khalil', 'Lena',
                       'Isabell', 'Howard', 'Lennie', 'Jibril', 'Christiana', 'Alan', 'Kimora',
                       'Muneeb', 'Iqrah',
                       'Hanna', 'Akbar',
                       'Beverly', 'Jill', 'Shania', 'T-Jay', 'George', 'Lexie', 'Gerard',
                       'Weronika', 'Alison',
                       'Reon',
                       'Piotr',
                       'Alya', 'Mitchel', 'Sally', 'Alfie-Lee', 'Abbie', 'Pola', 'Laylah', 'Zubair',
                       'Ali',
                       'Nicole',
                       'Lorna',
                       'Ember', 'Cora']
        surnames = ['Banks', 'Berg', 'Obrien', 'Talley', 'Mccray', 'Kramer', 'Cunningham', 'Dunn',
                    'Vu', 'Ferry',
                    'Wolfe', 'Haas', 'Bate', 'Tomlinson', 'Phelps', 'Goulding', 'Penn', 'Slater',
                    'Aguilar',
                    'Mellor',
                    'Bray', 'Potter', 'Metcalfe', 'Burch', 'Houston', 'Brandt', 'Nixon', 'Allison',
                    'Stephens',
                    'Webster', 'Lawrence', 'Wright', 'Knowles', 'Davidson', 'Dalton', 'Flower',
                    'Cameron', 'Baker',
                    'Portillo', 'Lord', 'Goodman', 'Roman', 'Wardle', 'Hayden', 'Bains', 'Romero',
                    'Iles',
                    'Navarro',
                    'Malone', 'Molina', 'Macfarlane', 'Hilton', 'Mckay', 'Novak', 'Gaines',
                    'Ratliff', 'Valdez',
                    'Zavala', 'Gibbons', 'Almond', 'Bruce', 'Felix', 'Reeve', 'Chang', 'Patrick',
                    'Hutchings',
                    'Ayala',
                    'Russell', 'Burn', 'Parra', 'Sharma', 'Emery', 'Burris', 'Southern', 'Mcleod',
                    'Mckee',
                    'Duggan',
                    'William', 'Dalby', 'Carr', 'Carty', 'Read', 'Marsh', 'Chase', 'Greene',
                    'Stafford', 'Greig',
                    'Woolley', 'Bird', 'Wyatt', 'Escobar', 'Bradley', 'Kirby', 'Whitney',
                    'Cartwright', 'Sargent',
                    'Plummer', 'Lucero', 'Reynolds', 'Melia', 'Davenport', 'Irving', 'Barrow',
                    'Senior', 'Mcgowan',
                    'Hancock', 'Povey', 'Mcmanus', 'Tyson', 'Hunt', 'Betts', 'Lopez', 'Molloy',
                    'Plant', 'Kirk',
                    'Cantu', 'Reid', 'Whelan', 'Dupont', 'Berry', 'Mueller', 'Lowery', 'Powell',
                    'Porter',
                    'Krueger',
                    'Griffiths', 'Garrett', 'Barrett', 'Gibbs', 'Calvert', 'Hills', 'Rice',
                    'Correa', 'Pineda',
                    'Beasley', 'Sanderson', 'Frye', 'Garrison', 'Trevino', 'Stafford', 'Rankin',
                    'Huerta', 'Luna',
                    'Mustafa', 'Lane', 'Russo', 'Richmond', 'Ferry', 'Wolfe', 'Schmidt', 'Mcnally',
                    'Power',
                    'Castaneda', 'Wickens', 'Romero', 'Smyth', 'Coulson', 'Riley', 'Carty', 'Hogan',
                    'Bonilla',
                    'Mcgee',
                    'Buck', 'Mccoy', 'Schneider', 'Gordon', 'Hardy', 'Ferreira', 'Jarvis', 'Haley',
                    'Bray',
                    'Barnett',
                    'Finch', 'Cox', 'Lawrence', 'Leech', 'Bain', 'Cross', 'Hyde', 'Soto', 'Bates',
                    'Knowles',
                    'Douglas',
                    'Roberts', 'Cornish', 'Robles', 'Macgregor', 'Hines', 'Oakley', 'Santos',
                    'Kirkpatrick',
                    'Alvarez',
                    'Piper', 'Murphy', 'Boyd', 'Haas', 'Corbett', 'Short', 'Alexander', 'Sloan']
        first_name = random.choice(first_names)
        surname = random.choice(surnames)
        _person_name_merge = first_name.lower() + surname.lower()
        client_email_input = f'matthew+{_person_name_merge}@salestrekker.com'
        WdWait(self.driver, 15).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'st-contact[form-name="contactEditForm"]')))
        self.driver.find_element(by=By.CSS_SELECTOR,
                                 value='input[ng-model="$ctrl.contact.person.information.firstName"]').send_keys(
            first_name)
        self.driver.find_element(by=By.CSS_SELECTOR,
                                 value='input[ng-model="$ctrl.contact.person.information.familyName"]').send_keys(
            surname)
        self.driver.find_element(by=By.CSS_SELECTOR,
                                 value='input[ng-model="$ctrl.contact.person.contact.email"]').send_keys(
            client_email_input)


# TODO - Make sure to handle properly if the year range is invalid 1960s for example
# TODO - Make sure to handle properly if one of the sub-options is not available (variant, series)
def glass_test(driver: Chrome, ent: str, link: str):
    kms = random.randint(10, 100)
    md_select_container_id = '0'
    md_select_container = []

    driver.get(link)
    element_waiter(driver, css_selector='st-contact')
    asset_finance = driver.find_element(by=By.XPATH,
                                        value="//span[contains(text(), 'Asset to be financed')]/..")
    element_clicker(driver, web_element=asset_finance)
    element_dissapear(driver, css_selector='alert-progress > md-progress-linear')
    returned_el = element_waiter(driver,
                                 css_selector='button[aria-label="Search asset with Glass\'s"]')
    element_clicker(driver, web_element=returned_el)
    element_waiter(driver, css_selector='md-dialog[aria-label="Glass"]')

    md_selects_opts = {
        'modelTypeCode': 'md-select[ng-model="$ctrl.modelTypeCode"]',
        'yearFrom': 'md-select[ng-model="$ctrl.searchQuery.yearFrom"]',
        'yearTo': 'md-select[ng-model="$ctrl.searchQuery.yearTo"]',
        'manufacturerCode': 'md-select[ng-model="$ctrl.searchQuery.manufacturerCode"]',
        'familyCode': 'md-select[ng-model="$ctrl.searchQuery.familyCode"]',
        'variantName': 'md-select[ng-model="$ctrl.searchQuery.variantName"]',
        'seriesCode': 'md-select[ng-model="$ctrl.searchQuery.seriesCode"]'
    }

    for key, opt in md_selects_opts.items():
        sleep(1)
        print(key)
        md_select = element_waiter(driver, css_selector=opt)
        # md_select = driver.find_element(by=By.CSS_SELECTOR, value='md-select[ng-model="$ctrl.searchQuery.yearFrom"]')
        element_clicker(driver, web_element=md_select)
        md_select_id = str(md_select.get_attribute('id'))
        md_select_container_id = str(int(md_select_id.split("_")[-1]) + 1)
        try:
            WdWait(driver, 5).until(
                ec.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'#select_container_{md_select_container_id}')))

        except exceptions.TimeoutException:
            if key not in ['variantName', 'seriesCode']:
                captured_time = datetime.now().strftime("%H:%M:%S")
                driver.get_screenshot_as_file(
                    f'Reports/{date.today()}/Screenshots/{captured_time} {ent}.png')
                print(f'Captured - Reports/{date.today()}/Screenshots/{captured_time} {ent}.png')
                break
            else:
                print('Timeouted moving on')

        else:
            md_select_container = driver.find_elements(by=By.CSS_SELECTOR,
                                                       value=f'#select_container_{md_select_container_id} md-option')

            if key == 'yearFrom':
                to_click = random.randrange(0, 46)
            else:
                to_click = random.randrange(0, len(md_select_container))

            element_clicker(driver, web_element=md_select_container[to_click])

    else:
        try:
            element_dissapear(driver, css_selector=f'#select_container_{md_select_container_id}')
        except exceptions.TimeoutException:
            element_clicker(driver, web_element=md_select_container[0])

        driver.find_element(by=By.CSS_SELECTOR,
                            value='input[ng-model="$ctrl.actualKilometers"]').send_keys(kms)
        element_clicker(driver, css_selector="button[ng-click='$ctrl.search()']")
        sleep(2)
        finished_glass(driver, ent)


def finished_glass(driver: Chrome, ent: str):
    element_waiter(driver, css_selector='button[aria-label="Select Vehicle"]')
    vehicles = driver.find_elements(by=By.CSS_SELECTOR, value='button[aria-label="Select Vehicle"]')
    vehicle_click = vehicles.index(random.choice(vehicles))
    element_clicker(driver, web_element=vehicles[vehicle_click])
    try:
        WdWait(driver, 5).until(
            ec.presence_of_element_located(
                (By.XPATH, "//md-toast/div/span/span[contains(text(), 'Error')]")))
    except exceptions.TimeoutException:
        element_clicker(driver, css_selector='button[ng-click="$ctrl.importVehicle()"]')
        sleep(2)
        random_date = f'{random.randint(1, 12)}' + f'/{random.randint(1950, 2050)}'
        element_dissapear(driver, css_selector='alert-progress > md-progress-linear')
        driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="MM/YYYY"]').send_keys(
            random_date + Keys.TAB)
        asset_age = driver.find_element(by=By.CSS_SELECTOR, value='select[ng-model="asset.age"]')
        selector(driver, select_element=asset_age)
        driver.find_element(by=By.CSS_SELECTOR, value='input[ng-model="asset.deposit"]').send_keys(
            '500')
        sleep(10)
    else:
        element_clicker(driver, css_selector='button[ng-click="$ctrl.back()"]')
        sleep(0.1)
        captured_time = datetime.now().strftime("%H:%M:%S")
        driver.get_screenshot_as_file(
            f'Reports/{date.today()}/Screenshots/Glass Error {vehicle_click} {captured_time} {ent}.png')
        print(
            f'Captured - Reports/{date.today()}/Screenshots/Glass Error {vehicle_click} {captured_time} {ent}.png')


def organization_query():
    auth = """
    mutation{
        authenticate(email:"matthew@salestrekker.com",password:"+!'Y$pE+{Bw_oXB."){
            token
        }
    }
    """

    all_orgs = """
        query {
            organizations {
                id
                organization {
                    name
                }
            }
        }
    """

    workflows = """
        query{
            workflows{
                id,
                name
            }
        }
    """

    r = requests.post(url='https://dev.salestrekker.com/graphql', json={'query': auth})
    json_data = json.loads(r.text)
    token = json_data['data']['authenticate']['token']

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': '*\*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'dev.salestrekker.com',
        'Origin': 'https://dev.salestrekker.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }

    r = requests.post(url='https://dev.salestrekker.com/graphql', json={'query': all_orgs}, headers=headers)
    json_data = json.loads(r.text)
    org_list = json_data['data']['organizations']
    print(org_list)
    org_id = ''
    for org in org_list:
        if org['organization']['name'] == 'Changing name org test':
            org_id = org['id']

    org_auth = f"""
    mutation{{
        authenticateInDifferentOrganization(id: "{org_id}"){{
            token
            }}
        }}
    """
    r = requests.post(url='https://dev.salestrekker.com/graphql', json={'query': org_auth}, headers=headers)
    json_data = json.loads(r.text)
    token = json_data['data']['authenticateInDifferentOrganization']['token']
    headers['Authorization'] = 'Bearer ' + token

    r = requests.post(url='https://dev.salestrekker.com/graphql', json={'query': workflows}, headers=headers)
    json_data = json.loads(r.text)
    workflow_list = json_data['data']['workflows']
    print(workflow_list)


if __name__ == "__main__":
    organization_query()

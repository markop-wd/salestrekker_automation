from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Chrome
from selenium.common import exceptions

from main.Permanent.helper_funcs import random_string_create, AddressInput, element_clicker, selector
from main.Permanent.deal_fill_selectors import *

from time import sleep
import json
import string
import random
import traceback
from pathlib import Path


class MultipleDealCreator:

    def __init__(self, driver: Chrome):
        # TODO - Review working with paths

        # These two below are for employment information (occupation and industry codes)
        occupation_path = Path(__file__).parent.resolve() / "../assets/occupations.json"
        with open(occupation_path) as occupation_codes:
            self.occupations = json.load(occupation_codes)

        industry_path = Path(__file__).parent.resolve() / "../assets/industries.json"
        with open(industry_path, 'r') as industry_codes:
            self.industries = json.load(industry_codes)

        # This is the main deal config file
        deal_config = Path(__file__).parent.resolve() / "../deal_config.json"
        with open(deal_config) as deal_config_json:
            self.deal_config = json.load(deal_config_json)

        self.driver = driver
        self.address_placeholders = ['Search Property (eg. 1 Walker Avenue)',
                                     'Search current address',
                                     'Search employer address', 'Search next of kin address',
                                     'Search mailing address',
                                     'Search previous address',
                                     'Search post settlement address']

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

    def employment_handler(self):

        self._first_employment()
        employ_num = self.deal_config["contacts"]["employment"]["num"]

        try:
            employment = self.driver.find_element(by=eval(EMPLOYMENT_BUTTON['by']),
                                                  value=EMPLOYMENT_BUTTON['value'])
        except exceptions.NoSuchElementException:
            print('Am in company, weird')
            return
            # self.driver.get_screenshot_as_file(
            #     f'Reports/{date.today()}/Screenshots/employment{random_string_create(3)}.png')

        for i in range(1, employ_num):
            element_clicker(self.driver, web_element=employment)

            employment_status = self.driver.find_elements(by=eval(EMPLOY_STATUS['by']),
                                                          value=EMPLOY_STATUS['value'])[i]
            selector(self.driver, select_element=employment_status, index='random', rand_range='0-2')

            employment_type = self.driver.find_elements(by=eval(EMPLOY_TYPE['by']),
                                                        value=EMPLOY_TYPE['value'])[i]
            selector(self.driver, select_element=employment_type, index='random', rand_range='1-5')

            employment_priority = self.driver.find_elements(by=eval(EMPLOY_PRIORITY['by']),
                                                            value=EMPLOY_PRIORITY['value'])[i]
            selector(self.driver, select_element=employment_priority, index='random', rand_range='1-3')
            emply_els = self.driver.find_elements(by=eval(EMPLOY_BASIS['by']),
                                                             value=EMPLOY_BASIS['value'])
            try:
                employment_basis = emply_els[i-1]
            except exceptions.NoSuchElementException:
                pass
            else:
                selector(self.driver, select_element=employment_basis, index='random')

    def _first_employment(self):
        try:
            employment = self.driver.find_element(by=eval(EMPLOYMENT_BUTTON['by']),
                                                  value=EMPLOYMENT_BUTTON['value'])
        except exceptions.NoSuchElementException:
            print('No employment element, something\'s gone off. First employment')
            # self.driver.get_screenshot_as_file(
            #     f'Reports/{date.today()}/Screenshots/employment{random_string_create(3)}.png')
        else:
            element_clicker(self.driver, web_element=employment)

            sleep(0.01)

            employ_status = self.driver.find_element(by=eval(EMPLOY_STATUS['by']),
                                                     value=EMPLOY_STATUS['value'])
            selector(self.driver, select_element=employ_status, index='0')

            employ_type = self.driver.find_element(by=eval(EMPLOY_TYPE['by']),
                                                   value=EMPLOY_TYPE['value'])
            selector(self.driver, select_element=employ_type, index='random', rand_range='1-3')

            employ_priority = self.driver.find_element(by=eval(EMPLOY_PRIORITY['by']),
                                                       value=EMPLOY_PRIORITY['value'])
            selector(self.driver, select_element=employ_priority, index='random', rand_range='1-3')

            employ_basis = self.driver.find_element(by=eval(EMPLOY_BASIS['by']),
                                                    value=EMPLOY_BASIS['value'])
            selector(self.driver, select_element=employ_basis, index='random')

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

                    elif ng_model in ['$ctrl.contact.person.contact.work', '$ctrl.contact.person.contact.home']:
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
                    ec.element_to_be_clickable((By.ID, 'select_container_' + md_select_container_id)))
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

    def client_profile_input(self, deal_url):
        if deal_url != self.driver.current_url:
            self.driver.get(deal_url)

        WdWait(self.driver, 20).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'st-sidebar-block > div > button')))
        """
        A couple of ways to click this tools/profile button. One way is to click st-sidebar-block button:nth-child(2),
        but getting all els and going for the last one seems solid enough
        """
        profile_buttons = self.driver.find_elements(by=By.CSS_SELECTOR, value='st-sidebar-block button')
        element_clicker(self.driver, web_element=profile_buttons[-1])
        # TODO - 30 seconds wait for the st-contact which is in 90% of situations the first page, maybe try another way
        try:
            WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'st-contact')))
        except exceptions.TimeoutException:
            WdWait(self.driver, 20).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'st-contact')))

        contact_buttons = self.driver.find_elements(by=eval(CONTACT_BUTTONS['by']),
                                                    value=CONTACT_BUTTONS['value'])

        contact_info = []
        for contact in contact_buttons:
            contact_info.append(
                {
                    'web_el': contact,
                    'type': contact.find_element(by=By.CSS_SELECTOR, value='small > span').text,
                    'contact_name': contact.find_element(by=By.CSS_SELECTOR, value='span.truncate').text
                 }
            )

        for contact_button in contact_info:

            if not element_clicker(self.driver, web_element=contact_button['web_el']):
                contact_button['web_el'] = self.driver.find_element(by=By.XPATH,
                                                                    value=f"//st-sidebar-block/div/button/span[contains(text(),'{contact_button['contact_name']}')]/..")
                element_clicker(self.driver, web_element=contact_button['web_el'])

            content = WdWait(self.driver, 10).until(
                ec.presence_of_element_located((eval(CONTENT['by']), CONTENT['value'])))

            self.select_el_handler(content)

            self.md_select_handler(content)

            self.md_radio_group(content)

            if contact_button['type'] == 'Personal':
                self.employment_handler()

            self.select_el_handler(content)

            self.input_el_handler(content)

            self.checkbox_handler(content)

            textarea_handler(content)

        # self.driver.refresh()
        WdWait(self.driver, 20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'form-content > form')))

        try:
            buttons = self.driver.find_elements(by=eval(PROFILE_BUTTONS['by']),
                                                value=PROFILE_BUTTONS['value'])
        except exceptions.NoSuchElementException:
            print('No div > buttons')
        else:
            separators = []

            for button in buttons:

                try:
                    current_separator = button.find_element(by=eval(BUTTON_TEXT['by']),
                                                            value=BUTTON_TEXT['value']).text
                except exceptions.StaleElementReferenceException as inst:
                    # TODO ?
                    print(inst.stacktrace)
                    print('Current separator exception')
                    continue

                if current_separator in ['Asset to be financed', 'Lender and product',
                                         'Compare products',
                                         'Security details', 'Funding worksheet',
                                         'Maximum borrowing']:
                    break
                if current_separator in ['Connect to Mercury', 'Connect to Flex']:
                    continue

                separators.append(current_separator)

            # I am using separator names rather than buttons as the page might need to be reloaded and the buttons might go stale
            for separator in separators:
                try:
                    current_button = self.driver.find_element(by=By.XPATH,
                                                              value=f"//span[text()='{separator}']/ancestor::button[position()=1]")
                except exceptions.NoSuchElementException:
                    # For other advisers separator
                    current_button = self.driver.find_element(by=By.XPATH,
                                                              value=f"//*[normalize-space(span)='{separator}']")

                if not element_clicker(self.driver, web_element=current_button):
                    print('didn\'t click', separator)
                    continue

                content = WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((eval(CONTENT['by']), CONTENT['value'])))

                if separator == 'Income':
                    income_buttons = self.driver.find_elements(by=eval(INFO_BUTTONS['by']),
                                                               value=INFO_BUTTONS['value'])
                    for income_button in income_buttons:

                        if not element_clicker(self.driver, web_element=income_button):
                            continue

                    sleep(0.1)

                    self.md_select_handler(content)

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                elif separator == 'Expenses':
                    # TODO - Make this smarter, check if one is already added and so forth
                    WdWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.TAG_NAME, 'st-households')))
                    self.driver.find_element(by=eval(ADD_HOUSEHOLD['by']),
                                             value=ADD_HOUSEHOLD['value']).click()

                    household_picker = WdWait(self.driver, 10).until(ec.presence_of_element_located(
                        (eval(HOUSEHOLD_PICKER['by']), HOUSEHOLD_PICKER['value'])))
                    element_clicker(self.driver, web_element=household_picker)

                    household_picker_id = household_picker.get_attribute('id')
                    household_picker_container_id = str(int(household_picker_id.split("_")[-1]) + 1)
                    household_picker_container = WdWait(self.driver, 10).until(
                        ec.element_to_be_clickable(
                            (By.ID, "select_container_" + household_picker_container_id)))
                    household_members = household_picker_container.find_elements(by=By.CSS_SELECTOR,
                                                                                 value='md-option')

                    for household_member in household_members:
                        household_member.click()

                    sleep(0.5)

                    self.driver.find_element(by=By.TAG_NAME, value='md-backdrop').click()

                    self.input_el_handler(content)

                    self.select_el_handler(content)

                if separator == 'Assets':
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

                elif separator == 'Liabilities':

                    liabilities = self.driver.find_elements(by=eval(INFO_BUTTONS['by']),
                                                            value=INFO_BUTTONS['value'])

                    for _ in range(0, random.randint(3, 7)):
                        element_clicker(self.driver, web_element=random.choice(liabilities))

                    # for liability in liabilities:
                    #     if not element_clicker(self.driver, web_element=liability):
                    #         continue
                    #     if not element_clicker(self.driver, web_element=liability):
                    #         continue

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    self.md_select_handler(content)

                elif separator == 'Needs and objectives':

                    textarea_handler(content)

                    self.md_radio_group(content)

                    self.checkbox_handler(content)

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    textarea_handler(content)

                elif separator == 'Product requirements':
                    textarea_handler(content)

                    self.select_el_handler(content)

                    self.md_radio_group(content)

                    self.checkbox_handler(content)

                    self.input_el_handler(content)

                    textarea_handler(content)

                elif separator == 'Insurance':
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

                elif separator == 'Other advisers':
                    # TODO - Fix other adviser adding
                    other_advisers = self.driver.find_elements(by=eval(INFO_BUTTONS['by']),
                                                               value=INFO_BUTTONS['value'])
                    for other_adviser in other_advisers:
                        if not element_clicker(self.driver, web_element=other_adviser):
                            continue
                        if not element_clicker(self.driver, web_element=other_adviser):
                            continue

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                elif separator == 'Analysis':

                    textarea_handler(content)

                    self.select_el_handler(content)

                    self.md_radio_group(content)

                    self.checkbox_handler(content)

                    self.input_el_handler(content)

                    textarea_handler(content)

                else:
                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    self.md_select_handler(content)


def textarea_handler(content):
    for textarea in content.find_elements(by=By.TAG_NAME, value='textarea'):
        try:
            textarea.send_keys(random_string_create())
        except exceptions.ElementNotInteractableException:
            continue

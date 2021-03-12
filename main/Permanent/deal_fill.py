from main.Permanent import workflow_manipulation

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Chrome
from selenium.common import exceptions

from main.Permanent.helper_funcs import random_string_create, md_toast_remover

from time import sleep
from datetime import datetime
import json
import random
import traceback
from pathlib import Path


class MultipleDealCreator:

    def __init__(self, ent, driver: Chrome):
        # self.current_export_array = []
        occupation_path = Path(__file__).parent.resolve() / "../assets/occupations.json"
        with open(occupation_path) as occupation_codes:
            self.occupations = json.load(occupation_codes)

        industry_path = Path(__file__).parent.resolve() / "../assets/industries.json"
        with open(industry_path, 'r') as industry_codes:
            self.industries = json.load(industry_codes)

        with open("deal_config.json") as deal_config_json:
            self.deal_config = json.load(deal_config_json)

        self.users_in_workflow = ''
        self.number_of_contacts = None
        self.driver = driver
        self.main_url = 'https://' + ent + '.salestrekker.com'
        # self.wf_manipulate = workflow_manipulation.WorkflowManipulation(self.driver, ent)
        self.address_repeat = 0
        self.address_placeholders = ['Search Property (eg. 1 Walker Avenue)',
                                     'Search current address',
                                     'Search employer address', 'Search next of kin address',
                                     'Search mailing address',
                                     'Search previous address']

    def selector(self, select_element, index='random'):
        try:
            current_sel = Select(select_element)
        except exceptions.StaleElementReferenceException as inst:
            print('Stale reference', inst)
            print(inst.stacktrace)
        except:
            traceback.print_stack()
            traceback.print_exc()
        else:
            if index == 'random':
                try:
                    index = random.randrange(1, len(current_sel.options))
                except ValueError:
                    index = random.randrange(0, 2)
            else:
                index = int(index)
            # TODO - Handle the selector exceptions properly
            try:
                current_sel.select_by_index(index)
            except exceptions.ElementClickInterceptedException:
                md_toast_remover(self.driver)
                try:
                    current_sel.select_by_index(index)
                except exceptions.ElementClickInterceptedException:
                    print('removing header')
                    md_toast_remover(self.driver)

                    try:
                        header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                          value='st-header.new.ng-scope')
                    except exceptions.NoSuchElementException:
                        pass
                    else:
                        self.driver.execute_script("arguments[0].remove();", header)

                    try:
                        scroll_mask = self.driver.find_element(by=By.CSS_SELECTOR,
                                                               value='div.md-scroll-mask')
                        self.driver.execute_script("arguments[0].remove();", scroll_mask)
                    except exceptions.NoSuchElementException:
                        pass

                    try:
                        current_sel.select_by_index(index)
                    except ValueError:
                        current_sel.select_by_index(index)

                except ValueError:
                    current_sel.select_by_index(index)

            except exceptions.NoSuchElementException:
                pass

            except ValueError:
                try:
                    current_sel.select_by_index(index)
                except exceptions.ElementClickInterceptedException:
                    md_toast_remover(self.driver)
                    try:
                        current_sel.select_by_index(index)
                    except exceptions.ElementClickInterceptedException:
                        print('removing header')
                        md_toast_remover(self.driver)
                        header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                          value='st-header.new.ng-scope')
                        self.driver.execute_script("arguments[0].remove();", header)
                        current_sel.select_by_index(index)

    def select_el_handler(self, content):

        md_toast_remover(self.driver)

        for select_el in content.find_elements(by=By.TAG_NAME, value='select'):
            try:
                if select_el.get_attribute('ng-model') == '$ctrl.address.country':
                    self.selector(select_el, index='1')
                elif select_el.get_attribute('ng-model') in ['$ctrl.employment.isCurrent',
                                                             '$ctrl.employment.type',
                                                             '$ctrl.employment.status',
                                                             '$ctrl.employment.basis']:
                    continue
                else:
                    self.selector(select_el)
            except exceptions.StaleElementReferenceException:
                continue

    def md_radio_group(self, content):
        for md_radio_group in content.find_elements(by=By.TAG_NAME, value='md-radio-group'):
            try:
                md_radio_buttons = md_radio_group.find_elements(by=By.TAG_NAME,
                                                                value='md-radio-button')
                radio_button_to_click = random.randrange(0, len(md_radio_buttons))
                try:
                    md_radio_buttons[radio_button_to_click].click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();",
                                               md_radio_buttons[radio_button_to_click])
                except Exception as inst:
                    print('Exception', inst)
                    continue
            except exceptions.StaleElementReferenceException:
                continue

    def employment_handler(self):

        self._first_employment()
        employ_num = self.deal_config["contacts"]["employment"]["num"]

        for i in range(employ_num):
            try:
                employment = self.driver.find_element(by=By.CSS_SELECTOR,
                                                      value='st-block-form-header > button[ng-click="$ctrl.employmentAdd($event)"]')
            except exceptions.NoSuchElementException:
                print('No employment element, something\'s gone off. Handler')
            else:
                try:
                    employment.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', employment)

                for count, employment_status in enumerate(self.driver.find_elements(by=By.CSS_SELECTOR,
                                                                                    value='select[ng-change="$ctrl.toggleEmployment()"]')):
                    if count == 0:
                        continue
                    try:
                        Select(employment_status).select_by_index(random.randrange(0, 2))
                    except exceptions.ElementClickInterceptedException:
                        md_toast_remover(self.driver)
                        try:
                            Select(employment_status).select_by_index(random.randrange(0, 2))
                        except exceptions.ElementClickInterceptedException:
                            header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                              value='st-header.new.ng-scope')
                            self.driver.execute_script("arguments[0].remove();", header)
                            Select(employment_status).select_by_index(random.randrange(0, 2))

                for count, employment_type in enumerate(self.driver.find_elements(by=By.CSS_SELECTOR,
                                                                                  value='select[ng-change="$ctrl.toggleEmploymentType()"]')):
                    if count == 0:
                        continue
                    try:
                        Select(employment_type).select_by_index(random.randrange(1, 5))
                    except exceptions.ElementClickInterceptedException:
                        md_toast_remover(self.driver)
                        try:
                            Select(employment_type).select_by_index(random.randrange(1, 5))
                        except exceptions.ElementClickInterceptedException:
                            header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                              value='st-header.new.ng-scope')
                            self.driver.execute_script("arguments[0].remove();", header)
                            Select(employment_type).select_by_index(random.randrange(1, 5))

                for count, employment_priority in enumerate(self.driver.find_elements(by=By.CSS_SELECTOR,
                                                                                      value='select[ng-model="$ctrl.employment.status"]')):
                    if count == 0:
                        continue
                    try:
                        Select(employment_priority).select_by_index(random.randrange(1, 3))
                    except exceptions.ElementClickInterceptedException:
                        md_toast_remover(self.driver)
                        try:
                            Select(employment_priority).select_by_index(random.randrange(1, 3))
                        except exceptions.ElementClickInterceptedException:
                            header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                              value='st-header.new.ng-scope')
                            self.driver.execute_script("arguments[0].remove();", header)
                            Select(employment_priority).select_by_index(random.randrange(1, 3))

                try:
                    employment_basis = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                                 value='select[ng-model="$ctrl.employment.basis"]')
                except exceptions.NoSuchElementException:
                    pass
                else:
                    for count, basis in enumerate(employment_basis):
                        if count == 0:
                            continue
                        try:
                            num_basis_options = len(Select(basis).options)
                        except exceptions.ElementClickInterceptedException:
                            md_toast_remover(self.driver)
                            try:
                                num_basis_options = len(Select(basis).options)
                            except exceptions.ElementClickInterceptedException:
                                header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                                  value='st-header.new.ng-scope')
                                self.driver.execute_script("arguments[0].remove();", header)
                                num_basis_options = len(Select(basis).options)

                        try:
                            Select(basis).select_by_index(random.randrange(1, num_basis_options))
                        except exceptions.ElementClickInterceptedException:
                            md_toast_remover(self.driver)
                            try:
                                Select(basis).select_by_index(
                                    random.randrange(1, num_basis_options))
                            except exceptions.ElementClickInterceptedException:
                                header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                                  value='st-header.new.ng-scope')
                                self.driver.execute_script("arguments[0].remove();", header)
                                Select(basis).select_by_index(
                                    random.randrange(1, num_basis_options))

    def _first_employment(self):
        try:
            employment = self.driver.find_element(by=By.CSS_SELECTOR,
                                                  value='st-block-form-header > button[ng-click="$ctrl.employmentAdd($event)"]')
        except exceptions.NoSuchElementException:
            print('No employment element, something\'s gone off. First employment')
        else:
            try:
                employment.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script('arguments[0].click();', employment)

            finally:
                sleep(0.01)

                employ_status = self.driver.find_element(by=By.CSS_SELECTOR,
                                                         value='select[ng-change="$ctrl.toggleEmployment()"]')
                try:
                    Select(employ_status).select_by_index(0)
                except exceptions.ElementClickInterceptedException:
                    md_toast_remover(self.driver)
                    try:
                        Select(employ_status).select_by_index(0)
                    except exceptions.ElementClickInterceptedException:
                        header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                          value='st-header.new.ng-scope')
                        self.driver.execute_script("arguments[0].remove();", header)
                        Select(employ_status).select_by_index(0)

                employ_type = self.driver.find_element(by=By.CSS_SELECTOR,
                                                       value='select[ng-change="$ctrl.toggleEmploymentType()"]')
                try:
                    Select(employ_type).select_by_index(random.randrange(1, 3))
                except exceptions.ElementClickInterceptedException:
                    md_toast_remover(self.driver)
                    try:
                        Select(employ_type).select_by_index(random.randrange(1, 3))
                    except exceptions.ElementClickInterceptedException:
                        header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                          value='st-header.new.ng-scope')
                        self.driver.execute_script("arguments[0].remove();", header)
                        Select(employ_type).select_by_index(random.randrange(1, 3))

                employ_priority = self.driver.find_element(by=By.CSS_SELECTOR,
                                                           value='select[ng-model="$ctrl.employment.status"]')
                try:
                    Select(employ_priority).select_by_index(random.randrange(1, 3))
                except exceptions.ElementClickInterceptedException:
                    md_toast_remover(self.driver)
                    try:
                        Select(employ_priority).select_by_index(random.randrange(1, 3))
                    except exceptions.ElementClickInterceptedException:
                        header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                          value='st-header.new.ng-scope')
                        self.driver.execute_script("arguments[0].remove();", header)
                        Select(employ_priority).select_by_index(random.randrange(1, 3))

                employ_basis = self.driver.find_element(by=By.CSS_SELECTOR,
                                                        value='select[ng-model="$ctrl.employment.basis"]')
                try:
                    num_basis_options = len(Select(employ_basis).options)
                except exceptions.ElementClickInterceptedException:
                    md_toast_remover(self.driver)
                    try:
                        num_basis_options = len(Select(employ_basis).options)
                    except exceptions.ElementClickInterceptedException:
                        header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                          value='st-header.new.ng-scope')
                        self.driver.execute_script("arguments[0].remove();", header)
                        num_basis_options = len(Select(employ_basis).options)

                try:
                    Select(employ_basis).select_by_index(random.randrange(1, num_basis_options))
                except exceptions.ElementClickInterceptedException:
                    md_toast_remover(self.driver)
                    try:
                        Select(employ_basis).select_by_index(
                            random.randrange(1, num_basis_options))
                    except exceptions.ElementClickInterceptedException:
                        header = self.driver.find_element(by=By.CSS_SELECTOR,
                                                          value='st-header.new.ng-scope')
                        self.driver.execute_script("arguments[0].remove();", header)
                        Select(employ_basis).select_by_index(
                            random.randrange(1, num_basis_options))

    def ul_list_selector(self, input_el, input_text):
        sleep(5)
        self.address_repeat += 1
        input_el.send_keys(input_text)
        ul_el_id = 'ul-' + str(input_el.get_attribute('id')).split('-')[-1]
        try:
            WdWait(self.driver, 15).until(ec.visibility_of_element_located((By.ID, ul_el_id)))
        except exceptions.TimeoutException:
            print('No list returned after 15 seconds')
            if self.address_repeat > 4:
                print('No list returned after 4 timeout attempts.')
            else:
                sleep(5)
                self.ul_list_selector(input_el, input_text)
        else:
            li_els = self.driver.find_element(By.ID, ul_el_id).find_elements(by=By.CSS_SELECTOR,
                                                                             value='li span')
            if len(li_els) == 0:
                input_el.send_keys(Keys.CONTROL + 'a')
                sleep(0.1)
                input_el.send_keys(Keys.DELETE)
                sleep(0.2)
                if self.address_repeat > 4:
                    print('List not returning after 4 attempts')
                else:
                    self.ul_list_selector(input_el, input_text)
            else:
                self.driver.execute_script("arguments[0].click();",
                                           li_els[random.randrange(0, len(li_els))])

    def input_el_handler(self, content):

        try:
            for input_el in content.find_elements(by=By.TAG_NAME, value='input'):
                self.address_repeat = 0

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

                elif not value_test:
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
                            self.ul_list_selector(input_el, f'{random.randrange(1, 200)} oi')

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

                    elif ng_change == '$ctrl.saveAddress()':
                        continue

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
                try:
                    md_select.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", md_select)
                except exceptions.ElementNotInteractableException:
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
                try:
                    md_select_container[to_click].click()
                except exceptions.ElementNotInteractableException:
                    pass
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", md_select_container[to_click])
                except:
                    traceback.print_stack()
                    traceback.print_exc()
            except:
                traceback.print_stack()
                traceback.print_exc()
                continue

    def checkbox_handler(self, content):
        for checkbox in content.find_elements(by=By.TAG_NAME, value='md-checkbox'):
            try:
                if checkbox.get_attribute('ng-change') == '$ctrl.marketingToggle()':
                    continue
                else:
                    if random.randrange(0, 100) > 30:
                        try:
                            checkbox.click()
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script('arguments[0].click();', checkbox)
                        except:
                            traceback.print_stack()
                            traceback.print_exc()
            except exceptions.NoSuchElementException:
                print('excepted exception but why')
            except exceptions.StaleElementReferenceException:
                print('Stale elemento')

    def client_profile_input(self, deal_url):
        self.driver.get(deal_url)
        try:
            WdWait(self.driver, 20).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, 'st-sidebar-block button:nth-child(2)')))
        except exceptions.TimeoutException:
            WdWait(self.driver, 20).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, 'st-sidebar-block > div > button')))

        test = self.driver.find_elements(by=By.CSS_SELECTOR, value='st-sidebar-block button')
        test[-1].click()
        try:
            WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'st-contact')))
        except exceptions.TimeoutException:
            WdWait(self.driver, 20).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'st-contact')))

        contact_buttons = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                    value='st-sidebar-content > st-sidebar-block:first-of-type > div '
                                                          '> button')

        for button_count, contact_button in enumerate(contact_buttons, start=1):
            self.address_repeat = 0
            try:
                current_button = self.driver.find_element(by=By.XPATH,
                                                          value=f'//span[text()={button_count}]/ancestor::*[position()=2]')
            except exceptions.NoSuchElementException:
                print(f'{button_count}')
                print('No such element?')
            else:
                try:
                    current_button.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', current_button)

                content = WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))

                self.select_el_handler(content)

                self.md_select_handler(content)

                self.md_radio_group(content)

                self.employment_handler()

                self.select_el_handler(content)

                self.input_el_handler(content)

                self.checkbox_handler(content)

                textarea_handler(content)

        # self.driver.refresh()
        WdWait(self.driver, 20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'form-content > form')))

        try:
            buttons = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                value='st-sidebar-content > st-sidebar-block > div > div > button')
        except exceptions.NoSuchElementException:
            print('No div > button')
            pass
        else:
            separators = []

            for button_count, button in enumerate(buttons, start=1):

                try:
                    current_separator = button.find_element(by=By.CSS_SELECTOR,
                                                            value='div > button > span.truncate').text
                except exceptions.StaleElementReferenceException as inst:
                    # TODO TODO TODO TODO TODO
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

            for separator in separators:
                self.address_repeat = 0
                try:
                    current_button = self.driver.find_element(by=By.XPATH,
                                                              value=f"//span[text()='{separator}']/ancestor::button[position()=1]")
                except exceptions.NoSuchElementException as inst:
                    print(inst.stacktrace)
                    print('No such separator')
                    print(f'{separator}')
                    current_button = self.driver.find_element(by=By.XPATH,
                                                              value=f"//*[normalize-space(span)='{separator}']")
                try:
                    current_button.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', current_button)

                except exceptions.ElementNotInteractableException:
                    self.driver.execute_script('arguments[0].click();', current_button)

                content = WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))

                if separator == 'Income':
                    income_buttons = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                               value='div.mt0 button')
                    for income_button in income_buttons:
                        try:
                            income_button.click()
                        except exceptions.ElementNotInteractableException:
                            continue
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", income_button)
                        else:
                            sleep(0.01)
                            income_button.click()

                    sleep(0.1)

                    self.md_select_handler(content)

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                elif separator == 'Expenses':
                    WdWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.TAG_NAME, 'st-households')))
                    self.driver.find_element(by=By.CSS_SELECTOR,
                                             value='st-block-form-header > button').click()

                    household_picker = WdWait(self.driver, 10).until(ec.presence_of_element_located(
                        (By.CSS_SELECTOR,
                         'st-tabs-list-content > div > div > div > md-input-container > md-select')))
                    try:
                        household_picker.click()
                    except exceptions.ElementClickInterceptedException:
                        pass
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
                    assets = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.mt0 button')
                    for asset in assets:
                        try:
                            asset.click()
                        except exceptions.ElementNotInteractableException:
                            continue
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", asset)
                        else:
                            sleep(0.01)
                            asset.click()

                    self.checkbox_handler(content)

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    self.md_select_handler(content)

                elif separator == 'Liabilities':

                    liabilities = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                            value='div.mt0 button')
                    for liability in liabilities:
                        try:
                            liability.click()
                        except exceptions.ElementNotInteractableException:
                            continue
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", liability)
                        else:
                            sleep(0.01)
                            try:
                                liability.click()
                            except exceptions.ElementClickInterceptedException:
                                self.driver.execute_script("arguments[0].click();", liability)

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
                    insurance = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                          value='div.mt0 button')
                    for insuranc in insurance:
                        try:
                            insuranc.click()
                        except exceptions.ElementNotInteractableException:
                            continue
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", insuranc)
                        else:
                            sleep(0.01)
                            try:
                                insuranc.click()
                            except exceptions.ElementNotInteractableException:
                                continue

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    self.md_select_handler(content)

                elif separator == 'Other advisers':
                    # TODO - Fix other adviser adding
                    other_advisers = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                               value='div.mt0 button')
                    for other_adviser in other_advisers:
                        try:
                            other_adviser.click()
                        except exceptions.ElementNotInteractableException:
                            continue
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", other_adviser)
                        except exceptions.StaleElementReferenceException:
                            continue
                        else:
                            sleep(0.01)
                            other_adviser.click()

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

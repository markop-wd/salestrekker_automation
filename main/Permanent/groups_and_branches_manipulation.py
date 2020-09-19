import csv
import traceback
from os import path
from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as WdWait

from main.Permanent.csv_reader import billables


# TODO - Empty lender accreditation check
# TODO -
class GroupsAndBranches:

    def __init__(self, driver: Chrome, ent):
        self.driver = driver
        self.ent = ent
        self.organisations = []
        self.organisation_names = []
        self.lender = ''
        self.gateway = ''

    def existing_lender_accreditation(self, lender: str, lender_value: str, overwrite: bool):
        # TODO - Add numbers
        for md_select in self.driver.find_elements_by_css_selector('st-block-form-content md-select:first-of-type'):
            if lender.lower() in md_select.get_attribute('aria-label').lower():
                md_select_input_value = md_select.find_element_by_xpath(
                    '../../md-input-container/input[@ng-model="lenderAccreditation.brokerIdPrimary"]')
                if md_select_input_value.get_attribute('value') == lender_value:
                    return True
                else:
                    if overwrite:
                        md_select_input_value.send_keys(Keys.CONTROL + 'a')
                        md_select_input_value.send_keys(Keys.DELETE)
                        md_select_input_value.send_keys(lender_value)

                    return True
        else:
            return False

    def existing_gateway_accreditation(self, gateway: str, gateway_value: str, overwrite: bool):
        for select in self.driver.find_elements_by_css_selector('st-block-form-content select'):
            if gateway.lower() in str(Select(select).first_selected_option.text).lower():
                select_input_value = select.find_element_by_xpath(
                    '../../md-input-container/input[@ng-model="gatewayAccreditation.brokerUsername"]')
                if select_input_value.get_attribute('value') == gateway_value:
                    return True
                else:
                    if overwrite:
                        select_input_value.send_keys(Keys.CONTROL + 'a')
                        select_input_value.send_keys(Keys.DELETE)
                        select_input_value.send_keys(gateway_value)
                    return True
        else:
            return False

    def md_select_handler(self, md_select, to_find: str):

        try:
            md_select.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", md_select)
        except exceptions.ElementNotInteractableException:
            self.driver.execute_script("arguments[0].click();", md_select)
        finally:
            md_select_id = str(md_select.get_attribute('id'))
            md_select_container_id = 'select_container_' + str(int(md_select_id.split("_")[-1]) + 1)

            WdWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.ID, md_select_container_id)))

        self.driver.find_element_by_id(md_select_container_id).click()

        lender_element = self.driver.find_element_by_xpath(
            f"//div[@id='{md_select_container_id}']/md-select-menu/md-content/md-option[contains(text(), '{to_find}')]")

        try:
            lender_element.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', lender_element)
        except exceptions.ElementNotInteractableException:
            self.driver.execute_script('arguments[0].click();', lender_element)

    def css_clicker(self, css_selector: str):
        try:
            element = self.driver.find_element_by_css_selector(css_selector)

        except exceptions.NoSuchElementException:
            return False
        else:
            try:
                element.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script('arguments[0].click();', element)
            except exceptions.ElementNotInteractableException:
                self.driver.execute_script('arguments[0].click();', element)
            except:
                print('Broke here')
                traceback.print_exc()
                traceback.print_stack()
                return False
            finally:
                return True

    def group_and_branches_scroller(self, element_with_scroll):

        scroll_total = self.driver.execute_script("return arguments[0].scrollHeight;", element_with_scroll)

        while True:

            sleep(1)

            self.driver.execute_script(f"arguments[0].scroll(0,{scroll_total});", element_with_scroll)

            scroll_new = self.driver.execute_script("return arguments[0].scrollHeight;", element_with_scroll)

            self.driver.execute_script(f"arguments[0].scroll(0,{scroll_new});", element_with_scroll)

            scroll_total = self.driver.execute_script("return arguments[0].scrollHeight;", element_with_scroll)

            if scroll_new == scroll_total:
                try:
                    WdWait(self.driver, 2).until(
                        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'md-progress-linear#whenScrolled')))
                except exceptions.TimeoutException:
                    self.driver.execute_script(f"arguments[0].scroll(0,0);", element_with_scroll)
                    continue
                else:
                    break

    def groups_and_branches_main(self, organizations: list, ran_number: str, identification: str,
                                 organization_name: str,
                                 email: bool = True):

        self.organisation_names = []
        for organization in organizations:
            name_of_the_organization_el = str(organization.find_element_by_tag_name('span').text).lower()
            self.organisation_names.append(name_of_the_organization_el)

        if email:
            billable_orgs = billables(identification, self.ent)
            if billable_orgs:
                for billable_org_name in billable_orgs:
                    if str(billable_org_name).lower() in self.organisation_names:
                        for count, organization in enumerate(organizations):
                            name_of_the_organization_el = self.organisation_names[count]
                            if name_of_the_organization_el == billable_org_name.lower():
                                organization_name = billable_org_name

                                if organization_name not in self.organisations:

                                    try:
                                        organization.click()
                                    except exceptions.ElementClickInterceptedException:
                                        try:
                                            self.driver.execute_script(
                                                "document.querySelector('.new.ng-scope').remove()")
                                        except exceptions.JavascriptException:
                                            pass
                                        self.driver.execute_script('arguments[0].click();', organization)
                                    except exceptions.ElementNotInteractableException:
                                        try:
                                            self.driver.execute_script(
                                                "document.querySelector('.new.ng-scope').remove()")
                                        except exceptions.JavascriptException:
                                            pass
                                        self.driver.execute_script('arguments[0].click();', organization)
                                    finally:
                                        try:
                                            WdWait(self.driver, 10).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                                              '//st-list-item/div/a/../../st-list-item[@aria-hidden="false"]/md-progress-linear')))
                                        except exceptions.TimeoutException:
                                            try:
                                                WdWait(self.driver, 15).until(
                                                    ec.invisibility_of_element_located((By.XPATH,
                                                                                        '//st-list-item/div/a/../../st-list-item[@aria-hidden="false"]/md-progress-linear')))
                                            except exceptions.TimeoutException:
                                                return 'Sooomething weeent wrooong'
                                else:

                                    content = self.driver.find_element_by_css_selector('body > md-content')

                                    self.driver.execute_script(
                                        f"arguments[0].scroll({organization.location['x']},{organization.location['y']});",
                                        content)

                                for account in organization.find_elements_by_xpath(
                                        '//../st-list-item[@ng-show="$ctrl.showAccounts(branch) && $ctrl.hasAccounts(branch)"]'):

                                    sleep(0.1)

                                    if email:
                                        if str(account.find_element_by_css_selector('em').text).lower() == str(
                                                identification).lower():
                                            account.find_element_by_css_selector(
                                                'a > span[aria-label="Edit Account"]').click()
                                            self.user_edit_box(ran_number, [identification, billable_org_name, email])
                                            break

                                    else:
                                        if str(account.find_element_by_css_selector(
                                                'span[ng-bind="::account.getName()"]').text).lower() == str(identification).lower():
                                            account.find_element_by_css_selector(
                                                'a > span[aria-label="Edit Account"]').click()
                                            self.user_edit_box(ran_number, [identification, billable_org_name, email])
                                            break
                                else:
                                    self.csv_writer(account=identification, organization=organization_name,
                                                    statement='No such account')

                                break
                        break

            else:
                self.csv_writer(account=identification, organization=organization_name,
                                statement='Email doesn\'t exist in the billable list')
        else:
            self.csv_writer(account=identification, organization=organization_name,
                            statement='Email not provided for the user')

        self.organisations.append(organization_name)

    def user_edit_box(self, ran_number, account_info):

        statement = ''

        try:
            WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > st-tabs > st-tabs-nav')))
        except exceptions.TimeoutException:
            try:
                WdWait(self.driver, 20).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'md-content > st-tabs > st-tabs-nav')))
            except exceptions.TimeoutException:
                statement = 'Internal exception - the user information box didn\'t load after 20 seconds - manual recheck needed'
            else:
                statement = self.accreditation_input(ran_number)

        else:
            statement = self.accreditation_input(ran_number)

        finally:
            if self.css_clicker('button[ng-click="$ctrl.confirm()"]'):
                if statement == 'No accreditations under that account':
                    pass
                self.csv_writer(account=account_info[0], organization=account_info[1],
                                statement=statement)
            else:
                self.csv_writer(account=account_info[0], organization=account_info[1],
                                statement='Internal exception - Unable to save')
            sleep(3)

    def accreditation_input(self, ran_number):
        try:
            accreditations_button = self.driver.find_element_by_css_selector('button[aria-label="Accreditations"]')
        except exceptions.NoSuchElementException:
            statement = 'No accreditations under that account'
        else:
            try:
                accreditations_button.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script(
                    """document.querySelector('button[aria-label="Accreditations"]').click();""")

            finally:

                lender_accr = self.existing_lender_accreditation(self.lender, ran_number, overwrite=False)
                gateway_accr = self.existing_gateway_accreditation(self.gateway, ran_number, overwrite=False)

                if not lender_accr:

                    try:
                        self.driver.execute_script(
                            """document.querySelector('button[aria-label="Add new lender accreditation"]').click();""")
                    except exceptions.ElementClickInterceptedException:
                        self.driver.execute_script(
                            """document.querySelector('button[aria-label="Add new lender accreditation"]').click();""")
                    except exceptions.NoSuchElementException:
                        statement = 'Missing the button to add new lender accreditation - manual checkup needed'
                        return statement

                    lender_box = self.driver.find_element_by_css_selector(
                        'st-block:first-of-type > st-block-form-content:last-of-type')
                    lender_md_select = lender_box.find_element_by_css_selector('md-input-container > md-select')

                    self.md_select_handler(lender_md_select, self.lender)

                    lender_box.find_element_by_css_selector(
                        'md-input-container > input[ng-model="lenderAccreditation.brokerIdPrimary"]').send_keys(
                        ran_number)

                    sleep(1)

                if not gateway_accr:
                    try:
                        self.driver.execute_script(
                            """document.querySelector('button[aria-label="Add new gateway accreditation"]').click();""")
                    except exceptions.ElementClickInterceptedException:
                        self.driver.execute_script(
                            """document.querySelector('button[aria-label="Add new gateway accreditation"]').click();""")
                    except exceptions.NoSuchElementException:
                        statement = 'Missing the button to add new gateway accreditation - manual checkup needed'
                        return statement

                    gateway_box = self.driver.find_element_by_css_selector(
                        'st-block:nth-of-type(2) > st-block-form-content:last-of-type')
                    selectino = Select(gateway_box.find_element_by_css_selector('st-form-field-container > select'))
                    selectino.select_by_visible_text(self.gateway)
                    gateway_box.find_element_by_css_selector(
                        'input[ng-model="gatewayAccreditation.brokerUsername"]').send_keys(
                        ran_number)

                    sleep(1)

                statement = 'Succesful input'

        return statement

    def csv_writer(self, account='', organization='', statement=''):

        csv_path = f'/home/mark/PycharmProjects/InitTest/main/csvs/report_{self.ent}.csv'
        if path.exists(csv_path):
            write_header = False
        else:
            write_header = True

        with open(csv_path, 'a') as csv_ent:
            writer = csv.DictWriter(csv_ent, fieldnames=['account', 'organization', 'statement'])
            if write_header:
                writer.writeheader()

            writer.writerow({'account': account, 'organization': organization, 'statement': statement})

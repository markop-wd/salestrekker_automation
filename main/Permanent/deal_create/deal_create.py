import json
import random
from datetime import datetime
from pathlib import Path
from time import sleep

from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as WdWait

from main.Permanent.deal_create.deal_create_names import first_names, surnames, company_names
from main.Permanent.deal_create.deal_create_selectors import DEAL_NAME, STAGE_SELECT, COMPANY_NAME, \
    COMPANY_EMAIL, MAIN_INFO_BLOCK, DEAL_VALUE, DEAL_OWNER_MD, DEAL_OWNER_LIST, PERSON_EMAIL, \
    PERSON_NAME, PERSON_SURNAME, PHONE_NUM, TICKET_CONTENT, \
    TICKET_EDIT, CONTACTS, ADD_CONTACT, CONTACT_LABEL, FIRST_CLIENT_INPUT, CLIENT_TYPE, \
    SETTLEMENT_DATE, LOAN_PURPOSE, CONSUMER_PURPOSE, COMMERCIAL_PURPOSE, SUMMARY_NOTES, HOME_BUTTON, \
    SAVE_BUTTON
from main.Permanent.helper_funcs import element_clicker, selector


# TODO - Move to an API call
class CreateDeal:
    def __init__(self, ent: str, driver: Chrome, config: dict = None, deal_name: str = ''):
        if deal_name:
            self.deal_name = deal_name
        else:
            self.deal_name = f'Test {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

        if config is None:
            deal_config = Path(__file__).parent.resolve() / "../../deal_config.json"
            with open(deal_config, 'r', encoding='utf-8') as deal_config_json:
                deal_config = json.load(deal_config_json)
        else:
            deal_config = config

        self.users_in_workflow = ''
        self.driver = driver
        self.main_url = 'https://' + ent + '.salestrekker.com'

        self.contacts = deal_config['contacts']
        self.deal_info = deal_config['deal_info']
        number_of_contacts = self.contacts['number_of_contacts']

        if number_of_contacts['random']:
            # Take a random value between the min and the max random value in deal config
            self.number_of_contacts = int(random.randrange(
                number_of_contacts['rand_val']['min'],
                number_of_contacts['rand_val']['max'])
            )
        else:
            # Otherwise just take the value from deal config
            self.number_of_contacts = int(number_of_contacts['value'])
        # Subtract 1 in both cases (as when you create a deal one contact is present by default)
        self.number_of_contacts -= 1

    def run(self, workflow: str = 'test', af_type: str = "cons", deal_owner_name: str = '',
            client_email: str = ""):
        """
        This is the main logic for the deal creation, this one calls the 'private' functions
        It makes sure we are at the correct place and time when not filling in input fields
        """

        if workflow == 'test':
            self.driver.get(self.main_url)
            in_workflow = self.driver.current_url.split('/')[-1]
        else:
            in_workflow = workflow.split('/')[-1]

        if not deal_owner_name:
            # TODO - maybe take the current user as the default deal owner
            #  rather than going by the config
            deal_owner_name = self.deal_info['deal_owner']

        self.driver.get(self.main_url + '/deal/edit/' + in_workflow + '/0')

        try:
            WdWait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'top')))
        except exceptions.TimeoutException:
            try:
                WdWait(self.driver, 30).until(ec.presence_of_element_located((By.ID, 'top')))
            except exceptions.TimeoutException:
                self.driver.refresh()
                WdWait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'top')))

        self._select_deal_owner(deal_owner_name)

        try:
            purpose_radio_group = WdWait(self.driver, 5).until(
                ec.presence_of_element_located(
                    (eval(LOAN_PURPOSE['by']),
                     LOAN_PURPOSE['value']
                     )))
        except exceptions.TimeoutException:
            pass
        else:
            if af_type == "comm":
                comm_button = purpose_radio_group.find_element(
                    by=eval(COMMERCIAL_PURPOSE['by']),
                    value=COMMERCIAL_PURPOSE['value']
                )
                element_clicker(self.driver, web_element=comm_button)
            elif af_type == "cons":
                cons_button = purpose_radio_group.find_element(
                    by=eval(CONSUMER_PURPOSE['by']),
                    value=CONSUMER_PURPOSE['value'])
                element_clicker(self.driver, web_element=cons_button)

        self._contact_add()
        self._contact_input(client_email)
        self._deal_info_input()

        # Save
        deal_url = self._save()
        return deal_url

    def _contact_add(self):

        add_contact = WdWait(self.driver, 10).until(
            ec.presence_of_element_located((
                eval(ADD_CONTACT['by']),
                ADD_CONTACT['value']
            )))

        if self.contacts['contact_types']['types'] == 'custom':

            element_clicker(self.driver, css_selector='button[aria-label="Remove Contact"]')

            order = self.contacts['contact_types']['custom']
            for custom_el in order.split(','):
                element_clicker(self.driver, web_element=add_contact)

                add_contact_container_id = add_contact.get_attribute('aria-owns')
                contact_type_container = WdWait(self.driver, 5).until(
                    ec.presence_of_element_located((By.ID, add_contact_container_id)))
                contact_type = contact_type_container.find_elements(by=By.TAG_NAME,
                                                                    value='button')
                if custom_el == 'pers':
                    element_clicker(self.driver, web_element=contact_type[0])
                elif custom_el == 'comp':
                    element_clicker(self.driver, web_element=contact_type[1])
                else:
                    # TODO raise a warning here
                    print('Bad deal_config custom values')
        else:
            incrementer = 0
            no_of_companies = self.contacts['contact_types']['no_of_companies']

            for contact in range(self.number_of_contacts):
                element_clicker(self.driver, web_element=add_contact)

                add_contact_container_id = add_contact.get_attribute('aria-owns')
                contact_type_container = WdWait(self.driver, 5).until(
                    ec.presence_of_element_located((By.ID, add_contact_container_id)))
                contact_type = contact_type_container.find_elements(by=By.TAG_NAME,
                                                                    value='button')
                if self.contacts['contact_types']['types'] == 'mixed':

                    if 0 < no_of_companies > incrementer:
                        element_clicker(self.driver, web_element=contact_type[1])

                        incrementer += 1
                    else:

                        element_clicker(self.driver, web_element=contact_type[0])

                elif self.contacts['contact_types']['types'] == 'company':
                    element_clicker(self.driver, web_element=contact_type[1])

                elif self.contacts['contact_types']['types'] == 'person':
                    element_clicker(self.driver, web_element=contact_type[0])

    def _contact_input(self, client_email):

        person_list = []
        company_list = []
        WdWait(self.driver, 6).until(
            ec.presence_of_element_located((
                eval(FIRST_CLIENT_INPUT['by']),
                FIRST_CLIENT_INPUT['value']
            )))

        contacts = self.driver.find_elements(
            by=eval(CONTACTS['by']),
            value=CONTACTS['value']
        )

        for contact in contacts:
            contact_label = contact.find_element(
                by=eval(CONTACT_LABEL['by']),
                value=CONTACT_LABEL['value']
            )
            if contact_label.text == 'First name':
                person_list.append(contact)
            elif contact_label.text == 'Entity name':
                company_list.append(contact)

        if person_list:
            for count, person in enumerate(person_list):
                # person_name = person_names[random.randrange(0, len(person_names))]
                first_name = random.choice(first_names)
                surname = random.choice(surnames)

                if not client_email:
                    client_email_input = f'{first_name.lower()}@{surname.lower()}.com'
                else:
                    _mejl_split = client_email.split('@')
                    _person_name_merge = first_name.lower() + surname.lower()
                    client_email_input = f'{_mejl_split[0]}+{_person_name_merge}@{_mejl_split[1]}'

                person.find_element(by=eval(PERSON_NAME['by']),
                                    value=PERSON_NAME['value']).send_keys(first_name)
                sleep(0.1)
                person.find_element(by=eval(PERSON_SURNAME['by']),
                                    value=PERSON_SURNAME['value']).send_keys(surname)

                person.find_element(by=eval(PHONE_NUM['by']),
                                    value=PHONE_NUM['value']).send_keys('0412341234')
                person.find_element(by=eval(PERSON_EMAIL['by']),
                                    value=PERSON_EMAIL['value']).send_keys(client_email_input)

                client_type = person.find_element(by=eval(CLIENT_TYPE['by']),
                                                  value=CLIENT_TYPE['value'])

                if self.contacts['non_client']['active']:
                    if count < int(self.contacts['non_client']['no_of_clients']):
                        selector(self.driver, client_type, rand_range="0-4")
                    else:
                        client_type_len = int(len(Select(client_type).options))
                        selector(self.driver, client_type, rand_range=f'4-{client_type_len}')
                else:
                    if count == 0:
                        selector(self.driver, client_type, index=0)
                    else:
                        selector(self.driver, client_type, rand_range="1-4")

        if company_list:
            for count, company in enumerate(company_list):
                company_name = random.choice(company_names)
                company_name_short = company_name.split(' ')[0].lower()
                if not client_email:
                    client_email_input = f'{company_name_short}@entity.com'
                else:
                    _mejl_split = client_email.split('@')
                    client_email_input = f'{_mejl_split[0]}+{company_name_short}@{_mejl_split[1]}'
                company.find_element(by=eval(COMPANY_NAME['by']),
                                     value=COMPANY_NAME['value']).send_keys(company_name)

                company.find_element(
                    by=eval(PHONE_NUM['by']),
                    value=PHONE_NUM['value']).send_keys('0412341234')

                company.find_element(by=eval(COMPANY_EMAIL['by']),
                                     value=COMPANY_EMAIL['value']).send_keys(client_email_input)

                client_type = company.find_element(
                    by=eval(CLIENT_TYPE['by']),
                    value=CLIENT_TYPE['value']
                )

                if self.contacts['non_client']['active']:
                    if count < int(self.contacts['non_client']['no_of_clients']):
                        selector(self.driver, client_type, rand_range='0-4')
                    else:
                        client_type_len = int(len(Select(client_type).options))

                        selector(self.driver, client_type, rand_range=f'0-{client_type_len}')

                else:
                    if count == 0:
                        selector(self.driver, client_type, index=0)
                    else:
                        selector(self.driver, client_type, rand_range='1-4')

    def _deal_info_input(self):

        main_info_block = self.driver.find_element(by=eval(MAIN_INFO_BLOCK['by']),
                                                   value=MAIN_INFO_BLOCK['value'])

        # Deal Name
        deal_name_input = main_info_block.find_element(by=eval(DEAL_NAME['by']),
                                                       value=DEAL_NAME['value'])

        deal_name_input.send_keys(Keys.CONTROL + 'a')
        deal_name_input.send_keys(self.deal_name)

        # self.select_deal_owner(main_info_block, 'Salestrekker Help Desk')

        stage_select_element = main_info_block.find_element(by=eval(STAGE_SELECT['by']),
                                                            value=STAGE_SELECT['value'])

        element_clicker(self.driver, web_element=stage_select_element)

        stage_select_id = str(stage_select_element.get_attribute('aria-owns'))
        stages = self.driver.find_elements(by=By.CSS_SELECTOR,
                                           value=f'#{stage_select_id} md-option')

        sleep(0.1)
        if self.deal_info['random']:
            stage_num = random.randrange(0, len(stages))
        else:
            stage_num = int(self.deal_info['stage_num']) - 1

        element_clicker(driver=self.driver, web_element=stages[stage_num])

        # Deal Value
        deal_value = 500000
        sleep(0.2)

        deal_value_input = main_info_block.find_element(by=eval(DEAL_VALUE['by']),
                                                        value=DEAL_VALUE['value'])
        deal_value_input.send_keys(Keys.CONTROL + 'a')
        deal_value_input.send_keys(deal_value)

        try:
            WdWait(self.driver, 5).until(ec.text_to_be_present_in_element_value(
                (eval(DEAL_VALUE['by']), DEAL_VALUE['value']),
                '$' + f'{deal_value:,}'))
        except exceptions.TimeoutException:
            deal_value_input.send_keys(Keys.CONTROL + 'a')
            deal_value_input.send_keys(deal_value)

        # Estimated settlement date
        # Add two months on top of the current one for the settlement date (and don't go over 12)
        today = datetime.now()
        # TODO - replace this, this was created as modulo loops over to 0 so I add 1 on top of the result
        new_month = ((today.month + 1) % 12)+1
        settlement_date = today.replace(month=new_month).strftime("%d/%m/%Y")

        settlement_date_input = main_info_block.find_element(by=eval(SETTLEMENT_DATE['by']),
                                                             value=SETTLEMENT_DATE['value'])
        settlement_date_input.send_keys(Keys.CONTROL + 'a')
        settlement_date_input.send_keys(settlement_date)

        try:
            WdWait(self.driver, 5).until(ec.text_to_be_present_in_element_value(
                (eval(SETTLEMENT_DATE['by']), SETTLEMENT_DATE['value']),
                settlement_date))
        except exceptions.TimeoutException:
            settlement_date_input.send_keys(Keys.CONTROL + 'a')
            settlement_date_input.send_keys(settlement_date)

        # Summary notes
        summary_notes = 'Summary Notes-u'
        main_info_block.find_element(by=eval(SUMMARY_NOTES['by']),
                                     value=SUMMARY_NOTES['value']).send_keys(summary_notes)

    def _select_deal_owner(self, deal_owner_name: str):

        main_info_block = WdWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (eval(MAIN_INFO_BLOCK['by']),
                 MAIN_INFO_BLOCK['value']
                 )))

        # Deal Owner
        deal_owner_select_element = main_info_block.find_element(
            by=eval(DEAL_OWNER_MD['by']),
            value=DEAL_OWNER_MD['value'])

        element_clicker(driver=self.driver, web_element=deal_owner_select_element)

        deal_owner_id = str(deal_owner_select_element.get_attribute('aria-owns'))
        try:
            deal_owner_list = WdWait(self.driver, 5).until(
                ec.visibility_of_element_located(
                    (By.ID, deal_owner_id)))
        except exceptions.TimeoutException:
            element_clicker(driver=self.driver, web_element=deal_owner_select_element)
            deal_owner_list = WdWait(self.driver, 5).until(
                ec.visibility_of_element_located(
                    (By.ID, deal_owner_id)))

        _deal_owners = []
        sleep(0.1)
        deal_owners = deal_owner_list.find_elements(by=eval(DEAL_OWNER_LIST['by']),
                                                    value=DEAL_OWNER_LIST['value'])
        for owner in deal_owners:
            if owner.text == deal_owner_name:
                element_clicker(self.driver, web_element=owner)
                break
            _deal_owners.append({'name': owner.text, 'el': owner})
        else:
            print('No owner with that name')
            raise ValueError
            # TODO - sensible, concurrent agnostic owner picker
            # for count, owner in enumerate(_deal_owners, start=1):
            #     print(count, owner['name'])
            # # owner_index = int(input('Select a owner index: ')) - 1
            # element_clicker(self.driver, web_element=_deal_owners[owner_index]['el'])

    def _save(self):
        sleep(5)
        element_clicker(self.driver, css_selector=SAVE_BUTTON['value'])

        # Wait 10 seconds for the ticket-content tag to appear (only visible in the deal front page)
        try:
            WdWait(self.driver, 10).until(
                ec.presence_of_element_located((
                    eval(TICKET_CONTENT['by']),
                    TICKET_CONTENT['value']
                )))
        except exceptions.TimeoutException:
            # If ticket-content was not loaded check if we are still within the deal creation page
            try:
                WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((
                        eval(TICKET_EDIT['by']),
                        TICKET_EDIT['value']
                    )))
            # If it timed out - just check if the deal front page loading took longer
            except exceptions.TimeoutException:
                WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((
                        eval(TICKET_CONTENT['by']),
                        TICKET_CONTENT['value']
                    )))
            else:
                # If we are still in deal creation page, there is an overlay that needs to be
                # clicked in order to save
                home_button = self.driver.find_element(by=eval(HOME_BUTTON['by']),
                                                       value=HOME_BUTTON['value'])
                element_clicker(self.driver, web_element=home_button)

                # After clicking the overlay, wait for the ticket-content to load
                WdWait(self.driver, 20).until(
                    ec.presence_of_element_located((
                        eval(TICKET_CONTENT['by']),
                        TICKET_CONTENT['value']
                    )))

        deal_url = self.driver.current_url

        return deal_url

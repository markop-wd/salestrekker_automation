from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import json
import random
from selenium.common import exceptions


class MultipleDealCreator:

    def __init__(self, ent, driver):
        self.current_export_array = []
        with open("deal_config") as deal_config_json:
            self.deal_config = json.load(deal_config_json)
        # self.edit_input_array = []
        # self.md_select_array = []
        # self.first = []
        # self.last = []
        # self.md_options = []
        # self.contact_type = []
        # self.client_type = ''
        # self.placeholder = ''
        # self.email = ''
        # self.password = ''
        # self.one_to_four = None
        # self.main_export_array = []
        self.users_in_workflow = ''
        self.number_of_contacts = None
        self.driver = driver
        self.main_url = 'https://' + ent + '.salestrekker.com'

    def create_deal(self):
        self.driver.get(self.main_url)
        TEST_entry_workflow_id = self.driver.current_url.split('/')[-1]

        if users_in_workflow := self.who_is_in_the_workflow(TEST_entry_workflow_id):
            self.users_in_workflow = users_in_workflow
        else:
            print('test')

        self.driver.get(self.main_url + '/deal/edit/' + TEST_entry_workflow_id + '/0')

        WdWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'top')))

        assert "Add New Ticket" in self.driver.title

        self.contact_add()
        self.contact_input()
        self.deal_info_input()
        input('All good?')
        # self.edit_input_array = self.driver.find_elements_by_tag_name("input")
        # self.md_select_array = self.driver.find_elements_by_tag_name("md-select")
        # self.client_type = self.driver.find_elements_by_tag_name('select')

    def who_is_in_the_workflow(self, workflow_id):
        self.driver.get(self.main_url + '/settings/workflow/' + workflow_id)
        WdWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-block.mb0')))
        try:
            return_list = [user.text for user in self.driver.find_elements_by_css_selector('md-chip div.md-contact-name')]
        except exceptions.NoSuchElementException:
            return_list = []

        return return_list

    def contact_add(self):

        number_of_contacts = self.deal_config['number_of_contacts']

        if number_of_contacts['random']:
            self.number_of_contacts = random.randrange(number_of_contacts['rand_val']['min'],
                                                       number_of_contacts['rand_val']['max'])
        else:
            self.number_of_contacts = number_of_contacts['value']

        for contact in range(self.number_of_contacts):
            add_contact = WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                                                                        '#top > form-content > form > '
                                                                                        'div > st-block > '
                                                                                        'st-block-form-header > '
                                                                                        'md-menu > button')))
            try:
                add_contact.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script('arguments[0].click();', add_contact)

            add_contact_container_id = add_contact.get_attribute('aria-owns')
            contact_type_container = WdWait(self.driver, 5).until(
                ec.presence_of_element_located((By.ID, add_contact_container_id)))

            if self.deal_config['contact_types'] == 'mixed':
                contact_type = contact_type_container.find_elements_by_tag_name('button')
                rand_val = random.randrange(0, 2)
                try:
                    contact_type[rand_val].click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', contact_type[rand_val])
                type_of_cont = contact_type[rand_val].get_attribute('ng-click')

                if type_of_cont == 'contactAdd(false)':
                    self.current_export_array.append('Person ')

                if type_of_cont == 'contactAdd(true)':
                    self.current_export_array.append('Company ')

            elif self.deal_config['contact_types'] == 'company':
                contact_type = contact_type_container.find_elements_by_tag_name('button')
                for contact_button in contact_type:
                    if contact_button.find_element_by_tag_name('span').text == 'Company':
                        try:
                            contact_button.click()
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script('arguments[0].click();', contact_button)
                        self.current_export_array.append('Company ')
                        break
                else:
                    raise Exception
                    pass

            elif self.deal_config['contact_types'] == 'person':
                contact_type = contact_type_container.find_elements_by_tag_name('button')
                for contact_button in contact_type:
                    if contact_button.find_element_by_tag_name('span').text == 'Person':
                        try:
                            contact_button.click()
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script('arguments[0].click();', contact_button)
                            self.current_export_array.append('Person ')
                        break
                else:
                    raise Exception
                    pass

        self.current_export_array.append("No. of clients: " + str(number_of_contacts) + ", ")

    # TODO - Figure out what to pass in here, some generators maybe for names or should I pre-generate those names
    #  once I generate the class?
    def contact_input(self):

        person_list = []
        company_list = []

        WdWait(self.driver, 6).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.mt0 > div > div:nth-child(1) input')))
        for contact in self.driver.find_elements_by_css_selector('div.mt0'):
            if contact.find_element_by_css_selector('md-autocomplete-wrap > md-input-container > label').text == 'First name':
                person_list.append(contact)
            elif contact.find_element_by_css_selector('md-autocomplete-wrap > md-input-container > label').text == 'Entity name':
                company_list.append(contact)

        if person_list:
            for person in person_list:
                person.find_element_by_css_selector('div:nth-child(2) > div:nth-child(1) > md-autocomplete > md-autocomplete-wrap > md-input-container >input').send_keys('First')
                person.find_element_by_css_selector('div:nth-child(2) > div:nth-child(2) > md-input-container > input').send_keys('Surname')
                num_prefix = person.find_element_by_css_selector('div:nth-child(2) > div:nth-child(3) > md-input-container:nth-child(1) > input')
                num_prefix.send_keys(Keys.CONTROL + 'a')
                num_prefix.send_keys('11')
                person.find_element_by_css_selector('div:nth-child(2) > div:nth-child(3) > md-input-container:nth-child(2) > input').send_keys('123456789')
                person.find_element_by_css_selector('div:nth-child(2) > div:nth-child(4) > md-input-container > input').send_keys('email@person.real')
                current_sel = person.find_element_by_css_selector('div:nth-child(2) > div:nth-child(4) > st-form-field-container > select')
                Select(current_sel).select_by_index(random.randrange(0, 4))

        if company_list:
            for company in company_list:
                company.find_element_by_css_selector('div:nth-child(2) > div:nth-child(1) > md-autocomplete > md-autocomplete-wrap > md-input-container >input').send_keys('Company Name')
                num_prefix = company.find_element_by_css_selector('div:nth-child(2) > div:nth-child(2) > md-input-container:nth-child(1) > input')
                num_prefix.send_keys(Keys.CONTROL + 'a')
                num_prefix.send_keys('22')
                company.find_element_by_css_selector('div:nth-child(2) > div:nth-child(2) > md-input-container:nth-child(2) > input').send_keys('987654321')
                company.find_element_by_css_selector('div:nth-child(2) > div:nth-child(3) input').send_keys('email@company.real')
                current_sel = company.find_element_by_css_selector('div > div:nth-child(3) > st-form-field-container > select')
                Select(current_sel).select_by_index(random.randrange(0, 4))

    def deal_info_input(self):
        main_info_block = self.driver.find_element_by_css_selector('st-block > st-block-form-content > div.layout-wrap')
        main_info_block.find_element_by_css_selector('div:nth-child(1) > md-input-container > input').send_keys(Keys.CONTROL + 'a')
        main_info_block.find_element_by_css_selector('div:nth-child(1) > md-input-container > input').send_keys('Deal Name')

        deal_owner_select_element = main_info_block.find_element_by_css_selector('div:nth-child(2) > md-input-container > md-select')
        try:
            deal_owner_select_element.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', deal_owner_select_element)

        deal_owner_select_id = str(deal_owner_select_element.get_attribute('id'))
        deal_owner_id = str(int(deal_owner_select_id.split("_")[-1]) + 1)

        WdWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div#select_container_" + deal_owner_id)))

        deal_owners = self.driver.find_elements_by_css_selector(
            "div#select_container_" + deal_owner_id + " > md-select-menu > md-content > md-option > div > span")
        for deal_owner in deal_owners:
            sleep(0.1)
            if deal_owner.text == 'Zac Test':
                try:
                    deal_owner.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', deal_owner)
                break
        else:
            deal_owners[0].click()

        sleep(2)

        team_members_field = main_info_block.find_element_by_css_selector('div > md-chips input')
        for user in self.users_in_workflow:
            team_members_field.send_keys(user)
            try:
                WdWait(self.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'md-autocomplete-parent-scope > div')))
            except exceptions.TimeoutException:
                print('this shouldn\'t happen as we\'ve already ensured that users are in that workflow, but here we '
                      'are ')

            offered_users = self.driver.find_elements_by_css_selector('md-autocomplete-parent-scope > div')
            for offered_user in offered_users:
                offered_user.click()

        stage_select_element = main_info_block.find_element_by_css_selector(
            'div:nth-child(4) > md-input-container > md-select')
        try:
            stage_select_element.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', stage_select_element)
        stage_select_id = str(stage_select_element.get_attribute('id'))
        stage_container_id = str(int(stage_select_id.split("_")[-1]) + 1)

        stages = self.driver.find_elements_by_css_selector(
            "div#select_container_" + stage_container_id + " > md-select-menu > md-content > md-option")

        random_stage = random.randrange(0, len(stages))
        try:
            stages[random_stage].click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', stages[random_stage])

        # Deal Value
        sleep(1)
        deal_value_input = main_info_block.find_element_by_css_selector('div:nth-child(5) > md-input-container > input')
        deal_value_input.send_keys(Keys.CONTROL + 'a')
        deal_value_input.send_keys('500000')
        try:
            WdWait(self.driver, 5).until(ec.text_to_be_present_in_element_value((By.CSS_SELECTOR, 'div:nth-child(5) > md-input-container > input'), '500000'))
        except exceptions.TimeoutException:
            deal_value_input.send_keys(Keys.CONTROL + 'a')
            deal_value_input.send_keys('500000')

        # Estimated settlement date
        estimated_settlement_date_input = main_info_block.find_element_by_css_selector('div:nth-child(6) > md-input-container > md-datepicker > div > input')
        estimated_settlement_date_input.send_keys(Keys.CONTROL + 'a')
        estimated_settlement_date_input.send_keys('01/01/1998')
        try:
            WdWait(self.driver, 5).until(ec.text_to_be_present_in_element_value((By.CSS_SELECTOR, 'div:nth-child(6) > md-input-container > md-datepicker > div > input'), '01/01/1998'))
        except exceptions.TimeoutException:
            estimated_settlement_date_input.send_keys(Keys.CONTROL + 'a')
            estimated_settlement_date_input.send_keys('01/01/1998')


        # Summary notes
        main_info_block.find_element_by_css_selector('div:nth-child(7) > md-input-container textarea').send_keys('Summary summary')

    # def CreateDeal(self, name, surname):
    #
    #     # re-write the as there is no need for a loop, you can just find particular elements rather than looping
    #     # through each one
    #     name_counter = 0
    #     surname_counter = 0
    #     email_counter = 0
    #     deal_name_counter = 0
    #     for element in self.edit_input_array:
    #         try:
    #             if element.get_attribute('placeholder') == self.placeholder:
    #                 search_el_id = element.get_attribute('id')
    #             elif element.get_attribute('placeholder') == 'Add team member(s)':
    #                 add_team_member_id = element.get_attribute('id')
    #             elif element.get_attribute('ng-model') == '$mdAutocompleteCtrl.scope.searchText':
    #                 element.clear()
    #                 element.send_keys(name[name_counter])
    #                 self.current_export_array.append("FName: " + name[name_counter] + ", ")
    #                 name_counter += 1
    #             elif element.get_attribute('ng-model') == '$ctrl.contact.familyName':
    #                 element.clear()
    #                 element.send_keys(surname[surname_counter])
    #                 self.current_export_array.append("LName: " + surname[surname_counter] + ", ")
    #                 surname_counter += 1
    #             elif element.get_attribute('ng-model') == '$ctrl.contact.phoneCode':
    #                 element.clear()
    #                 cur_phone_prefix = str(random.randrange(10, 1000))
    #                 element.send_keys(cur_phone_prefix)
    #                 self.current_export_array.append("Phone prefix: +" + cur_phone_prefix + ", ")
    #             elif element.get_attribute('name') == 'phone':
    #                 element.clear()
    #                 cur_phone_num = str(random.randrange(100000, 1000000))
    #                 element.send_keys(cur_phone_num)
    #                 self.current_export_array.append("Phone: " + cur_phone_num + ", ")
    #             elif element.get_attribute('ng-model') == '$ctrl.contact.email':
    #                 element.clear()
    #                 element.send_keys(
    #                     name[email_counter].lower() + "_" + surname[email_counter].lower() + "@empty.com.jp")
    #                 self.current_export_array.append("Email: " + name[email_counter].lower() + "_" + surname[
    #                     email_counter].lower() + "@empty.com.jp, ")
    #                 email_counter += 1
    #             elif element.get_attribute('ng-model') == 'Model.currentTicket.values.onceOff':
    #                 element.clear()
    #                 cur_ticket_value = str(random.randrange(10000, 3000000))
    #                 element.send_keys(cur_ticket_value)
    #                 self.current_export_array.append("Value: " + cur_ticket_value + ", ")
    #             elif element.get_attribute('placeholder') == 'DD/MM/YYYY':
    #                 element.clear()
    #                 cur_date = str(random.randrange(1, 31)) + "/" + str(random.randrange(1, 13)) + "/" + str(
    #                     random.randrange(2020, 2040))
    #                 element.send_keys(cur_date)
    #                 self.current_export_array.append("Settl. Date: " + cur_date + ", ")
    #             elif element.get_attribute('ng-model') == 'Model.currentTicket.name':
    #                 element.clear()
    #                 temp_arr = []
    #                 if self.one_to_four == 0:
    #                     element.send_keys(name[deal_name_counter] + " " + str(time.asctime()))
    #                     self.current_export_array.append(
    #                         "Deal name: " + name[deal_name_counter] + " " + str(time.asctime()) + ", ")
    #                     continue
    #                 while self.number_of_contacts + 1 != deal_name_counter:
    #                     element.send_keys(name[deal_name_counter] + " ")
    #                     temp_arr.append(name[deal_name_counter] + " ")
    #                     deal_name_counter += 1
    #                 element.send_keys(str(time.asctime()))
    #                 self.current_export_array.append(
    #                     "Deal name: " + ' '.join([str(elem) for elem in temp_arr]) + str(time.asctime()) + ", ")
    #
    #         except exceptions.ElementNotInteractableException:
    #             print(element.text)
    #             continue
    #
    #     for element in self.md_select_array:
    #         element.click()
    #         time.sleep(0.5)
    #         element_id = element.get_attribute('aria-owns')
    #         try:
    #             current_selector = WdWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, element_id)))
    #         except exceptions.TimeoutException:
    #             element.click()
    #             time.sleep(1)
    #             current_selector = WdWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, element_id)))
    #         self.md_options = current_selector.find_elements_by_tag_name('md-option')
    #         optional = self.md_options[random.randrange(0, len(self.md_options))]
    #         optional.click()
    #         if element.get_attribute('ng-model') == 'Model.currentTicket.idStage':
    #             self.current_export_array.append("Stage: " + element.find_element(By.TAG_NAME, 'span').text + ", ")
    #         elif element.get_attribute('ng-model') == 'Model.currentTicket.idOwner':
    #             self.current_export_array.append(
    #                 "Owner: " + element.find_element(By.CSS_SELECTOR, 'span > div > span').text + ", ")
    #
    #     for i, element in enumerate(self.client_type):
    #         if i == 0:
    #             Select(element).select_by_index(random.randrange(0, 4))
    #             self.current_export_array.append(
    #                 "First client type: " + Select(element).first_selected_option.text + ", ")
    #         else:
    #             Select(element).select_by_index(random.randrange(0, len(Select(element).options) - 1))
    #             self.current_export_array.append(
    #                 "Other client type(s): " + Select(element).first_selected_option.text + ", ")
    #
    #     WdWait(self.driver, 10).until(ec.element_to_be_clickable(
    #         (By.CSS_SELECTOR, '#top > form-content > div > button.save.md-button.md-ink-ripple.flex'))).click()
    #     try:
    #         WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
    #     except exceptions.TimeoutException:
    #         try:
    #             WdWait(self.driver, 10).until(ec.element_to_be_clickable(
    #                 (By.CSS_SELECTOR, '#top > form-content > div > button.save.md-button.md-ink-ripple.flex'))).click()
    #         except exceptions.TimeoutException:
    #             self.driver.refresh()
    #         WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
    #     self.main_export_array.append(self.current_export_array)

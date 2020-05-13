from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import json
import random
from selenium.common import exceptions
from main.Permanent import workflow_manipulation


class MultipleDealCreator:

    def __init__(self, ent, driver):
        # self.current_export_array = []
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
        self.wf_manipulate = workflow_manipulation.WorkflowManipulation(self.driver, ent)

    def create_deal(self, workflow='test'):

        if workflow == 'test':
            self.driver.get(self.main_url)
            in_workflow = self.driver.current_url.split('/')[-1]
        else:
            in_workflow = workflow

        if users_in_workflow := self.wf_manipulate.workflow_users(in_workflow):
            self.users_in_workflow = users_in_workflow
        else:
            self.wf_manipulate.add_users_to_workflow(worklfow_id=in_workflow)

        self.driver.get(self.main_url + '/deal/edit/' + in_workflow + '/0')

        WdWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'top')))

        assert "Add New Ticket" in self.driver.title

        self.contact_add()
        self.contact_input()
        self.deal_info_input()

        # Save
        save_button = WdWait(self.driver, 6).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.save')))
        try:
            save_button.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", save_button)

        try:
            WdWait(self.driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
        except exceptions.TimeoutException:
            try:
                WdWait(self.driver, 5).until(ec.presence_of_element_located((By.ID, 'navBar')))
            except exceptions.TimeoutException:
                raise exceptions.TimeoutException
            else:
                WdWait(self.driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
                deal_id = self.driver.current_url.split('/')[-1]

        self.client_profile_input()
        # WdWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-sidebar-block > div > button > span')))

    def contact_add(self):

        contacts = self.deal_config['contacts']
        number_of_contacts = contacts['number_of_contacts']

        if number_of_contacts['random']:
            self.number_of_contacts = random.randrange(number_of_contacts['rand_val']['min'],
                                                       number_of_contacts['rand_val']['max'])
        else:
            # Decreasing one as a contact already exists within a deal
            self.number_of_contacts = int(number_of_contacts['value']) - 1

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

            if contacts['contact_types'] == 'mixed':
                contact_type = contact_type_container.find_elements_by_tag_name('button')
                rand_val = random.randrange(0, 2)
                try:
                    contact_type[rand_val].click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', contact_type[rand_val])
                type_of_cont = contact_type[rand_val].get_attribute('ng-click')
                #
                # if type_of_cont == 'contactAdd(false)':
                #     self.current_export_array.append('Person ')
                #
                # if type_of_cont == 'contactAdd(true)':
                #     self.current_export_array.append('Company ')

            elif contacts['contact_types'] == 'company':
                contact_type = contact_type_container.find_elements_by_tag_name('button')
                for contact_button in contact_type:
                    if contact_button.find_element_by_tag_name('span').text == 'Company':
                        try:
                            contact_button.click()
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script('arguments[0].click();', contact_button)
                            # self.current_export_array.append('Company ')
                        break
                else:
                    raise Exception
                    pass

            elif contacts['contact_types'] == 'person':
                contact_type = contact_type_container.find_elements_by_tag_name('button')
                for contact_button in contact_type:
                    if contact_button.find_element_by_tag_name('span').text == 'Person':
                        try:
                            contact_button.click()
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script('arguments[0].click();', contact_button)
                            # self.current_export_array.append('Person ')
                        break
                else:
                    raise Exception
                    pass

        # self.current_export_array.append("No. of clients: " + str(number_of_contacts) + ", ")

    # TODO - Figure out what to pass in here, some generators maybe for names or should I pre-generate those names
    #  once I generate the class?
    def contact_input(self):

        names = [['Misty', 'Banks'], ['Karl', 'Berg'], ['Tanisha', 'Obrien'], ['Jasmin', 'Talley'],
                 ['Lexi-Mai', 'Mccray'], ['Chandni', 'Kramer'], ['Musab', 'Cunningham'], ['Spike', 'Dunn'],
                 ['Doris', 'Vu'], ['Dominick', 'Ferry'], ['Rudi', 'Wolfe'], ['Saira', 'Haas'], ['Keeleigh', 'Bate'],
                 ['Nana', 'Tomlinson'], ['Andrew', 'Phelps'], ['Kirandeep', 'Goulding'], ['Roland', 'Penn'],
                 ['Harry', 'Slater'], ['Alexie', 'Aguilar'], ['Adelaide', 'Mellor'], ['Finbar', 'Bray'],
                 ['Nasir', 'Potter'], ['Patrycja', 'Metcalfe'], ['Nela', 'Burch'], ['Belinda', 'Houston'],
                 ['Amaya', 'Brandt'], ['Husnain', 'Nixon'], ['Tiana', 'Allison'], ['Wyatt', 'Stephens'],
                 ['Kenneth', 'Webster'], ['April', 'Lawrence'], ['Leia', 'Wright'], ['Bushra', 'Knowles'],
                 ['Levi', 'Davidson'], ['Keira', 'Dalton'], ['Amin', 'Flower'], ['Samiha', 'Cameron'],
                 ['Marianne', 'Baker'], ['Habib', 'Portillo'], ['Yousuf', 'Lord'], ['Nicola', 'Goodman'],
                 ['Samanta', 'Roman'], ['Benedict', 'Wardle'], ['Nikhil', 'Hayden'], ['Aurora', 'Bains'],
                 ['Giulia', 'Romero'], ['Rosa', 'Iles'], ['Alannah', 'Navarro'], ['Marian', 'Malone'],
                 ['Dionne', 'Molina'], ['Xanthe', 'Macfarlane'], ['Anabel', 'Hilton'], ['Samira', 'Mckay'],
                 ['Mason', 'Novak'], ['Colleen', 'Gaines'], ['Esther', 'Ratliff'], ['Faheem', 'Valdez'],
                 ['Rachael', 'Zavala'], ['Kuba', 'Gibbons'], ['Callam', 'Almond'], ['Nick', 'Bruce'], ['Ayub', 'Felix'],
                 ['Esmay', 'Reeve'], ['Aimee', 'Chang'], ['Sarah', 'Patrick'], ['Billy', 'Hutchings'],
                 ['Enid', 'Ayala'], ['Katie-Louise', 'Russell'], ['Ashlee', 'Burn'], ['Tamar', 'Parra'],
                 ['Darla', 'Sharma'], ['Whitney', 'Emery'], ['Helena', 'Burris'], ['Rachelle', 'Southern'],
                 ['Maisie', 'Mcleod'], ['Julia', 'Mckee'], ['Mandy', 'Duggan'], ['Isaiah', 'William'],
                 ['Sally', 'Dalby'], ['Marianna', 'Carr'], ['Jasleen', 'Carty'], ['Evie-Mae', 'Read'],
                 ['Lana', 'Marsh'], ['Kiana', 'Chase'], ['Preston', 'Greene'], ['Rae', 'Stafford'],
                 ['Poppy-Rose', 'Greig'], ['Lyla', 'Woolley'], ['Christy', 'Bird'], ['Maheen', 'Wyatt'],
                 ['Cordelia', 'Escobar'], ['Mariya', 'Bradley'], ['Amelia-Grace', 'Kirby'], ['Kier', 'Whitney'],
                 ['Sonny', 'Cartwright'], ['Alessia', 'Sargent'], ['Inigo', 'Plummer'], ['Hareem', 'Lucero'],
                 ['Caitlyn', 'Reynolds'], ['Ayana', 'Melia'], ['Danielle', 'Davenport'], ['Charlotte', 'Irving'],
                 ['Bronwyn', 'Barrow'], ['Eliot', 'Senior'], ['Lesley', 'Mcgowan'], ['Ada', 'Hancock'],
                 ['Azra', 'Povey'], ['Wilbur', 'Mcmanus'], ['Lillian', 'Tyson'], ['Yannis', 'Hunt'],
                 ['Sherri', 'Betts'], ['Cosmo', 'Lopez'], ['Nella', 'Molloy'], ['Hasan', 'Plant'], ['Tyrique', 'Kirk'],
                 ['Jonah', 'Cantu'], ['Lexi-Mae', 'Reid'], ['Nigel', 'Whelan'], ['Zavier', 'Dupont'],
                 ['Bevan', 'Berry'], ['Leo', 'Mueller'], ['Israel', 'Lowery'], ['Sharna', 'Powell'],
                 ['Jagoda', 'Porter'], ['Deborah', 'Krueger'], ['Claire', 'Griffiths'], ['Anabelle', 'Garrett'],
                 ['Kobie', 'Barrett'], ['Nabeel', 'Gibbs'], ['Kayley', 'Calvert'], ['Zahrah', 'Hills'],
                 ['Beck', 'Rice'], ['Kingsley', 'Correa'], ['Micah', 'Pineda'], ['Jerry', 'Beasley'],
                 ['Haydn', 'Sanderson'], ['Robyn', 'Frye'], ['Carwyn', 'Garrison'], ['Rhys', 'Trevino'],
                 ['Seamus', 'Stafford'], ['Maia', 'Rankin'], ['Iman', 'Huerta'], ['Rahul', 'Luna'], ['Judy', 'Mustafa'],
                 ['Arwa', 'Lane'], ['Jeevan', 'Russo'], ['Francesco', 'Richmond'], ['Shyam', 'Ferry'],
                 ['Amal', 'Wolfe'], ['Gabrielle', 'Schmidt'], ['Kellie', 'Mcnally'], ['Derry', 'Power'],
                 ['Quentin', 'Castaneda'], ['Hashir', 'Wickens'], ['Alma', 'Romero'], ['Rheanna', 'Smyth'],
                 ['Sebastian', 'Coulson'], ['Sahara', 'Riley'], ['Miriam', 'Carty'], ['Debbie', 'Hogan'],
                 ['Niyah', 'Bonilla'], ['Lillie-May', 'Mcgee'], ['Petra', 'Buck'], ['Khalil', 'Mccoy'],
                 ['Lena', 'Schneider'], ['Isabell', 'Gordon'], ['Howard', 'Hardy'], ['Lennie', 'Ferreira'],
                 ['Jibril', 'Jarvis'], ['Christiana', 'Haley'], ['Alan', 'Bray'], ['Kimora', 'Barnett'],
                 ['Muneeb', 'Finch'], ['Iqrah', 'Cox'], ['Hanna', 'Lawrence'], ['Akbar', 'Leech'], ['Beverly', 'Bain'],
                 ['Jill', 'Cross'], ['Shania', 'Hyde'], ['T-Jay', 'Soto'], ['George', 'Bates'], ['Lexie', 'Knowles'],
                 ['Gerard', 'Douglas'], ['Weronika', 'Roberts'], ['Alison', 'Cornish'], ['Reon', 'Robles'],
                 ['Piotr', 'Macgregor'], ['Alya', 'Hines'], ['Mitchel', 'Oakley'], ['Sally', 'Santos'],
                 ['Alfie-Lee', 'Kirkpatrick'], ['Abbie', 'Alvarez'], ['Pola', 'Piper'], ['Laylah', 'Murphy'],
                 ['Zubair', 'Boyd'], ['Ali', 'Haas'], ['Nicole', 'Corbett'], ['Lorna', 'Short'], ['Ember', 'Alexander'],
                 ['Cora', 'Sloan']]

        person_list = []
        company_list = []
        try:
            WdWait(self.driver, 6).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'div.mt0 > div > div:nth-child(1) input')))
        except exceptions.TimeoutException:
            pass
        for contact in self.driver.find_elements_by_css_selector('div.mt0'):
            if contact.find_element_by_css_selector(
                    'md-autocomplete-wrap > md-input-container > label').text == 'First name':
                person_list.append(contact)
            elif contact.find_element_by_css_selector(
                    'md-autocomplete-wrap > md-input-container > label').text == 'Entity name':
                company_list.append(contact)

        if person_list:
            for person in person_list:
                person_name = names[random.randrange(0, len(names))]

                person.find_element_by_css_selector(
                    'div:nth-child(2) > div:nth-child(1) > md-autocomplete > md-autocomplete-wrap > md-input-container >input').send_keys(
                    person_name[0])
                person.find_element_by_css_selector(
                    'div:nth-child(2) > div:nth-child(2) > md-input-container > input').send_keys(person_name[1])
                num_prefix = person.find_element_by_css_selector(
                    'div:nth-child(2) > div:nth-child(3) > md-input-container:nth-child(1) > input')
                num_prefix.send_keys(Keys.CONTROL + 'a')
                num_prefix.send_keys('11')
                person.find_element_by_css_selector(
                    'div:nth-child(2) > div:nth-child(3) > md-input-container:nth-child(2) > input').send_keys(
                    '123456789')
                person.find_element_by_css_selector(
                    'div:nth-child(2) > div:nth-child(4) > md-input-container > input').send_keys('email@person.real')
                current_sel = person.find_element_by_css_selector(
                    'div:nth-child(2) > div:nth-child(4) > st-form-field-container > select')
                Select(current_sel).select_by_index(random.randrange(0, 4))

        if company_list:
            for company in company_list:
                company.find_element_by_css_selector(
                    'div:nth-child(2) > div:nth-child(1) > md-autocomplete > md-autocomplete-wrap > md-input-container >input').send_keys(
                    'Company Name')
                num_prefix = company.find_element_by_css_selector(
                    'div:nth-child(2) > div:nth-child(2) > md-input-container:nth-child(1) > input')
                num_prefix.send_keys(Keys.CONTROL + 'a')
                num_prefix.send_keys('22')
                company.find_element_by_css_selector(
                    'div:nth-child(2) > div:nth-child(2) > md-input-container:nth-child(2) > input').send_keys(
                    '987654321')
                company.find_element_by_css_selector('div:nth-child(2) > div:nth-child(3) input').send_keys(
                    'email@company.real')
                current_sel = company.find_element_by_css_selector(
                    'div > div:nth-child(3) > st-form-field-container > select')
                Select(current_sel).select_by_index(random.randrange(0, 4))

    def deal_info_input(self):
        from datetime import datetime

        main_info_block = self.driver.find_element_by_css_selector('st-block > st-block-form-content > div.layout-wrap')

        # Deal Name
        main_info_block.find_element_by_css_selector('div:nth-child(1) > md-input-container > input').send_keys(
            Keys.CONTROL + 'a')
        main_info_block.find_element_by_css_selector('div:nth-child(1) > md-input-container > input').send_keys(
            str(datetime.today()))

        # Deal Owner
        deal_owner_select_element = main_info_block.find_element_by_css_selector(
            'div:nth-child(2) > md-input-container > md-select')

        try:
            deal_owner_select_element.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', deal_owner_select_element)

        deal_owner_select_id = str(deal_owner_select_element.get_attribute('id'))
        deal_owner_id = str(int(deal_owner_select_id.split("_")[-1]) + 1)

        WdWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "div#select_container_" + deal_owner_id)))

        deal_owners = self.driver.find_elements_by_css_selector(
            "div#select_container_" + deal_owner_id + " > md-select-menu > md-content > md-option > div > span")
        for deal_owner in deal_owners:
            sleep(0.1)
            if deal_owner.text == 'Matthew Test':
                try:
                    deal_owner.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', deal_owner)
                break
        else:
            deal_owners[0].click()

        sleep(2)

        # Team Members
        team_members_field = main_info_block.find_element_by_css_selector('div > md-chips input')
        for user in self.users_in_workflow:
            team_members_field.send_keys(user)
            try:
                WdWait(self.driver, 5).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'md-autocomplete-parent-scope > div')))
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
        sleep(0.1)
        if self.deal_config['deal_info']['random']:
            stage_num = random.randrange(0, len(stages))
        else:
            stage_num = int(self.deal_config['deal_info']['stage_num']) - 1
        try:
            stages[stage_num].click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', stages[stage_num])
        except exceptions.ElementNotInteractableException:
            self.driver.execute_script('arguments[0].click();', stages[stage_num])
        except IndexError:
            print('Non-existent number of stages entered')

        # Deal Value
        deal_value = 500000
        sleep(1)
        deal_value_input = main_info_block.find_element_by_css_selector('div:nth-child(5) > md-input-container > input')
        deal_value_input.send_keys(Keys.CONTROL + 'a')
        deal_value_input.send_keys(deal_value)
        try:
            WdWait(self.driver, 5).until(ec.text_to_be_present_in_element_value(
                (By.CSS_SELECTOR, 'div:nth-child(5) > md-input-container > input'), '$' + f'{deal_value:,}'))
        except exceptions.TimeoutException:
            print('erroooor')
            deal_value_input.send_keys(Keys.CONTROL + 'a')
            deal_value_input.send_keys(f'{deal_value}')

        # Estimated settlement date
        estimated_settlement_date = '01/01/1998'
        estimated_settlement_date_input = main_info_block.find_element_by_css_selector(
            'div:nth-child(6) > md-input-container > md-datepicker > div > input')
        estimated_settlement_date_input.send_keys(Keys.CONTROL + 'a')
        estimated_settlement_date_input.send_keys(f'{estimated_settlement_date}')
        try:
            WdWait(self.driver, 5).until(ec.text_to_be_present_in_element_value(
                (By.CSS_SELECTOR, 'div:nth-child(6) > md-input-container > md-datepicker > div > input'),
                f'{estimated_settlement_date}'))
        except exceptions.TimeoutException:
            estimated_settlement_date_input.send_keys(Keys.CONTROL + 'a')
            estimated_settlement_date_input.send_keys(f'{estimated_settlement_date}')

        # Summary notes
        summary_notes = 'Summary Notes-u'
        main_info_block.find_element_by_css_selector('div:nth-child(7) > md-input-container textarea').send_keys(
            f'{summary_notes}')

    def client_profile_input(self):
        WdWait(self.driver, 20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'st-sidebar-block button:nth-child(2)')))
        test = self.driver.find_elements_by_css_selector('st-sidebar-block button')
        test[-1].click()
        WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-contact')))
        contact_buttons = self.driver.find_elements_by_css_selector(
            'st-sidebar-content > st-sidebar-block:first-of-type > div > button')

        for button_count, contact_button in enumerate(contact_buttons, start=1):
            try:
                current_button = self.driver.find_element_by_xpath(
                    f'//span[text()={button_count}]/ancestor::*[position()=2]')
            except exceptions.NoSuchElementException:
                print('No such element?')
            else:
                try:
                    current_button.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', current_button)

                content = WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))

                for select_el in content.find_elements_by_tag_name('select'):
                    try:
                        current_sel = Select(select_el)
                    except exceptions.StaleElementReferenceException:
                        pass
                    except:
                        pass
                    else:
                        try:
                            current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                        except ValueError:
                            current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                for md_radio_group in content.find_elements_by_tag_name('md-radio-group'):
                    md_radio_buttons = md_radio_group.find_elements_by_tag_name('md-radio-button')
                    radio_button_to_click = random.randrange(0, len(md_radio_buttons))
                    try:
                        md_radio_buttons[radio_button_to_click].click()
                    except exceptions.ElementClickInterceptedException:
                        self.driver.execute_script("arguments[0].click();",
                                                   md_radio_buttons[radio_button_to_click])
                    except Exception as inst:
                        print('Exception', inst)
                        continue

                for select_el in content.find_elements_by_tag_name('select'):
                    try:
                        current_sel = Select(select_el)
                    except exceptions.StaleElementReferenceException:
                        pass
                    except:
                        pass
                    else:
                        try:
                            current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                        except ValueError:
                            current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                try:
                    employment = self.driver.find_element_by_css_selector(
                        'st-block-form-header > button[ng-click="$ctrl.employmentAdd($event)"]')
                except exceptions.NoSuchElementException:
                    pass
                else:
                    try:
                        employment.click()
                    except exceptions.ElementClickInterceptedException:
                        self.driver.execute_script('arguments[0].click();', employment)

                    else:
                        employment.click()
                        sleep(0.01)
                        for employment_type in self.driver.find_elements_by_css_selector(
                                'st-contact-employment div > div > st-form-field-container:nth-child(2) > select'):
                            Select(employment_type).select_by_index(random.randrange(1, 3))

                sleep(1)
                for input_el in content.find_elements_by_tag_name('input'):
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
                    elif input_el.get_attribute('st-input-default-value') == '0':
                        value = random.randrange(0, 50000)
                        try:
                            input_el.send_keys(value)
                        except exceptions.ElementNotInteractableException:
                            continue
                    else:
                        try:
                            input_el.send_keys('nanobots')
                        except exceptions.ElementNotInteractableException:
                            continue

                for md_select in content.find_elements_by_tag_name('md-select'):
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
                    md_select_container = self.driver.find_elements_by_css_selector(
                        '#select_container_' + md_select_container_id + ' md-option')
                    to_click = random.randrange(0, len(md_select_container))
                    try:
                        md_select_container[to_click].click()
                    except exceptions.ElementNotInteractableException:
                        pass
                    except exceptions.ElementClickInterceptedException:
                        self.driver.execute_script("arguments[0].click();", md_select_container[to_click])
                    except:
                        pass

                for select_el in content.find_elements_by_tag_name('select'):
                    try:
                        current_sel = Select(select_el)
                    except exceptions.StaleElementReferenceException:
                        pass
                    except:
                        pass
                    else:
                        try:
                            current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                        except ValueError:
                            current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                for input_el in content.find_elements_by_tag_name('input'):
                    if not input_el.get_attribute('value'):
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
                        elif input_el.get_attribute('st-input-default-value') == '0':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                # TODO
                                # if
                                input_el.send_keys('nanobots')
                            except exceptions.ElementNotInteractableException:
                                continue

                for checkbox in content.find_elements_by_tag_name('md-checkbox'):
                    if random.randrange(0,100) > 30:
                        try:
                            checkbox.click()
                        except:
                            continue

                for input_el in content.find_elements_by_tag_name('input'):
                    if not input_el.get_attribute('value'):
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
                        elif input_el.get_attribute('st-input-default-value') == '0':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                # TODO
                                # if
                                input_el.send_keys('nanobots')
                            except exceptions.ElementNotInteractableException:
                                continue

                sleep(2)

        sleep(2)
        self.driver.refresh()
        WdWait(self.driver, 20).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'form-content > form')))

        try:
            buttons = self.driver.find_elements_by_css_selector(
                'st-sidebar-content > st-sidebar-block > div > div > button')
        except exceptions.NoSuchElementException:
            print('No div > button')
            pass
        else:
            separators = []

            for button_count, button in enumerate(buttons, start=1):

                try:
                    current_separator = button.find_element_by_css_selector('span.truncate').text
                except exceptions.StaleElementReferenceException:
                    # TODO TODO TODO TODO TODO
                    continue

                if current_separator in ['Asset to be financed', 'Lender and product', 'Compare products',
                                         'Security details', 'Funding worksheet', 'Maximum borrowing']:
                    break
                if current_separator in ['Connect to Mercury', 'Connect to Flex']:
                    continue

                separators.append(current_separator)

            for separator in separators:
                try:
                    current_button = self.driver.find_element_by_xpath(
                        f"//span[text()='{separator}']/ancestor::*[position()=1]")
                except exceptions.NoSuchElementException:
                    # print(separator)
                    current_button = self.driver.find_element_by_xpath(f"//*[normalize-space(span)='{separator}']")
                try:
                    current_button.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', current_button)

                content = WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))

                # TODO TODO TODO TODO TODO
                if separator == 'Income':
                    income_buttons = self.driver.find_elements_by_css_selector('div.mt0 button')
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

                    for select_el in content.find_elements_by_tag_name('select'):
                        try:
                            current_sel = Select(select_el)
                        except exceptions.StaleElementReferenceException as inst:
                            print('Stale reference', inst)
                            pass
                        except Exception as inst:
                            print('bad reference', inst)
                            pass
                        else:
                            # print(len(current_sel.options))
                            try:
                                current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                            except ValueError:
                                current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                    sleep(1)
                    for input_el in content.find_elements_by_tag_name('input'):
                        if input_el.get_attribute('class') == 'md-datepicker-input md-input':
                            year = random.randrange(1930, 2030)
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
                        elif input_el.get_attribute('st-input-default-value') == '0':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        elif input_el.get_attribute('currency-symbol') == '$':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                input_el.send_keys('nanobots')
                            except exceptions.ElementNotInteractableException:
                                continue
                    sleep(2)

                elif separator == 'Expenses':
                    self.driver.find_element_by_css_selector('st-block-form-header > button').click()
                    household_picker = WdWait(self.driver, 10).until(ec.presence_of_element_located(
                        (By.CSS_SELECTOR, 'st-tabs-list-content > div > div > div > md-input-container > md-select')))
                    household_picker.click()
                    household_picker_id = household_picker.get_attribute('id')
                    household_picker_container_id = str(int(household_picker_id.split("_")[-1]) + 1)
                    household_picker_container = WdWait(self.driver, 10).until(
                        ec.element_to_be_clickable((By.ID, "select_container_" + household_picker_container_id)))
                    household_members = household_picker_container.find_elements_by_css_selector('md-option')

                    for household_member in household_members:
                        household_member.click()

                    sleep(1)
                    for input_el in content.find_elements_by_tag_name('input'):
                        if input_el.get_attribute('ng-model') == 'householdExpense.value':
                            try:
                                input_el.send_keys(random.randrange(0, 5000))
                            except:
                                pass
                        elif input_el.get_attribute('ng-model') == 'householdExpense.comments':
                            try:
                                input_el.send_keys('expense comment')
                            except:
                                pass
                    for select_el in content.find_elements_by_tag_name('select'):
                        select = Select(select_el)
                        select.select_by_index(random.randrange(0, len(select.options)))
                    sleep(2)

                elif separator == 'Assets':
                    assets = self.driver.find_elements_by_css_selector('div.mt0 button')
                    for asset in assets:
                        try:
                            asset.click()
                        except exceptions.ElementNotInteractableException:
                            continue
                        else:
                            sleep(0.01)
                            asset.click()

                    for select_el in content.find_elements_by_tag_name('select'):
                        try:
                            current_sel = Select(select_el)
                        except exceptions.StaleElementReferenceException:
                            pass
                        except:
                            pass
                        else:
                            try:
                                current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                            except ValueError:
                                current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                    for input_el in content.find_elements_by_tag_name('input'):
                        if input_el.get_attribute('class') == 'md-datepicker-input md-input':
                            year = random.randrange(1930, 2030)
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
                        elif input_el.get_attribute('st-input-default-value') == '0':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                input_el.send_keys('nanobots')
                            except exceptions.ElementNotInteractableException:
                                continue

                    for md_select in content.find_elements_by_tag_name('md-select'):
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
                        md_select_container = self.driver.find_elements_by_css_selector(
                            '#select_container_' + md_select_container_id + ' md-option')
                        to_click = random.randrange(0, len(md_select_container))
                        try:
                            md_select_container[to_click].click()
                        except exceptions.ElementNotInteractableException:
                            pass
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", md_select_container[to_click])
                        except:
                            pass
                    sleep(2)

                elif separator == 'Liabilities':

                    liabilities = self.driver.find_elements_by_css_selector('div.mt0 button')
                    for liability in liabilities:
                        try:
                            liability.click()
                        except exceptions.ElementNotInteractableException:
                            continue
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", liability)
                        else:
                            sleep(0.01)
                            liability.click()

                    for select_el in content.find_elements_by_tag_name('select'):
                        try:
                            current_sel = Select(select_el)
                        except exceptions.StaleElementReferenceException:
                            pass
                        except:
                            pass
                        else:
                            try:
                                current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                            except ValueError:
                                current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                    for input_el in content.find_elements_by_tag_name('input'):
                        if input_el.get_attribute('class') == 'md-datepicker-input md-input':
                            year = random.randrange(1930, 2030)
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
                        elif input_el.get_attribute('st-input-default-value') == '0':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                input_el.send_keys('nanobots')
                            except exceptions.ElementNotInteractableException:
                                continue
                    for md_select in content.find_elements_by_tag_name('md-select'):
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
                        md_select_container = self.driver.find_elements_by_css_selector(
                            '#select_container_' + md_select_container_id + ' md-option')
                        to_click = random.randrange(0, len(md_select_container))
                        try:
                            md_select_container[to_click].click()
                        except exceptions.ElementNotInteractableException:
                            pass
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", md_select_container[to_click])
                        except:
                            pass
                    sleep(2)

                elif separator == 'Needs and objectives':
                    for textarea in content.find_elements_by_tag_name('textarea'):
                        textarea.send_keys('nanobots')

                    for select_el in content.find_elements_by_tag_name('select'):
                        try:
                            current_sel = Select(select_el)
                        except exceptions.StaleElementReferenceException:
                            pass
                        except:
                            pass
                        else:
                            try:
                                current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                            except ValueError:
                                current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                    for input_el in content.find_elements_by_tag_name('input'):
                        if input_el.get_attribute('class') == 'md-datepicker-input md-input':
                            year = random.randrange(1930, 2030)
                            try:
                                input_el.send_keys(f'01/01/{year}')
                            except exceptions.ElementNotInteractableException:
                                continue
                        elif input_el.get_attribute('st-input-default-value') == '0':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                input_el.send_keys('nanobots')
                            except exceptions.ElementNotInteractableException:
                                continue

                    for md_radio_group in content.find_elements_by_tag_name('md-radio-group'):
                        md_radio_buttons = md_radio_group.find_elements_by_tag_name('md-radio-button')
                        radio_button_to_click = random.randrange(0, len(md_radio_buttons))
                        try:
                            md_radio_buttons[radio_button_to_click].click()
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", md_radio_buttons[radio_button_to_click])
                        except Exception as inst:
                            print('Exception', inst)
                            continue

                    for checkbox in content.find_elements_by_tag_name('md-checkbox'):
                        if random.randrange(0,100) > 30:
                            try:
                                checkbox.click()
                            except:
                                continue

                    for input_el in content.find_elements_by_tag_name('input'):
                        if input_el.get_attribute('class') == 'md-datepicker-input md-input':
                            year = random.randrange(1930, 2030)
                            try:
                                input_el.send_keys(f'01/01/{year}')
                            except exceptions.ElementNotInteractableException:
                                continue
                        elif input_el.get_attribute('st-input-default-value') == '0':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                input_el.send_keys('nanobots')
                            except exceptions.ElementNotInteractableException:
                                continue
                    sleep(2)



                # elif current_separator == 'Product requirements':
                #     pass
                elif separator == 'Insurance':
                    insurance = self.driver.find_elements_by_css_selector('div.mt0 button')
                    for insuranc in insurance:
                        try:
                            insuranc.click()
                        except exceptions.ElementNotInteractableException:
                            continue
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", insuranc)
                        else:
                            sleep(0.01)
                            insuranc.click()

                    for select_el in content.find_elements_by_tag_name('select'):
                        try:
                            current_sel = Select(select_el)
                        except exceptions.StaleElementReferenceException:
                            pass
                        except:
                            pass
                        else:
                            try:
                                current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                            except ValueError:
                                current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                    for input_el in content.find_elements_by_tag_name('input'):
                        if input_el.get_attribute('class') == 'md-datepicker-input md-input':
                            year = random.randrange(1930, 2030)
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
                        elif input_el.get_attribute('st-input-default-value') == '0':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                input_el.send_keys('nanobots')
                            except exceptions.ElementNotInteractableException:
                                continue

                    for md_select in content.find_elements_by_tag_name('md-select'):
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
                        md_select_container = self.driver.find_elements_by_css_selector(
                            '#select_container_' + md_select_container_id + ' md-option')
                        to_click = random.randrange(0, len(md_select_container))
                        try:
                            md_select_container[to_click].click()
                        except exceptions.ElementNotInteractableException:
                            pass
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", md_select_container[to_click])
                        except:
                            pass

                elif separator == 'Other advisers':
                    other_advisers = self.driver.find_elements_by_css_selector('div.mt0 button')
                    for other_adviser in other_advisers:
                        try:
                            other_adviser.click()
                        except exceptions.ElementNotInteractableException:
                            continue
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", other_adviser)
                        else:
                            sleep(0.01)
                            other_adviser.click()

                    for select_el in content.find_elements_by_tag_name('select'):
                        try:
                            current_sel = Select(select_el)
                        except exceptions.StaleElementReferenceException:
                            pass
                        except:
                            pass
                        else:
                            try:
                                current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                            except ValueError:
                                current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                    for input_el in content.find_elements_by_tag_name('input'):
                        try:
                            input_el.send_keys('nanobots')
                        except exceptions.ElementNotInteractableException:
                            continue
                        sleep(2)

                    for md_select in content.find_elements_by_tag_name('md-select'):
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
                        md_select_container = self.driver.find_elements_by_css_selector(
                            '#select_container_' + md_select_container_id + ' md-option')
                        to_click = random.randrange(0, len(md_select_container))
                        try:
                            md_select_container[to_click].click()
                        except exceptions.ElementNotInteractableException:
                            pass
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", md_select_container[to_click])
                        except:
                            pass
                        sleep(2)


                else:
                    for select_el in content.find_elements_by_tag_name('select'):
                        try:
                            current_sel = Select(select_el)
                        except exceptions.StaleElementReferenceException:
                            pass
                        except:
                            pass
                        else:
                            try:
                                current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                            except ValueError:
                                current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                    for select_el in content.find_elements_by_tag_name('select'):
                        try:
                            current_sel = Select(select_el)
                        except exceptions.StaleElementReferenceException:
                            pass
                        except:
                            pass
                        else:
                            try:
                                current_sel.select_by_index(random.randrange(1, len(current_sel.options)))
                            except ValueError:
                                current_sel.select_by_index(random.randrange(0, len(current_sel.options)))

                    sleep(1)
                    for input_el in content.find_elements_by_tag_name('input'):
                        if input_el.get_attribute('class') == 'md-datepicker-input md-input':
                            year = random.randrange(1930, 2030)
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
                        elif input_el.get_attribute('st-input-default-value') == '0':
                            value = random.randrange(0, 50000)
                            try:
                                input_el.send_keys(value)
                            except exceptions.ElementNotInteractableException:
                                continue
                        else:
                            try:
                                input_el.send_keys('nanobots')
                            except exceptions.ElementNotInteractableException:
                                continue
                    for md_select in content.find_elements_by_tag_name('md-select'):
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
                        md_select_container = self.driver.find_elements_by_css_selector(
                            '#select_container_' + md_select_container_id + ' md-option')
                        to_click = random.randrange(0, len(md_select_container))
                        try:
                            md_select_container[to_click].click()
                        except exceptions.ElementNotInteractableException:
                            pass
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", md_select_container[to_click])
                        except:
                            pass
                sleep(2)

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

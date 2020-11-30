from main.Permanent import workflow_manipulation

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Firefox
from selenium.common import exceptions

from time import sleep
from datetime import datetime
import json
import random
import traceback
from pathlib import Path

import string


class EditDeal:
    def __init__(self, ent, driver: Firefox):
        # self.current_export_array = []
        with open("deal_config") as deal_config_json:
            self.deal_config = json.load(deal_config_json)
        self.users_in_workflow = ''
        self.number_of_contacts = None
        self.driver = driver
        self.main_url = 'https://' + ent + '.salestrekker.com'
        self.wf_manipulate = workflow_manipulation.WorkflowManipulation(self.driver, ent)
        self.incrementer = 0

    def create_deal(self, workflow='test', af_type="cons"):

        if workflow == 'test':
            self.driver.get(self.main_url)
            in_workflow = self.driver.current_url.split('/')[-1]
        else:
            in_workflow = workflow

        # if users_in_workflow := self.wf_manipulate.workflow_users(in_workflow):
        #     self.users_in_workflow = users_in_workflow
        # else:
        #     self.wf_manipulate.add_users_to_workflow(worklfow_id=in_workflow)

        self.driver.get(self.main_url + '/deal/edit/' + in_workflow + '/0')

        WdWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'top')))

        # assert "Add New Ticket" in self.driver.title

        main_info_block = WdWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'st-block > st-block-form-content > div.layout-wrap')))
        self.select_deal_owner(main_info_block, 'Marko P')

        try:
            purpose_radio_group = WdWait(self.driver, 5).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'md-radio-group[ng-change="toggleCommercial()"]')))
        except exceptions.TimeoutException:
            pass
        else:
            if af_type == "comm":
                purpose_radio_group.find_element(by=By.CSS_SELECTOR,
                                                 value='md-radio-button[aria-label="Commercial"]').click()
            elif af_type == "cons":
                purpose_radio_group.find_element(by=By.CSS_SELECTOR,
                                                 value='md-radio-button[aria-label="Consumer"]').click()

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
            WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
        except exceptions.TimeoutException:
            try:
                WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'form[name="ticketEdit"]')))
            except exceptions.TimeoutException:
                WdWait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
            else:
                try:
                    save_button.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", save_button)
                finally:
                    try:
                        WdWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
                    except exceptions.TimeoutException:
                        pass
        finally:
            deal_url = self.driver.current_url

        return deal_url
        # self.client_profile_input()

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

                rand_val = random.randrange(0, 2)

                if self.incrementer < 2:

                    contact_type = contact_type_container.find_elements(by=By.TAG_NAME, value='button')
                    try:
                        contact_type[0].click()
                    except exceptions.ElementClickInterceptedException:
                        self.driver.execute_script('arguments[0].click();', contact_type[0])
                    self.incrementer += 1
                else:
                    contact_type = contact_type_container.find_elements(by=By.TAG_NAME, value='button')
                    try:
                        contact_type[1].click()
                    except exceptions.ElementClickInterceptedException:
                        self.driver.execute_script('arguments[0].click();', contact_type[1])

                    self.incrementer += 1

                    # type_of_cont = contact_type[rand_val].get_attribute('ng-click')
                    #
                    # if type_of_cont == 'contactAdd(false)':
                    #     self.current_export_array.append('Person ')
                    #
                    # if type_of_cont == 'contactAdd(true)':
                    #     self.current_export_array.append('Company ')

            elif contacts['contact_types'] == 'company':
                contact_type = contact_type_container.find_elements(by=By.TAG_NAME, value='button')
                for contact_button in contact_type:
                    if contact_button.find_element(by=By.TAG_NAME, value='span').text == 'Company':
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
                contact_type = contact_type_container.find_elements(by=By.TAG_NAME, value='button')
                for contact_button in contact_type:
                    sleep(1)
                    if contact_button.find_element(by=By.TAG_NAME, value='span').text == 'Person':
                        try:
                            contact_button.click()
                        except exceptions.ElementClickInterceptedException:
                            self.driver.execute_script('arguments[0].click();', contact_button)
                            # self.current_export_array.append('Person ')
                        finally:
                            break
                else:
                    raise Exception
                    pass

        # self.current_export_array.append("No. of clients: " + str(number_of_contacts) + ", ")

    # TODO - Get a better way to pass in names
    def contact_input(self):

        person_names = [['Misty', 'Banks'], ['Karl', 'Berg'], ['Tanisha', 'Obrien'], ['Jasmin', 'Talley'],
                        ['Lexi-Mai', 'Mccray'], ['Chandni', 'Kramer'], ['Musab', 'Cunningham'], ['Spike', 'Dunn'],
                        ['Doris', 'Vu'], ['Dominick', 'Ferry'], ['Rudi', 'Wolfe'], ['Saira', 'Haas'],
                        ['Keeleigh', 'Bate'],
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
                        ['Rachael', 'Zavala'], ['Kuba', 'Gibbons'], ['Callam', 'Almond'], ['Nick', 'Bruce'],
                        ['Ayub', 'Felix'],
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
                        ['Sherri', 'Betts'], ['Cosmo', 'Lopez'], ['Nella', 'Molloy'], ['Hasan', 'Plant'],
                        ['Tyrique', 'Kirk'],
                        ['Jonah', 'Cantu'], ['Lexi-Mae', 'Reid'], ['Nigel', 'Whelan'], ['Zavier', 'Dupont'],
                        ['Bevan', 'Berry'], ['Leo', 'Mueller'], ['Israel', 'Lowery'], ['Sharna', 'Powell'],
                        ['Jagoda', 'Porter'], ['Deborah', 'Krueger'], ['Claire', 'Griffiths'], ['Anabelle', 'Garrett'],
                        ['Kobie', 'Barrett'], ['Nabeel', 'Gibbs'], ['Kayley', 'Calvert'], ['Zahrah', 'Hills'],
                        ['Beck', 'Rice'], ['Kingsley', 'Correa'], ['Micah', 'Pineda'], ['Jerry', 'Beasley'],
                        ['Haydn', 'Sanderson'], ['Robyn', 'Frye'], ['Carwyn', 'Garrison'], ['Rhys', 'Trevino'],
                        ['Seamus', 'Stafford'], ['Maia', 'Rankin'], ['Iman', 'Huerta'], ['Rahul', 'Luna'],
                        ['Judy', 'Mustafa'],
                        ['Arwa', 'Lane'], ['Jeevan', 'Russo'], ['Francesco', 'Richmond'], ['Shyam', 'Ferry'],
                        ['Amal', 'Wolfe'], ['Gabrielle', 'Schmidt'], ['Kellie', 'Mcnally'], ['Derry', 'Power'],
                        ['Quentin', 'Castaneda'], ['Hashir', 'Wickens'], ['Alma', 'Romero'], ['Rheanna', 'Smyth'],
                        ['Sebastian', 'Coulson'], ['Sahara', 'Riley'], ['Miriam', 'Carty'], ['Debbie', 'Hogan'],
                        ['Niyah', 'Bonilla'], ['Lillie-May', 'Mcgee'], ['Petra', 'Buck'], ['Khalil', 'Mccoy'],
                        ['Lena', 'Schneider'], ['Isabell', 'Gordon'], ['Howard', 'Hardy'], ['Lennie', 'Ferreira'],
                        ['Jibril', 'Jarvis'], ['Christiana', 'Haley'], ['Alan', 'Bray'], ['Kimora', 'Barnett'],
                        ['Muneeb', 'Finch'], ['Iqrah', 'Cox'], ['Hanna', 'Lawrence'], ['Akbar', 'Leech'],
                        ['Beverly', 'Bain'],
                        ['Jill', 'Cross'], ['Shania', 'Hyde'], ['T-Jay', 'Soto'], ['George', 'Bates'],
                        ['Lexie', 'Knowles'],
                        ['Gerard', 'Douglas'], ['Weronika', 'Roberts'], ['Alison', 'Cornish'], ['Reon', 'Robles'],
                        ['Piotr', 'Macgregor'], ['Alya', 'Hines'], ['Mitchel', 'Oakley'], ['Sally', 'Santos'],
                        ['Alfie-Lee', 'Kirkpatrick'], ['Abbie', 'Alvarez'], ['Pola', 'Piper'], ['Laylah', 'Murphy'],
                        ['Zubair', 'Boyd'], ['Ali', 'Haas'], ['Nicole', 'Corbett'], ['Lorna', 'Short'],
                        ['Ember', 'Alexander'],
                        ['Cora', 'Sloan']]

        company_names = ['Indeed Entity', 'Finally Entity', 'Seem Entity', 'They Entity', 'Reallysatisfied Entity',
                         'Rethoughtbut Entity', 'Fantasticbut Entity', 'Vastbut Entity', 'Saferbut Entity',
                         'Addbut Entity', 'Butanywhere Entity', 'Ensuredbut Entity', 'Characterbut Entity',
                         'Then&Seem Entity', 'Only&Like Entity', 'Upstartbut Entity', 'Butworks Entity',
                         'Believebut Entity', 'Barely&Would Entity', 'Know&Although Entity', 'Butcollate Entity',
                         'Mostbut Entity', 'Butaiming Entity', 'Mean&Roundly Entity', 'Make&Werent Entity',
                         'Unlikelyally Entity', 'Soon Entity', 'Admitly Entity', 'Expectably Entity', 'Sureably Entity',
                         'Butorignal Entity', 'Thinkbut Entity', 'Sillybut Entity', 'Butunable Entity',
                         'Commentbut Entity', 'Lose&Entirely Entity', 'Butrewards Entity', 'Butalternate Entity',
                         'Afraid&Vastly Entity', 'Recoversbut Entity', 'Believe&Thus Entity', 'Butnever Entity',
                         'Believe&⡌ Entity', 'Darned&Only Entity', 'Avail&Any Entity', 'Sunnierbut Entity',
                         'Butabsolute Entity', 'Afaict&Hoping Entity', 'Buttheory Entity', 'Blastingbut Entity',
                         'Tellingly Entity', 'Knew.Me Entity', 'Everythiing Entity', 'Definitely Entity',
                         'Definitelyright Entity', 'Butcase Entity', 'Petered&Now Entity', 'Extent&Wouldn Entity',
                         'Ignored&They Entity', 'Going&Seldom Entity', 'Couldn&Remain Entity', 'Mightn&Singly Entity',
                         'Hint&Avail Entity', 'Him&Didn Entity', 'Does&Inclined Entity', 'Butbit Entity',
                         'Explaining&It Entity', 'Butprimary Entity', 'Butscape Entity', 'Unable&Which Entity',
                         'Almost&Weren Entity', 'Butweblinks Entity', 'Easily&Apart Entity', 'Thinking&To Entity',
                         'Butfox Entity', 'Debatably Entity', 'Muchsooner Entity', 'Reallysure Entity',
                         'Besides.Io Entity', 'Phairly Entity', 'Quickbut Entity', 'Wellbut Entity', 'Outbut Entity',
                         'Often&Nobody Entity', 'Be&Darned Entity', 'Butgigantic Entity', 'Savedbut Entity',
                         'Linkedbut Entity', 'Butprefer Entity', 'Amazinglybut Entity', 'Weren&Feels Entity',
                         'Chosebut Entity', 'Butmost Entity', 'Butkicking Entity', 'Calmnessbut Entity',
                         'Powerfullbut Entity', 'Astutebut Entity', 'Sensiblebut Entity', 'Imho&Worried Entity',
                         'Butfalsehood Entity', 'Believingg Entity', 'Thenly Entity', 'Entire Entity',
                         'Extremelysatisfied Entity', 'Wrong.Io Entity', 'When&Proves Entity', 'Helpfulbut Entity',
                         'Seldom&Nope Entity', 'Butquoting Entity', 'Unawares&To Entity', 'Then&Often Entity',
                         'Honestly&Once Entity', 'Butweek Entity', 'Idea&Badly Entity', 'Wishbut Entity',
                         'Butmessage Entity', 'Insofar&Didn Entity', 'Butpiping Entity', 'Happen&Which Entity',
                         'Entirebut Entity', 'Geniusbut Entity', 'Thebut Entity', 'The&Vaguely Entity',
                         'Butgirl Entity', 'Butactuality Entity', 'Doingly Entity', 'Reliantly Entity',
                         'Unreally Entity', 'Anymore.Io Entity', 'Chargefully Entity', 'We&Vainly Entity',
                         'Releasingbut Entity', 'Well&Seeing Entity', 'Recoversbut Entity', 'Butaction Entity',
                         'Usually&Again Entity', 'Where&Frankly Entity', 'Would&Barely Entity', 'Redapplebut Entity',
                         'Longer&When Entity', 'Isn&Hesitant Entity', 'Butnames Entity', 'Forbut Entity',
                         'Buteye Entity', 'Retainbut Entity', 'Butoptimal Entity', 'Faltering&Any Entity',
                         'Wholebut Entity', 'Able&Bothers Entity', 'Cannot&There Entity', 'Wherever.Io Entity',
                         'Willing.Io Entity', 'Lookfully Entity', 'Cannotmiss Entity', 'Telling Entity',
                         'Butproduct Entity', 'Butstandard Entity', 'Moreover&Soon Entity', 'Buttrusting Entity',
                         'Butsuppose Entity', 'Knightlybut Entity', 'Confidentbut Entity', 'Butopening Entity',
                         'Approachbut Entity', 'Unnoticed&Btw Entity', 'Butanswering Entity', 'Butguys Entity',
                         'Butfavored Entity', 'Letting&Soon Entity', 'Butspeed Entity', 'Butstill Entity',
                         'Excitesbut Entity', 'Aware&These Entity', 'Slicingbut Entity', 'Butvitally Entity',
                         'Anythiing Entity', 'Veryquietly Entity', 'Unfortunate Entity', 'Potfully Entity',
                         'Dashfully Entity', 'These&Concede Entity', 'Butmay Entity', 'What&Contend Entity',
                         'Itself&Thinks Entity', 'Butomatic Entity', 'Butalso Entity', 'Rest&•• Entity',
                         'Butmachine Entity', 'Butbalanced Entity', 'Butaddicts Entity', 'Smootherbut Entity',
                         'Safebut Entity', '&&Bother Entity', 'Butcompare Entity', 'Awful&Hence Entity',
                         'Ensuredbut Entity', 'Valuablebut Entity', 'Butrepairing Entity', 'Butback Entity',
                         'Curiously&We Entity']

        person_list = []
        company_list = []
        try:
            WdWait(self.driver, 6).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'div.mt0 > div > div:nth-child(1) input')))
        except exceptions.TimeoutException:
            pass
        for contact in self.driver.find_elements(by=By.CSS_SELECTOR, value='div.mt0'):
            if contact.find_element(by=By.CSS_SELECTOR,
                                    value='md-autocomplete-wrap > md-input-container > label').text == 'First name':
                person_list.append(contact)
            elif contact.find_element(by=By.CSS_SELECTOR,
                                      value='md-autocomplete-wrap > md-input-container > label').text == 'Entity name':
                company_list.append(contact)

        if person_list:
            for count, person in enumerate(person_list):
                person_name = person_names[random.randrange(0, len(person_names))]

                person.find_element(by=By.CSS_SELECTOR,
                                    value='div:nth-child(2) > div:nth-child(1) > md-autocomplete > md-autocomplete-wrap > md-input-container >input').send_keys(
                    person_name[0])
                person.find_element(by=By.CSS_SELECTOR,
                                    value='div:nth-child(2) > div:nth-child(2) > md-input-container > input').send_keys(
                    person_name[1])
                num_prefix = person.find_element(by=By.CSS_SELECTOR,
                                                 value='div:nth-child(2) > div:nth-child(3) > md-input-container:nth-child(1) > input')
                num_prefix.send_keys(Keys.CONTROL + 'a')
                num_prefix.send_keys('11')
                person.find_element(by=By.CSS_SELECTOR,
                                    value='div:nth-child(2) > div:nth-child(3) > md-input-container:nth-child(2) > input').send_keys(
                    '123456789')
                person.find_element(by=By.CSS_SELECTOR,
                                    value='div:nth-child(2) > div:nth-child(4) > md-input-container > input').send_keys(
                    'email@person.real')
                current_sel = person.find_element(by=By.CSS_SELECTOR,
                                                  value='div:nth-child(2) > div:nth-child(4) > st-form-field-container > select')

                if self.deal_config['contacts']['non_client']['active']:
                    if count < int(self.deal_config['contacts']['non_client']['no_of_clients']):
                        try:
                            Select(current_sel).select_by_index(random.randrange(0, 4))
                        except exceptions.ElementClickInterceptedException:
                            WdWait(self.driver, 20).until(
                                ec.invisibility_of_element_located((By.CSS_SELECTOR, 'md-toast.ng-scope')))

                            Select(current_sel).select_by_index(random.randrange(0, 4))
                    else:
                        try:
                            Select(current_sel).select_by_index(random.randrange(0, len(Select(current_sel).options)))
                        except exceptions.ElementClickInterceptedException:
                            Select(current_sel).select_by_index(random.randrange(0, len(Select(current_sel).options)))
                else:
                    try:
                        Select(current_sel).select_by_index(random.randrange(0, 4))
                    except exceptions.ElementClickInterceptedException:
                        Select(current_sel).select_by_index(random.randrange(0, 4))

        if company_list:
            for count, company in enumerate(company_list):
                company.find_element(by=By.CSS_SELECTOR,
                                     value='div:nth-child(2) > div:nth-child(1) > md-autocomplete > md-autocomplete-wrap > md-input-container >input').send_keys(
                    company_names[random.randrange(0, len(company_names))])
                num_prefix = company.find_element(by=By.CSS_SELECTOR,
                                                  value='div:nth-child(2) > div:nth-child(2) > md-input-container:nth-child(1) > input')
                num_prefix.send_keys(Keys.CONTROL + 'a')
                num_prefix.send_keys('22')
                company.find_element(by=By.CSS_SELECTOR,
                                     value='div:nth-child(2) > div:nth-child(2) > md-input-container:nth-child(2) > input').send_keys(
                    '987654321')
                company.find_element(by=By.CSS_SELECTOR, value='div:nth-child(2) > div:nth-child(3) input').send_keys(
                    'email@company.real')
                current_sel = company.find_element(by=By.CSS_SELECTOR,
                                                   value='div > div:nth-child(3) > st-form-field-container > select')

                if self.deal_config['contacts']['non_client']['active']:
                    if count < int(self.deal_config['contacts']['non_client']['no_of_clients']):
                        Select(current_sel).select_by_index(random.randrange(0, 4))
                    else:
                        Select(current_sel).select_by_index(random.randrange(0, len(Select(current_sel).options)))
                else:
                    Select(current_sel).select_by_index(random.randrange(0, 4))

    def deal_info_input(self):

        main_info_block = self.driver.find_element(by=By.CSS_SELECTOR,
                                                   value='st-block > st-block-form-content > div.layout-wrap')

        # Deal Name
        main_info_block.find_element(by=By.CSS_SELECTOR,
                                     value='div:nth-child(1) > md-input-container > input').send_keys(
            Keys.CONTROL + 'a')
        # main_info_block.find_element(by=By.CSS_SELECTOR,value='div:nth-child(1) > md-input-container > input').send_keys(str(datetime.today()))
        main_info_block.find_element(by=By.CSS_SELECTOR,
                                     value='div:nth-child(1) > md-input-container > input').send_keys(
            f'{datetime.now()}')

        # self.select_deal_owner(main_info_block, 'Salestrekker Help Desk')

        sleep(2)

        # # Team Members
        # team_members_field = main_info_block.find_element(by=By.CSS_SELECTOR,value='div > md-chips input')
        # for user in self.users_in_workflow:
        #     team_members_field.send_keys(user)
        #     sleep(2)
        #     try:
        #         WdWait(self.driver, 5).until(
        #             ec.visibility_of_element_located((By.CSS_SELECTOR, 'md-autocomplete-parent-scope > div')))
        #     except exceptions.TimeoutException:
        #         print('this shouldn\'t happen as we\'ve already ensured that users are in that workflow, but here we '
        #               'are ')
        #
        #     offered_users = self.driver.find_elements(by=By.CSS_SELECTOR,value='md-autocomplete-parent-scope > div')
        #     for offered_user in offered_users:
        #         try:
        #             self.driver.execute_script('arguments[0].click();', offered_user.find_element(by=By.XPATH,value='../..'))
        #         except exceptions.StaleElementReferenceException:
        #             continue
        #         # offered_user.click()

        stage_select_element = main_info_block.find_element(by=By.CSS_SELECTOR,
                                                            value='div:nth-child(4) > md-input-container > md-select')
        try:
            stage_select_element.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', stage_select_element)
        stage_select_id = str(stage_select_element.get_attribute('id'))
        stage_container_id = str(int(stage_select_id.split("_")[-1]) + 1)

        stages = self.driver.find_elements(by=By.CSS_SELECTOR,
                                           value="div#select_container_" + stage_container_id + " > md-select-menu > md-content > md-option")
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
        sleep(0.2)
        deal_value_input = main_info_block.find_element(by=By.CSS_SELECTOR,
                                                        value='div:nth-child(5) > md-input-container > input')
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
        estimated_settlement_date_input = main_info_block.find_element(by=By.CSS_SELECTOR,
                                                                       value='div:nth-child(6) > md-input-container > md-datepicker > div > input')
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
        main_info_block.find_element(by=By.CSS_SELECTOR, value='div > md-input-container > div > textarea').send_keys(
            f'{summary_notes}')

    def select_deal_owner(self, main_info_block, deal_owner_name):

        # Deal Owner
        deal_owner_select_element = main_info_block.find_element(by=By.CSS_SELECTOR,
                                                                 value='div:nth-child(2) > md-input-container > md-select')

        try:
            deal_owner_select_element.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', deal_owner_select_element)

        deal_owner_select_id = str(deal_owner_select_element.get_attribute('id'))
        deal_owner_id = str(int(deal_owner_select_id.split("_")[-1]) + 1)
        try:
            WdWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, "div#select_container_" + deal_owner_id)))
        except exceptions.TimeoutException:
            pass

        deal_owners = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                value="div#select_container_" + deal_owner_id + " > md-select-menu > md-content > md-option > div > span")

        # TODO Rewrite to do a javascript search instead of a for loop
        for deal_owner in deal_owners:
            sleep(0.1)
            if deal_owner.text == deal_owner_name:
                try:
                    deal_owner.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', deal_owner)
                break
        else:
            try:
                deal_owners[0].click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script('arguments[0].click();', deal_owners[0])


class MultipleDealCreator:

    def __init__(self, ent, driver: Firefox):
        # self.current_export_array = []
        occupation_path = Path(__file__).parent.resolve() / "../assets/occupations.json"
        with open(occupation_path) as occupation_codes:
            self.occupations = json.load(occupation_codes)

        industry_path = Path(__file__).parent.resolve() / "../assets/industries.json"
        with open(industry_path, 'r') as industry_codes:
            self.industries = json.load(industry_codes)

        with open("deal_config") as deal_config_json:
            self.deal_config = json.load(deal_config_json)

        self.users_in_workflow = ''
        self.number_of_contacts = None
        self.driver = driver
        self.main_url = 'https://' + ent + '.salestrekker.com'
        self.wf_manipulate = workflow_manipulation.WorkflowManipulation(self.driver, ent)
        self.address_repeat = 0
        self.address_placeholders = ['Search Property (eg. 1 Walker Avenue)','Search current address','Search employer address','Search next of kin address','Search mailing address','Search previous address']

    def md_toast_waiter(self):
        try:
            WdWait(self.driver, 5).until(
                ec.invisibility_of_element((By.CSS_SELECTOR, 'md-toast.ng-scope')))
        except exceptions.TimeoutException:
            pass
        while True:
            sleep(3)
            try:
                md_toast = self.driver.find_element(by=By.TAG_NAME, value='md-toast')
            except exceptions.NoSuchElementException:
                break
            else:
                self.driver.execute_script("arguments[0].remove();", md_toast)
                try:
                    md_toast2 = self.driver.find_element(by=By.TAG_NAME, value='md-toast')
                except exceptions.NoSuchElementException:
                    break
                else:
                    self.driver.execute_script("arguments[0].remove();", md_toast2)

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
                self.md_toast_waiter()
                try:
                    current_sel.select_by_index(index)
                except exceptions.ElementClickInterceptedException:
                    print('removing header')
                    self.md_toast_waiter()

                    try:
                        header = self.driver.find_element(by=By.CSS_SELECTOR, value='st-header.new.ng-scope')
                    except exceptions.NoSuchElementException:
                        pass
                    else:
                        self.driver.execute_script("arguments[0].remove();", header)

                    try:
                        scroll_mask = self.driver.find_element(by=By.CSS_SELECTOR, value='div.md-scroll-mask')
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
                    self.md_toast_waiter()
                    try:
                        current_sel.select_by_index(index)
                    except exceptions.ElementClickInterceptedException:
                        print('removing header')
                        self.md_toast_waiter()
                        header = self.driver.find_element(by=By.CSS_SELECTOR, value='st-header.new.ng-scope')
                        self.driver.execute_script("arguments[0].remove();", header)
                        current_sel.select_by_index(index)

    def select_el_handler(self, content):

        self.md_toast_waiter()

        for select_el in content.find_elements(by=By.TAG_NAME, value='select'):
            try:
                if select_el.get_attribute('ng-model') == '$ctrl.address.country':
                    self.selector(select_el, index='1')
                elif select_el.get_attribute('ng-model') in ['$ctrl.employment.isCurrent','$ctrl.employment.type','$ctrl.employment.status','$ctrl.employment.basis']:
                    continue
                else:
                    self.selector(select_el)
            except exceptions.StaleElementReferenceException:
                continue

    def md_radio_group(self, content):
        for md_radio_group in content.find_elements(by=By.TAG_NAME, value='md-radio-group'):
            try:
                md_radio_buttons = md_radio_group.find_elements(by=By.TAG_NAME, value='md-radio-button')
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
        try:
            employment = self.driver.find_element(by=By.CSS_SELECTOR,
                                                  value='st-block-form-header > button[ng-click="$ctrl.employmentAdd($event)"]')
        except exceptions.NoSuchElementException:
            pass
        else:
            try:
                employment.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script('arguments[0].click();', employment)

            else:
                sleep(0.01)

                for employment_status in self.driver.find_elements(by=By.CSS_SELECTOR,
                                                                   value='select[ng-change="$ctrl.toggleEmployment()"]'):
                    try:
                        Select(employment_status).select_by_index(random.randrange(0, 2))
                    except exceptions.ElementClickInterceptedException:
                        self.md_toast_waiter()
                        try:
                            Select(employment_status).select_by_index(random.randrange(0, 2))
                        except exceptions.ElementClickInterceptedException:
                            header = self.driver.find_element(by=By.CSS_SELECTOR, value='st-header.new.ng-scope')
                            self.driver.execute_script("arguments[0].remove();", header)
                            Select(employment_status).select_by_index(random.randrange(0, 2))

                for employment_type in self.driver.find_elements(by=By.CSS_SELECTOR,
                                                                 value='select[ng-change="$ctrl.toggleEmploymentType()"]'):
                    try:
                        Select(employment_type).select_by_index(random.randrange(1, 5))
                    except exceptions.ElementClickInterceptedException:
                        self.md_toast_waiter()
                        try:
                            Select(employment_type).select_by_index(random.randrange(1, 5))
                        except exceptions.ElementClickInterceptedException:
                            header = self.driver.find_element(by=By.CSS_SELECTOR, value='st-header.new.ng-scope')
                            self.driver.execute_script("arguments[0].remove();", header)
                            Select(employment_type).select_by_index(random.randrange(1, 5))

                for employment_priority in self.driver.find_elements(by=By.CSS_SELECTOR,
                                                                     value='select[ng-model="$ctrl.employment.status"]'):
                    try:
                        Select(employment_priority).select_by_index(random.randrange(1, 3))
                    except exceptions.ElementClickInterceptedException:
                        self.md_toast_waiter()
                        try:
                            Select(employment_priority).select_by_index(random.randrange(1, 3))
                        except exceptions.ElementClickInterceptedException:
                            header = self.driver.find_element(by=By.CSS_SELECTOR, value='st-header.new.ng-scope')
                            self.driver.execute_script("arguments[0].remove();", header)
                            Select(employment_priority).select_by_index(random.randrange(1, 3))

                try:
                    employment_basis = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                                 value='select[ng-model="$ctrl.employment.basis"]')
                except exceptions.NoSuchElementException:
                    pass
                else:
                    for basis in employment_basis:
                        try:
                            num_basis_options = len(Select(basis).options)
                        except exceptions.ElementClickInterceptedException:
                            self.md_toast_waiter()
                            try:
                                num_basis_options = len(Select(basis).options)
                            except exceptions.ElementClickInterceptedException:
                                header = self.driver.find_element(by=By.CSS_SELECTOR, value='st-header.new.ng-scope')
                                self.driver.execute_script("arguments[0].remove();", header)
                                num_basis_options = len(Select(basis).options)

                        try:
                            Select(basis).select_by_index(random.randrange(1, num_basis_options))
                        except exceptions.ElementClickInterceptedException:
                            self.md_toast_waiter()
                            try:
                                Select(basis).select_by_index(random.randrange(1, num_basis_options))
                            except exceptions.ElementClickInterceptedException:
                                header = self.driver.find_element(by=By.CSS_SELECTOR, value='st-header.new.ng-scope')
                                self.driver.execute_script("arguments[0].remove();", header)
                                Select(basis).select_by_index(random.randrange(1, num_basis_options))

    def address_selector(self, input_el):
        self.address_repeat += 1
        input_el.send_keys(f'{random.randrange(0, 1000)} address')
        ul_el_id = 'ul-' + str(input_el.get_attribute('id')).split('-')[-1]
        try:
            WdWait(self.driver, 15).until(ec.visibility_of_element_located((By.ID, ul_el_id)))
        except exceptions.TimeoutException:
            print('No address returned after 15 seconds')
            if self.address_repeat > 4:
                print('No address list returned after 4 timeout attempts.')
            else:
                self.address_selector(input_el)
        else:
            li_els = self.driver.find_element(By.ID, ul_el_id).find_elements(by=By.CSS_SELECTOR,
                                                                             value='li span')

            if len(li_els) == 0:
                input_el.send_keys(Keys.CONTROL + 'a')
                sleep(0.1)
                input_el.send_keys(Keys.DELETE)
                sleep(0.2)
                if self.address_repeat > 4:
                    print('Address not returning after 4 attempts')
                else:
                    self.address_selector(input_el)
            else:
                self.driver.execute_script("arguments[0].click();", li_els[random.randrange(0, len(li_els))])

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
                            input_el.send_keys(self.random_string_create())
                        except:
                            traceback.print_stack()
                            traceback.print_exc()
                            continue

                    elif ng_model == '$mdAutocompleteCtrl.scope.searchText':
                        input_aria_label = input_el.get_attribute('aria-label')
                        if input_aria_label in self.address_placeholders:
                            self.address_selector(input_el)

                        elif input_aria_label == 'Employer ABN':
                            input_el.send_keys(str(random.randrange(10000000000, 100000000000)))

                        elif input_aria_label == 'Employer ACN':
                            input_el.send_keys(str(random.randrange(100000000, 1000000000)))

                        elif input_aria_label == 'ABS occupation code':
                            occupation = self.occupations[random.randrange(0, len(self.occupations) - 1)]
                            input_el.send_keys(occupation['value'] + ' ' + occupation['id'])

                        elif input_aria_label == 'ANZSCO industry code':
                            industry = self.industries[random.randrange(0, len(self.industries) - 1)]
                            input_el.send_keys(industry['value'] + ' ' + industry['id'])

                    elif ng_change == '$ctrl.saveAddress()':
                        continue

                    else:
                        try:
                            input_el.send_keys(self.random_string_create())
                        except exceptions.ElementNotInteractableException:
                            continue

        except exceptions.StaleElementReferenceException:
            pass

    def md_select_handler(self, content):
        for md_select in content.find_elements(by=By.TAG_NAME, value='md-select'):
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

    def textarea_handler(self, content):
        for textarea in content.find_elements(by=By.TAG_NAME, value='textarea'):
            try:
                textarea.send_keys(self.random_string_create())
            except exceptions.ElementNotInteractableException:
                continue

    def random_string_create(self):
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(10))
        return result_str

    def client_profile_input(self, deal_url):
        self.driver.get(deal_url)
        try:
            WdWait(self.driver, 20).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'st-sidebar-block button:nth-child(2)')))
        except exceptions.TimeoutException:
            WdWait(self.driver, 20).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'st-sidebar-block > div > button')))

        test = self.driver.find_elements(by=By.CSS_SELECTOR, value='st-sidebar-block button')
        test[-1].click()
        WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-contact')))
        contact_buttons = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                    value='st-sidebar-content > st-sidebar-block:first-of-type > div > button')

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

                self.textarea_handler(content)

        # self.driver.refresh()
        WdWait(self.driver, 20).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'form-content > form')))

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

                if current_separator in ['Asset to be financed', 'Lender and product', 'Compare products',
                                         'Security details', 'Funding worksheet', 'Maximum borrowing']:
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
                    income_buttons = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.mt0 button')
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
                    WdWait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'st-households')))
                    self.driver.find_element(by=By.CSS_SELECTOR, value='st-block-form-header > button').click()

                    household_picker = WdWait(self.driver, 10).until(ec.presence_of_element_located(
                        (By.CSS_SELECTOR, 'st-tabs-list-content > div > div > div > md-input-container > md-select')))
                    try:
                        household_picker.click()
                    except exceptions.ElementClickInterceptedException:
                        pass
                    household_picker_id = household_picker.get_attribute('id')
                    household_picker_container_id = str(int(household_picker_id.split("_")[-1]) + 1)
                    household_picker_container = WdWait(self.driver, 10).until(
                        ec.element_to_be_clickable((By.ID, "select_container_" + household_picker_container_id)))
                    household_members = household_picker_container.find_elements(by=By.CSS_SELECTOR, value='md-option')

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

                    liabilities = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.mt0 button')
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

                    self.textarea_handler(content)

                    self.md_radio_group(content)

                    self.checkbox_handler(content)

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    self.textarea_handler(content)

                elif separator == 'Product requirements':
                    self.textarea_handler(content)

                    self.select_el_handler(content)

                    self.md_radio_group(content)

                    self.checkbox_handler(content)

                    self.input_el_handler(content)

                    self.textarea_handler(content)

                elif separator == 'Insurance':
                    insurance = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.mt0 button')
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
                    other_advisers = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.mt0 button')
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

                    self.select_el_handler(content)

                    self.input_el_handler(content)

                elif separator == 'Analysis':

                    self.textarea_handler(content)

                    self.select_el_handler(content)

                    self.md_radio_group(content)

                    self.checkbox_handler(content)

                    self.input_el_handler(content)

                    self.textarea_handler(content)

                else:
                    self.select_el_handler(content)

                    self.input_el_handler(content)

                    self.md_select_handler(content)


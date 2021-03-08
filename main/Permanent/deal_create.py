import string

from main.Permanent import workflow_manipulation

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Chrome
from selenium.common import exceptions

from main.Permanent.helper_funcs import md_toast_remover, element_clicker

from time import sleep
from datetime import datetime
import json
import random
# import traceback
# from pathlib import Path
#


class EditDeal:
    def __init__(self, ent: str, driver: Chrome):
        with open("deal_config.json") as deal_config_json:
            deal_config = json.load(deal_config_json)

        self.users_in_workflow = ''
        self.driver = driver
        self.main_url = 'https://' + ent + '.salestrekker.com'
        self.ent = ent

        self.contacts = deal_config['contacts']
        self.deal_info = deal_config['deal_info']
        number_of_contacts = self.contacts['number_of_contacts']

        # in both cases decrease 1 as one contact already exists within a deal
        if number_of_contacts['random']:
            self.number_of_contacts = int(random.randrange(number_of_contacts['rand_val']['min'],
                                                           number_of_contacts['rand_val'][
                                                               'max'])) - 1
        else:
            self.number_of_contacts = int(number_of_contacts['value']) - 1

    def run(self, workflow: str = 'test', af_type: str = "cons",
            settlement_date: str = f'{datetime.now().strftime("%d/%m/%Y")}',
            deal_owner_name: str = '', add_all_team: bool = False):

        if workflow == 'test':
            self.driver.get(self.main_url)
            in_workflow = self.driver.current_url.split('/')[-1]
        else:
            in_workflow = workflow
        if not deal_owner_name:
            deal_owner_name = self.deal_info['deal_owner']

        if add_all_team:
            if users_in_workflow := workflow_manipulation.workflow_users(driver=self.driver,
                                                                         ent=self.ent,
                                                                         workflow_id=in_workflow):
                self.users_in_workflow = users_in_workflow
            else:
                workflow_manipulation.add_users_to_workflow(driver=self.driver,ent=self.ent,
                                                            workflow_id=in_workflow)

        self.driver.get(self.main_url + '/deal/edit/' + in_workflow + '/0')

        WdWait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'top')))

        # assert "Add New Ticket" in self.driver.title

        self._select_deal_owner(deal_owner_name)

        try:
            purpose_radio_group = WdWait(self.driver, 5).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, 'md-radio-group[ng-change="toggleCommercial()"]')))
        except exceptions.TimeoutException:
            pass
        else:
            if af_type == "comm":
                purpose_radio_group.find_element(by=By.CSS_SELECTOR,
                                                 value='md-radio-button[aria-label="Commercial"]').click()
            elif af_type == "cons":
                purpose_radio_group.find_element(by=By.CSS_SELECTOR,
                                                 value='md-radio-button[aria-label="Consumer"]').click()

        self._contact_add()
        self._contact_input()
        self._deal_info_input(settlement_date)

        # Save
        sleep(5)
        save_button = WdWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.save')))
        try:
            save_button.click()
        except exceptions.ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", save_button)

        try:
            WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
        except exceptions.TimeoutException:
            try:
                WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'form[name="ticketEdit"]')))
            except exceptions.TimeoutException:
                WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
            else:
                home_button = self.driver.find_element(by=By.CSS_SELECTOR,
                                                       value='md-toolbar > div > a.brand')
                try:
                    home_button.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", home_button)
                finally:
                    try:
                        WdWait(self.driver, 20).until(
                            ec.presence_of_element_located((By.TAG_NAME, 'ticket-content')))
                    except exceptions.TimeoutException:
                        pass

        finally:
            deal_url = self.driver.current_url

        return deal_url
        # self.client_profile_input()

    def _contact_add(self):

        incrementer = 0

        for contact in range(self.number_of_contacts):
            add_contact = WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR,
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

            if self.contacts['contact_types'] == 'mixed':

                # rand_val = random.randrange(0, 2)

                if incrementer < 2:

                    contact_type = contact_type_container.find_elements(by=By.TAG_NAME,
                                                                        value='button')
                    try:
                        contact_type[0].click()
                    except exceptions.ElementClickInterceptedException:
                        self.driver.execute_script('arguments[0].click();', contact_type[0])
                    incrementer += 1
                else:
                    contact_type = contact_type_container.find_elements(by=By.TAG_NAME,
                                                                        value='button')
                    try:
                        contact_type[1].click()
                    except exceptions.ElementClickInterceptedException:
                        self.driver.execute_script('arguments[0].click();', contact_type[1])

                    incrementer += 1

                    # type_of_cont = contact_type[rand_val].get_attribute('ng-click')
                    #
                    # if type_of_cont == 'contactAdd(false)':
                    #     self.current_export_array.append('Person ')
                    #
                    # if type_of_cont == 'contactAdd(true)':
                    #     self.current_export_array.append('Company ')

            elif self.contacts['contact_types'] == 'company':
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

            elif self.contacts['contact_types'] == 'person':
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
    def _contact_input(self):

        person_names = [['Misty', 'Banks'], ['Karl', 'Berg'], ['Tanisha', 'Obrien'],
                        ['Jasmin', 'Talley'],
                        ['Lexi-Mai', 'Mccray'], ['Chandni', 'Kramer'], ['Musab', 'Cunningham'],
                        ['Spike', 'Dunn'],
                        ['Doris', 'Vu'], ['Dominick', 'Ferry'], ['Rudi', 'Wolfe'],
                        ['Saira', 'Haas'],
                        ['Keeleigh', 'Bate'],
                        ['Nana', 'Tomlinson'], ['Andrew', 'Phelps'], ['Kirandeep', 'Goulding'],
                        ['Roland', 'Penn'],
                        ['Harry', 'Slater'], ['Alexie', 'Aguilar'], ['Adelaide', 'Mellor'],
                        ['Finbar', 'Bray'],
                        ['Nasir', 'Potter'], ['Patrycja', 'Metcalfe'], ['Nela', 'Burch'],
                        ['Belinda', 'Houston'],
                        ['Amaya', 'Brandt'], ['Husnain', 'Nixon'], ['Tiana', 'Allison'],
                        ['Wyatt', 'Stephens'],
                        ['Kenneth', 'Webster'], ['April', 'Lawrence'], ['Leia', 'Wright'],
                        ['Bushra', 'Knowles'],
                        ['Levi', 'Davidson'], ['Keira', 'Dalton'], ['Amin', 'Flower'],
                        ['Samiha', 'Cameron'],
                        ['Marianne', 'Baker'], ['Habib', 'Portillo'], ['Yousuf', 'Lord'],
                        ['Nicola', 'Goodman'],
                        ['Samanta', 'Roman'], ['Benedict', 'Wardle'], ['Nikhil', 'Hayden'],
                        ['Aurora', 'Bains'],
                        ['Giulia', 'Romero'], ['Rosa', 'Iles'], ['Alannah', 'Navarro'],
                        ['Marian', 'Malone'],
                        ['Dionne', 'Molina'], ['Xanthe', 'Macfarlane'], ['Anabel', 'Hilton'],
                        ['Samira', 'Mckay'],
                        ['Mason', 'Novak'], ['Colleen', 'Gaines'], ['Esther', 'Ratliff'],
                        ['Faheem', 'Valdez'],
                        ['Rachael', 'Zavala'], ['Kuba', 'Gibbons'], ['Callam', 'Almond'],
                        ['Nick', 'Bruce'],
                        ['Ayub', 'Felix'],
                        ['Esmay', 'Reeve'], ['Aimee', 'Chang'], ['Sarah', 'Patrick'],
                        ['Billy', 'Hutchings'],
                        ['Enid', 'Ayala'], ['Katie-Louise', 'Russell'], ['Ashlee', 'Burn'],
                        ['Tamar', 'Parra'],
                        ['Darla', 'Sharma'], ['Whitney', 'Emery'], ['Helena', 'Burris'],
                        ['Rachelle', 'Southern'],
                        ['Maisie', 'Mcleod'], ['Julia', 'Mckee'], ['Mandy', 'Duggan'],
                        ['Isaiah', 'William'],
                        ['Sally', 'Dalby'], ['Marianna', 'Carr'], ['Jasleen', 'Carty'],
                        ['Evie-Mae', 'Read'],
                        ['Lana', 'Marsh'], ['Kiana', 'Chase'], ['Preston', 'Greene'],
                        ['Rae', 'Stafford'],
                        ['Poppy-Rose', 'Greig'], ['Lyla', 'Woolley'], ['Christy', 'Bird'],
                        ['Maheen', 'Wyatt'],
                        ['Cordelia', 'Escobar'], ['Mariya', 'Bradley'], ['Amelia-Grace', 'Kirby'],
                        ['Kier', 'Whitney'],
                        ['Sonny', 'Cartwright'], ['Alessia', 'Sargent'], ['Inigo', 'Plummer'],
                        ['Hareem', 'Lucero'],
                        ['Caitlyn', 'Reynolds'], ['Ayana', 'Melia'], ['Danielle', 'Davenport'],
                        ['Charlotte', 'Irving'],
                        ['Bronwyn', 'Barrow'], ['Eliot', 'Senior'], ['Lesley', 'Mcgowan'],
                        ['Ada', 'Hancock'],
                        ['Azra', 'Povey'], ['Wilbur', 'Mcmanus'], ['Lillian', 'Tyson'],
                        ['Yannis', 'Hunt'],
                        ['Sherri', 'Betts'], ['Cosmo', 'Lopez'], ['Nella', 'Molloy'],
                        ['Hasan', 'Plant'],
                        ['Tyrique', 'Kirk'],
                        ['Jonah', 'Cantu'], ['Lexi-Mae', 'Reid'], ['Nigel', 'Whelan'],
                        ['Zavier', 'Dupont'],
                        ['Bevan', 'Berry'], ['Leo', 'Mueller'], ['Israel', 'Lowery'],
                        ['Sharna', 'Powell'],
                        ['Jagoda', 'Porter'], ['Deborah', 'Krueger'], ['Claire', 'Griffiths'],
                        ['Anabelle', 'Garrett'],
                        ['Kobie', 'Barrett'], ['Nabeel', 'Gibbs'], ['Kayley', 'Calvert'],
                        ['Zahrah', 'Hills'],
                        ['Beck', 'Rice'], ['Kingsley', 'Correa'], ['Micah', 'Pineda'],
                        ['Jerry', 'Beasley'],
                        ['Haydn', 'Sanderson'], ['Robyn', 'Frye'], ['Carwyn', 'Garrison'],
                        ['Rhys', 'Trevino'],
                        ['Seamus', 'Stafford'], ['Maia', 'Rankin'], ['Iman', 'Huerta'],
                        ['Rahul', 'Luna'],
                        ['Judy', 'Mustafa'],
                        ['Arwa', 'Lane'], ['Jeevan', 'Russo'], ['Francesco', 'Richmond'],
                        ['Shyam', 'Ferry'],
                        ['Amal', 'Wolfe'], ['Gabrielle', 'Schmidt'], ['Kellie', 'Mcnally'],
                        ['Derry', 'Power'],
                        ['Quentin', 'Castaneda'], ['Hashir', 'Wickens'], ['Alma', 'Romero'],
                        ['Rheanna', 'Smyth'],
                        ['Sebastian', 'Coulson'], ['Sahara', 'Riley'], ['Miriam', 'Carty'],
                        ['Debbie', 'Hogan'],
                        ['Niyah', 'Bonilla'], ['Lillie-May', 'Mcgee'], ['Petra', 'Buck'],
                        ['Khalil', 'Mccoy'],
                        ['Lena', 'Schneider'], ['Isabell', 'Gordon'], ['Howard', 'Hardy'],
                        ['Lennie', 'Ferreira'],
                        ['Jibril', 'Jarvis'], ['Christiana', 'Haley'], ['Alan', 'Bray'],
                        ['Kimora', 'Barnett'],
                        ['Muneeb', 'Finch'], ['Iqrah', 'Cox'], ['Hanna', 'Lawrence'],
                        ['Akbar', 'Leech'],
                        ['Beverly', 'Bain'],
                        ['Jill', 'Cross'], ['Shania', 'Hyde'], ['T-Jay', 'Soto'],
                        ['George', 'Bates'],
                        ['Lexie', 'Knowles'],
                        ['Gerard', 'Douglas'], ['Weronika', 'Roberts'], ['Alison', 'Cornish'],
                        ['Reon', 'Robles'],
                        ['Piotr', 'Macgregor'], ['Alya', 'Hines'], ['Mitchel', 'Oakley'],
                        ['Sally', 'Santos'],
                        ['Alfie-Lee', 'Kirkpatrick'], ['Abbie', 'Alvarez'], ['Pola', 'Piper'],
                        ['Laylah', 'Murphy'],
                        ['Zubair', 'Boyd'], ['Ali', 'Haas'], ['Nicole', 'Corbett'],
                        ['Lorna', 'Short'],
                        ['Ember', 'Alexander'],
                        ['Cora', 'Sloan']]

        company_names = ['Indeed Entity', 'Finally Entity', 'Seem Entity', 'They Entity',
                         'Reallysatisfied Entity',
                         'Rethoughtbut Entity', 'Fantasticbut Entity', 'Vastbut Entity',
                         'Saferbut Entity',
                         'Addbut Entity', 'Butanywhere Entity', 'Ensuredbut Entity',
                         'Characterbut Entity',
                         'Then&Seem Entity', 'Only&Like Entity', 'Upstartbut Entity',
                         'Butworks Entity',
                         'Believebut Entity', 'Barely&Would Entity', 'Know&Although Entity',
                         'Butcollate Entity',
                         'Mostbut Entity', 'Butaiming Entity', 'Mean&Roundly Entity',
                         'Make&Werent Entity',
                         'Unlikelyally Entity', 'Soon Entity', 'Admitly Entity',
                         'Expectably Entity', 'Sureably Entity',
                         'Butorignal Entity', 'Thinkbut Entity', 'Sillybut Entity',
                         'Butunable Entity',
                         'Commentbut Entity', 'Lose&Entirely Entity', 'Butrewards Entity',
                         'Butalternate Entity',
                         'Afraid&Vastly Entity', 'Recoversbut Entity', 'Believe&Thus Entity',
                         'Butnever Entity',
                         'Believe&⡌ Entity', 'Darned&Only Entity', 'Avail&Any Entity',
                         'Sunnierbut Entity',
                         'Butabsolute Entity', 'Afaict&Hoping Entity', 'Buttheory Entity',
                         'Blastingbut Entity',
                         'Tellingly Entity', 'Knew.Me Entity', 'Everythiing Entity',
                         'Definitely Entity',
                         'Definitelyright Entity', 'Butcase Entity', 'Petered&Now Entity',
                         'Extent&Wouldn Entity',
                         'Ignored&They Entity', 'Going&Seldom Entity', 'Couldn&Remain Entity',
                         'Mightn&Singly Entity',
                         'Hint&Avail Entity', 'Him&Didn Entity', 'Does&Inclined Entity',
                         'Butbit Entity',
                         'Explaining&It Entity', 'Butprimary Entity', 'Butscape Entity',
                         'Unable&Which Entity',
                         'Almost&Weren Entity', 'Butweblinks Entity', 'Easily&Apart Entity',
                         'Thinking&To Entity',
                         'Butfox Entity', 'Debatably Entity', 'Muchsooner Entity',
                         'Reallysure Entity',
                         'Besides.Io Entity', 'Phairly Entity', 'Quickbut Entity', 'Wellbut Entity',
                         'Outbut Entity',
                         'Often&Nobody Entity', 'Be&Darned Entity', 'Butgigantic Entity',
                         'Savedbut Entity',
                         'Linkedbut Entity', 'Butprefer Entity', 'Amazinglybut Entity',
                         'Weren&Feels Entity',
                         'Chosebut Entity', 'Butmost Entity', 'Butkicking Entity',
                         'Calmnessbut Entity',
                         'Powerfullbut Entity', 'Astutebut Entity', 'Sensiblebut Entity',
                         'Imho&Worried Entity',
                         'Butfalsehood Entity', 'Believingg Entity', 'Thenly Entity',
                         'Entire Entity',
                         'Extremelysatisfied Entity', 'Wrong.Io Entity', 'When&Proves Entity',
                         'Helpfulbut Entity',
                         'Seldom&Nope Entity', 'Butquoting Entity', 'Unawares&To Entity',
                         'Then&Often Entity',
                         'Honestly&Once Entity', 'Butweek Entity', 'Idea&Badly Entity',
                         'Wishbut Entity',
                         'Butmessage Entity', 'Insofar&Didn Entity', 'Butpiping Entity',
                         'Happen&Which Entity',
                         'Entirebut Entity', 'Geniusbut Entity', 'Thebut Entity',
                         'The&Vaguely Entity',
                         'Butgirl Entity', 'Butactuality Entity', 'Doingly Entity',
                         'Reliantly Entity',
                         'Unreally Entity', 'Anymore.Io Entity', 'Chargefully Entity',
                         'We&Vainly Entity',
                         'Releasingbut Entity', 'Well&Seeing Entity', 'Recoversbut Entity',
                         'Butaction Entity',
                         'Usually&Again Entity', 'Where&Frankly Entity', 'Would&Barely Entity',
                         'Redapplebut Entity',
                         'Longer&When Entity', 'Isn&Hesitant Entity', 'Butnames Entity',
                         'Forbut Entity',
                         'Buteye Entity', 'Retainbut Entity', 'Butoptimal Entity',
                         'Faltering&Any Entity',
                         'Wholebut Entity', 'Able&Bothers Entity', 'Cannot&There Entity',
                         'Wherever.Io Entity',
                         'Willing.Io Entity', 'Lookfully Entity', 'Cannotmiss Entity',
                         'Telling Entity',
                         'Butproduct Entity', 'Butstandard Entity', 'Moreover&Soon Entity',
                         'Buttrusting Entity',
                         'Butsuppose Entity', 'Knightlybut Entity', 'Confidentbut Entity',
                         'Butopening Entity',
                         'Approachbut Entity', 'Unnoticed&Btw Entity', 'Butanswering Entity',
                         'Butguys Entity',
                         'Butfavored Entity', 'Letting&Soon Entity', 'Butspeed Entity',
                         'Butstill Entity',
                         'Excitesbut Entity', 'Aware&These Entity', 'Slicingbut Entity',
                         'Butvitally Entity',
                         'Anythiing Entity', 'Veryquietly Entity', 'Unfortunate Entity',
                         'Potfully Entity',
                         'Dashfully Entity', 'These&Concede Entity', 'Butmay Entity',
                         'What&Contend Entity',
                         'Itself&Thinks Entity', 'Butomatic Entity', 'Butalso Entity',
                         'Rest&•• Entity',
                         'Butmachine Entity', 'Butbalanced Entity', 'Butaddicts Entity',
                         'Smootherbut Entity',
                         'Safebut Entity', '&&Bother Entity', 'Butcompare Entity',
                         'Awful&Hence Entity',
                         'Ensuredbut Entity', 'Valuablebut Entity', 'Butrepairing Entity',
                         'Butback Entity',
                         'Curiously&We Entity']

        person_list = []
        company_list = []
        try:
            WdWait(self.driver, 6).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.mt0 > div > div:nth-child(1) input')))
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
                                    value='div:nth-child(2) > div:nth-child(1) > md-autocomplete > '
                                          'md-autocomplete-wrap > md-input-container >input').send_keys(
                    person_name[0])
                person.find_element(by=By.CSS_SELECTOR,
                                    value='div:nth-child(2) > div:nth-child(2) > md-input-container > input').send_keys(
                    person_name[1])
                num_prefix = person.find_element(by=By.CSS_SELECTOR,
                                                 value='div:nth-child(2) > div:nth-child(3) > '
                                                       'md-input-container:nth-child(1) > input')
                num_prefix.send_keys(Keys.CONTROL + 'a')
                num_prefix.send_keys('61')
                person.find_element(by=By.CSS_SELECTOR,
                                    value='div:nth-child(2) > div:nth-child(3) > md-input-container:nth-child(2) > '
                                          'input').send_keys("".join(random.sample(string.digits, 9)))
                person.find_element(by=By.CSS_SELECTOR,
                                    value='div:nth-child(2) > div:nth-child(4) > md-input-container > input').send_keys(
                    f'{person_name[0].lower()}@website.com')
                current_sel = person.find_element(by=By.CSS_SELECTOR,
                                                  value='div:nth-child(2) > div:nth-child(4) > '
                                                        'st-form-field-container > select')

                # try:
                #     Select(current_sel).select_by_value(contact_type)
                # except exceptions.ElementClickInterceptedException:
                #     md_toast_waiter(self.driver)
                #     try:
                #         Select(current_sel).select_by_value(contact_type)
                #     except exceptions.ElementClickInterceptedException:
                #         self.driver.find_element(by=By.TAG_NAME, value='md-backdrop').click()

                if self.contacts['non_client']['active']:
                    if count < int(self.contacts['non_client']['no_of_clients']):
                        try:
                            Select(current_sel).select_by_index(random.randrange(0, 4))
                        except exceptions.ElementClickInterceptedException:
                            md_toast_remover(self.driver)
                            Select(current_sel).select_by_index(random.randrange(0, 4))
                    else:
                        try:
                            Select(current_sel).select_by_index(
                                random.randrange(0, len(Select(current_sel).options)))
                        except exceptions.ElementClickInterceptedException:
                            md_toast_remover(self.driver)
                            Select(current_sel).select_by_index(
                                random.randrange(0, len(Select(current_sel).options)))
                else:
                    try:
                        Select(current_sel).select_by_index(random.randrange(0, 4))
                    except exceptions.ElementClickInterceptedException:
                        md_toast_remover(self.driver)
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
                    "".join(random.sample(string.digits, 9)))
                company.find_element(by=By.CSS_SELECTOR,
                                     value='div:nth-child(2) > div:nth-child(3) input').send_keys(
                    'email@company.real')
                current_sel = company.find_element(by=By.CSS_SELECTOR,
                                                   value='div > div:nth-child(3) > st-form-field-container > select')

                # try:
                #     Select(current_sel).select_by_value(contact_type)
                # except exceptions.ElementClickInterceptedException:
                #     md_toast_waiter(self.driver)
                #     try:
                #         Select(current_sel).select_by_value(contact_type)
                #     except exceptions.ElementClickInterceptedException:
                #         self.driver.find_element(by=By.TAG_NAME, value='md-backdrop').click()

                if self.contacts['non_client']['active']:
                    if count < int(self.contacts['non_client']['no_of_clients']):
                        try:
                            Select(current_sel).select_by_index(random.randrange(0, 4))
                        except exceptions.ElementClickInterceptedException:
                            md_toast_remover(self.driver)
                            Select(current_sel).select_by_index(random.randrange(0, 4))
                    else:
                        try:
                            Select(current_sel).select_by_index(
                                random.randrange(0, len(Select(current_sel).options)))
                        except exceptions.ElementClickInterceptedException:
                            md_toast_remover(self.driver)
                            Select(current_sel).select_by_index(
                                random.randrange(0, len(Select(current_sel).options)))
                else:
                    try:
                        Select(current_sel).select_by_index(random.randrange(0, 4))
                    except exceptions.ElementClickInterceptedException:
                        md_toast_remover(self.driver)
                        Select(current_sel).select_by_index(random.randrange(0, 4))

    def _deal_info_input(self, date: str):

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
        if self.deal_info['random']:
            stage_num = random.randrange(0, len(stages))
        else:
            stage_num = int(self.deal_info['stage_num']) - 1
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
                (By.CSS_SELECTOR, 'div:nth-child(5) > md-input-container > input'),
                '$' + f'{deal_value:,}'))
        except exceptions.TimeoutException:
            print('erroooor')
            deal_value_input.send_keys(Keys.CONTROL + 'a')
            deal_value_input.send_keys(f'{deal_value}')

        # Estimated settlement date
        estimated_settlement_date_input = main_info_block.find_element(by=By.CSS_SELECTOR,
                                                                       value='md-datepicker[ng-model="getSetOnceOffDueDate"] > div > input')
        estimated_settlement_date_input.send_keys(Keys.CONTROL + 'a')
        estimated_settlement_date_input.send_keys(f'{date}')
        try:
            WdWait(self.driver, 5).until(ec.text_to_be_present_in_element_value(
                (By.CSS_SELECTOR,
                 'div:nth-child(6) > md-input-container > md-datepicker > div > input'),
                f'{date}'))
        except exceptions.TimeoutException:
            estimated_settlement_date_input.send_keys(Keys.CONTROL + 'a')
            estimated_settlement_date_input.send_keys(f'{date}')

        # Summary notes
        summary_notes = 'Summary Notes-u'
        main_info_block.find_element(by=By.CSS_SELECTOR,
                                     value='div > md-input-container > div > textarea').send_keys(
            f'{summary_notes}')

    def _select_deal_owner(self, deal_owner_name: str):

        main_info_block = WdWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'st-block > st-block-form-content > div.layout-wrap')))

        # Deal Owner
        deal_owner_select_element = main_info_block.find_element(by=By.CSS_SELECTOR,
                                                                 value='div:nth-child(2) > md-input-container > md-select')

        element_clicker(driver=self.driver, web_element=deal_owner_select_element)

        deal_owner_select_id = str(deal_owner_select_element.get_attribute('id'))
        deal_owner_id = str(int(deal_owner_select_id.split("_")[-1]) + 1)
        try:
            WdWait(self.driver, 10).until(
                ec.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div#select_container_" + deal_owner_id)))
        except exceptions.TimeoutException:
            pass

        try:
            self.driver.find_element(by=By.XPATH, value=f"//md-option/div/span[contains(text(), '{deal_owner_name}')]").click()
        except Exception:
            print('looping')
            deal_owners = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                    value="div#select_container_" + deal_owner_id + " > md-select-menu > md-content > md-option > div > span")

            # TODO Rewrite to do a javascript search instead of a for loop
            for deal_owner in deal_owners:
                sleep(0.1)
                if deal_owner.text == deal_owner_name:
                    element_clicker(self.driver, deal_owner)
                    break
            else:
                element_clicker(self.driver, deal_owners[0])


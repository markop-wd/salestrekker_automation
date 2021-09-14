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

from main.Permanent.helper_funcs import md_toast_remover, element_clicker, phone_num_gen, selector
from main.Permanent.deal_create_selectors import *


class CreateDeal:
    def __init__(self, ent: str, driver: Chrome, config: dict = None, deal_name: str = ''):
        if deal_name:
            self.deal_name = deal_name
        else:
            self.deal_name = f'Test {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

        if config is None:
            deal_config = Path(__file__).parent.resolve() / "../deal_config.json"
            with open(deal_config) as deal_config_json:
                deal_config = json.load(deal_config_json)
        else:
            deal_config = config

        self.users_in_workflow = ''
        self.driver = driver
        self.main_url = 'https://' + ent + '.salestrekker.com'
        self.ent = ent

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

    def run(self, workflow: str = 'test', af_type: str = "cons", deal_owner_name: str = '', client_email: str = ""):
        """
        This is the main logic for the deal creation, this one calls the 'private' functions
        Also it makes sure we are at the correct place and the correct time when not filling in input fields
        """

        if workflow == 'test':
            self.driver.get(self.main_url)
            in_workflow = self.driver.current_url.split('/')[-1]
        else:
            in_workflow = workflow.split('/')[-1]

        if not deal_owner_name:
            # TODO - maybe take the current user as the default deal owner rather than going by the config
            deal_owner_name = self.deal_info['deal_owner']

        # TODO - Review this little snippet as it might not be needed at all and can only be left in the off case
        # if add_all_team:
        #     if users_in_workflow := workflow_manipulation.workflow_users(driver=self.driver,
        #                                                                  ent=self.ent,
        #                                                                  workflow_id=in_workflow):
        #         self.users_in_workflow = users_in_workflow
        #     else:
        #         workflow_manipulation.add_users_to_workflow(driver=self.driver, ent=self.ent,
        #                                                     workflow_id=in_workflow)

        self.driver.get(self.main_url + '/deal/edit/' + in_workflow + '/0')

        try:
            WdWait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'top')))
        except exceptions.TimeoutException:
            try:
                WdWait(self.driver, 30).until(ec.presence_of_element_located((By.ID, 'top')))
            except exceptions.TimeoutException:
                self.driver.refresh()
                WdWait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'top')))

        # assert "Add New Ticket" in self.driver.title

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
                comm_button = purpose_radio_group.find_element(by=eval(COMMERCIAL_PURPOSE['by']),
                                                               value=COMMERCIAL_PURPOSE['value'])
                element_clicker(self.driver, web_element=comm_button)
            elif af_type == "cons":
                cons_button = purpose_radio_group.find_element(by=eval(CONSUMER_PURPOSE['by']),
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
            for el in order.split(','):
                element_clicker(self.driver, web_element=add_contact)

                add_contact_container_id = add_contact.get_attribute('aria-owns')
                contact_type_container = WdWait(self.driver, 5).until(
                    ec.presence_of_element_located((By.ID, add_contact_container_id)))
                contact_type = contact_type_container.find_elements(by=By.TAG_NAME,
                                                                    value='button')
                if el == 'pers':
                    element_clicker(self.driver, web_element=contact_type[0])
                elif el == 'comp':
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

    # TODO - Get a better way to pass in names
    def _contact_input(self, client_email):

        first_names = ['Misty', 'Karl', 'Tanisha', 'Jasmin', 'Lexi-Mai', 'Chandni', 'Musab', 'Spike', 'Doris',
                       'Dominick', 'Rudi',
                       'Saira', 'Keeleigh', 'Nana', 'Andrew', 'Kirandeep', 'Roland', 'Harry', 'Alexie', 'Adelaide',
                       'Finbar', 'Nasir',
                       'Patrycja', 'Nela', 'Belinda', 'Amaya', 'Husnain', 'Tiana', 'Wyatt', 'Kenneth', 'April', 'Leia',
                       'Bushra',
                       'Levi', 'Keira', 'Amin', 'Samiha', 'Marianne', 'Habib', 'Yousuf', 'Nicola', 'Samanta',
                       'Benedict', 'Nikhil',
                       'Aurora', 'Giulia', 'Rosa', 'Alannah', 'Marian', 'Dionne', 'Xanthe', 'Anabel', 'Samira', 'Mason',
                       'Colleen',
                       'Esther', 'Faheem', 'Rachael', 'Kuba', 'Callam', 'Nick', 'Ayub', 'Esmay', 'Aimee', 'Sarah',
                       'Billy', 'Enid',
                       'Katie-Louise', 'Ashlee', 'Tamar', 'Darla', 'Whitney', 'Helena', 'Rachelle', 'Maisie', 'Julia',
                       'Mandy',
                       'Isaiah', 'Sally', 'Marianna', 'Jasleen', 'Evie-Mae', 'Lana', 'Kiana', 'Preston', 'Rae',
                       'Poppy-Rose', 'Lyla',
                       'Christy', 'Maheen', 'Cordelia', 'Mariya', 'Amelia-Grace', 'Kier', 'Sonny', 'Alessia', 'Inigo',
                       'Hareem',
                       'Caitlyn', 'Ayana', 'Danielle', 'Charlotte', 'Bronwyn', 'Eliot', 'Lesley', 'Ada', 'Azra',
                       'Wilbur', 'Lillian',
                       'Yannis', 'Sherri', 'Cosmo', 'Nella', 'Hasan', 'Tyrique', 'Jonah', 'Lexi-Mae', 'Nigel', 'Zavier',
                       'Bevan',
                       'Leo', 'Israel', 'Sharna', 'Jagoda', 'Deborah', 'Claire', 'Anabelle', 'Kobie', 'Nabeel',
                       'Kayley', 'Zahrah',
                       'Beck', 'Kingsley', 'Micah', 'Jerry', 'Haydn', 'Robyn', 'Carwyn', 'Rhys', 'Seamus', 'Maia',
                       'Iman', 'Rahul',
                       'Judy', 'Arwa', 'Jeevan', 'Francesco', 'Shyam', 'Amal', 'Gabrielle', 'Kellie', 'Derry',
                       'Quentin', 'Hashir',
                       'Alma', 'Rheanna', 'Sebastian', 'Sahara', 'Miriam', 'Debbie', 'Niyah', 'Lillie-May', 'Petra',
                       'Khalil', 'Lena',
                       'Isabell', 'Howard', 'Lennie', 'Jibril', 'Christiana', 'Alan', 'Kimora', 'Muneeb', 'Iqrah',
                       'Hanna', 'Akbar',
                       'Beverly', 'Jill', 'Shania', 'T-Jay', 'George', 'Lexie', 'Gerard', 'Weronika', 'Alison', 'Reon',
                       'Piotr',
                       'Alya', 'Mitchel', 'Sally', 'Alfie-Lee', 'Abbie', 'Pola', 'Laylah', 'Zubair', 'Ali', 'Nicole',
                       'Lorna',
                       'Ember', 'Cora']

        surnames = ['Banks', 'Berg', 'Obrien', 'Talley', 'Mccray', 'Kramer', 'Cunningham', 'Dunn', 'Vu', 'Ferry',
                    'Wolfe', 'Haas', 'Bate', 'Tomlinson', 'Phelps', 'Goulding', 'Penn', 'Slater', 'Aguilar', 'Mellor',
                    'Bray', 'Potter', 'Metcalfe', 'Burch', 'Houston', 'Brandt', 'Nixon', 'Allison', 'Stephens',
                    'Webster', 'Lawrence', 'Wright', 'Knowles', 'Davidson', 'Dalton', 'Flower', 'Cameron', 'Baker',
                    'Portillo', 'Lord', 'Goodman', 'Roman', 'Wardle', 'Hayden', 'Bains', 'Romero', 'Iles', 'Navarro',
                    'Malone', 'Molina', 'Macfarlane', 'Hilton', 'Mckay', 'Novak', 'Gaines', 'Ratliff', 'Valdez',
                    'Zavala', 'Gibbons', 'Almond', 'Bruce', 'Felix', 'Reeve', 'Chang', 'Patrick', 'Hutchings', 'Ayala',
                    'Russell', 'Burn', 'Parra', 'Sharma', 'Emery', 'Burris', 'Southern', 'Mcleod', 'Mckee', 'Duggan',
                    'William', 'Dalby', 'Carr', 'Carty', 'Read', 'Marsh', 'Chase', 'Greene', 'Stafford', 'Greig',
                    'Woolley', 'Bird', 'Wyatt', 'Escobar', 'Bradley', 'Kirby', 'Whitney', 'Cartwright', 'Sargent',
                    'Plummer', 'Lucero', 'Reynolds', 'Melia', 'Davenport', 'Irving', 'Barrow', 'Senior', 'Mcgowan',
                    'Hancock', 'Povey', 'Mcmanus', 'Tyson', 'Hunt', 'Betts', 'Lopez', 'Molloy', 'Plant', 'Kirk',
                    'Cantu', 'Reid', 'Whelan', 'Dupont', 'Berry', 'Mueller', 'Lowery', 'Powell', 'Porter', 'Krueger',
                    'Griffiths', 'Garrett', 'Barrett', 'Gibbs', 'Calvert', 'Hills', 'Rice', 'Correa', 'Pineda',
                    'Beasley', 'Sanderson', 'Frye', 'Garrison', 'Trevino', 'Stafford', 'Rankin', 'Huerta', 'Luna',
                    'Mustafa', 'Lane', 'Russo', 'Richmond', 'Ferry', 'Wolfe', 'Schmidt', 'Mcnally', 'Power',
                    'Castaneda', 'Wickens', 'Romero', 'Smyth', 'Coulson', 'Riley', 'Carty', 'Hogan', 'Bonilla', 'Mcgee',
                    'Buck', 'Mccoy', 'Schneider', 'Gordon', 'Hardy', 'Ferreira', 'Jarvis', 'Haley', 'Bray', 'Barnett',
                    'Finch', 'Cox', 'Lawrence', 'Leech', 'Bain', 'Cross', 'Hyde', 'Soto', 'Bates', 'Knowles', 'Douglas',
                    'Roberts', 'Cornish', 'Robles', 'Macgregor', 'Hines', 'Oakley', 'Santos', 'Kirkpatrick', 'Alvarez',
                    'Piper', 'Murphy', 'Boyd', 'Haas', 'Corbett', 'Short', 'Alexander', 'Sloan']

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
        new_month = (today.month + 2) % 12
        settlement_date = today.replace(month=new_month).strftime("%d/%m/%Y")

        settlement_date_input = main_info_block.find_element(by=eval(SETTLEMENT_DATE['by']),
                                                             value=SETTLEMENT_DATE['value'])
        settlement_date_input.send_keys(Keys.CONTROL + 'a')
        settlement_date_input.send_keys(settlement_date)

        # TODO - I like this pattern, maybe it should move the helper_funcs and re-use it for text inputs where feasible
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
        deal_owner_select_element = main_info_block.find_element(by=eval(DEAL_OWNER_MD['by']),
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
                # If we are still in deal creation page, there is an overlay that needs to be clicked in order to save
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

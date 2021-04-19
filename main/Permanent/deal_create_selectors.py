# Run
LOAN_PURPOSE = {'by': 'By.CSS_SELECTOR', 'value': 'md-radio-group[ng-change="toggleCommercial()"]'}
COMMERCIAL_PURPOSE = {'by': 'By.CSS_SELECTOR', 'value': 'md-radio-button[aria-label="Commercial"]'}
CONSUMER_PURPOSE = {'by': 'By.CSS_SELECTOR', 'value': 'md-radio-button[aria-label="Consumer"]'}

# Deal Information Block
MAIN_INFO_BLOCK = {'by': 'By.CSS_SELECTOR', 'value': 'st-block > st-block-form-content > div.layout-wrap'}
DEAL_NAME = {'by': 'By.CSS_SELECTOR', 'value': 'div:nth-child(1) > md-input-container > input'}
STAGE_SELECT = {'by': 'By.CSS_SELECTOR', 'value': 'div:nth-child(4) > md-input-container > md-select'}
DEAL_VALUE = {'by': 'By.CSS_SELECTOR', 'value': 'div:nth-child(5) > md-input-container > input'}
SETTLEMENT_DATE = {'by': 'By.CSS_SELECTOR', 'value': 'md-datepicker[ng-model="getSetOnceOffDueDate"] > div > input'}
SUMMARY_NOTES = {'by': 'By.CSS_SELECTOR', 'value': 'div > md-input-container > div > textarea'}

# Contact Add
ADD_CONTACT = {'by': 'By.CSS_SELECTOR', 'value': 'st-block-form-header > md-menu > button'}

# Contact input
FIRST_CLIENT_INPUT = {'by': 'By.CSS_SELECTOR', 'value': 'div.mt0 > div > div:nth-child(1) input'}
CONTACTS = {'by': 'By.CSS_SELECTOR', 'value': 'div.mt0'}
PHONE_NUM = {'by': 'By.CSS_SELECTOR', 'value': 'div > md-input-container:nth-child(2) > input'}
CLIENT_TYPE = {'by': 'By.CSS_SELECTOR', 'value': 'st-form-field-container > select'}
PERSON_NAME = {'by': 'By.CSS_SELECTOR', 'value': 'md-autocomplete-wrap > md-input-container > input'}
PERSON_SURNAME = {'by': 'By.CSS_SELECTOR', 'value': 'div:nth-child(2) > div:nth-child(2) > md-input-container > input'}
PERSON_NUM_PREFIX = {'by': 'By.CSS_SELECTOR', 'value': 'div:nth-child(3) > md-input-container:nth-child(1) > input'}
PERSON_EMAIL = {'by': 'By.CSS_SELECTOR', 'value': 'div:nth-child(2) > div:nth-child(4) > md-input-container > input'}
COMPANY_NAME = {'by': 'By.CSS_SELECTOR', 'value': 'md-autocomplete-wrap > md-input-container > input'}
COMPANY_NUM_PREFIX = {'by': 'By.CSS_SELECTOR', 'value': 'div:nth-child(2) > md-input-container:nth-child(1) > input'}
COMPANY_EMAIL = {'by': 'By.CSS_SELECTOR', 'value': 'div > div:nth-child(3) input'}

# Select deal owner
DEAL_OWNER_MD = {'by': 'By.CSS_SELECTOR', 'value': 'div:nth-child(2) > md-input-container > md-select'}
DEAL_OWNER_LIST = {'by': 'By.CSS_SELECTOR', 'value': 'md-option > div > span'}
CONTACT_LABEL = {'by': 'By.CSS_SELECTOR', 'value': 'md-autocomplete-wrap > md-input-container > label'}

# Save
SAVE_BUTTON = {'by': 'By.CSS_SELECTOR', 'value': 'button.save'}
TICKET_CONTENT = {'by': 'By.TAG_NAME', 'value': 'ticket-content'}
TICKET_EDIT = {'by': 'By.CSS_SELECTOR', 'value': 'form[name="ticketEdit"]'}
HOME_BUTTON = {'by': 'By.CSS_SELECTOR', 'value': 'md-toolbar > div > a.brand'}

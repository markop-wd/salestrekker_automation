"""
When something out of the ordinary has to be done
Instead of programming in the main business logic just implement it here and import it there
"""
import random
import string
import threading
import traceback
from datetime import date, timedelta
from time import sleep

from selenium.common import exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as WdWait


def random_string_create(char_nums: int = 10, chars: bool = True):
    if chars:
        result_str = ''.join(random.choice(string.ascii_letters) for _ in range(char_nums))
        return result_str
    else:
        result_str = ''.join(random.choice(string.digits) for _ in range(char_nums))
        return result_str

# TODO
def accreditation_fill(driver: Chrome, ent: str, all_new: bool = True):
    if driver.current_url != f"https://{ent}.salestrekker.com/settings/my-accreditations":
        driver.get(f"https://{ent}.salestrekker.com/settings/my-accreditations")
    WdWait(driver, 50).until(
        ec.visibility_of_element_located((By.TAG_NAME, 'st-block-form-content')))

    if all_new:
        try:
            for delete_button in driver.find_elements(by=By.CSS_SELECTOR, value='button.delete'):
                try:
                    driver.execute_script("arguments[0].click();", delete_button)
                except exceptions.ElementClickInterceptedException:
                    element_clicker(driver=driver, web_element=delete_button)
                    # driver.execute_script("arguments[0].click();", delete_button)
        except exceptions.NoSuchElementException:
            pass

        add_new = driver.find_element(by=By.CSS_SELECTOR,
                                      value='button[aria-label="Add new lender accreditation"]')
        element_clicker(driver=driver, web_element=add_new)
        # # md_select = driver.find_element(by=By.CSS_SELECTOR, value='md-select[ng-change="pickLender('
        # #                                                           'lenderAccreditation)"]')
        # # element_clicker(driver=driver, web_element=md_select)
        # md_select_id = str(md_select.get_attribute('id'))
        # md_select_container_id = str(int(md_select_id.split("_")[-1]) + 1)

        # all_lenders = driver.find_elements(by=By.CSS_SELECTOR,
        #                                    value=f'#select_container_{md_select_container_id} md-option')
        #
        # element_clicker(driver=driver, web_element=all_lenders[0])
        #
        # number_lenders = range(len(all_lenders) - 1)
        #
        # print(number_lenders)

        # for _ in number_lenders:
        #     driver.execute_script("arguments[0].click();", add_new)

        broker_ids = driver.find_elements(by=By.CSS_SELECTOR,
                                          value='input[ng-model="lenderAccreditation.brokerIdPrimary"]')

        # TODO TODO TODO TODO TODO TODO
        def id_input(input_list: list):

            for broker_id in input_list:
                broker_id.send_keys('1234')

        def chunks(split_list, parts):
            """ Yield n successive chunks from l.
            """
            newn = int(len(split_list) / parts)
            for i in range(0, parts - 1):
                yield split_list[i * newn:i * newn + newn]
            yield split_list[parts * newn - newn:]

        chunky = chunks(broker_ids, 4)
        threads = list()
        for i in chunky:
            x = threading.Thread(target=id_input, args=(i,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

        threading.Thread(target=id_input, args=())
        # TODO TODO TODO TODO TODO TODO

        # all_bre = driver.find_elements(by=By.CSS_SELECTOR,
        #                                value='md-select[ng-change="pickLender(lenderAccreditation)"]')
        #
        # for count, element in enumerate(all_bre):
        #     # driver.execute_script("arguments[0].click();", element)
        #     element_clicker(driver=driver, web_element=element)
        #     md_select_id = str(element.get_attribute('id'))
        #     md_select_container_id = str(int(md_select_id.split("_")[-1]) + 1)
        #     to_click = \
        #         driver.find_elements(by=By.CSS_SELECTOR, value=f'#select_container_{md_select_container_id} md-option')[
        #             count]
        #     driver.execute_script("arguments[0].click();", to_click)
        #     # helper_funcs.element_clicker(driver=driver, web_element=to_click)

        md_toast_wait(driver=driver)


def password_string_create(char_nums: int = 10):
    result_str = ''

    result_str += random.choice(string.ascii_lowercase)
    result_str += random.choice(string.ascii_uppercase)
    result_str += random.choice(string.digits)
    result_str += random.choice(string.punctuation)

    result_str += ''.join(random.choice(string.printable[:-6]) for i in range(char_nums))
    return result_str


# TODO make an element waiter, like WebdriverWait but for web-elements (input a web element, find its child element or just wait for it to be visible)
def waiter(driver: Chrome, el_selector, by, timeout: WebElement):
    poll_freq = 0.5
    try:
        timeout.is_displayed()
        driver.find_element(by=by, value=el_selector)
    except exceptions.NoSuchElementException:
        pass


class AddressInput:
    """
    This is just a hacky way to input addresses,
    needs to be rewritten as the function calls itself, if no address is found, then steps out in a messy way
    TODO - Change so the input is generated in this class rather than inputting it outside
    """

    def __init__(self):
        self.address_repeat = 0

    # TODO TODO
    # def ul_progress_linear(self, driver: Chrome, input_el: WebElement, input_text):
    #     input_el.send_keys(input_text)
    #     try:
    #         progress_el = WdWait(driver, 5).until(ec.visibility_of_element_located((By.XPATH,
    #                                                                                 '../../md-progress-linear')))
    #     except exceptions.TimeoutException:
    #         sleep(5)
    #     else:
    #         WdWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, 'tt')))

    def ul_list_selector(self, driver: Chrome, input_el: WebElement, input_text):
        sleep(2)
        self.address_repeat += 1
        input_el.clear()
        input_el.send_keys(input_text)
        ul_el_id = 'ul-' + str(input_el.get_attribute('id')).split('-')[-1]
        try:
            WdWait(driver, 10).until(ec.visibility_of_element_located((By.ID, ul_el_id)))
        except exceptions.TimeoutException:
            # print('No list returned after 15 seconds')
            if self.address_repeat > 1:
                # print('No list returned after 2 timeout attempts.')
                return False
            else:
                sleep(5)
                self.ul_list_selector(driver, input_el, input_text)
        else:
            li_els = driver.find_element(By.ID, ul_el_id).find_elements(by=By.CSS_SELECTOR,
                                                                        value='li span')
            if len(li_els) == 0:
                input_el.send_keys(Keys.CONTROL + 'a')
                input_el.send_keys(Keys.BACKSPACE)
                sleep(0.2)
                if self.address_repeat > 1:
                    # print('List not returning after 2 attempts')
                    return False
                else:
                    self.ul_list_selector(driver, input_el, input_text)
            else:
                driver.execute_script("arguments[0].click();",
                                      li_els[random.randrange(0, len(li_els))])

                return True


def md_toast_remover(driver: Chrome):
    try:
        driver.find_element(by=By.TAG_NAME, value='md-toast')
    except exceptions.NoSuchElementException:
        try:
            WdWait(driver, 3).until(ec.invisibility_of_element_located((By.TAG_NAME, 'md-toast')))
        except exceptions.TimeoutException:
            md_toast_remover(driver)
    else:
        while True:
            try:
                md_toast = driver.find_element(by=By.TAG_NAME, value='md-toast')
            except exceptions.NoSuchElementException:
                break
            else:
                try:
                    driver.execute_script("arguments[0].remove();", md_toast)
                except exceptions.StaleElementReferenceException:
                    pass
                else:
                    try:
                        md_toast2 = driver.find_element(by=By.TAG_NAME, value='md-toast')
                    except exceptions.NoSuchElementException:
                        break
                    else:
                        driver.execute_script("arguments[0].remove();", md_toast2)
                    sleep(3)


def md_toast_wait(driver: Chrome):
    try:
        WdWait(driver, 5).until(ec.visibility_of_element_located((By.TAG_NAME, 'md-toast')))
    except exceptions.TimeoutException:
        print('no md_toast')
    else:
        try:
            WdWait(driver, 10).until(ec.invisibility_of_element_located((By.TAG_NAME, 'md-toast')))
        except exceptions.TimeoutException:
            pass
        else:
            sleep(2)


def element_clicker(driver: Chrome, web_element: WebElement = None, css_selector: str = ''):
    if css_selector:
        try:
            element = WdWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        except exceptions.TimeoutException:
            raise exceptions.ElementNotInteractableException(
                'Element not clickable after 10 seconds')
        except exceptions.NoSuchElementException:
            raise exceptions.NoSuchElementException(
                f'No element found with css selector: {css_selector}')
        except Exception as e:
            print(traceback.format_exc())
            raise e
        else:
            try:
                element.click()
            except exceptions.ElementClickInterceptedException:
                md_toast_remover(driver)
                driver.execute_script('arguments[0].click();', element)
            except Exception as e:
                print(traceback.format_exc())
                raise e

    elif web_element:
        try:
            web_element.click()
        except exceptions.ElementClickInterceptedException:
            try:
                driver.execute_script('arguments[0].click();', web_element)
            except exceptions.JavascriptException:
                md_toast_remover(driver)
                driver.execute_script('arguments[0].click();', web_element)
            finally:
                return True
        except exceptions.ElementNotInteractableException:
            return False
        except exceptions.StaleElementReferenceException:
            return False

        except Exception as e:
            print(traceback.format_exc())
            return False
        else:
            return True


def selector(driver: Chrome, select_element: WebElement, index='random', rand_range=''):
    try:
        current_sel = Select(select_element)
    except exceptions.StaleElementReferenceException as inst:
        traceback.print_exc()
        traceback.print_stack()
        return False
    except Exception:
        traceback.print_exc()
        traceback.print_stack()
        return False
    else:
        if index == 'random':
            if not rand_range:
                try:
                    select_value = random.randrange(1, len(current_sel.options))
                except ValueError:
                    select_value = random.randrange(0, 2)
            else:
                a, b = [int(t) for t in rand_range.split('-')]
                select_value = random.randrange(a, b)
        else:
            select_value = int(index)
        # TODO - Handle the selector exceptions properly
        try:
            current_sel.select_by_index(select_value)
        except exceptions.ElementClickInterceptedException:
            md_toast_remover(driver)
            try:
                current_sel.select_by_index(select_value)
            except exceptions.ElementClickInterceptedException:
                md_toast_remover(driver)

                try:
                    header = driver.find_element(by=By.CSS_SELECTOR,
                                                 value='st-header.new.ng-scope')
                except exceptions.NoSuchElementException:
                    pass
                else:
                    driver.execute_script("arguments[0].remove();", header)

                try:
                    scroll_mask = driver.find_element(by=By.CSS_SELECTOR,
                                                      value='div.md-scroll-mask')
                except exceptions.NoSuchElementException:
                    pass
                else:
                    driver.execute_script("arguments[0].remove();", scroll_mask)

                current_sel.select_by_index(select_value)
                return True

        except exceptions.NoSuchElementException:
            try:
                current_sel.select_by_index(0)
                return True
            except:
                traceback.print_exc()
                traceback.print_stack()
                return False

        except ValueError:
            traceback.print_exc()
            traceback.print_stack()
            return False

        else:
            return True


def unique_strings(nwords: int, pool: str = string.ascii_letters) -> str:
    """Generate a string of unique words.

    nwords: Number of words
    pool: Iterable of characters to choose from

    For a highly optimized version:
    https://stackoverflow.com/a/48421303/7954504

    Modified version from the RealPython website
    """

    seen = set()

    # An optimization for tightly-bound loops:
    # Bind these methods outside of a loop
    join = ''.join
    add = seen.add

    while len(seen) < nwords:
        token = join(random.choices(pool, k=random.randrange(1, 9)))
        add(token)
    return " ".join(seen)


def phone_num_gen(char_nums: int = 8):
    result_str = '04' + ''.join(random.choice(string.digits) for _ in range(char_nums))
    return result_str


def simple_expense_calc(driver: Chrome, deal_url: str):
    expense_total = 0
    hem_total = 0
    no_hem_total = 0
    driver.get(deal_url)
    expense_button = WdWait(driver, 10).until(ec.visibility_of_element_located(
        (By.XPATH,
         '//*[@id="top"]/st-sidebar/st-sidebar-content/st-sidebar-block[1]/div/div/button[2]')))
    expense_button.click()
    sleep(2)
    expenses = WdWait(driver, 10).until(
        ec.visibility_of_element_located((By.TAG_NAME, 'st-household-expenses')))

    values = expenses.find_elements(by=By.CSS_SELECTOR,
                                    value='input[ng-model="householdExpense.value"]')
    frequencies = expenses.find_elements(by=By.CSS_SELECTOR,
                                         value='select[ng-model="householdExpense.frequency"]')

    hem = "//span[contains(@class, 'success')]/../input"
    no_hem = "//span[contains(@class, 'danger')]/../input"
    select = '../../../div/st-form-field-container/select'

    hem_els = expenses.find_elements(by=By.XPATH, value=hem)
    no_hem_els = expenses.find_elements(by=By.XPATH, value=no_hem)

    for hem_el in hem_els:
        value = hem_el.get_attribute('value')
        value = int(value.lstrip('$').replace(',', ''))
        freq = Select(hem_el.find_element(by=By.XPATH, value=select)).first_selected_option.text
        if freq == 'Weekly':
            hem_total += (52 * value)
        elif freq == 'Fortnightly':
            hem_total += (26 * value)
        elif freq == 'Monthly':
            hem_total += (12 * value)
        elif freq == 'Quarterly':
            hem_total += (4 * value)
        elif freq == 'Semiannual':
            hem_total += (2 * value)
        elif freq == 'Annually':
            hem_total += value
        else:
            pass

    for no_hem_el in no_hem_els:
        value = no_hem_el.get_attribute('value')
        value = int(value.lstrip('$').replace(',', ''))
        freq = Select(no_hem_el.find_element(by=By.XPATH, value=select)).first_selected_option.text
        if freq == 'Weekly':
            no_hem_total += (52 * value)
        elif freq == 'Fortnightly':
            no_hem_total += (26 * value)
        elif freq == 'Monthly':
            no_hem_total += (12 * value)
        elif freq == 'Quarterly':
            no_hem_total += (4 * value)
        elif freq == 'Semiannual':
            no_hem_total += (2 * value)
        elif freq == 'Annually':
            no_hem_total += value
        else:
            pass

    for count, i_value in enumerate(values):
        value = i_value.get_attribute('value')
        value = int(value.lstrip('$').replace(',', ''))
        freq = Select(frequencies[count]).first_selected_option.text
        if freq == 'Weekly':
            expense_total += (52 * value)
        elif freq == 'Fortnightly':
            expense_total += (26 * value)
        elif freq == 'Monthly':
            expense_total += (12 * value)
        elif freq == 'Quarterly':
            expense_total += (4 * value)
        elif freq == 'Semiannual':
            expense_total += (2 * value)
        elif freq == 'Annually':
            expense_total += value
        else:
            pass

    print('Expense total: ', expense_total)
    print('Hem total: ', hem_total)
    print('No hem total: ', no_hem_total)


# only for payg and one client for now
def income_calc(driver: Chrome, deal_url: str):
    total = 0
    driver.get(deal_url)
    income_button = WdWait(driver, 10).until(ec.visibility_of_element_located(
        (By.XPATH,
         '//*[@id="top"]/st-sidebar/st-sidebar-content/st-sidebar-block[1]/div/div/button[1]')))
    income_button.click()
    sleep(2)
    WdWait(driver, 10).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.flex.layout-column.ng-scope.layout-gt-sm-row')))
    paygs = driver.find_elements(by=By.CSS_SELECTOR,
                                 value='div.flex.layout-column.ng-scope.layout-gt-sm-row')
    for payg in paygs:
        inputs = payg.find_elements(by=By.CSS_SELECTOR,
                                    value='div.flex.layout-column.ng-scope.layout-gt-sm-row md-input-container > input')
        selects = payg.find_elements(by=By.CSS_SELECTOR,
                                     value='div.flex.layout-column.ng-scope.layout-gt-sm-row st-form-field-container > select[ng-change="$ctrl.saveIncome()"]')
        for count, input_el in enumerate(inputs):
            value = input_el.get_attribute('value')
            value = int(value.lstrip('$').replace(',', ''))
            freq = Select(selects[count]).first_selected_option.text
            if freq == 'Weekly':
                total += (52 * value)
            elif freq == 'Fortnightly':
                total += (26 * value)
            elif freq == 'Monthly':
                total += (12 * value)
            elif freq == 'Quarterly':
                total += (4 * value)
            elif freq == 'Semiannual':
                total += (2 * value)
            elif freq == 'Annually':
                total += value
            else:
                pass

    print('Income total:', total)


def element_waiter(driver: Chrome, css_selector: str, url: str = '') -> WebElement:
    """
    Pass in a css selector and a URL and this will retry finding it
    """
    condition = ec.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    try:
        ret_el = WdWait(driver, 10).until(condition)
    except exceptions.TimeoutException:
        if url:
            driver.get(url)

        try:
            ret_el = WdWait(driver, 5).until(condition)
        except exceptions.TimeoutException:
            if url:
                driver.get(url)

            ret_el = WdWait(driver, 5).until(condition)

    return ret_el


def element_dissapear(driver, css_selector):
    try:
        WdWait(driver, 5).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    except exceptions.TimeoutException:
        sleep(5)
    else:
        WdWait(driver, 10).until(
            ec.invisibility_of_element_located((By.CSS_SELECTOR, css_selector)))


def element_scroll(driver, main_documents):
    while True:
        last_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)
        driver.execute_script(f"arguments[0].scroll(0,{last_height});", main_documents)
        sleep(5)
        new_height = driver.execute_script("return arguments[0].scrollHeight", main_documents)

        if new_height == last_height:
            break


def add_contact(driver: Chrome):
    driver.get('https://dev.salestrekker.com/contact/edit/person/0')
    WdWait(driver, 10).until(ec.visibility_of_element_located((By.TAG_NAME, 'st-contact')))

    first_names = ['Misty', 'Karl', 'Tanisha', 'Jasmin', 'Lexi-Mai', 'Chandni', 'Musab', 'Spike',
                   'Doris',
                   'Dominick', 'Rudi',
                   'Saira', 'Keeleigh', 'Nana', 'Andrew', 'Kirandeep', 'Roland', 'Harry', 'Alexie',
                   'Adelaide',
                   'Finbar', 'Nasir',
                   'Patrycja', 'Nela', 'Belinda', 'Amaya', 'Husnain', 'Tiana', 'Wyatt', 'Kenneth',
                   'April', 'Leia',
                   'Bushra',
                   'Levi', 'Keira', 'Amin', 'Samiha', 'Marianne', 'Habib', 'Yousuf', 'Nicola',
                   'Samanta',
                   'Benedict', 'Nikhil',
                   'Aurora', 'Giulia', 'Rosa', 'Alannah', 'Marian', 'Dionne', 'Xanthe', 'Anabel',
                   'Samira', 'Mason',
                   'Colleen',
                   'Esther', 'Faheem', 'Rachael', 'Kuba', 'Callam', 'Nick', 'Ayub', 'Esmay',
                   'Aimee', 'Sarah',
                   'Billy', 'Enid',
                   'Katie-Louise', 'Ashlee', 'Tamar', 'Darla', 'Whitney', 'Helena', 'Rachelle',
                   'Maisie', 'Julia',
                   'Mandy',
                   'Isaiah', 'Sally', 'Marianna', 'Jasleen', 'Evie-Mae', 'Lana', 'Kiana', 'Preston',
                   'Rae',
                   'Poppy-Rose', 'Lyla',
                   'Christy', 'Maheen', 'Cordelia', 'Mariya', 'Amelia-Grace', 'Kier', 'Sonny',
                   'Alessia', 'Inigo',
                   'Hareem',
                   'Caitlyn', 'Ayana', 'Danielle', 'Charlotte', 'Bronwyn', 'Eliot', 'Lesley', 'Ada',
                   'Azra',
                   'Wilbur', 'Lillian',
                   'Yannis', 'Sherri', 'Cosmo', 'Nella', 'Hasan', 'Tyrique', 'Jonah', 'Lexi-Mae',
                   'Nigel', 'Zavier',
                   'Bevan',
                   'Leo', 'Israel', 'Sharna', 'Jagoda', 'Deborah', 'Claire', 'Anabelle', 'Kobie',
                   'Nabeel',
                   'Kayley', 'Zahrah',
                   'Beck', 'Kingsley', 'Micah', 'Jerry', 'Haydn', 'Robyn', 'Carwyn', 'Rhys',
                   'Seamus', 'Maia',
                   'Iman', 'Rahul',
                   'Judy', 'Arwa', 'Jeevan', 'Francesco', 'Shyam', 'Amal', 'Gabrielle', 'Kellie',
                   'Derry',
                   'Quentin', 'Hashir',
                   'Alma', 'Rheanna', 'Sebastian', 'Sahara', 'Miriam', 'Debbie', 'Niyah',
                   'Lillie-May', 'Petra',
                   'Khalil', 'Lena',
                   'Isabell', 'Howard', 'Lennie', 'Jibril', 'Christiana', 'Alan', 'Kimora',
                   'Muneeb', 'Iqrah',
                   'Hanna', 'Akbar',
                   'Beverly', 'Jill', 'Shania', 'T-Jay', 'George', 'Lexie', 'Gerard', 'Weronika',
                   'Alison', 'Reon',
                   'Piotr',
                   'Alya', 'Mitchel', 'Sally', 'Alfie-Lee', 'Abbie', 'Pola', 'Laylah', 'Zubair',
                   'Ali', 'Nicole',
                   'Lorna',
                   'Ember', 'Cora']

    surnames = ['Banks', 'Berg', 'Obrien', 'Talley', 'Mccray', 'Kramer', 'Cunningham', 'Dunn', 'Vu',
                'Ferry',
                'Wolfe', 'Haas', 'Bate', 'Tomlinson', 'Phelps', 'Goulding', 'Penn', 'Slater',
                'Aguilar', 'Mellor',
                'Bray', 'Potter', 'Metcalfe', 'Burch', 'Houston', 'Brandt', 'Nixon', 'Allison',
                'Stephens',
                'Webster', 'Lawrence', 'Wright', 'Knowles', 'Davidson', 'Dalton', 'Flower',
                'Cameron', 'Baker',
                'Portillo', 'Lord', 'Goodman', 'Roman', 'Wardle', 'Hayden', 'Bains', 'Romero',
                'Iles', 'Navarro',
                'Malone', 'Molina', 'Macfarlane', 'Hilton', 'Mckay', 'Novak', 'Gaines', 'Ratliff',
                'Valdez',
                'Zavala', 'Gibbons', 'Almond', 'Bruce', 'Felix', 'Reeve', 'Chang', 'Patrick',
                'Hutchings', 'Ayala',
                'Russell', 'Burn', 'Parra', 'Sharma', 'Emery', 'Burris', 'Southern', 'Mcleod',
                'Mckee', 'Duggan',
                'William', 'Dalby', 'Carr', 'Carty', 'Read', 'Marsh', 'Chase', 'Greene', 'Stafford',
                'Greig',
                'Woolley', 'Bird', 'Wyatt', 'Escobar', 'Bradley', 'Kirby', 'Whitney', 'Cartwright',
                'Sargent',
                'Plummer', 'Lucero', 'Reynolds', 'Melia', 'Davenport', 'Irving', 'Barrow', 'Senior',
                'Mcgowan',
                'Hancock', 'Povey', 'Mcmanus', 'Tyson', 'Hunt', 'Betts', 'Lopez', 'Molloy', 'Plant',
                'Kirk',
                'Cantu', 'Reid', 'Whelan', 'Dupont', 'Berry', 'Mueller', 'Lowery', 'Powell',
                'Porter', 'Krueger',
                'Griffiths', 'Garrett', 'Barrett', 'Gibbs', 'Calvert', 'Hills', 'Rice', 'Correa',
                'Pineda',
                'Beasley', 'Sanderson', 'Frye', 'Garrison', 'Trevino', 'Stafford', 'Rankin',
                'Huerta', 'Luna',
                'Mustafa', 'Lane', 'Russo', 'Richmond', 'Ferry', 'Wolfe', 'Schmidt', 'Mcnally',
                'Power',
                'Castaneda', 'Wickens', 'Romero', 'Smyth', 'Coulson', 'Riley', 'Carty', 'Hogan',
                'Bonilla', 'Mcgee',
                'Buck', 'Mccoy', 'Schneider', 'Gordon', 'Hardy', 'Ferreira', 'Jarvis', 'Haley',
                'Bray', 'Barnett',
                'Finch', 'Cox', 'Lawrence', 'Leech', 'Bain', 'Cross', 'Hyde', 'Soto', 'Bates',
                'Knowles', 'Douglas',
                'Roberts', 'Cornish', 'Robles', 'Macgregor', 'Hines', 'Oakley', 'Santos',
                'Kirkpatrick', 'Alvarez',
                'Piper', 'Murphy', 'Boyd', 'Haas', 'Corbett', 'Short', 'Alexander', 'Sloan']

    first_name = random.choice(first_names)
    last_name = random.choice(surnames)
    email = f'matthew+{first_name.lower()}{last_name.lower()}@salestrekker.com'
    date_of_birth = f'09/07/{random.randrange(1950, 1990)}'

    driver.find_element(by=By.CSS_SELECTOR,
                        value='input[ng-model="$ctrl.contact.person.information.firstName"]').send_keys(
        first_name)
    driver.find_element(by=By.CSS_SELECTOR,
                        value='input[ng-model="$ctrl.contact.person.information.familyName"]').send_keys(
        last_name)
    driver.find_element(by=By.CSS_SELECTOR,
                        value='md-datepicker[ng-model="$ctrl.getSetDateOfBirth"] input').send_keys(
        date_of_birth)
    phone_code = driver.find_element(by=By.CSS_SELECTOR,
                                     value='input[ng-model="$ctrl.contact.person.contact.primaryCode"]')
    phone_code.clear()
    phone_code.send_keys('381')
    driver.find_element(by=By.CSS_SELECTOR,
                        value='input[ng-model="$ctrl.contact.person.contact.primary"]').send_keys(
        '695242544')
    driver.find_element(by=By.CSS_SELECTOR,
                        value='input[ng-model="$ctrl.contact.person.contact.email"]').send_keys(
        email)
    driver.find_element(by=By.CSS_SELECTOR,
                        value='md-datepicker[ng-model="$ctrl.getSetPassportExpiryDate"] input').send_keys(
        '09/07/2021')
    try:
        WdWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))
    except exceptions.TimeoutException:
        sleep(7)
    else:
        WdWait(driver, 10).until(
            ec.invisibility_of_element_located((By.CSS_SELECTOR, 'md-progress-linear.mt1')))


def random_date(test_date1: date = date(1980, 1, 1), test_date2: date = date.today()):
    total_days = test_date2 - test_date1
    randay = random.randrange(total_days.days)
    return_date = test_date1 + timedelta(days=randay)
    return return_date


def ent_extract(url: str) -> str:
    extract_url = ''
    return extract_url

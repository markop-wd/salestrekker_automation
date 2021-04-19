"""
When something out of the ordinary has to be done
Instead of programming in the main business logic just implement it here and import it there
"""
import random
import threading
import traceback
import string
from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from selenium.webdriver import Chrome

from main.Permanent.login import LogIn
from main.mail import mail_get


def random_string_create(char_nums: int = 10):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(char_nums))
    return result_str


# TODO
def accreditation_fill(driver: Chrome, ent: str, all_new: bool = True):
    if driver.current_url != f"https://{ent}.salestrekker.com/settings/my-accreditations":
        driver.get(f"https://{ent}.salestrekker.com/settings/my-accreditations")
    WdWait(driver, 50).until(ec.visibility_of_element_located((By.TAG_NAME, 'st-block-form-content')))

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

        add_new = driver.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Add new lender accreditation"]')
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


def user_setup_raw(driver: Chrome, ent: str):
    """
    This is a basic version of setting up a user for the first time
    # TODO Improve this version and connect it to the LogIn class
    :param driver:
    :param ent:
    :return:
    """
    driver.maximize_window()
    add_input = AddressInput()

    mail_dict = mail_get(ent)
    if mail_dict['email'] and mail_dict['password']:
        LogIn(driver, ent, mail_dict['email'], mail_dict['password']).log_in()
        try:
            driver.find_element(by=By.CSS_SELECTOR, value='input[name="phoneNumber"]')

        except exceptions.NoSuchElementException:
            pass
        else:
            phone_num_el = WdWait(driver, 10).until(
                ec.visibility_of_element_located((
                    By.CSS_SELECTOR, 'input[name="phoneNumber"]')))
            phone_num_el.send_keys(Keys.CONTROL + "A")
            sleep(0.1)
            phone_num_el.send_keys(Keys.DELETE)
            phone_num_el.send_keys('0412341234')

            address_el = WdWait(driver, 10).until(
                ec.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    'input[aria-label="Search address"]')))
            add_input.ul_list_selector(driver, address_el, f'{random.randrange(1, 100)} ae')

        sleep(5)
        element_clicker(driver, css_selector='a[ui-sref=".password-and-security"]')

        WdWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
        new_password = password_string_create()
        print(new_password)
        for element in driver.find_elements_by_css_selector('input[type="password"]'):
            if element.get_attribute('ng-model') == 'Model.oldPassword':
                element.send_keys(mail_dict['password'])
            else:
                element.send_keys(new_password)
            sleep(1)

        WdWait(driver, 10).until(ec.element_to_be_clickable((
            By.CSS_SELECTOR, 'button[ng-click="changePassword()"]'))).click()

        WdWait(driver, 10).until(ec.element_to_be_clickable
                                 ((By.CSS_SELECTOR,
                                   'div[ng-if="Model.AUTH.isPasswordChangeRequired()"] button'))) \
            .click()

        # TODO - Better, robust waits
        WdWait(driver, 50).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'board#board')))
        # driver.get("https://"+ent+".salestrekker.com/settings/my-accreditations")
        # WdWait(driver, 50).until(ec.visibility_of_element_located((By.TAG_NAME, 'st-block-form-content')))
        # input(f'{ent} finish')
        return mail_dict['email'], new_password
    else:
        print('Oj dios mio no email information')


class AddressInput:
    """
    This is just a hacky way to input addresses,
    needs to be rewritten as the function calls itself, if no address is found, then steps out in a messy way
    TODO - Change so the input is generated in this class rather than inputting it outside
    """
    def __init__(self):
        self.address_repeat = 0

    def ul_list_selector(self, driver: Chrome, input_el, input_text):
        sleep(5)
        self.address_repeat += 1
        input_el.send_keys(input_text)
        ul_el_id = 'ul-' + str(input_el.get_attribute('id')).split('-')[-1]
        try:
            WdWait(driver, 15).until(ec.visibility_of_element_located((By.ID, ul_el_id)))
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


def md_toast_wait(driver: Chrome, second_sleep=0):
    try:
        WdWait(driver, 15).until(ec.invisibility_of_element_located((By.TAG_NAME, 'md-toast')))
    except exceptions.NoSuchElementException:
        sleep(5)
        try:
            WdWait(driver, 15).until(ec.invisibility_of_element_located((By.TAG_NAME, 'md-toast')))
        except exceptions.NoSuchElementException:
            sleep(second_sleep)
        else:
            sleep(5)
    except exceptions.TimeoutException:
        pass
    else:
        sleep(5)


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

        except Exception as e:
            print(traceback.format_exc())
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

if __name__ == '__main__':
    # user_setup_raw(Chrome(executable_path=GeckoDriverManager().install()), ent='dev')
    print(password_string_create())

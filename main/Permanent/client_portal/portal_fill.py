import os
import random
import string
from datetime import datetime
from time import sleep

from selenium.common import exceptions
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as wd_wait

from main.Permanent import helper_funcs

# TODO - Adapt this to the pages model


class _SelectElHandler:

    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self.driver.implicitly_wait(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.implicitly_wait(10)

    def __call__(self, *args, **kwargs):
        self._select_el_handler(kwargs['section'])

    def _select_el_handler(self, content):
        all_selects = content.find_elements(by=By.TAG_NAME, value='select')
        if all_selects:
            for select_el in all_selects:
                try:
                    helper_funcs.selector(self.driver, select_element=select_el)
                except exceptions.StaleElementReferenceException:
                    print('select el handler stale')
                    continue


class _TextAreaHandler:

    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self.driver.implicitly_wait(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.implicitly_wait(10)

    def __call__(self, *args, **kwargs):
        self._textarea_el_handler(kwargs['section'])

    @staticmethod
    def _textarea_logic(text_area_el: WebElement):

        initial_value = text_area_el.get_attribute('value')

        if not initial_value:
            text_area_el.send_keys(helper_funcs.unique_strings(20))

    def _textarea_el_handler(self, content):
        # TODO - First handle checkboxes
        text_area_els = content.find_elements(by=By.TAG_NAME, value="textarea")
        if text_area_els:
            for text_area_el in text_area_els:
                try:
                    self._textarea_logic(text_area_el)
                except exceptions.ElementNotInteractableException:
                    continue


class _InputElHandler:

    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self.driver.implicitly_wait(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.implicitly_wait(10)

    def __call__(self, *args, **kwargs):
        self._input_el_handler(kwargs['section'])

    @staticmethod
    def _input_logic(input_el: WebElement):

        initial_value = input_el.get_attribute('value')
        placeholder = input_el.get_attribute('placeholder')
        name = input_el.get_attribute('name')

        if initial_value == '$0':
            value = str(random.randrange(0, 50000))
            input_el.send_keys(value)

        elif initial_value == '$0.00':
            value = str(random.randrange(100, 500000))
            input_el.send_keys(value)

        elif initial_value == '0':
            value = str(random.randrange(0, 10000))
            input_el.send_keys(value)

        elif placeholder == 'DD/MM/YYYY':
            if not initial_value:
                year = random.randrange(1930, 2010)

                _day = random.randrange(1, 29)
                _month = random.randrange(1, 13)

                day = f"0{_day}" if _day in range(1, 10) else _day
                month = f"0{_month}" if _month in range(1, 10) else _month

                input_el.send_keys(f'{day}/{month}/{year}')

        elif placeholder == 'MM/YYYY':
            if not initial_value:
                year = random.randrange(1930, 2010)

                _month = random.randrange(1, 13)

                month = f"0{_month}" if _month in range(1, 10) else _month

                input_el.send_keys(f'{month}/{year}')

        elif placeholder == 'Start typing address here...':
            print('Address')
            # TODO - Address handler

        elif name in ['work', 'home']:
            if not initial_value:
                input_el.send_keys(helper_funcs.random_string_create(char_nums=9, chars=False))

        elif not initial_value:
            input_el.send_keys(helper_funcs.random_string_create(char_nums=6))

    def _checkbox_logic(self, input_el):
        if bool(random.randrange(0, 2)):
            try:
                input_el.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", input_el)

    def _input_el_handler(self, content):
        # TODO - First handle checkboxes
        all_inputs = content.find_elements(by=By.TAG_NAME, value='input')

        if all_inputs:
            checkboxes = [input_el for input_el in all_inputs if
                          input_el.get_attribute('type') == 'checkbox']
            reg_input = [input_el for input_el in all_inputs if
                         input_el.get_attribute('type') != 'checkbox']

            if checkboxes:
                for input_el in checkboxes:
                    try:
                        if bool(random.randrange(0, 2)):
                            try:
                                input_el.click()
                            except exceptions.ElementClickInterceptedException:
                                self.driver.execute_script("arguments[0].click();", input_el)

                    except exceptions.ElementNotInteractableException:
                        print('No interacto')
                        continue
                    except exceptions.StaleElementReferenceException:
                        print('Stalino')
                        continue
            for input_el in reg_input:
                # TODO - Here I get the input el
                #  make him call different logic functions based on different properties
                try:
                    self._input_logic(input_el)
                except exceptions.ElementNotInteractableException:
                    print('No interacto')
                    continue
                except exceptions.StaleElementReferenceException:
                    print('Stalino')
                    continue


class PortalFill:

    def __init__(self, driver: Chrome):
        self.driver = driver
        self.header_titles = []
        self.li_els = []
        self.header_div = None
        self.main()

    def main(self):

        self.driver.get(self.driver.current_url.split('dashboard')[0])

        self._header_loop_logic()

    def _header_loop_logic(self):

        # div_sections = self.driver.find_elements(by=By.CSS_SELECTOR,
        #                                               value='div.sections > div.section')

        header_titles_els = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                      value='div.sections > div.section > '
                                                            'div.section-header > '
                                                            'span:nth-of-type(2)')

        self.header_titles = [span.text
                              for span in header_titles_els]

        len_headers = len(self.header_titles)

        for header_num in range(0, len_headers):

            # TODO - Utilize the data-active attribute as it requires that the header is selected
            #  and any element within the header
            # if div_sections[header_num].get_attribute('data-active') != 'true':
            #     div_sections[header_num].click()

            self._main_header_reselect(header_num)

            # if self.header_titles[header_num] != 'Needs and objectives':
            #     continue
            if self.header_titles[header_num] == 'Documents':
                continue

            self._li_loop_logic(header_num)

    def _li_loop_logic(self, header_num):

        current_li_num = 0

        while True:
            self.li_els = self.header_div.find_elements(by=By.CSS_SELECTOR, value='ul.steps > li')
            len_li_els = len(self.li_els)

            for li_num in range(current_li_num, len_li_els):

                if self.li_els != self.header_div.find_elements(by=By.CSS_SELECTOR,
                                                                value='ul.steps > li'):
                    break

                # TODO - Testing li_text text
                li_text = self.li_els[li_num].text
                current_li_num = li_num
                # li_text = self.li_els[li_num].find_element(by=By.CSS_SELECTOR,
                # value="span:nth-of-type(2)").text

                self.driver.execute_script("arguments[0].click();", self.li_els[li_num])
                sections_handled = self._section_loop_logic(header_num=header_num, li_num=li_num)
                if not sections_handled:
                    current_li_num += 1

                try:
                    self.li_els[current_li_num].is_displayed()
                except exceptions.StaleElementReferenceException:
                    print('Stale Element Reference')
                    print(self.header_titles[header_num])
                    print(li_text)
                    print(current_li_num)

                    self._main_header_reselect(header_num)

                    # TODO ?
                    # current_li_num += 1
                except IndexError:
                    continue

                if self.li_els != self.header_div.find_elements(by=By.CSS_SELECTOR,
                                                                value='ul.steps > li'):
                    break

            else:
                return None
                # break

    def _section_loop_logic(self, header_num, li_num):

        current_section_num = 0
        while True:

            section_divs = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                     value="#wizardSection > div")
            len_section_divs = len(section_divs)
            if not section_divs:
                print('Section div first break')

                self._main_header_reselect(header_num)

                self.li_els = self.header_div.find_elements(by=By.CSS_SELECTOR,
                                                            value='ul.steps > li')

                self.driver.execute_script("arguments[0].click();", self.li_els[li_num])

                continue

            for section_num in range(current_section_num, len_section_divs):

                if section_divs != self.driver.find_elements(by=By.CSS_SELECTOR,
                                                             value="#wizardSection > div"):
                    break

                section = section_divs[section_num]
                current_section_num = section_num
                # print(li_text)

                section_class = section.get_attribute('class')

                if section_class == 'top-header':
                    continue

                if section_class == 'select-box-container':

                    clicked = self._section_box_handler(section)

                    # TODO - Stopped here - checking for li.steps-active and its use

                    if clicked:
                        if self.li_els[li_num].get_attribute('class') != 'steps-active':
                            print('Moving on')
                            return False

                    # if clicked:
                    #     current_li_num += 1

                elif section_class == 'row':

                    with _SelectElHandler(self.driver) as select_h:
                        select_h(section=section)
                    with _InputElHandler(self.driver) as input_h:
                        input_h(section=section)
                    with _TextAreaHandler(self.driver) as text_h:
                        text_h(section=section)

                elif section_class in ['row-compact', 'row row-singular']:
                    self._section_box_handler(section)
                    with _TextAreaHandler(self.driver) as text_h:
                        text_h(section=section)
                elif section_class == 'row row-block':
                    with _InputElHandler(self.driver) as input_h:
                        input_h(section=section)
                    with _TextAreaHandler(self.driver) as text_h:
                        text_h(section=section)

                else:
                    continue

            else:
                break
        return True

    def _section_box_handler(self, section: WebElement):
        div_box_to_click = random.choice(
            section.find_elements(by=By.CSS_SELECTOR, value='div.select-box'))

        if 'select-box-has-dropdown' in div_box_to_click.get_attribute('class'):
            div_dropbox_options = div_box_to_click.find_elements(by=By.CSS_SELECTOR,
                                                                 value='div.select-box-dropdown'
                                                                       '-option')
            div_option_to_click = random.choice(div_dropbox_options)
            action = ActionChains(self.driver)
            for _ in range(3):
                action.move_to_element(div_box_to_click).perform()
                try:
                    wd_wait(self.driver, 5).until(ec.visibility_of(div_box_to_click))
                except exceptions.TimeoutException:
                    sleep(0.5)
                else:
                    break

            try:
                div_option_to_click.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", div_option_to_click)
                return True
            else:
                return True
            finally:
                return False

        else:
            try:
                div_box_to_click.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", div_box_to_click)
                return True
            else:
                return True
            finally:
                return False

    def _main_header_reselect(self, pos, repeat=2):
        """
        Selecting/opening the main header section and returning the header div element
        Also updating the full list of headers in case they have changed (first or surname changed)

        """
        header_title = self.header_titles[pos]
        section_header_titles = []
        i = 1

        while True:
            if i > repeat:
                raise Exception("Cannot find the main element")

            try:
                self.driver.find_element(by=By.TAG_NAME, value="main")
            except exceptions.NoSuchElementException:
                print(f'No Main, waiting {i}. time')
                self.driver.refresh()
                sleep(5 * i)
                i += 1
            else:
                break

        try:
            div = self.driver.find_element(by=By.XPATH,
                                           value=f"//span[text() = '{header_title}']/../..")
        except exceptions.NoSuchElementException:
            header_text_els = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                        value='div.sections > div.section > '
                                                              'div.section-header > '
                                                              'span:nth-of-type(2)')

            section_header_titles = [div.text
                                     for div in header_text_els]

            header_text = section_header_titles[pos]
            div = self.driver.find_element(by=By.XPATH,
                                           value=f"//span[text() = '{header_text}']/../..")

            # return section_header_titles, section_header_titles[pos]

        steps = str(
            div.find_element(by=By.CSS_SELECTOR, value='ul.steps').get_attribute('class')).split()

        # In case the header is not open
        if 'steps-hidden' in steps:
            section_header = div.find_element(by=By.CSS_SELECTOR, value='div.section-header')
            try:
                section_header.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", section_header)

        if section_header_titles:
            self.header_titles = section_header_titles
            self.header_div = div
        else:
            self.header_div = div

    def screenshot(self):

        deal_id = datetime.now().strftime("%d-%m-%Y-%H-%M") + ' ' + ''.join(
            random.sample(string.ascii_letters, 7))

        os.mkdir(f"CP_Screenshots/{deal_id}")

        header_titles_els = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                      value='div.sections > div.section > '
                                                            'div.section-header > '
                                                            'span:nth-of-type(2)')

        self.header_titles = [span.text
                              for span in header_titles_els]

        len_headers = len(self.header_titles)

        for header_num in range(0, len_headers):

            self._main_header_reselect(header_num)

            try:
                os.mkdir(
                    f"CP_Screenshots/{deal_id}/{header_num + 1}. {self.header_titles[header_num]}")
            except FileExistsError:
                pass

            self.li_els = self.header_div.find_elements(by=By.CSS_SELECTOR, value='ul.steps > li')
            len_li_els = len(self.li_els)

            for li_num in range(0, len_li_els):
                li_text = self.li_els[li_num].text
                # li_text = self.li_els[li_num].find_element(by=By.CSS_SELECTOR,
                # value="span:nth-of-type(2)").text

                self.driver.execute_script("arguments[0].click();", self.li_els[li_num])

                if self.header_titles[header_num] == 'Documents':
                    # TODO - Wait for the stuff to load on this page
                    sleep(10)

                self.driver.get_screenshot_as_file(
                    f"CP_Screenshots/{deal_id}/{header_num + 1}. "
                    f"{self.header_titles[header_num]}/{li_num + 1}. {li_text}.png")

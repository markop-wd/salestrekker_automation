import os
import random
import time
import traceback
import string
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as wd_wait
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Remote
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from Permanent.client_portal.login import LogIn
from main.Permanent import helper_funcs


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

    def _select_logic(self, select_element, index='random'):
        try:
            current_sel = Select(select_element)
        except exceptions.StaleElementReferenceException as inst:
            print('Stale reference', inst)
            print(inst.stacktrace)
        except Exception as exc:
            traceback.print_stack()
            traceback.print_exc()
            raise exc
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

            except exceptions.NoSuchElementException:
                print('No such sel')

            except ValueError:
                try:
                    current_sel.select_by_index(1)
                except ValueError:
                    current_sel.select_by_index(0)

    def _select_el_handler(self, content):
        all_selects = content.find_elements(by=By.TAG_NAME, value='select')
        if all_selects:
            for select_el in all_selects:
                try:
                    self._select_logic(select_el)
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

    def _textarea_logic(self, text_area_el: WebElement):

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

    def _input_logic(self, input_el: WebElement):

        initial_value = input_el.get_attribute('value')
        placeholder = input_el.get_attribute('placeholder')
        type_attr = input_el.get_attribute('type')
        name = input_el.get_attribute('name')

        if initial_value == '$0':
            value = str(random.randrange(0, 50000))
            self._input_send(input_el, value)

        elif initial_value == '$0.00':
            value = str(random.randrange(100, 500000))
            self._input_send(input_el, value)

        elif initial_value == '0':
            value = str(random.randrange(0, 10000))
            self._input_send(input_el, value)

        elif placeholder == 'DD/MM/YYYY':
            if not initial_value:

                year = random.randrange(1930, 2010)

                _day = random.randrange(1, 29)
                _month = random.randrange(1, 13)

                day = f"0{_day}" if _day in range(1, 10) else _day
                month = f"0{_month}" if _month in range(1, 10) else _month

                self._input_send(input_el, f'{day}/{month}/{year}')

        elif placeholder == 'MM/YYYY':
            if not initial_value:

                year = random.randrange(1930, 2010)

                _month = random.randrange(1, 13)

                month = f"0{_month}" if _month in range(1, 10) else _month

                self._input_send(input_el, f'{month}/{year}')

        elif placeholder == 'Start typing address here...':
            print('Address')
            # TODO - Address handler

        elif name in ['work', 'home']:
            if not initial_value:
                random_string = ''.join(random.sample(string.digits, 9))
                self._input_send(input_el, random_string)

        elif type_attr == 'checkbox':
            if bool(random.randrange(0, 2)):
                try:
                    input_el.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", input_el)

        elif not initial_value:

            random_string = ''.join(random.sample(string.ascii_letters, random.randrange(4, 7)))
            self._input_send(input_el, random_string)

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
            for input_el in all_inputs:
                sleep(.5)
                # TODO - Here I get the input el, make him call different logic functions based on different properties
                try:
                    self._input_logic(input_el)
                except exceptions.ElementNotInteractableException:
                    print('No interacto')
                    continue
                except exceptions.StaleElementReferenceException:
                    print('Stalino')
                    continue

    # TODO this might be useless
    def _input_send(self, input_el: WebElement, input_string: str):
        # if input_el.get_attribute('value'):
        #     input_el.send_keys(Keys.CONTROL + "a")
        #     input_el.send_keys(Keys.DELETE)
        #     sleep(.2)
        input_el.send_keys(input_string)

        # input_el.send_keys(Keys.CONTROL + "a")
        # input_el.send_keys(Keys.DELETE)

# class PortalFill:
#
#     def __init__(self, driver: Remote):
#         self.driver = driver
#
#     def _section_box_handler(self, section: WebElement):
#         div_box_to_click = random.choice(
#             section.find_elements(by=By.CSS_SELECTOR, value='div.select-box'))
#
#         # div_box_to_click = driver.find_elements(by=By.CSS_SELECTOR, value='div.select-box')[-1]
#
#         if 'select-box-has-dropdown' in div_box_to_click.get_attribute('class'):
#             div_dropbox_options = div_box_to_click.find_elements(by=By.CSS_SELECTOR,
#                                                                  value='div.select-box-dropdown-option')
#             div_option_to_click = random.choice(div_dropbox_options)
#             action = ActionChains(self.driver)
#             for _ in range(3):
#                 action.move_to_element(div_box_to_click).perform()
#                 try:
#                     wd_wait(self.driver, 5).until(ec.visibility_of(div_box_to_click))
#                 except exceptions.TimeoutException:
#                     sleep(0.5)
#                 else:
#                     break
#
#             # css_visibility(driver)
#
#             try:
#                 div_option_to_click.click()
#             except exceptions.ElementNotInteractableException:
#                 return False
#             except exceptions.StaleElementReferenceException:
#                 return False
#             except exceptions.ElementClickInterceptedException:
#                 self.driver.execute_script("arguments[0].click();", div_option_to_click)
#                 return True
#             else:
#                 return True
#
#         else:
#             try:
#                 div_box_to_click.click()
#             except exceptions.ElementClickInterceptedException:
#                 self.driver.execute_script("arguments[0].click();", div_box_to_click)
#             except Exception as exc:
#                 print(exc)
#                 return False
#             else:
#                 return True
#
#     def _main_header_reselect(self, header_title, pos, repeat=2):
#         """
#         Selecting the main header returning the header div element
#         Also returning the full list of headers in case they have changed (first or surname changed)
#
#         """
#         section_header_titles = []
#         i = 0
#         while True:
#             if i > repeat:
#                 raise Exception("Cannot find the main element")
#
#             try:
#                 self.driver.find_element(by=By.TAG_NAME, value="main")
#             except exceptions.NoSuchElementException:
#                 print('no Main')
#                 self.driver.refresh()
#                 sleep(5 * i)
#                 i += 1
#             else:
#                 break
#
#         try:
#             div = self.driver.find_element(by=By.XPATH, value=f"//span[text() = '{header_title}']/../..")
#         except exceptions.NoSuchElementException:
#             header_text_els = self.driver.find_elements(by=By.CSS_SELECTOR,
#                                                         value='div.sections > div.section > div.section-header > span:nth-of-type(2)')
#
#             section_header_titles = [div.text
#                                      for div in header_text_els]
#
#             header_text = section_header_titles[pos]
#             div = self.driver.find_element(by=By.XPATH, value=f"//span[text() = '{header_text}']/../..")
#
#             # return section_header_titles, section_header_titles[pos]
#
#         # div = driver.find_element(by=By.XPATH, value=f"//span[text() = '{header_title}']/../..")
#         steps = str(div.find_element(by=By.CSS_SELECTOR, value='ul.steps').get_attribute('class')).split()
#
#         # In case the header is not open
#         if 'steps-hidden' in steps:
#             section_header = div.find_element(by=By.CSS_SELECTOR, value='div.section-header')
#             try:
#                 section_header.click()
#             except exceptions.ElementClickInterceptedException:
#                 self.driver.execute_script("arguments[0].click();", section_header)
#
#         if section_header_titles:
#             return div, section_header_titles
#
#         else:
#             return div, []
#
#     def main(self):
#         self.driver.get(self.driver.current_url.split('dashboard')[0])
#
#         div_section = self.driver.find_elements(by=By.CSS_SELECTOR,
#                                                 value='div.sections > div.section > div.section-header > span:nth-of-type(2)')
#
#         section_header_titles = [div.text
#                                  for div in div_section]
#
#         section_header_len = len(section_header_titles)
#
#         for t in range(0, section_header_len):
#
#             header_div, temp_list = self._main_header_reselect(section_header_titles[t], t)
#             if temp_list:
#                 section_header_titles = temp_list
#
#             if section_header_titles[t] != 'Needs and objectives':
#                 continue
#
#             current_num = 0
#
#             while True:
#                 li_els = header_div.find_elements(by=By.CSS_SELECTOR, value='ul.steps > li')
#                 len_li_els = len(li_els)
#
#                 for i in range(current_num, len_li_els):
#
#                     current_num = i
#
#                     li_text = li_els[i].find_element(by=By.CSS_SELECTOR, value="span:nth-of-type(2)").text
#
#                     if section_header_titles[t] == 'Documents':
#                         continue
#
#                     self.driver.execute_script("arguments[0].click();", li_els[i])
#
#                     section_divs = self.driver.find_elements(by=By.CSS_SELECTOR, value="#wizardSection > div")
#                     if not section_divs:
#                         print('Section div first break')
#
#                         header_div, temp_list = self._main_header_reselect(section_header_titles[t], t)
#                         if temp_list:
#                             section_header_titles = temp_list
#
#                         current_num += 1
#                         break
#
#                     len_section_divs = len(section_divs)
#
#                     # for section in section_divs:
#                     for d in range(0, len_section_divs):
#
#                         section_divs = self.driver.find_elements(by=By.CSS_SELECTOR, value="#wizardSection > div")
#
#                         section = self.driver.find_element(by=By.CSS_SELECTOR,
#                                                            value=f"#wizardSection > div:nth-of-type({d})")
#
#                         # print(li_text)
#                         section_class = section.get_attribute('class')
#
#                         if section_class == 'select-box-container':
#
#                             clicked = self._section_box_handler(section)
#
#                             if clicked:
#                                 current_num += 1
#
#                         elif section_class == 'row':
#
#                             with _SelectElHandler(self.driver) as select_h:
#                                 select_h(section=section)
#                             with _InputElHandler(self.driver) as input_h:
#                                 input_h(section=section)
#
#                             # TODO - Maybe make a textarea handler
#                             text_area_els = self.driver.find_elements(by=By.TAG_NAME, value="textarea")
#                             if text_area_els:
#                                 for text_area_el in text_area_els:
#                                     try:
#                                         text_area_el.send_keys(helper_funcs.unique_strings(20))
#                                     except exceptions.ElementNotInteractableException:
#                                         continue
#
#                         elif section_class == 'row-compact':
#                             self._section_box_handler(section)
#                             text_area_els = self.driver.find_elements(by=By.TAG_NAME, value="textarea")
#                             if text_area_els:
#                                 for text_area_el in text_area_els:
#                                     try:
#                                         text_area_el.send_keys(helper_funcs.unique_strings(20))
#                                     except exceptions.ElementNotInteractableException:
#                                         continue
#                         else:
#                             continue
#
#                     try:
#                         li_els = header_div.find_elements(by=By.CSS_SELECTOR, value='ul.steps > li')
#                     except exceptions.StaleElementReferenceException:
#                         print('Stale Element Reference')
#                         print(section_header_titles[t])
#                         print(li_text)
#                         print(current_num)
#
#                         header_div, temp_list = self._main_header_reselect(section_header_titles[t], t)
#                         if temp_list:
#                             section_header_titles = temp_list
#
#                         current_num += 1
#                     if len_li_els != len(li_els):
#                         break
#
#                 else:
#                     break


# def reselect_pattern(start_point, selector: str, current_num):
#     els = start_point.find_elements(by=By.CSS_SELECTOR, value=selector)
#     len(els)


class PortalFillRewrite:

    def __init__(self, driver: Chrome):
        self.driver = driver
        self.header_titles = []
        self.li_els = []
        self.header_div = None

    def _section_box_handler(self, section: WebElement):
        div_box_to_click = random.choice(
            section.find_elements(by=By.CSS_SELECTOR, value='div.select-box'))

        # div_box_to_click = driver.find_elements(by=By.CSS_SELECTOR, value='div.select-box')[-1]

        if 'select-box-has-dropdown' in div_box_to_click.get_attribute('class'):
            div_dropbox_options = div_box_to_click.find_elements(by=By.CSS_SELECTOR,
                                                                 value='div.select-box-dropdown-option')
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

            # css_visibility(driver)

            try:
                div_option_to_click.click()
            except exceptions.ElementNotInteractableException:
                return False
            except exceptions.StaleElementReferenceException:
                return False
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", div_option_to_click)
                return True
            else:
                return True

        else:
            try:
                div_box_to_click.click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", div_box_to_click)
            except Exception as exc:
                print(exc)
                return False
            else:
                return True

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
            div = self.driver.find_element(by=By.XPATH, value=f"//span[text() = '{header_title}']/../..")
        except exceptions.NoSuchElementException:
            header_text_els = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                        value='div.sections > div.section > div.section-header > span:nth-of-type(2)')

            section_header_titles = [div.text
                                     for div in header_text_els]

            header_text = section_header_titles[pos]
            div = self.driver.find_element(by=By.XPATH, value=f"//span[text() = '{header_text}']/../..")

            # return section_header_titles, section_header_titles[pos]

        steps = str(div.find_element(by=By.CSS_SELECTOR, value='ul.steps').get_attribute('class')).split()

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

    def _section_loop_logic(self, header_num, li_num):

        current_section_num = 0
        while True:

            section_divs = self.driver.find_elements(by=By.CSS_SELECTOR, value="#wizardSection > div")
            len_section_divs = len(section_divs)
            if not section_divs:
                print('Section div first break')

                self._main_header_reselect(header_num)

                self.li_els = self.header_div.find_elements(by=By.CSS_SELECTOR, value='ul.steps > li')

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

                elif section_class == 'select-box-container':

                    clicked = self._section_box_handler(section)

                    # TODO - Stopped here - checking for li.steps-active and its use

                    if clicked:
                        if self.li_els[li_num].get_attribute('class') != 'steps-active':
                            print('Moving on')
                            return False
                            pass

                    # if clicked:
                    #     current_li_num += 1

                elif section_class == 'row':

                    with _SelectElHandler(self.driver) as select_h:
                        select_h(section=section)
                    with _InputElHandler(self.driver) as input_h:
                        input_h(section=section)
                    with _TextAreaHandler(self.driver) as text_h:
                        text_h(section=section)

                    # TODO - Maybe make a textarea handler

                elif section_class == 'row-compact':
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

    def _li_loop_logic(self, header_num):

        current_li_num = 0

        while True:
            self.li_els = self.header_div.find_elements(by=By.CSS_SELECTOR, value='ul.steps > li')
            len_li_els = len(self.li_els)

            for li_num in range(current_li_num, len_li_els):

                if self.li_els != self.header_div.find_elements(by=By.CSS_SELECTOR, value='ul.steps > li'):
                    break

                # TODO - Testing li_text text
                li_text = self.li_els[li_num].text
                current_li_num = li_num
                # li_text = self.li_els[li_num].find_element(by=By.CSS_SELECTOR, value="span:nth-of-type(2)").text

                self.driver.execute_script("arguments[0].click();", self.li_els[li_num])
                if li_text == 'How many other current employments do you have?':
                    print(li_text)
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

                if self.li_els != self.header_div.find_elements(by=By.CSS_SELECTOR, value='ul.steps > li'):
                    break

            else:
                return None
                # break

    def _header_loop_logic(self):

        # div_sections = self.driver.find_elements(by=By.CSS_SELECTOR,
        #                                               value='div.sections > div.section')

        header_titles_els = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                      value='div.sections > div.section > div.section-header > span:nth-of-type(2)')

        self.header_titles = [span.text
                              for span in header_titles_els]

        len_headers = len(self.header_titles)

        for header_num in range(0, len_headers):

                # TODO - Utilize the data-active attribute as it requires that the header is selected and any element within the header
            # if div_sections[header_num].get_attribute('data-active') != 'true':
            #     div_sections[header_num].click()

            self._main_header_reselect(header_num)

            # if self.header_titles[header_num] != 'Needs and objectives':
            #     continue
            if self.header_titles[header_num] == 'Documents':
                continue

            self._li_loop_logic(header_num)

    def main(self):

        self.driver.get(self.driver.current_url.split('dashboard')[0])

        self._header_loop_logic()


def main(driver: Remote):
    li_els = driver.find_elements(by=By.CSS_SELECTOR, value='#root > div > div > div:nth-child(15) > ul > li')
    for i in range(0, len(li_els)):
        li_els[i].click()
        print(li_els[i].get_attribute('class'))


if __name__ == '__main__':

    with open("new_session.json", "r") as fajlino:
        json_fajlino = json.load(fajlino)


    options = Options()

    driver_r = webdriver.Remote(command_executor=json_fajlino['url'], options=options)
    # prevent annoying empty chrome windows
    driver_r.close()
    driver_r.session_id = json_fajlino['id']
    yup = False
    test = PortalFillRewrite(driver_r)

    try:
        test.main()
    except:
        traceback.print_exc()
    else:
        yup = True
        # driver_r.quit()
    finally:
        if not yup:
            sleep(10)
            driver_r.refresh()

# 68 select-box-container
# 80 row
# 5 row-compact
# 4 empty

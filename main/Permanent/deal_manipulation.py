import traceback
from time import sleep

from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from datetime import datetime

import os

main_folder_name = 'DealScreenshots'


class Screenshot:

    def __init__(self, driver):
        self.driver = driver
        if not os.path.exists(main_folder_name):
            os.mkdir(main_folder_name)

    def toast_remover(self):
        try:
            md_toast = self.driver.find_element_by_tag_name('md-toast')
        except exceptions.NoSuchElementException:
            pass
        else:
            self.driver.execute_script("arguments[0].remove();", md_toast)
            try:
                md_toast2 = self.driver.find_element_by_tag_name('md-toast')
            except exceptions.NoSuchElementException:
                pass
            else:
                self.driver.execute_script("arguments[0].remove();", md_toast2)

        WdWait(self.driver, 10).until(ec.invisibility_of_element_located((By.TAG_NAME, 'md-toast')))

    def screenshot_helper(self, element_with_scroll, sub_section_name, deal_name, vertical=True):

        if vertical:
            scroll = 'Height'
        else:
            scroll = 'Width'

        scroll_total = self.driver.execute_script(f"return arguments[0].scroll{scroll}", element_with_scroll)
        content = self.driver.execute_script(f"return arguments[0].client{scroll}", element_with_scroll)

        scroll_new = 0
        count = 1
        while scroll_new < (scroll_total - 100):

            self.toast_remover()

            if vertical:
                self.driver.execute_script(f"arguments[0].scroll(0,{scroll_new});", element_with_scroll)
            else:
                self.driver.execute_script(f"arguments[0].scroll({scroll_new},0);", element_with_scroll)

            self.driver.get_screenshot_as_file(f'{main_folder_name}/{deal_name}/{sub_section_name} no. {count}.png')
            scroll_new += (content - 120)
            count += 1
            if content == scroll_total:
                break

    def screenshot(self, deal):

        edit_deal = 'https://' + deal.split('.', maxsplit=1)[0].split('/')[-1] + '.salestrekker.com/deal/edit/' + \
                    deal.split('/', maxsplit=4)[-1]

        self.driver.get(edit_deal)
        try:
            WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > md-content')))
        except exceptions.TimeoutException:
            self.driver.get(edit_deal)
            try:
                WdWait(self.driver, 15).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > md-content')))
            except exceptions.TimeoutException:
                self.driver.get(edit_deal)
                try:
                    WdWait(self.driver, 30).until(
                        ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > md-content')))
                except exceptions.TimeoutException:
                    print('Edit get timeout:', deal)
                    print(edit_deal)
                    traceback.print_stack()
                    self.driver.get_screenshot_as_file(f'{self.driver.current_url} {datetime.now()}.png')
                    return

        WdWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'st-sidebar-block button:nth-child(2)')))
        deal_name = (self.driver.find_element_by_css_selector('header-title > h1').text).split(':', maxsplit=1)[
            -1].lstrip()

        if not os.path.exists(f'{main_folder_name}/{deal_name}'):
            os.mkdir(f'{main_folder_name}/{deal_name}')

        print('Deal Name:', deal_name, ', Scan began:', datetime.now())

        if str(deal_name).find('/') != -1:
            deal_name = ' '.join(deal_name.split('/'))

        try:
            for button_count, button in enumerate(
                    self.driver.find_elements_by_css_selector('st-sidebar-content > st-sidebar-block > button'),
                    start=1):
                current_separator = button.find_element_by_css_selector('span.truncate').text

                current_separator_text = f'Edit Deal: {button_count}. {current_separator}'

                try:
                    button.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', button)

                content = WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))
                self.screenshot_helper(element_with_scroll=content, sub_section_name=current_separator_text,
                                       deal_name=deal_name)

        except exceptions.TimeoutException:
            print('General edit timeout:', self.driver.current_url)
            traceback.print_stack()
            return
        except:
            traceback.print_exc()
            traceback.print_stack()
            self.driver.get_screenshot_as_file(f'{self.driver.current_url} {datetime.now()}.png')

            print('Unkown exception:', self.driver.current_url)
            return

        self.driver.get(deal)
        try:
            WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > md-content')))
        except exceptions.TimeoutException:
            self.driver.get(deal)
            try:
                WdWait(self.driver, 30).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > md-content')))
            except exceptions.TimeoutException:
                print('Deal URL timeout:', deal)
                self.driver.get_screenshot_as_file(f'{deal} - Timeout.png')
                return

        # deal_name = self.driver.find_element_by_css_selector('ticket-title > h1 > span').text

        try:
            WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'st-sidebar-block button:nth-child(2)')))
        except exceptions.TimeoutException:
            try:
                WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'st-sidebar-block > div > button')))
            except exceptions.TimeoutException:
                print('No Edit deal', self.driver.current_url)
                return

        try:
            self.driver.find_element_by_xpath("//button/span[contains(text(), 'quote')]")
        except exceptions.NoSuchElementException:
            pass
        else:
            credit_quote = self.driver.find_element_by_xpath("//button/span[contains(text(), 'quote')]")
            try:
                self.driver.find_element_by_xpath("//button/span[contains(text(), 'quote')]").click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script('arguments[0].click();', credit_quote)
            WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > md-content > form-content > form')))
            content = WdWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))
            try:
                self.screenshot_helper(element_with_scroll=content, sub_section_name='Quote:',
                                       deal_name=deal_name)
            except:
                pass
            else:
                self.driver.get(deal)
                try:
                    WdWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > md-content')))
                except exceptions.TimeoutException:
                    self.driver.get(deal)
                    try:
                        WdWait(self.driver, 20).until(
                            ec.presence_of_element_located((By.CSS_SELECTOR, 'md-content > md-content')))
                    except exceptions.TimeoutException:
                        print('Deal quote timeout:', deal)
                        return

                # deal_name = self.driver.find_element_by_css_selector('ticket-title > h1 > span').text

                try:
                    WdWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.CSS_SELECTOR, 'st-sidebar-block button:nth-child(2)')))
                except exceptions.TimeoutException:
                    WdWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.CSS_SELECTOR, 'st-sidebar-block > div > button')))

        test = self.driver.find_elements_by_css_selector('st-sidebar-block button')
        test[-1].click()
        WdWait(self.driver, 20).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'st-contact')))
        try:
            for button_count, button in enumerate(
                    self.driver.find_elements_by_css_selector('st-sidebar-content > st-sidebar-block > div button'),
                    start=1):
                current_separator = button.find_element_by_css_selector('span.truncate').text

                if current_separator in ['Connect to Mercury', 'Connect to Flex']:
                    continue
                if button.get_attribute('aria-label') == 'contact.getName()':
                    current_separator_text = f'{button_count}. Contact: {current_separator}'
                else:
                    current_separator_text = f'{button_count}. {current_separator}'

                try:
                    button.click()
                except exceptions.ElementClickInterceptedException:
                    self.driver.execute_script('arguments[0].click();', button)

                sleep(1)

                if current_separator == 'Maximum borrowing':
                    try:
                        WdWait(self.driver, 15).until(
                            ec.presence_of_element_located((By.TAG_NAME, 'st-maximum-borrowing main')))
                    except exceptions.TimeoutException:
                        print('No Max Borrow', deal_name, self.driver.current_url)
                elif current_separator == 'Review loan products':
                    try:
                        WdWait(self.driver, 15).until(
                            ec.presence_of_element_located((By.TAG_NAME, 'st-review-loan-products > st-block')))
                    except exceptions.TimeoutException:
                        print('No Review', deal_name, self.driver.current_url)
                elif current_separator == 'Finance proposal':
                    sleep(2)
                elif current_separator == 'Asset commitment schedule':
                    try:
                        content = WdWait(self.driver, 10).until(
                            ec.presence_of_element_located((By.CSS_SELECTOR, '.sheet > div:nth-child(1)')))
                    except exceptions.TimeoutException:
                        pass
                    else:
                        self.screenshot_helper(element_with_scroll=content,
                                               sub_section_name=current_separator_text,
                                               deal_name=deal_name, vertical=False)
                    continue

                elif current_separator == 'Expenses':
                    content = WdWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))
                    for count, household_button in enumerate(
                            self.driver.find_elements_by_css_selector('st-tabs-list-nav > button'), start=1):
                        if 'active' in household_button.get_attribute('class'):
                            pass
                        else:
                            household_button.click()
                        self.screenshot_helper(element_with_scroll=content,
                                               sub_section_name=f'{current_separator_text}{count}', deal_name=deal_name)
                    continue

                else:
                    sleep(0.5)

                content = WdWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))
                self.screenshot_helper(element_with_scroll=content, sub_section_name=current_separator_text,
                                       deal_name=deal_name)

        except exceptions.TimeoutException:
            print('General timeout buttons:', self.driver.current_url)
            traceback.print_stack()
            return
        except:
            traceback.print_exc()
            traceback.print_stack()
            self.driver.get_screenshot_as_file(f'{self.driver.current_url} {datetime.now()}.png')
            print('Unkown exception2:', self.driver.current_url)
            return

from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
# from datetime import date

# from time import sleep
import os

from main.Permanent import workflow_manipulation
# from selenium.webdriver.common.keys import Keys


class DealManipulation:

    def __init__(self, driver, ent):
        self.ent = ent
        self.driver = driver
        self.main_url = "https://" + ent + ".salestrekker.com"
        self.wf_manipulate = workflow_manipulation.WorkflowManipulation(self.driver, self.ent)
        self.all_deals = []
        if not os.path.exists('PNG'):
            os.mkdir('PNG')

    def get_deals(self, all_deals=True, workflow_id=''):
        if all_deals:
            all_wfs = self.wf_manipulate.get_all_workflows()
            for wf in all_wfs:
                # if wf == 'https://dev.salestrekker.com/board/64682eaf-3305-43cb-99b0-b7f067e0db95':
                #     continue
                self.driver.get(wf)
                WdWait(self.driver, 15).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))
                for deal in self.driver.find_elements_by_css_selector('st-ticket-tile > a'):
                    self.all_deals.append(deal.get_attribute('href'))
            return self.all_deals
        else:
            self.driver.get(workflow_id)
            WdWait(self.driver, 15).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'body > md-content')))

    def screenshot(self, element_with_scroll, sub_section_name, deal_name):

        import traceback
        try:
            WdWait(self.driver,10).until(ec.invisibility_of_element_located((By.TAG_NAME, 'md-toast')))
        except:
            print(traceback.format_exc())

        if not os.path.exists(f'PNG/{deal_name}'):
            os.mkdir(f'PNG/{deal_name}')

        scroll_height_total = self.driver.execute_script("return arguments[0].scrollHeight", element_with_scroll)
        content_height = self.driver.execute_script("return arguments[0].clientHeight", element_with_scroll)
        print(sub_section_name)
        print('scroll height', scroll_height_total)
        print('content height', content_height)
        scroll_height_new = 0
        count = 1
        while scroll_height_new < scroll_height_total:
            self.driver.execute_script(f"arguments[0].scroll(0,{scroll_height_new});", element_with_scroll)
            self.driver.get_screenshot_as_file(f'PNG/{deal_name}/{sub_section_name} image_no. {count}.png')
            scroll_height_new += (content_height - 80)
            count += 1

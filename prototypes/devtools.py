from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.common.devtools.v95 as devtools



options = Options()
service = Service(executable_path=ChromeDriverManager(log_level=0, print_first_line=False).install())
driver = Chrome(service=service, options=options)

# devtools.emulation.set_user_agent_override()


async def geo_location_test():
    async with driver.bidi_connection() as session:
        cdp_session = session.session
        await cdp_session.execute(devtools.emulation.set_user_agent_override())

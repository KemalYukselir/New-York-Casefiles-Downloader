import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lib.handler.readIdsFile import readIds
from lib.handler.downloadEdocuments import *
from lib.captcha.solveScaptcha import *

def automatedCases():
    caseIds = readIds()
    while len(caseIds) > 0:
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('log-level=3')

            link = "https://iapps.courts.state.ny.us/webcivil/FCASMain"

            # Open chrome
            browser = webdriver.Chrome(chrome_options)
            browser.get(link)

            # Get to the index page
            indexSearch = browser.find_element("link text",'Index Search')
            indexSearch.click()

            # 2captcha solver
            print("Waiting for captcha")
            captchaToken = get_captcha()
            browser.execute_script("document.querySelector('[name=g-recaptcha-response]').innerText = '%s' " % (captchaToken)) 
            time.sleep(3)
            browser.execute_script("onCaptchaSolved()")

            # Case field search id
            WebDriverWait(browser, 25).until(EC.presence_of_element_located(("id", 'txtIndex'))).send_keys(caseIds[0])
            print("Done...")

            # Search for case
            time.sleep(2)
            actions = ActionChains(browser)
            actions.send_keys(Keys.RETURN)
            actions.perform()

            # Access file
            time.sleep(3)
            indexSearchFile = browser.find_element("link text",caseIds[0])
            indexSearchFile.click()

            # Switching tabs
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[1])

            # Click show e documents
            eDocuments = browser.find_element("name", 'showEfiledButton')
            eDocuments.click()

            # Accessing all fields on the page
            time.sleep(1)
            browser.switch_to.window(browser.window_handles[2])
            allPageFields = browser.find_elements("class name",'smallfont')

            # Downloading the cases page
            pageSource = browser.page_source
            caseIds[0] = caseIds[0].replace("/"," ")

            # Download documents
            EDocuments(browser,caseIds[0],allPageFields,pageSource)
            
            # Onto the next id
            caseIds.pop(0)
        except Exception as e:
            # Exception likely due to requests for captcha. Continue to try again
            print(e)
            print("Trying again...")
            continue




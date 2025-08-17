from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from seleniumbase import Driver

import time
from datetime import datetime, timezone
from functions import getGmailCode

from config import *

##############################################################################

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = Driver(uc=True, headless=False)

# driver = webdriver.Chrome(options=options)
driver.delete_all_cookies()

# url of specific activity
driver.get(activityUrl)

# pick number of participants
countElem = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.ID, 'reservationCount')))
countElem.clear()
countElem.send_keys(participants)

# confirm number of participants
submitBtnElem = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.ID, 'submit-btn')))  
driver.execute_script("arguments[0].click();", submitBtnElem)

# choose date and time
dateTimeElem = driver.find_elements(By.CSS_SELECTOR, f"[aria-label='{dateTime}']")[0]
driver.execute_script("arguments[0].click();", dateTimeElem)

# time.sleep(1)

# input phone number
countElem = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.ID, 'telephone')))
countElem.clear()
countElem.send_keys(phoneNumer)

# input email
countElem = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.ID, 'email')))
countElem.clear()
countElem.send_keys(bookingEmail)

# input name
countElem = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.ID, 'field2021')))
countElem.clear()
countElem.send_keys(name)

emailSentTime = datetime.now(timezone.utc)

# confirm personal details (move to verification code)
submitBtnElem = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.ID, 'submit-btn')))  
driver.execute_script("arguments[0].click();", submitBtnElem)

code = getGmailCode(emailSentTime)

if code == -1:
    print("Couldn't fetch code")
    exit()

print(f'Verification code: {code}')

# type in code
codeElem = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.ID, 'code')))
codeElem.clear()
codeElem.send_keys(code)

# confirm booking
driver.execute_script("submitCommand('SubmitContactInfoValidationCode')")
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from soupsieve import select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

mxr = {'id': "yifeng1107@hotmail.com", 'pwd': "mg201107"}
SLEEP_INTERVAL = 120
MAX_TRIES = 240 / (SLEEP_INTERVAL / 60) - 10

def LOG(s):
    print(f"{datetime.datetime.now()}: {s}")

done = False
while done == False: 
    # Log in
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(10)
    driver.get("https://ais.usvisa-info.com/en-ca/niv/users/sign_in")
    email = driver.find_element("id", "user_email")
    pwd = driver.find_element("id", "user_password")
    email.clear()
    pwd.clear()
    email.send_keys(mxr['id'])
    pwd.send_keys(mxr['pwd'])
    policy_confirmed = driver.find_element("id", "policy_confirmed")
    driver.execute_script("arguments[0].click();", policy_confirmed)
    driver.find_element("name", "commit").click()

    # Inspect time slots
    # continue_link = driver.find_element_by_partial_link_text('continue_actions')
    nTries = 0
    while True:
        nTries += 1
        LOG(f"Attemp {nTries}")
        slot_found = False
        continue_link = driver.find_element("xpath", '/html/body/div[4]/main/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a')
        continue_link.click()
        reschedule = driver.find_element("xpath", '/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/a/h5')
        reschedule.click()
        reschedule_button = driver.find_elements("xpath", '/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/div/div/div[2]/p[2]/a')[0]
        reschedule_button.click()
        while '429' in driver.title:
            time.sleep(10)
            driver.refresh()

        clicked = False
        while not clicked:
            try:
                calendar = driver.find_element("id", 'appointments_consulate_appointment_date_input')
                calendar.click()
                clicked = True
            except:
                time.sleep(10)
                driver.refresh()
        nMonthsToTry = 2
        for i in range(nMonthsToTry):
            time.sleep(0.1)
            month = driver.find_element("xpath", '/html/body/div[5]/div[1]/table/tbody')
            dates = month.find_elements(By.TAG_NAME, 'td')
            for date in dates:
                date_class = date.get_attribute('class')
                if date_class == ' undefined':
                    slot_found = True
                    break

            if slot_found:
                LOG("Slot found!")
                date_confirm_button = date.find_element(By.TAG_NAME, 'a')
                date_confirm_button.click()
                LOG("Date confirmed!")
                time.sleep(1)
                time_slot_select = Select(driver.find_element("xpath", '/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select'))
                time_slot_select.select_by_index(len(time_slot_select.options) - 1)
                LOG("Time confirmed!")
                time.sleep(1)
                commit_button = driver.find_element("xpath", '/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/li/input')
                commit_button.click()
                LOG("Commited!")
                time.sleep(1)
                # cancel_button = driver.find_element_by_xpath('/html/body/div[6]/div/div/a[1]')
                # cancel_button.click()
                confirm_button = driver.find_element("xpath", '/html/body/div[6]/div/div/a[2]')
                confirm_button.click()
                LOG("Confirmed!")
                break
            else:
                next_month_button = driver.find_element("xpath", '/html/body/div[5]/div[2]/div/a')
                next_month_button.click()
        
        if slot_found:
            LOG("SLot confirmed!")
            done = True
            break

        close_button = driver.find_element("xpath", '/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/a')
        close_button.click()
        if nTries >= MAX_TRIES:
            LOG("Max limit reached, restarting in 1 hour")
            time.sleep(3600)
            nTries = 0
        else:
            time.sleep(SLEEP_INTERVAL)


driver.close()
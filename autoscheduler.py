from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, NoSuchWindowException

import math
import os
import json
import time

driver = webdriver.Chrome()

print(
    "Opening ICBC website at https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver"
)

driver.get("https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver")

lastName = ""
licenseNumber = ""
keyword = ""

# save in parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
file_path = os.path.join(parent_dir, "icbcinfo.json")

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    lastName = data["lastName"]
    licenseNumber = data["licenseNumber"]
    keyword = data["keyword"]

else:
    # save user info in json if json file does not exist
    lastName = input("Last name: ")
    licenseNumber = input("BC license number: ")
    keyword = input("ICBC keyword: ")
    info = {
        "lastName": lastName,
        "licenseNumber": licenseNumber,
        "keyword": keyword,
    }
    with open(file_path, "w") as f:
        json.dump(info, f)
    print("info saved in icbcinfo.json in path: ", file_path)

print(
    "Logging in with "
    + "\nlastName: "
    + lastName
    + " "
    + "\nlicenseNumber: "
    + licenseNumber
    + " "
    + "\nkeyword: "
    + ("*" * len(keyword))
)

fields = driver.find_elements(By.TAG_NAME, "input")
fields[0].send_keys(lastName)
fields[1].send_keys(licenseNumber)
fields[2].send_keys(keyword)


checkbox = driver.find_element(
    By.XPATH,
    "/html/body/app-root/app-login/mat-card/mat-card-content/form/span[2]/div[3]/mat-checkbox/label/span[1]",
)
checkbox.click()

submit = driver.find_element(
    By.XPATH,
    "/html/body/app-root/app-login/mat-card/mat-card-content/form/div[2]/div[2]/button",
)

submit.click()


# find reschedule button after user has landed on https://onlinebusiness.icbc.com/webdeas-ui/driver

while True:
    try:
        rescheduleButton = driver.find_element(
            By.XPATH,
            "/html/body/app-root/app-driver/div/mat-card/div[5]/div[1]/app-appointments/div/div[2]/div/div[4]/button[1]",
        )
        break
    except WebDriverException:
        print("login success, waiting for page to load")
        time.sleep(1)

rescheduleButton.click()

yesButton = driver.find_element(By.CSS_SELECTOR, "button.primary.ng-star-inserted")
yesButton.click()

# wait for https://onlinebusiness.icbc.com/webdeas-ui/booking

time.sleep(1)

searchForms = driver.find_element(
    By.XPATH,
    "/html/body/div/div/div/mat-dialog-container/app-search-modal/div/div/form/div[1]/mat-tab-group/div/mat-tab-body[1]/div/div/mat-form-field/div/div[1]",
)
searchForms.click()

inputField = driver.find_element(
    By.XPATH,
    "/html/body/div/div/div/mat-dialog-container/app-search-modal/div/div/form/div[1]/mat-tab-group/div/mat-tab-body[1]/div/div/mat-form-field/div/div[1]/div[3]/input",
)

inputField.send_keys("Kelowna, BC")


# I GIVE UP!!! I CANT GET THE SEARCH TO WORK


# searchButton = driver.find_element(By.CLASS_NAME, "mat-raised-button")
# searchButton.click()

time.sleep(20)

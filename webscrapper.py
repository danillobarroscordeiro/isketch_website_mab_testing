from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import time

path_webdriver ='/home/dbcordeiro/repos/isketch_website_mab_testing/chromedriver_linux64/chromedriver'
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(path_webdriver), options=options )

driver.get('http://127.0.0.1:5000/home')

clicks=10000
for click in range(clicks):
    button_color = driver.find_element('name', 'yescheckbox').get_attribute('value')

    if button_color == 'blue':
        if np.random.random() < 0.3:
            driver.find_element( 'name', 'yescheckbox').click()
            driver.find_element('id', 'yesbtn').click()
            time.sleep(1)
        else:
            driver.find_element( 'name', 'nocheckbox').click()
            driver.find_element('id', 'nobtn').click()
            time.sleep(1)
    else:
        if np.random.random() < 0.35:
            driver.find_element( 'name', 'yescheckbox').click()
            driver.find_element('id', 'yesbtn').click()
            time.sleep(1)
        else:
            driver.find_element( 'name', 'nocheckbox').click()
            driver.find_element('id', 'nobtn').click()
            time.sleep(1)

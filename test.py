import os
import sys
import time
from time import sleep
from selenium import webdriver
 
##
## More help on writing tests: 
## => http://selenium-python.readthedocs.org/en/latest/navigating.html
##
 
def log(msg):
    print (time.strftime("%H:%M:%S") + ": " + msg)
 
appium_URL = 'http://appium.testdroid.com/wd/hub';
 
screenshot_path = '/Users/your/local/path/here/for/screenshots';
 
desired_caps = {}
desired_caps['testdroid_username'] = 'firstname.lastname@email.com'
desired_caps['testdroid_password'] = 'xxxxx'
desired_caps['testdroid_target'] = 'chrome'
desired_caps['testdroid_project'] = 'Appium Chrome'
desired_caps['testdroid_testrun'] = 'TestRun 1'
desired_caps['testdroid_device'] = 'Asus Google Nexus 7 (2013) ME571KL'
desired_caps['platformName'] = 'android'
desired_caps['deviceName'] = 'AndroidDevice'
desired_caps['browserName'] = 'chrome'
 
log ("WebDriver request initiated. Waiting for response, this may take a while.")
driver = webdriver.Remote(appium_URL,desired_caps)
 
log ("Taking screenshot of home page: '0_chromeLaunched.png'")
driver.save_screenshot(screenshot_path + "/0_chromeLaunched.png")
 
log ("Loading page")
driver.get("http://testdroid.com")
log ("Taking screenshot of home page: '1_home.png'")
driver.save_screenshot(screenshot_path + "/1_home.png")
 
log ("Finding 'Products'")
elem = driver.find_element_by_xpath('//*[@id="menu"]/ul/li[1]/a')
log ("Clicking 'Products'")
elem.click()
 
log ("Taking screenshot of 'Products' page: '2_products.png'")
driver.save_screenshot(screenshot_path + "/2_products.png")
log ("Finding 'Learn More'")
elem = driver.find_element_by_xpath('//*[@id="products"]/div[1]/div/div[1]/div[3]/a')
log ("Clicking 'Learn More'")
elem.click()
 
log ("Taking screenshot of 'Learn More' page: '3_learnmore.png'")
driver.save_screenshot(screenshot_path + "/3_learnmore.png")
log ("Finding 'Supported Frameworks'")
elem = driver.find_element_by_xpath('//*[@id="topMenu"]/div[1]/div/a[2]')
log ("Clicking 'Supported Frameworks'")
elem.click()
 
log ("Taking screenshot of 'Supported Framworks' page: '4_supportedframeworks.png'")
driver.save_screenshot(screenshot_path + "/4_supportedframeworks.png")
log ("quitting")
driver.quit()
sys.exit()

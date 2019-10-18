from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# get Grubhub
browser = webdriver.Chrome()
browser.get('https://www.grubhub.com/')

# username and password
username = 'medrosadam@gmail.com' #"pooollabs@gmail.com"
password = 'adamMedros1!' #"poolLabs1!"

# food info
time = ''
address = ''
food = ''

def sign_in(browser, username, password):
    browser.implicitly_wait(1) # wait a second before going to sign in page
    sign_in_link = browser.find_element_by_link_text('Sign in')
    sign_in_link.click()

    # enter email and password
    email_elem = browser.find_element_by_id('email')
    email_elem.send_keys(username)
    password_elem = browser.find_element_by_id('password')
    password_elem.send_keys(password)
    browser.implicitly_wait(1) # wait a second before signing in
    
    # click sign in button
    sign_in_link = browser.find_element_by_xpath("//button[1]")
    sign_in_link.click()

# sign in
sign_in(browser, username, password)

# enter food options


# browser.quit()





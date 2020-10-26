import numpy as np
import time
import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Change current working directory to main directory
def main_directory(directory):
    """Load in .yml file to retrieve location of current working directory"""
    while True:
        try:
            info = yaml.load(open("info.yml"), Loader=yaml.FullLoader)
            os.chdir(os.getcwd() + info[directory])
        except FileNotFoundError:
            os.chdir(os.path.expanduser("~") + "/Projects")
            continue
        break
main_directory(directory="poshmark_directory")

def get_seller_page_url(username):
    """Obtain seller's page"""
    url_stem = 'https://poshmark.com/closet/'
    available = '?availability=available'
    url = '{}{}{}'.format(url_stem, username, available)
    return url

def get_user_main_page_url(username):
    """Obtain user's main page"""
    url_stem = 'https://poshmark.com/closet/'
    url = '{}{}'.format(url_stem, username)
    return url

def clicks_share_followers(share_icon):
    ## First share click
    driver.execute_script("arguments[0].click();", share_icon)
    time.sleep(np.random.choice(seconds, size=1)[0])

    ## Second share click
    ### share_pat = "//a[@class='pm-followers-share-link grey']"
    share_pat = "//div[@class='share-wrapper-container']"
    share_followers = driver.find_element(by='xpath', value=share_pat)
    driver.execute_script("arguments[0].click();", share_followers)
    time.sleep(np.random.choice(seconds, size=1)[0])

# Load in user info
user_info = yaml.load(open("user_info.yml"), Loader=yaml.FullLoader)

# List of seconds to sleep
seconds = np.arange(2,5)
# Amount of time to sleep between shares
share_sleep = 60*60*2

# Webdriver options
options = Options()
# Make call to Chrome headless
# options.add_argument('--headless')
# Define Chrome webdriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
url = "https://poshmark.com/login"
# Supply url
driver.get(url=url)

# Find username and supply
username = driver.find_element(by='name', value="login_form[username_email]")
username.send_keys(user_info['user']['jordan']['username'])
# Sleep for random time
time.sleep(np.random.choice(seconds, size=1)[0])

# Find password and supply
password = driver.find_element(by='name', value="login_form[password]")
password.send_keys(user_info['user']['jordan']['password'])
# Sleep for random time
time.sleep(np.random.choice(seconds, size=1)[0])

# Attempt to login with username and password
password.send_keys(Keys.RETURN)

### Write code to do captha

### After successfully logged in

while True:
    # Sleep for random time
    time.sleep(np.random.choice(seconds, size=1)[0])
    # Navigate to seller page
    seller_page = get_seller_page_url(username="jwilson3723")
    # Go to seller's page
    driver.get(seller_page)
    # Sleep for random time
    time.sleep(np.random.choice(seconds, size=1)[0])
    # Find items for sell using xpath
    ### items = driver.find_elements_by_xpath("//div[@class='social-info social-actions d-fl ai-c jc-c']")
    items = driver.find_elements(by='xpath', value="//div[@class='social-action-bar tile__social-actions']")
    # Find share icon for items
    ### share_icons = [i.find_element_by_css_selector("a[class='share']") for i in items]
    share_icons = [i.find_element(by='css selector', value="div[data-et-name='share']") for i in items]
    # Reverse order of share icons to preserve closet order
    share_icons.reverse()
    # Print number of items to share
    print(f"Number of items to share: {len(share_icons)}")
    # Obtain item number for bundle item for use later
    bundle_item_order_number = len(share_icons)
    # Share listings
    [clicks_share_followers(item) for item in share_icons]

    ### Share bundle purchase saver
    # Sleep for random time
    time.sleep(np.random.choice(seconds, size=1)[0])
    # Navigate to user's main page
    user_main_page = get_user_main_page_url(username="jwilson3723")
    # Go to user's main page
    driver.get(user_main_page)
    # Sleep for random time
    time.sleep(np.random.choice(seconds, size=1)[0])
    # Obtain bundle item
    ### bundle_item = driver.find_elements_by_xpath("//div[@class='social-info social-actions d-fl ai-c jc-c']")[bundle_item_order_number]
    bundle_item = driver.find_elements(by='xpath', value="//div[@class='social-action-bar tile__social-actions']")[bundle_item_order_number]
    # Find share icon for item
    ### bundle_item = bundle_item.find_element_by_css_selector("a[class='share']")
    bundle_item = bundle_item.find_element(by='css selector', value="div[data-et-name='share']")
    # Share bundle item
    clicks_share_followers(bundle_item)
    print(f"Time of completed sharing: {time.strftime('%A %B %d, %Y %I:%M:%S %p')}.")
    # Sleep for 2 hours
    time.sleep(share_sleep)

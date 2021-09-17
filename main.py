from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import pandas as pd
from prettytable import PrettyTable

## locating driver in system
# chrome_path = which("chromedriver")

## adding options 
chrome_options = Options()

## option for headless browser
chrome_options.add_argument("--headless")

## setting window size to regular
chrome_options.add_argument("--window-size=1280,1080")

## setting driver path
driver = webdriver.Chrome(executable_path="path-to-chromedriver", options=chrome_options)

## base_URL for web scrapping 
base_URL = "https://www.zoopla.co.uk/"
driver.get(base_URL)

## locating serach bar
search_input = driver.find_element_by_id("header-location")

## input text in search bar
search_input.send_keys("London")
search_input.send_keys(Keys.ENTER)

## all items on search page
items = driver.find_elements_by_xpath(
    "//div[@class='css-1anhqz4-ListingsContainer earci3d2']/div")

"""
## Handling pagination
next_page_flag = True

while next_page_flag:
    next_page = driver.find_element_by_link_text("Next >")
    if next_page:
        next_page.click()
        
        ## dismissing popup
        driver.switch_to().alert().dismiss()

        items.append(driver.find_elements_by_xpath("//div[@class='css-1anhqz4-ListingsContainer earci3d2']/div"))
        
    else:
        next_page_flag = False
        break
"""


## 'collection' for storing list of houses info
collection = []

for item in items:
    driver.implicitly_wait(2)
    ## Pulling info
    title = item.find_element_by_xpath(
    ".//a[@data-testid='listing-details-link']/h2[@data-testid='listing-title']").text
    address = item.find_element_by_xpath(".//a[@data-testid='listing-details-link']/p[@data-testid='listing-description']").text
    price = item.find_element_by_xpath(".//div[@data-testid='listing-price']/p[@class='css-1o565rw-Text eczcs4p0']").text
    contact_detail = item.find_element_by_xpath(".//a[@data-testid='agent-phone-number']").text
    publish_date = item.find_element_by_xpath(".//span[@data-testid='date-published']").text

    ## adding a house info to collection
    collection.append(
        [title, address, price, contact_detail, publish_date[10:]]
    )

## converting our data to df
# df = pd.DataFrame(collection, columns=['title', 'address', 'price', 'contact_detail', 'publish_date'])
# print(df)

## converting our data to table
houses_info = PrettyTable(
    ['title', 'address', 'price', 'contact_detail', 'publish_date']
)
## adding rows to table 
houses_info.add_rows(collection);
## printing table containing houses' info
print(houses_info)

## printing source page in case of headless browser
# print(driver.page_source)
driver.quit()

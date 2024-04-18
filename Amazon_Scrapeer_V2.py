import pandas as pd
import time
import pprint as pp
from bs4 import BeautifulSoup
from IPython.display import display
from urllib.error import HTTPError
from selenium import webdriver as wb
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

# Setting up the webdriver for Selenium
service = Service()
options = wb.ChromeOptions()
ua = UserAgent()
user_agent = ua.random
options.add_argument(f'--user-agent={user_agent}')
options.add_argument('--start-maximized')
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = wb.Chrome(service=service, options=options)
driver.set_window_size(500, 500)

# Setting up a dictionary to hold the data
data_dict = {
    'Asin': [],
    # 'Model_Number': [],
    'Product_Title': [],
    'Price': [],
    'Ship_From': [],
    'Sold_By': []
}

# Setting up a seperate dictionary to hold product info
dict_list = []

asin_list = [
'Asin list'
]

for asin in asin_list:
    # Adding the sku to the mc_dict Sku column
    data_dict['Asin'].append(asin)

    try:
        # Extracting the page source for the sku from Signature Hardwares website and creating a soup object
        page = 'https://www.amazon.com/dp/{}?th=1'.format(asin)
        driver.get(page)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # Extracting product title
        try:
            title_main = soup.find("h1", {"id": "title"})
            title = title_main.find("span", {"id": "productTitle"})
            title = title.text
            data_dict['Product_Title'].append(title.strip())
        except:
            data_dict['Product_Title'].append('NULL')

        # Extracting price
        try:
            price_main = soup.find("div", {"class": "a-section a-spacing-micro"})
            price = price_main.find("span", {"class": "a-offscreen"})
            price = price.text
            data_dict['Price'].append(price)
        except:
            data_dict['Price'].append('NULL')

        # Extracting ship from
        try:
            main_span = soup.find("div", {"class": "offer-display-feature-text a-spacing-none"})
            ship = soup.find("span", {"class": "a-size-small offer-display-feature-text-message"})
            data_dict['Ship_From'].append(ship.text)
        except:
            data_dict['Ship_From'].append('NULL'
                                        )
        # Extracting sold by
        try:
            main_span = soup.find_all("span", {"class": "a-size-small offer-display-feature-text-message"})
            sold = main_span[1].text
            data_dict['Sold_By'].append(sold)
        except:
            data_dict['Sold_By'].append('NULL') 
        
        pp.pprint(data_dict)
        time.sleep(1)
    
    except HTTPError as hp:
        print(hp)

# quitting the driver and manipulation the dictionary into a dataframe
driver.quit()

# Creating a dataframe from the data dictionary
amazon_df = pd.DataFrame.from_dict(data_dict, orient='index').fillna('NULL')
amazon_df = amazon_df.transpose()
display(amazon_df)

#  Writing the dataframe to an excel worksheet
amazon_df.to_excel('Amazon_Data.xlsx', sheet_name='Data')

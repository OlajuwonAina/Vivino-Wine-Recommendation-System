import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import numpy as np

# connecting to the browser
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome()

# defining the url
url = "https://www.vivino.com/US/en/"
driver.get(url)

# we will have to navigate to the homepage and then click on the wines link to go to the wines pages before scraping

page = driver.find_element(By.CLASS_NAME, 'menuLink_text__nDfIV').click()

# after navigating into the wines page, we then wait for 15 seconds before scraping
time.sleep(10)
print("Wait for 10 seconds")

# Here, we will deselect all the types of wines
the_buttons = driver.find_elements(By.CLASS_NAME, 'filterByWineType__pill--DDMJ3')
print(the_buttons)

# <label class="pill__pill--2AMAs pill__selected--3KX2r filterByWineType__pill--DDMJ3"><input type="checkbox" data-testid="wineTypes_7" value="7"><div class="pill__inner--2uty5"><span class="pill__text--24qI1">Dessert</span></div></label>
# the_buttons= driver.find_elements_by_xpath('')
time.sleep(5)

not_click = the_buttons[0]
for button in the_buttons[:4]:
    if button != not_click:
        button.click()
        time.sleep(3)

# We want to click on the all rating radio button to collect all ratings 
driver.find_elements(By.CLASS_NAME, '_2K-I_')[-1].click() 
time.sleep(3)

# I want to increase the price slider and wait for 3 seconds
the_slider = driver.find_element(By.CLASS_NAME, 'rc-slider-handle-2')
ActionChains(driver).move_to_element(the_slider).perform()
ActionChains(driver).drag_and_drop_by_offset(the_slider, 200, 0).perform()
ActionChains(driver).release().perform()
time.sleep(3)


times=0
while(times < 20) :
    print(f"Page scrolling: {(times + 1)} time(s)")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(8)
    times += 1


the_result = driver.find_elements(By.CLASS_NAME, 'wineCard__wineCard--2dj2T')
time.sleep(5)
print(f"{len(the_result)} Red Wine found!")

my_result_list = []
for item in the_result:

    try:
        Winery = item.find_element(By.CLASS_NAME, 'wineInfoVintage__truncate--3QAtw').text
    except:
        Winery = np.nan
    try:
        name = item.find_element(By.CLASS_NAME, 'wineInfoVintage__vintage--VvWlU').text
        
    except:
        name = np.nan
        vintage =np.nan
    try:
        location = item.find_element(By.CLASS_NAME, 'wineInfoLocation__wineInfoLocation--BmkcO').text
        Region=location.split(',')[:-1]
        Region=' '.join(Region)
        
        Country = location.split(',')[-1]
    except: 
        Region= np.nan
        Country=np.nan
    try:
        rating = item.find_element(By.CLASS_NAME, 'vivinoRating_averageValue__uDdPM').text
    except:
        rating = np.nan
    try:
        nbr_ratings = item.find_element(By.CLASS_NAME, 'vivinoRating_caption__xL84P').text
        nbr_rating = nbr_ratings.split(' ')[0]
    except:
        nbr_rating = np.nan
    try:
        price = item.find_element(By.CLASS_NAME, 'addToCartButton__price--qJdh4 div:nth-child(2)').text
    except:
        price = item.find_element(By.CLASS_NAME, 'addToCart__ppcPrice--ydrd5').text
        
    temp_dict = {"Winery":Winery, "Name":name, "Region":Region, "Country":Country, "Rating":rating, "Number of Ratings":nbr_rating,"Wine Type":"Red", "Price":price}
    my_result_list.append(temp_dict)
    print(f"Wine No. {len(my_result_list)} scrapped")
    
    
# convert it to a pandas dataframe so it can be saved to a csv file
df = pd.DataFrame(my_result_list)
df.to_csv('vivino_wines_dataset_red.csv', index = False)

driver.close()


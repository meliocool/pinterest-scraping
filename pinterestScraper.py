from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import os
import requests
import urllib.parse

options = Options()
options.headless = True  
driver = webdriver.Firefox(options=options)

def scroll_down_page(driver, wait_time=2):
    current_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        time.sleep(wait_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == current_height:
            break
        current_height = new_height

memberSearch = input("Enter the member name: ") 
encoded_search = urllib.parse.quote(memberSearch) 
search_url = f"https://www.pinterest.com/search/pins/?q={encoded_search}"
driver.get(search_url)

scroll_down_page(driver, wait_time=2)

soup = BeautifulSoup(driver.page_source, 'html.parser')

images = soup.find_all('img')

output_dir = f'C:/Users/Asus VivobookPro/Documents/CODING STUFF/AI/SimpleProjects/is_it_an_S/training_images/{memberSearch}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for index, img in enumerate(images):
    img_url = img.get('src') or img.get('data-src') or img.get('data-fallback-src')
    if img_url:
        try:
            img_data = requests.get(img_url).content
            with open(os.path.join(output_dir, f"{memberSearch}_{index}.jpg"), 'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded image {index}")
        except Exception as e:
            print(f"Failed to download image {index}: {e}")

driver.quit()
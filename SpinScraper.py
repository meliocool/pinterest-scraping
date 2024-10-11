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

def scroll_down_page(driver, wait_time=3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(wait_time)

memberSearch = input("Enter the member name: ")
folder_name = input("Enter the folder name: ") 
encoded_search = urllib.parse.quote(memberSearch)
search_url = f"https://www.pinterest.com/search/pins/?q={encoded_search}"
driver.get(search_url)

output_dir = f'C:/Users/Asus VivobookPro/Documents/CODING STUFF/AI/SimpleProjects/is_it_an_S/training_images/{folder_name}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

image_count = 0
previous_image_count = -1 

downloaded_images = set()

while True:
    scroll_down_page(driver, wait_time=5)  

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    images = soup.find_all('img')

    if image_count == previous_image_count:
        print("No new images found, Scraper Terminated.")
        break
    previous_image_count = image_count

    for img in images:
        img_url = img.get('src') or img.get('data-src') or img.get('data-fallback-src')
        if img_url and img_url not in downloaded_images:
            try:
                img_data = requests.get(img_url).content
                with open(os.path.join(output_dir, f"{memberSearch}_{image_count}.jpg"), 'wb') as handler:
                    handler.write(img_data)
                downloaded_images.add(img_url)
                image_count += 1
                print(f"{memberSearch} {image_count} Downloaded")
            except Exception as e:
                print(f"Failed to download image {image_count}: {e}")
driver.quit()

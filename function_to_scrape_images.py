import os
from selenium import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup


# functions definition:

def main():
    folder_to_save_images = input("Input the folder name to save the image:  ")
    
    if not os.path.exists(folder_to_save_images):
        os.mkdir(folder_to_save_images)
        os.chdir(folder_to_save_images)
    print("Scraping in Progress".center(100,'-'))
    ImageScraper()

# This function automates the process of scrolling through the webpages for sites that lazy loads
def scroll_up(driver_obj):
    last_height = driver_obj.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to end
        driver_obj.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #Allow some secs for page to load
        sleep(5)

        # Determine and compare new vs last scroll, if same, break out
        #Could be same if your internet is slow and it has not finished loading the page. 
        new_height = driver_obj.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
 # The function that does the scraping:       
def ImageScraper():
    
    url = input("Paste URL :  ")    
    #this defines path to ChromeDriver , edit if it's not in the same directory as your script:
    chromedriver_path = r"chromedriver.exe"
        
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(url)

    scroll_up(driver)

    file = open('DS.html', 'w')
    file.write(driver.page_source)
    file.close()

    driver.close()
    
    data = open('DS.html','r')
    soup = BeautifulSoup(data, 'html.parser')
    images = soup.find_all('img')
    count = 0
     
    for image in images[1:]:
        try:
            link = image['src']
        except:
            pass
        # This code block was peculiar to scraping images off google,  it can be adjusted;
        if link[:4] != 'data':
            count += 1
            with open(str(count) + '.jpg', 'wb') as f:
                im = requests.get(link)
                f.write(im.content)
                print('Saving: Image_', str(count))

        
        
                
if __name__ == "__main__":
    main()
    
# sample Output:
# Input the folder name to save the image:  scraped images 1
# ----------------------------------------Scraping in Progress----------------------------------------
# Paste URL : 
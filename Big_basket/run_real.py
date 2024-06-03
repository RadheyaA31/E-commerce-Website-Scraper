import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import os
import requests
from PIL import Image  # Import the Image class from PIL
from io import BytesIO

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument("--disable-infobars")

driver = webdriver.Chrome(options=chrome_options)

url="https://www.bigbasket.com"

driver.get(url)

driver.implicitly_wait(30)

category_button=driver.find_element(By.ID,'headlessui-menu-button-:R5bab6:')

category_button.click()

box=driver.find_element(By.XPATH,'//*[@id="headlessui-menu-items-:R9bab6:"]/nav/ul[1]')

categories=box.find_elements(By.XPATH,
'//*[@id="headlessui-menu-items-:R9bab6:"]/nav/ul[1]/li')

#print(len(categories))
#print(type(categories))

#list of column names
columns=['Product_Name','Product_Amount','Product_price']

#list of categories
list_of_categories_names=[]

#list of categories elements
list_of_categories_elements=[]

for category in categories:
    #print(category.text)
    list_of_categories_elements.append(category)#after appending the newestname,element is added at the end
    list_of_categories_names.append(category.text)
    
#print(list_of_categories_names)
#print(list_of_categories_elements)

print("Which of the following Categories you like to select?")

print("Options" , end=' : ')

for category_name in list_of_categories_names:
    
    if category_name==list_of_categories_names[-1]:
        print(category_name)
    else:
        print(category_name,end=" , ")
while True:
    global user_category_choice
    user_category_choice = input("Enter a category name: ")

    # Convert items of the categories name list to lowercase
    lowercase_list = [item.lower() for item in list_of_categories_names]

    if user_category_choice.lower() in lowercase_list:
        # Get the index of the lowercase input in the lowercase list
        index = lowercase_list.index(user_category_choice.lower())

        user_category_choice = list_of_categories_names[index]
        # Click the corresponding element
        list_of_categories_elements[index].click()
        
        print("Clicked on The Element.")
        
        break
    else:
        print("No such category exists. Try again!")


time.sleep(5)

#Product li updater limiter (to limit the amount of times li will be updated)
product_li_updater_limiter=3
#Number of time Li should be updated
product_li_updater_counter=0
#List container to contain all the 'li' we have gone through
#readed_li=[]

product_names=[]
product_amounts=[]
product_prices=[]
product_img_url=[]
product_urls=[]
x_number=0

while product_li_updater_counter<product_li_updater_limiter:

    # Number of scrolls
    # Input from the user
    scroll_increment = 500  # Pixels to scroll in each step
    max_scrolls = 15
    scroll_pause_time = 2  # Pause to allow content to load

    # Scroll incrementally
    for _ in range(max_scrolls):
        # Scroll down by a fixed number of pixels
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")

        # Wait to load the new content
        time.sleep(scroll_pause_time)


    body=driver.find_element(By.TAG_NAME, 'body')
    body_innerHTML=body.get_attribute('innerHTML')

    product_table=driver.find_element(By.XPATH,'//*[@id="siteLayout"]/div[5]/div[2]/section[2]/section/ul')
    #print('-1')
    # Use CSS selector to locate all product list items
    
    product_li = product_table.find_elements(By.CSS_SELECTOR, 'li[class*="PaginateItems"]')
    if not product_li:
        print("No elements found with the specified class name.")
        print(product_table.get_attribute('outerHTML'))  # Print the HTML to verify the structure
        driver.quit()
        exit()
    
        
    html_inside=product_table.get_attribute('innerHTML')
    
    driver.implicitly_wait(10)
    product_li_updater_counter+=1

def li_data_extractor(x_number,product_li):
    #global x_number
    #global product_li
    while x_number<len(product_li):
        product_info=product_li[x_number]
        product_info=product_info.find_element(By.XPATH,'./div/div')
        #print(prodcut_li[x_number].text)
        #print('1')
        product_info_img_container=product_info.find_element(By.XPATH,'./div')
        # Find all <img> tags within the container
        img_tag = product_info_img_container.find_elements(By.XPATH, './/img')

        # Directory to save the images (sibling to the current directory)
        current_dir = os.getcwd()  # Use the current working directory
        #current_dir = os.path.dirname(os.path.abspath(__file__))
        #The __file__ variable may not be defined when running the script in certain environments, such as Jupyter notebooks or interactive Python interpreters. To handle this, you can use the current working directory obtained via os.getcwd() instead of os.path.abspath(__file__).
        save_dir = os.path.join(current_dir, '.', f'{user_category_choice.upper()}')#now we will only go one directory outside(above)
        #!for '..'# we need to go two directories outside(above)


    # Create the directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)


        #print(len(img_tag))
        if len(img_tag)==0:
            print("Fucntion has ended!!")
            return  # Exit the function
            
        else:
            #print(type(img_tag))
            # Get the URL of the image
            img_url = img_tag[0].get_attribute('src')
            #print(img_url)
            product_img_url.append(img_url)
            # Ensure the URL is absolute
        if not img_url.startswith('http'):
            img_url = f'https://example.com{img_url}'
        product_info_h3_container=product_info.find_element(By.XPATH,'./h3')



        product_name=product_info_h3_container.find_element(By.XPATH,'.//a/div')
        #print(product_name.text)
        product_names.append(product_name.text)
        # Download and save the image with headers
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            img_data = requests.get(img_url, headers=headers)
            img_data.raise_for_status()  # Check if the request was successful

            # Use PIL to verify and save the image properly
            image = Image.open(BytesIO(img_data.content))

            # Create a valid filename by replacing invalid characters
            img_name = product_name.text.replace('/', '_').replace('\\', '_')
            img_name = f"{img_name}.jpg"
            img_path = os.path.join(save_dir, img_name)
            # Convert WebP to JPG if necessary
            if image.format == 'WEBP':
                img_name = img_name.replace('.jpg', '.webp')
                img_path = os.path.join(save_dir, img_name)
                image.save(img_path, 'WEBP')
            else:
                image.save(img_path, 'JPEG')

            #print(f'Image saved at {img_path}')
        except Exception as e:
            print(f"Failed to save image {img_name}: {e}")
            
            
        #getting image <a> ancestor tag to then get its url
        
        product_url_element=img_tag[0].find_element(By.XPATH,'./ancestor::a')
        product_url=product_url_element.get_attribute('href')
        product_urls.append(product_url)
        #print('2')
        product_amount_list=product_info_h3_container.find_elements(By.XPATH,'.//div//span')
        
        product_amount=product_amount_list[-1]
        #print(product_amount.text)
        product_amounts.append(product_amount.text)
        # Find element that contains the '₹' symbol

        #print('3')
        #finds an div element that has direct child as a element that contiains '₹' 
        product_price_parent_tag= product_info.find_element(By.XPATH, ".//div[*[contains(text(), '₹')]]")
        product_price=product_price_parent_tag.find_element(By.XPATH, "./*[contains(text(), '₹')]")

        #print(product_price.get_attribute('innerHTML'))
        product_prices.append(product_price.get_attribute('innerHTML'))
        x_number+=1
        

def product_data_saver_in_excel(product_names,product_amounts,product_prices,product_urls):
    # Create a dictionary with the data
    data = {
        'Prodcut_Name': product_names,
        'Category_Name': user_category_choice,
        'Product_Amount': product_amounts,
        'Product_price': product_prices,
        'Product_url':product_urls,
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)

    # Define the path to save the Excel file
    excel_file_path = './product_data.xlsx'

    # Save the DataFrame to an Excel file
    df.to_excel(excel_file_path, index=False)
    print(f"Data has been successfully saved to {excel_file_path}")

li_data_extractor(x_number,product_li)
product_data_saver_in_excel(product_names,product_amounts,product_prices,product_urls)
print('Program has ended!!')
driver.quit()
import json
import random
import time
import pyautogui # the action thing was giving errors so now ..using pyautogui to move cursor on pc itself
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from broweserAutomation import BrowserAutomation#a file i created which contains a class with functions realted to browser Automation


# Main function
def main():
    coordinates = BrowserAutomation.load_coordinates()

    try:
        selected_coordinates = BrowserAutomation.get_random_coordinates_range(coordinates)
    except ValueError as e:
        print(e)
        return

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.bigbasket.com"
    driver.get(url)

    time.sleep(20)

    automation = BrowserAutomation(driver)


    # Perform actions using Selenium
    try:
        automation.perform_actions(selected_coordinates)
    except Exception as e:
        print(f"Error while performing actions: {e}")

    # Quit the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()

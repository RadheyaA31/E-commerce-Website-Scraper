import json
import random
import time
import pyautogui # the action thing was giving errors so now ..using pyautogui to move cursor on pc itself
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class BrowserAutomation:
    def __init__(self, driver):
        self.driver = driver


    # Load coordinates from JSON file
    @staticmethod
    def load_coordinates(filename='coordinates.json'):
        with open(filename, 'r') as file:
            return json.load(file)

    # Function to get random range of coordinates
    @staticmethod
    def get_random_coordinates_range(coordinates):
        length = len(coordinates)
        print(length)
        if length == 0:
            raise ValueError("The coordinates list is empty.")
        
        random_index = random.randint(0, length - 1)
        end_index = min(random_index + 500, length)#this min() ensures that end_index does not exceed length
        
        return coordinates[random_index:end_index]


    # Function to simulate moving the cursor to specified coordinates
    @staticmethod
    def move_cursor(x, y):
        start_time = time.time() # Record the start time
        pyautogui.moveTo(x, y, duration=0) # Move cursor to (x, y) without any duration
        end_time = time.time() # Record the end time
        movement_time = end_time - start_time # Calculate the time taken for cursor movement
        print(f"Time taken for cursor movement: {movement_time} seconds")


    # Function to perform click action at the current cursor position
    @staticmethod
    def perform_click():
        pyautogui.click()# Perform left-click action


    # Function to perform actions using Selenium
    def perform_actions(self, coordinates):
        reference_element = self.driver.find_element(By.TAG_NAME, 'body')
        actions = ActionChains(self.driver)
        
        # Get window size
        window_size = self.driver.get_window_size()
        window_width = window_size['width']
        window_height = window_size['height']
        print(f"Window size: width={window_width}, height={window_height}")

        for (x, y) in coordinates:
            print(f"Processing coordinate: ({x}, {y})")

             # Ensure coordinates are within the window bounds
            if 0 <= x <= window_width and 0 <= y <= window_height:
                #actions.move_to_element_with_offset(reference_element, x, y).perform()# Move to the absolute position and click
                #time.sleep(1)  # Explicitly sleep for 1 second
                self.move_cursor(x, y)
            else:
                print(f"Skipping out-of-bounds coordinate: ({x}, {y})")
        
        actions.perform()

#this file will include a class with instance methods 
#that will be resposnsible to interact with our webiste 
#after we have som results , to apply filteration 
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time 
class BookingFilteration():
    def __init__(self,driver:webdriver):
        self.driver=driver
    
    def apply_star_rating(self,*star_values):
        #print("1")
        #time.sleep(30)
        star_filteration_box=self.driver.find_element(
            #By.ID,
            #'filter_group_class_:r7g:'
            By.XPATH,
            '//div[@id="left_col_wrapper"]//div[contains(@class,"ffb9c3d6a3 ad9a06523f")and contains(@data-testid,"filters-group") and contains(@data-filters-group,"class")]'
            #'//div[@id="left_col_wrapper"]//div[contains(@id,"filter_group_class_:r7g:")]]'
        )
            #By.CSS_SELECTOR,'div[id="filter_group_class_:r6u:"]')
        #print("2")
        #print(star_filteration_box.text)
        star_child_elements=star_filteration_box.find_elements(By.CSS_SELECTOR,'*')
        #print(len(star_child_elements))

        for star_value in star_values:
            for star_element in star_child_elements:
                if star_element.get_attribute('innerHTML')=='1 star':#<h1>jim</h1> it will check for jim part
                    star_element.click()
                
                elif star_element.get_attribute('innerHTML')==f'{star_value} stars':#had to use elif cause for 1 it had only 'star' and for rest it was 'stars'
                    star_element.click()
    
    def sort_price_lowest_first(self):
        sorting_box=self.driver.find_element(
            By.XPATH,
            #'//button[contains(@aria-expanded,"false") and contains(@data-testid,"sorters-dropdown-trigger") and contians(@data-selected-sorter,"popularity") and contains(@type,"button")]'
            '//div[@id="search_results_table"]/div[2]/div[1]/div[1]/div[1]/span[1]/button[1]'
        )
        sorting_box.click()

        accending_element=sorting_box.find_element(
            By.XPATH,
            '//div[contains(@class,"a0ac0ffd76 eb4b382ac4 b00e0292fd")]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[3]/button[contains(@class,"a83ed08757 aee4999c52 d4c8bef76c ac7953442b")]'
        )
        accending_element.click()
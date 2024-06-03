#This file is going to include method that will parse 
#The specific data that we need from each one of the deal boxes.

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class BookingReport:
    def __init__(self,boxes_selection_element):
        self.boxes_selection_element=boxes_selection_element
        self.deal_boxes=self.pull_deal_boxes()


    def  pull_deal_boxes(self):
        return self.boxes_selection_element.find_elements(By.XPATH,'//div[contains(@class,"c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 da89aeb942")]')
    
    def pull_deal_box_attributes(self):
        print(len(self.deal_boxes))
        #creating a list to add attributes , here we are going to create a list within list which will help us to grp elements for every hotel box
        collections=[]
        for deal_box in self.deal_boxes:
            #print(deal_box.text)
            #taking hotel name data

            hotel_name=deal_box.find_element(
                By.XPATH,
                '/descendant-or-self::A[contains(@class,"e13098a59f")]//DIV[1]'
                ).get_attribute('innerHTML').strip()
            #print(hotel_name)
            #taking hotel price data
            hotel_price=deal_box.find_element(
                By.XPATH,
                '/descendant-or-self::SPAN[contains(@class,"f6431b446c fbd1d3018c e729ed5ab6")]'
            ).get_attribute('innerHTML').strip()
            #taking hotel score/rating data
            hotel_score=deal_box.find_element(
                By.XPATH,
                '/descendant-or-self::DIV[contains(@class,"a3b8729ab1 d86cee9b25")]'
            ).get_attribute('innerHTML').strip()
            collections.append(
                [hotel_name,hotel_price,hotel_score]
            )
        #giving out collections
        return collections
        
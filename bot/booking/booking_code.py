import booking.constants  as const
from selenium import webdriver 
from selenium.webdriver.common.by import By
from booking.booking_filteration import BookingFilteration 
from booking.booking_report import BookingReport
import time
import os

class Booking(webdriver.Chrome):
    def __init__(self,driver_path=r"C:\Selenium Drivers\chromedriver-win64.zip",teardown=False):
        self.driver_path=driver_path
        self.teardown=teardown
        os.environ['PATH']+=self.driver_path
        options=webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        super(Booking,self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __enter__(self):
        return self
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        try:
            no_thanks_element=self.find_element(
               By.XPATH, '//button[contains(@aria-label,"Dismiss sign-in info.")]'
            )
            no_thanks_element.click()
        except:
            print('No element with given name')
    
    def change_currency(self,currency='AUD'):
        currency_element=self.find_element(
            By.CSS_SELECTOR,
            'button[data-testid="header-currency-picker-trigger"]'
            )
        currency_element.click()
        
        #print('checking for it')
        #time.sleep(10)
        
        selected_currency_element=self.find_element(
           By.XPATH,
           f"//div[contains(@class,'a448481077')]//button[.//div[contains(text(),'{currency}')]]"
           #f"//button[contains(@class,'a83ed08757 aee4999c52 ffc914f84a c39dd9701b ac7953442b') and .//div[contains(@class,' ea1163d21f') and contains(text(),'{currency}')]]"
           #f"//button[contains(@class,'a83ed08757 aee4999c52 ffc914f84a c39dd9701b ac7953442b')and contains(text(),'{currency}')]]"
           #f"//button[contains(@class,'a83ed08757 aee4999c52 ffc914f84a c39dd9701b ac7953442b')][.//div[contains(@class,' ea1163d21f') and contains(text(),{currency})]]"
           #f"//button[contains(@data-testid,'selection-item')]//div[@class=' ea1163d21f' and contains(text(),{currency})]"
           #f"//BUTTON[@class='a83ed08757 aee4999c52 ffc914f84a c39dd9701b ac7953442b' and normalize-space(.)='{currency}']"
            #f"//BUTTON[@class='a83ed08757 aee4999c52 ffc914f84a c39dd9701b ac7953442b' and contains(text(),{currency})]"
            #f"//html/body[1]/div[contains(@class,'b9720ed41e cdf0a9297c')]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/ul[contains(@class,'aca0ade214 ebac6e22e9 c2931f4182 c27e5d305d db150fece4')]/li/button[contains(text(),'AED')]"
            #f"//html/body[1]/div[contains(@class,'b9720ed41e cdf0a9297c')]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/button[contains(text(),{currency})]"
        )
        #print(f"Selected element  element clickable: {selected_currency_element.is_enabled()}")
        #print(selected_currency_element)
        #print(selected_currency_element.text)
        selected_currency_element.click()
        #print('clicked')
        #time.sleep(300)
        #print('this done as well')
    def select_place_to_go(self,place_to_go):
        search_field=self.find_element(
            By.XPATH,
            f"//div[contains(@class,'ffb9c3d6a3 db27349d3a cc9bf48a25')]//input[contains(@name,'ss')]"
        )
        #print('hi')
        search_field.clear()
        search_field.send_keys(place_to_go)
        #search_field.click()
        
        first_element=self.find_element(
            By.XPATH,
            f"//div[contains(@data-testid,'autocomplete-results')]//li[1]"
        )
        first_element.click()
        #time.sleep(30)
    
    def select_dates(self,check_in_date,check_out_date):
        check_in_element=self.find_element(
            By.CSS_SELECTOR,
            f'span[data-date="{check_in_date}"]'
        )
        check_in_element.click()

        check_out_element=self.find_element(
            By.CSS_SELECTOR,
            f'span[data-date="{check_out_date}"]'
        )
        check_out_element.click()
        #time.sleep(30)


    def select_adults(self,adult_count=2):
        selection_element=self.find_element(
            By.XPATH,
            "//div[contains(@class,'d67edddcf0') and contains(@tabindex,'-1')]"
        )
        selection_element.click()
        #print(1)
        def decrease():
            while True:
                decrease_adults_element=self.find_element(
                    By.XPATH,
                    "//div[@class='hero-banner-searchbox']/div[1]/form[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[1]"
                )
                decrease_adults_element.click()

                adult_value_element=self.find_element(
                    By.XPATH,
                    '//div[@class="hero-banner-searchbox"]/div[1]/form[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]'
                    #'//div[contians(@class,"bfb38641b0")]/span[conatins(@class,"d723d73d5f") and contains(@aria-hidden,"true")]'
                )
                adult_value=int(adult_value_element.text)
                #print(4)
                if str(adult_value)==adult_count:
                    break



        def increase():  
            while True:
                increase_adults_element=self.find_element(
                    By.XPATH,
                    "//div[@class='hero-banner-searchbox']/div[1]/form[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[2]"
                )
                increase_adults_element.click()

                adult_value_element=self.find_element(
                    By.XPATH,
                    '//div[@class="hero-banner-searchbox"]/div[1]/form[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]'
                    #'//div[contians(@class,"bfb38641b0")]/span[conatins(@class,"d723d73d5f") and contains(@aria-hidden,"true")]'
                )
                adult_value=int(adult_value_element.text)
                #print(5)
                if str(adult_value)==adult_count:
                    break

        if int(adult_count)<2:
            decrease()
            #print(2)

        elif int(adult_count)>2:
            increase()
            #print(3)
        #time.sleep(30)

    def click_search(self):
        search_button_element=self.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        )
        search_button_element.click()

        #print("done")
        #time.sleep(30)

    def apply_filteration(self):
        filteration=BookingFilteration(driver=self)
        filteration.apply_star_rating(3,4)
        filteration.sort_price_lowest_first()

    def report_reults(self):
        hotel_boxes=self.find_element(
            By.XPATH,
            '//div[contains(@class,"d4924c9e74")]'
        )
        report=BookingReport(hotel_boxes)
        print(report.pull_deal_box_attributes())

    
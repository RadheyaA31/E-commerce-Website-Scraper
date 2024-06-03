from booking.booking_code import Booking
import time
try:
    with Booking(teardown=False) as bot:
        bot.land_first_page()
        bot.change_currency(currency='USD')
        bot.select_place_to_go(place_to_go='Goa')
        bot.select_dates(check_in_date="2023-09-18",check_out_date="2023-10-16")
        bot.select_adults(adult_count='1')
        bot.click_search()
        #time.sleep(600)
        bot.apply_filteration()
        bot.report_reults()
        time.sleep(30)
        #print('Exiting')
except Exception as e:
    if 'in PATH' in str(e):
         print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise
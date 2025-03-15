from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
import random
from typing import List
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from util import write
from selenium.webdriver.remote.webelement import WebElement
from threading import Thread
from selenium.webdriver.common.keys import Keys

class Reserver:
    def __init__(self, headless, url, proxy, from_addr, to_addr, date, month, service_no, phone, email, selected_seats, passenger_list):

        self.firefox_options = webdriver.FirefoxOptions()
        if headless:
            self.firefox_options.add_argument("--headless")
            self.firefox_options.add_argument("--width=1920")
            self.firefox_options.add_argument("--height=1080")

        self.proxy = proxy
        if self.proxy:
            self.firefox_options.set_preference("network.proxy.type", 1)  # Manual proxy configuration
            self.firefox_options.set_preference("network.proxy.http", self.proxy.split(':')[0])
            self.firefox_options.set_preference("network.proxy.http_port", int(self.proxy.split(':')[1]))
            self.firefox_options.set_preference("network.proxy.ssl", self.proxy.split(':')[0])
            self.firefox_options.set_preference("network.proxy.ssl_port", int(self.proxy.split(':')[1]))


        

        self.current_month = datetime.now().month
        # Open the URL
        self.url = url

        self.from_addr = from_addr#"Shimla isbt"
        self.to_addr = to_addr#"kangra"

        self.journy_date = date#"14"
        self.journy_month = month
        self.desired_service_no = service_no

        self.phone = phone
        self.email_id = email

        self.is_finished = False
        self.selected_seats = selected_seats
        self.passenger_list = passenger_list
        self.thrd = None

        self.book_time = 0

    def get_avail_seats(self) -> (List[List[str]]):
        return self.run(get_data=True)
    
    def run_thrd(self) -> Thread:
        self.thrd = Thread(target=self.run, daemon=True)
        self.thrd.start()
        return self.thrd


    def run(self, get_data = False):
        self.start_browser()
        self.from_place()
        self.to_place()
        self.date_input()
        self.search_btn()
        self.select_service()
        self.show_layout()

        if get_data:
            return self.get_seats_data()
        
        self.select_actions()

    def select_actions(self, selected_seats = None, passenger_list = None):
        if passenger_list != None:
            self.passenger_list = passenger_list

        if selected_seats != None:
            self.selected_seats = selected_seats

        self.select_seats(to_select=self.selected_seats)
        self.mobile_email_input()
        self.passenger_details(passenger_list=self.passenger_list)
        self.book_button()

        # time for booking.....
        self.book_time = time.time()
        self.payment()

        self.is_finished = True

        sleep((20 * 60) - (time.time() - self.book_time))
        print("Task is finished, now repeting that task...")
        self.driver.quit()
        self.run()
    

    def start_browser(self):
        self.driver = webdriver.Firefox(options=self.firefox_options)

        self.driver.maximize_window()  
        self.driver.implicitly_wait(10) 

        self.actions = ActionChains(self.driver)

        self.max_wait = WebDriverWait(self.driver, 180)
        self.min_wait = WebDriverWait(self.driver, 30)

        # geting url
        # self.driver.get("https://mahadevadity8080.pythonanywhere.com/ipaddr")
        # self.driver.execute_script("window.open('');")
        # self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get(self.url)

        self.actions = ActionChains(self.driver)


    def close(self):
        self.driver.quit()
        exit()


    def from_place(self):
        xpath_from = '//*[@id="fromPlaceName"]'
        try:
            leaving_from = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, xpath_from)))
        except:
            print("Can't found <FromPlace> input")
            self.close()

        leaving_from.click()
        sleep(random.uniform(0.2, 0.8))
        write(leaving_from, self.from_addr)
        sleep(random.uniform(0.9, 2.5))

        auto_complete_xpath = '//*[@id="ui-id-1"]'

        try:
            auto_complete = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, auto_complete_xpath)))
        except:
            print("No values to select in <FromPlace> input")
            self.close()
            
        list_items = auto_complete.find_elements(By.TAG_NAME, "a")
        # Print the text of each <li> element
        n = 1
        for a_tag in list_items:
            print(f"Item {n}: {a_tag.text}")
            n += 1
        #click on 1st elemnt from list 
        list_items[0].click()
        sleep(random.uniform(1.5, 4.5))


    def to_place(self):
        xpath_to = '//*[@id="toPlaceName"]'
        try:
            going_to = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, xpath_to)))
        except:
            print("Can't found <toPlaceName> input")
            self.close()

        going_to.click()
        sleep(random.uniform(0.2, 0.8))
        write(going_to, self.to_addr)
        sleep(random.uniform(1, 2.3))

        auto_complete_css = '#ui-id-8'

        # auto_complete2 = self.max_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, auto_complete_css)))
      

            
        # list_items2 = auto_complete2.find_elements(By.TAG_NAME, "a")
        # # Print the text of each <li> element
        # n = 1
        # for a_tag in list_items2:
        #     print(f"Item {n}: {a_tag.text}")
        #     n += 1
        # #click on 1st elemnt from list 
        # list_items2[0].click()
        going_to.send_keys(Keys.ENTER)
        sleep(random.uniform(1.5, 4.5))




    def date_input(self):
        xpath_date = '//*[@id="txtJourneyDate"]'
        try:
            
            date = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, xpath_date)))
        except:
            print("Can't found <date> input")
            self.close()
        
        date.click()

        sleep(random.uniform(0.2, 0.8))
        write(date, self.journy_date)
        sleep(random.uniform(0.9, 2.5))
        # next_button = driver.find_element(By.CLASS_NAME, "ui-datepicker-next")
        # next_button.click()


        date_picker = self.max_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-datepicker-calendar")))
            

        december_table_xpath = "//div[contains(@class, 'ui-datepicker-group-last')]//table"
        december_table = self.driver.find_element(By.XPATH, december_table_xpath)


        # Select a specific date from December (e.g., "20")
        date_xpath = f".//a[text()='{self.journy_date}']"  # Relative XPath within the December table
        date_element = december_table.find_element(By.XPATH, date_xpath)

        # Click the desired date
        date_element.click()
        sleep(random.uniform(1.2, 2.5))
        print(f"Selected date: {self.journy_date}")


    def search_btn(self):
        search_button_xpath = '//*[@id="searchBtn"]'
        try:
            search_btn = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
        except:
            print("Search button not exits..")
            self.close()


        search_btn.click()
        print("Search button clicked....")
        sleep(random.uniform(1.2, 2.5))


    def select_service(self):
        #select the desired service number
        form_xpath = '//*[@id="bookingsForm"]'
        try:
            booking_form = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, form_xpath)))
        except:
            print("Booking form not found")
            self.close()

        print("booking form is found...")

        row_container = booking_form.find_elements(By.CLASS_NAME, "rSetForward")

        for rows in row_container:
                # Find the service number in the row
                service_no_element = rows.find_element(By.CLASS_NAME, "srvceNO")
                print(f"ServiceNum: ", service_no_element.text)
                if self.desired_service_no in service_no_element.text:
                    # Found the desired service number
                    print(f"Service {self.desired_service_no} found.")
                    
                    # Locate the associated button and click it
                    button = rows.find_element(By.CLASS_NAME, "btnSelectLO")
                    sleep(random.uniform(1.3, 4))
                    ActionChains(self.driver).move_to_element(button).click().perform()
                    print(f"Clicked the 'Select Seats' button for service {self.desired_service_no}.")
                    break
        else:
            print(f"Service {self.desired_service_no} not found.")
            print("So can't move further...")
            self.close()

        
    def show_layout(self):
        show_layout = '//*[@id="fwLtBtn"]'
        try:
            show_layout_btn = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, show_layout)))
        except:
            print("Show Layout button is not found...")
            self.close()
        sleep(random.uniform(1, 2))
        show_layout_btn.click()

    def avail_seats(self) -> List[WebElement]:
        seats_table_xpath = ".seatsSteerCS"
        try:
            seats_table = self.max_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seats_table_xpath)))
        except:
            print("Table of seats not found...")
            self.close()

        print("Seats table found.....", seats_table)
        sleep(random.uniform(1, 2))

        #scroll to the seat....
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seats_table)
        sleep(random.uniform(1, 2))
        seats = seats_table.find_elements(By.CSS_SELECTOR, "td.availSeatClassS")
        
        return seats


    def get_seats_data(self) -> (List[List[str]]):

        seats = self.avail_seats()

        window_seats = []
        other_seats = []

        for seat in seats:
            title = seat.get_attribute("title")
            seat_num = title[:title.find("(")]
            if 'W' in title:
                window_seats.append(seat_num)
            else:
                other_seats.append(seat_num)

        return (other_seats, window_seats)



    def select_seats(self, to_select: list):
        seats = self.avail_seats()
        selected_count = 0

        for seat in seats:
            title = seat.get_attribute("title")
            seat_num = title[:title.find("(")]

            if seat_num not in to_select:
                continue

            sleep(random.uniform(2, 3))
            seat.click()
            selected_count += 1

        print(f"Total seat selected  : {selected_count}")


    def mobile_email_input(self):
        #numberr
        num_xpath = '//*[@id="mobileNo"]'
        number = self.driver.find_element(By.XPATH, num_xpath)
        sleep(random.uniform(0.2, 0.8))
        write(number, self.phone)
        sleep(random.uniform(0.9, 2.5))


        email_xpath = '//*[@id="email"]'
        email = self.driver.find_element(By.XPATH, email_xpath)
        sleep(random.uniform(0.2, 0.8))
        write(email, self.email_id)
        sleep(random.uniform(0.9, 2.5))


    def passenger_details(self, passenger_list: List[List[str]]):
        passenger_table_xpath = '//*[@id="PaxTblForward"]'
        passenger_table = self.driver.find_element(By.XPATH, passenger_table_xpath)

        count = 0

        for passenger in passenger_list:
                
            # Find the dropdown element
            gender_dropdown = Select(passenger_table.find_element(By.ID, f"genderCodeIdForward{count}"))
            # Select by visible text
            gender_dropdown.select_by_visible_text(passenger[1].upper())

            #name
            name_id = f"passengerNameForward{count}"
            name = passenger_table.find_element(By.ID, name_id)
            sleep(random.uniform(0.2, 0.8))
            write(name, passenger[0])
            sleep(random.uniform(0.9, 2.5))

            #age
            age_id = f"passengerAgeForward{count}"
            age = passenger_table.find_element(By.ID, age_id)

            sleep(random.uniform(0.2, 0.8))
            write(age, passenger[2])

            #sleep for next
            sleep(random.uniform(1, 3))
            count += 1


    def book_button(self):
        #book button
        sleep(random.uniform(5, 10))
        book_btn_xpath = '//*[@id="BookNowBtn"]'
        book_btn = self.driver.find_element(By.XPATH, book_btn_xpath)
        book_btn.click()

    def payment(self):
        payu_xpath = '//*[@id="citrus"]'

        payu = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, payu_xpath)))
        sleep(random.uniform(1, 4))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payu)
        sleep(random.uniform(1, 3))
        payu.click()

        payment_btn_xpath = '//*[@id="PgBtn"]'
        payment_btn_xpath = self.driver.find_element(By.XPATH, payment_btn_xpath)
        sleep(random.uniform(1, 3))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payment_btn_xpath)
        sleep(random.uniform(0.8, 1.5))

        payment_btn_xpath.click()



if __name__ == "__main__":
    htrc_res = Reserver()
    htrc_res.from_place()
    htrc_res.to_place()
    htrc_res.date_input()
    htrc_res.search_btn()
    htrc_res.select_service()
    htrc_res.show_layout()
    seats, window = htrc_res.get_seats_data()

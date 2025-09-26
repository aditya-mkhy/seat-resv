from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
import random
from typing import List, TYPE_CHECKING
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from util import write, get_phone, get_email, timeCal, log
from selenium.webdriver.remote.webelement import WebElement
from threading import Thread
from selenium.webdriver.common.keys import Keys

if TYPE_CHECKING:
    from seat_holder import SeatHolder

class Reserver:
    def __init__(self, headless, url, proxy, from_addr, to_addr, date, service_no, phone, email, selected_seats, passenger_list):

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
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.journy_date = date
        self.desired_service_no = service_no
        self.phone = phone
        self.email_id = email

        self.selected_seats = selected_seats
        self.passenger_list = passenger_list
        self.thrd = None

        self.prev_book_time = 0
        self.is_finished = False
        self.unique_id = self.journy_date
        self.time_taken = 10 # to available the seat for booking again -> default 5 minute
        self.repeat_count = 1

        self.error_count = 0


    def hold_selected_seat_forver(self, parent: 'SeatHolder', selected_seats = None):

        while not self.is_finished:
            # holding seat until the time expires
            try:
                status = self.hold_selected_seat(parent=parent, selected_seats=selected_seats)
                if status == "exit":
                    self.close()
                    return
                
                self.error_count = 0

            except Exception as e:
                log(f"[{self.unique_id}] Error[hold_selected_seat_forver] : {e}")

                if parent.is_doomsday(for_this_date=self.journy_date) or self.is_finished:
                    log(f"Task is completed for id : {self.unique_id}")
                    self.close()
                    return
                
                # close the previous driver
                try:
                    self.driver.quit()
                except:
                    pass

                # check if something causing error continously...
                self.error_count += 1
                if self.error_count > 200:
                    log(f"[{self.unique_id}] Maximus error count is excceded... So can't go further...")
                    log(f"Task is completed for id : {self.unique_id}")
                    self.close()
                    return
            
            log(f"Restarting the task for id : {self.unique_id}")



    def hold_selected_seat(self, parent: 'SeatHolder', selected_seats = None):
        self.start_browser()
        self.from_place()
        self.to_place()
        self.date_input()
        self.search_btn()
        self.select_service()
        self.show_layout()


        if selected_seats:
            self.selected_seats = selected_seats
            log(f"[{self.unique_id}] Selected Seats are  : {self.selected_seats}")

        if not self.selected_seats:
            log(f"[{self.unique_id}] No seat is selected.. so i'm useless..goodbye..")
            self.close()
            return "exit"


        # run until the seat is available for booking
        count = 0
        while not self.is_finished: 

            list1, list2 = self.get_seats_data()
            list1.extend(list2)
            count += 1


            if not self.check_if_present(list1, self.selected_seats):
                log(f"[{self.unique_id}] Selected seat is still occupied....{count}")
                #sleep for 1 minute..
                time.sleep(60)

                # after sleeping.. refresh the page
                self.show_layout()
                print("clicked on layout...")
                time.sleep(10)

                #check for end time...
                if parent.is_doomsday(for_this_date=self.journy_date):
                    log(f"Task is completed for id : {self.unique_id}")
                    self.close()
                    return "exit"
                
            else:
                log(f"[{self.unique_id}] Seats are now availabe for blocking....")
                
                if self.prev_book_time:
                    self.time_taken = (time.time() - self.prev_book_time) / 60
                    log(f"[{self.unique_id}] Time taken -> {timeCal(self.time_taken * 60)}")

                break



        log(f"[{self.unique_id}] Selected Seat : {self.selected_seats}")

        #get the random passenger list
        self.passenger_list = parent.passenger_info(count=len(self.selected_seats))
        self.phone = get_phone() # get random phone number
        self.email_id = get_email(self.passenger_list) # get email on the basis of passenger list

    
        
        self.select_seats(to_select = self.selected_seats) # select seats
        self.mobile_email_input()
        self.passenger_details(passenger_list = self.passenger_list)
        self.book_button() # click on book button
        

        #check for end time
        if parent.is_doomsday(for_this_date=self.journy_date):
            log(f"Task is completed for id : {self.unique_id}")
            self.close()
            return "exit"

        # time for booking.....
        self.payment()
        self.prev_book_time = time.time()

        self.driver.quit()

        #sleep for time_taken....
        status = self.sleep_wait(parent=parent, mint = (self.time_taken - 3))
        if status ==  "exit": # close 
            return status
        
        self.repeat_count += 1
        log(f"[{self.unique_id}] Task is finished, now repeting that task..for {self.repeat_count} times")
        # self.driver.quit()
        return True


    def sleep_wait(self, parent: 'SeatHolder', mint: int):
        for i in range(int(mint) * 2):
            time.sleep(30)
            if parent.is_doomsday(for_this_date=self.journy_date):
                log(f"Task is completed for id : {self.unique_id}")
                self.close()
                return "exit"


    def check_if_present(self, big_list: list, small_list: list):
        # to chek if all the items of the small list is present in the big list
        for item in small_list:
            if item not in big_list:
                return False
        return True
    
    
    def remove_list_from_list(self, list1: list, list2: list) -> list:
        remaining_item = []

        for item in list1:
            if item not in list2:
                remaining_item.append(item)

        return remaining_item


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

        # Create ActionChains object
        self.actions = ActionChains(self.driver)

        self.max_wait = WebDriverWait(self.driver, 180)
        self.min_wait = WebDriverWait(self.driver, 30)

        self.driver.get(self.url)


    def close(self):
        self.is_finished = True
        try:
            self.driver.quit()
        except:
            pass
        log(f"Drive closed for id = {self.unique_id}")


    def from_place(self):
        xpath_from = '//*[@id="fromPlaceName"]'
        try:
            leaving_from = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, xpath_from)))
        except:
            raise ValueError("Can't found <FromPlace> input")
            

        leaving_from.click()
        sleep(random.uniform(0.2, 0.8))
        write(leaving_from, self.from_addr)
        sleep(random.uniform(0.9, 2.5))

        auto_complete_xpath = '//*[@id="ui-id-1"]'

        try:
            auto_complete = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, auto_complete_xpath)))
        except:
            raise ValueError("No values to select in <FromPlace> input")
            
        list_items = auto_complete.find_elements(By.TAG_NAME, "a")

        # Print the text of each <li> element
        n = 1
        for a_tag in list_items:
            # print(f"Item {n}: {a_tag.text}")
            n += 1
        #click on 1st elemnt from list 
        list_items[0].click()
        sleep(random.uniform(1.5, 4.5))


    def to_place(self):
        xpath_to = '//*[@id="toPlaceName"]'
        try:
            going_to = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, xpath_to)))
        except:
            raise ValueError("Can't found <toPlaceName> input")

        going_to.click()
        sleep(random.uniform(0.2, 0.8))
        write(going_to, self.to_addr)
        sleep(random.uniform(1, 2.3))

        auto_complete_css = '#ui-id-8'

        going_to.send_keys(Keys.ENTER)
        sleep(random.uniform(1.5, 4.5))


    def date_input(self, date_str: str = None):

        if date_str == None:
            date_str = self.journy_date

        # date_str  = "28-03-2025"
        # Convert to datetime object 
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        month_year = date_obj.strftime("%B %Y")  # Output: "March 2025"
        day = date_obj.strftime("%d")  # Output: "28"

        current_date = datetime.today()

        # Calculate difference in months
        year_diff = date_obj.year - current_date.year
        month_diff = date_obj.month - current_date.month
        total_month_diff = year_diff * 12 + month_diff

        print(f"The diffence current and entered month : {total_month_diff}")

        if total_month_diff > 2:
            log(f"[{self.unique_id}] HTRC only allow booking upto 3 months form current month")
            log(f"[{self.unique_id}] So, please enter the accordingly...")
            raise ValueError(f"[{self.unique_id}] HTRC only allow booking upto 3 months form current month")


        xpath_date = '//*[@id="txtJourneyDate"]'
        try:
            
            date = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, xpath_date)))
        except:
            raise ValueError("Can't found <date> input")
        
        date.click()

    
        sleep(random.uniform(0.5, 1.2))
        # write(date, self.journy_date)
        # sleep(random.uniform(0.9, 2.5))
        # next_button = driver.find_element(By.CLASS_NAME, "ui-datepicker-next")
        # next_button.click()

        for i in range(3):
            current_month_year = self.max_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-datepicker-title"))).text

            if month_year in current_month_year:
                break

            else:
                # Click the next button to navigate to the next month
                next_btn = self.max_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-datepicker-next")))
                next_btn.click()
                sleep(random.uniform(1.5, 2.5)) # Wait for transition

        # Select the specific date (e.g., 27)
        date_element = self.driver.find_element(By.XPATH, f"//a[text()='{day}']")
        date_element.click()

        sleep(random.uniform(1.2, 2.5))
        log(f"[{self.unique_id}] Selected date: {date_str}")



    def search_btn(self):
        search_button_xpath = '//*[@id="searchBtn"]'
        try:
            search_btn = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
        except:
            raise ValueError("Search button not exits..")


        search_btn.click()
        log(f"[{self.unique_id}] Search button clicked....")
        sleep(random.uniform(1.2, 2.5))


    def select_service(self):
        #select the desired service number
        form_xpath = '//*[@id="bookingsForm"]'
        try:
            booking_form = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, form_xpath)))
        except:
            raise ValueError("Booking form not found")

        log(f"[{self.unique_id}] booking form is found...")

        row_container = booking_form.find_elements(By.CLASS_NAME, "rSetForward")

        for rows in row_container:
                # Find the service number in the row
                service_no_element = rows.find_element(By.CLASS_NAME, "srvceNO")
                print(f"ServiceNum: ", service_no_element.text)
                if self.desired_service_no in service_no_element.text:
                    # Found the desired service number
                    print(f"Service {self.desired_service_no} found.")
                       #scroll to the seat....

                    # Locate the associated button and click it
                    button = rows.find_element(By.CLASS_NAME, "btnSelectLO")

                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

                    sleep(random.uniform(1.3, 3))
                    ActionChains(self.driver).move_to_element(button).click().perform()
                    log(f"[{self.unique_id}] Clicked the 'Select Seats' button for service {self.desired_service_no}.")
                    break
        else:
            log(f"[{self.unique_id}] Service {self.desired_service_no} not found.")
            log(f"[{self.unique_id}] So can't move further...")
            raise ValueError(f"[{self.unique_id}] Service {self.desired_service_no} not found.")

        
    def show_layout(self):
        show_layout = '//*[@id="fwLtBtn"]'
        try:
            show_layout_btn = self.max_wait.until(EC.element_to_be_clickable((By.XPATH, show_layout)))
        except:
            raise ValueError(f"[{self.unique_id}] Show Layout button is not found...")

        sleep(random.uniform(1, 2))
        show_layout_btn.click()

    def avail_seats(self) -> List[WebElement]:
        seats_table_xpath = ".seatsSteerCS"
        try:
            seats_table = self.max_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seats_table_xpath)))
        except:
            raise ValueError(f"[{self.unique_id}] Table of seats not found...")

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

    # date_str = "28-05-2025"
    # date_input(date_str)

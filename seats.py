from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


#
#  A test file.....

def write(path, word):
    for w in word:
        sleep(random.uniform(0.03, 0.09))
        path.send_keys(w)

def get_age():
    return str(random.randint(17, 50))

def get_gender():
    return random.choice(["MALE", "FEMALE"])

def get_pessanger(name_list: list):
    name = random.choice(name_list)
    name_list.remove(name)

    age = get_age()
    gender = get_gender()

    return [gender, name, age]

name_list = []
seats_book_list = [8, 12, 16, 20, 24, 28]



firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument("--headless")  # Run Firefox in headless mode
firefox_options.add_argument("--width=1920")  # Set screen width
firefox_options.add_argument("--height=1080")# options.add_argument("-headless")

# Set up the Firefox WebDriver

driver = webdriver.Firefox()#options=firefox_options)

driver.maximize_window()  
driver.implicitly_wait(10) 

actions = ActionChains(driver)

max_wait = WebDriverWait(driver, 180)
min_wait = WebDriverWait(driver, 30)

current_month = datetime.now().month

# Open the URL
url = "https://online.hrtchp.com/oprs-web/guest/home.do?h=1"
from_addr = "Shimla isbt"
to_addr = "kangra"
journy_date = "14"
journy_month = 12
desired_service_no = 10
phone = ""
email_id = ""
desired_service_no = str(desired_service_no)
driver.get(url)

actions = ActionChains(driver)

# Wait until a specific element is loaded

try:
    xpath_from = '//*[@id="fromPlaceName"]'
    leaving_from = max_wait.until(EC.element_to_be_clickable((By.XPATH, xpath_from)))
    leaving_from.click()
    sleep(random.uniform(0.2, 0.8))
    write(leaving_from, from_addr)
    sleep(random.uniform(0.9, 2.5))

    auto_complete_xpath = '//*[@id="ui-id-1"]'

    auto_complete = max_wait.until(EC.element_to_be_clickable((By.XPATH, auto_complete_xpath)))


    list_items = auto_complete.find_elements(By.TAG_NAME, "a")

    # Print the text of each <li> element
    n = 1
    for a_tag in list_items:
        print(f"Item {n}: {a_tag.text}")
        n += 1
    
    list_items[0].click()
    sleep(random.uniform(1.5, 4.5))


except:
    print("Page is not loaded sucessfully")
    driver.quit()



try:
    xpath_to = '//*[@id="toPlaceName"]'
    going_to = max_wait.until(EC.element_to_be_clickable((By.XPATH, xpath_to)))
    going_to.click()

    sleep(random.uniform(0.2, 0.8))
    write(going_to, to_addr)
    sleep(random.uniform(0.9, 2.5))


    auto_complete_xpath = '//*[@id="ui-id-3"]'
    auto_complete = max_wait.until(EC.element_to_be_clickable((By.XPATH, auto_complete_xpath)))

    list_items = auto_complete.find_elements(By.TAG_NAME, "a")

    # Print the text of each <li> element
    n = 1
    for a_tag in list_items:
        print(f"Item {n}: {a_tag.text}")
        n += 1
    
    list_items[0].click()
    sleep(random.uniform(1, 2.5))

except:
    print("Page is not loaded sucessfully")
    driver.quit()


#   Date input

try:
    xpath_date = '//*[@id="txtJourneyDate"]'
    date = max_wait.until(EC.element_to_be_clickable((By.XPATH, xpath_date)))
    date.click()

    sleep(random.uniform(0.2, 0.8))
    write(date, journy_date)
    sleep(random.uniform(0.9, 2.5))
    # next_button = driver.find_element(By.CLASS_NAME, "ui-datepicker-next")
    # next_button.click()


    date_picker = max_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-datepicker-calendar")))
    

    december_table_xpath = "//div[contains(@class, 'ui-datepicker-group-last')]//table"
    december_table = driver.find_element(By.XPATH, december_table_xpath)


  # Select a specific date from December (e.g., "20")
    date_xpath = f".//a[text()='{journy_date}']"  # Relative XPath within the December table
    date_element = december_table.find_element(By.XPATH, date_xpath)

    # Click the desired date
    date_element.click()
    sleep(random.uniform(1.2, 2.5))
    print(f"Selected date: {journy_date}")

except:
    print("Page is not loaded sucessfully")
    driver.quit()

try: 
    search_button_xpath = '//*[@id="searchBtn"]'
    search_btn = max_wait.until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
    search_btn.click()
    print("Search button clicked....")
    sleep(random.uniform(1.2, 2.5))

except:
    print("Search button not found...")
    driver.quit()


# try:

form_xpath = '//*[@id="bookingsForm"]'
booking_form = max_wait.until(EC.element_to_be_clickable((By.XPATH, form_xpath)))
print("booking form is found...")

row_container = booking_form.find_elements(By.CLASS_NAME, "rSetForward")

for rows in row_container:
        print("row---", rows.text)
        # Find the service number in the row
        service_no_element = rows.find_element(By.CLASS_NAME, "srvceNO")
        print(f"ServiceNum: ", service_no_element.text)
        if desired_service_no in service_no_element.text:
            # Found the desired service number
            print(f"Service {desired_service_no} found.")
            
            # Locate the associated button and click it
            button = rows.find_element(By.CLASS_NAME, "btnSelectLO")
            sleep(random.uniform(1.3, 4))
            ActionChains(driver).move_to_element(button).click().perform()
            print(f"Clicked the 'Select Seats' button for service {desired_service_no}.")
            break
else:
    print(f"Service {desired_service_no} not found.")

# except:
#     print("Error occured in server number")


show_layout = '//*[@id="fwLtBtn"]'
show_layout_btn = max_wait.until(EC.element_to_be_clickable((By.XPATH, show_layout)))
sleep(random.uniform(1, 2))
show_layout_btn.click()

# scrolling to the elemnt
actions.move_to_element(show_layout_btn).perform()

seats_table_xpath = ".seatsSteerCS"
print("finding the table")
seats_table = max_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seats_table_xpath)))
print("seat found.....", seats_table)
#actions.move_to_element(seats_table).perform()
print("done......")
print(seats_table.tag_name)

sleep(random.uniform(1, 2))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seats_table)
sleep(random.uniform(1, 2))
seats = seats_table.find_elements(By.CSS_SELECTOR, "td.availSeatClassS")

# Filter elements whose 'title' attribute contains 'W'
seats_with_w = [seat for seat in seats if 'W' in seat.get_attribute("title")]

if not seats_with_w:
    driver.quit()
    print("no seat to book")

total_seats_selected = 0
for i in range(5):
    selected_seat = seats_with_w[0]
    sleep(random.uniform(2, 3))
    selected_seat.click()
    total_seats_selected += 1

    seats_with_w.remove(selected_seat)
    if (len(seats_with_w)) == 0:
        print("less seats are availble.....")
        break



#numberr
num_xpath = '//*[@id="mobileNo"]'
number = driver.find_element(By.XPATH, num_xpath)
sleep(random.uniform(0.2, 0.8))
write(number, phone)
sleep(random.uniform(0.9, 2.5))


email_xpath = '//*[@id="email"]'
email = driver.find_element(By.XPATH, email_xpath)
sleep(random.uniform(0.2, 0.8))
write(email, email_id)
sleep(random.uniform(0.9, 2.5))


passenger_table_xpath = '//*[@id="PaxTblForward"]'
passenger_table = driver.find_element(By.XPATH, passenger_table_xpath)

for count in range(total_seats_selected):

    passenger = get_pessanger(name_list)
        
    # Find the dropdown element
    gender_dropdown = Select(passenger_table.find_element(By.ID, f"genderCodeIdForward{count}"))
    # Select by visible text
    gender_dropdown.select_by_visible_text(passenger[0])

    name_id = f"passengerNameForward{count}"
    name = passenger_table.find_element(By.ID, name_id)

    sleep(random.uniform(0.2, 0.8))
    write(name, passenger[1])
    sleep(random.uniform(0.9, 2.5))


    age_id = f"passengerAgeForward{count}"
    age = passenger_table.find_element(By.ID, age_id)

    sleep(random.uniform(0.2, 0.8))
    write(age, passenger[2])

    sleep(random.uniform(1, 3))




#book button
sleep(random.uniform(5, 10))
book_btn_xpath = '//*[@id="BookNowBtn"]'
book_btn = driver.find_element(By.XPATH, book_btn_xpath)
book_btn.click()


payu_xpath = '//*[@id="citrus"]'

payu = max_wait.until(EC.element_to_be_clickable((By.XPATH, payu_xpath)))
sleep(random.uniform(1, 4))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payu)
sleep(random.uniform(1, 3))
payu.click()

payment_btn_xpath = '//*[@id="PgBtn"]'
payment_btn_xpath = driver.find_element(By.XPATH, payment_btn_xpath)
sleep(random.uniform(1, 3))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payment_btn_xpath)
sleep(random.uniform(0.8, 1.5))

payment_btn_xpath.click()

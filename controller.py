from threading import Thread
from reserver import Reserver
from util import get_passenger_list, sleep, PyDb, get_phone, get_email
import random
from prox import Proxy
import time
from datetime import datetime

class SeatLocker:
    def __init__(self):
        #setting

        self.use_proxy = True
        self.headless_mode = False

        self.from_addr = "Shimla isbt"
        self.to_addr = "kangra"

        self.journy_date = "28"
        self.journy_month = 3
        self.service_no = "10"
        self.url = "https://online.hrtchp.com/oprs-web/guest/home.do?h=1"

        self.db = PyDb()

        self.reserver_obj = {}
        self.email = "makemelove@gmail.com"
        self.min_select_seat = 4
        self.max_select_seat = 6

        #time to stop code exe
        self.end_time = None

        self.obj_count = 0
        self.proxy_obj = Proxy()

    def run_until(self, date_str, time_str):
        # Combine date and time into a single string
        datetime_str = f"{date_str} {time_str}"

        # Convert to datetime object

        self.end_time = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M")
        print(f"Stop Time : {self.end_time}")


    def hold_seat(self, selected_seats: list = None, use_proxy = False, upto: datetime  = None):
        """To hold a specific seat...."""
        proxy = None
        fastest_proxy = []

        #check for end time
        if self.end_time != None:
            if datetime.now() >= self.end_time:
                print("Time reached! Script stopped.")
                exit()


        if use_proxy:
            if len(self.proxy_obj.working_proxies) == 0:
                #get proxy ony first run
                self.proxy_obj.run()

            fastest_proxy = self.proxy_obj.get_faster_proxy(count=10)
            if len(fastest_proxy) == 0:
                print("No proxy found...")
                use_proxy = False

            else:
                proxy = fastest_proxy[0]

        if len(selected_seats) == 0:
            selected_seats = None


        reserver = Reserver(self.headless_mode, self.url, proxy, self.from_addr, self.to_addr, self.journy_date,
                        self.journy_month, self.service_no, None, None, selected_seats, None)
        
        reserver.hold_selected_seat(self)


    
    def book_method_1(self, use_proxy = True):
        proxy = None
        fastest_proxy = []



        if use_proxy:
            if len(self.proxy_obj.working_proxies) == 0:
                #get proxy ony first run
                self.proxy_obj.run()

            fastest_proxy = self.proxy_obj.get_faster_proxy(count=10)
            if len(fastest_proxy) == 0:
                print("No proxy found...")
                use_proxy = False

            else:
                proxy = fastest_proxy[0]


        self.main_reserver = Reserver(self.headless_mode, self.url, proxy, self.from_addr, self.to_addr, self.journy_date,
                            self.journy_month, self.service_no, get_phone(), self.email, None, None)
        
        self.ord_seats, self.window_seats = self.main_reserver.get_avail_seats()

        print(f"self.ord_seats ==> {self.ord_seats}")
        print(f"self.window_seats  ==> {self.window_seats}")

        self.combined_seats = []
        if len(self.ord_seats) != 0:
            self.combined_seats.append(self.ord_seats)

        if len(self.window_seats) != 0:
            self.combined_seats.append(self.window_seats)

        print("Total Seats : ", len(self.window_seats) + len(self.ord_seats))

        
        total_proxy = len(fastest_proxy)
        on_proxy = 1

        while True:

            num_seats_to_select = random.randint(self.min_select_seat, self.max_select_seat)
            selected_seats = []

            for i in range(num_seats_to_select):
                if len(self.combined_seats) == 0:
                    print("All Seats are seleted....")
                    break

                select_from = random.choice(self.combined_seats)

                selected_seats.append(select_from[0])
                select_from.remove(select_from[0])

                if len(select_from) == 0:
                    self.combined_seats.remove(select_from)

            if len(selected_seats) == 0:
                print("Seleted seat is empty... so stop the loop..")
                break

            self.obj_count += 1

            if len(self.combined_seats) == 0:
                print("This is the last seleted seats...")
                print("So using the main thread... For blocking seats...")
                print("SeletedSeats :", selected_seats)
                passenger_list = self.passenger_info(count=len(selected_seats))
                self.main_reserver.select_actions(selected_seats, passenger_list)
                break

            print(f"This is thread : <{self.obj_count}> {selected_seats}")
            passenger_list = self.passenger_info(count=len(selected_seats))

            if use_proxy:
                proxy = fastest_proxy[on_proxy]
                on_proxy += 1
                if on_proxy >= total_proxy:
                    on_proxy = 0


            # thrd_reserver = Reserver(self.headless_mode, self.url, proxy, self.from_addr, self.to_addr, self.journy_date,
            #                 self.journy_month, self.service_no, get_phone(), self.email, selected_seats, passenger_list)
            
            # self.reserver_obj[self.obj_count] = thrd_reserver
            # thrd_reserver.run_thrd()

            
        print("Finished...")


    def passenger_info(self, count = 5):
        pointer = self.db['namePointer']
        passenger_list = get_passenger_list(count = count, pointer = pointer)

        if len(passenger_list) < count:
            count = count - len(passenger_list)
            passenger_list.extend(get_passenger_list(count = count, pointer = 0))
            self.db['namePointer'] = count

        else:
            self.db['namePointer'] = pointer + count

        return passenger_list
    



if __name__ == "__main__":

    seat_locker = SeatLocker()

    date_str = "25-03-2025"
    time_str = "12:50"

    seat_locker.from_addr = "Shimla isbt"
    seat_locker.to_addr = "kangra"
    seat_locker.journy_date = "28"
    seat_locker.journy_month = 3
    seat_locker.service_no = "10"

    selected_seats = []
    use_proxy = False

    # set the end time...
    seat_locker.run_until(date_str = date_str, time_str = time_str)

    seat_locker.hold_seat(use_proxy = use_proxy, selected_seats = selected_seats)
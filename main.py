from threading import Thread
from reserver import Reserver
from util import get_passenger_list, sleep, PyDb, get_phone, get_email, get_equal_sleep, timeCal
import random
from prox import Proxy
from typing import Dict, List
from datetime import datetime
from util import log, print
import os
import time


OBJECT_TO_CLEAN : List[Reserver]  = []


class MutliReserver(Reserver):
    def __init__(self, my_id: str, data: dict, url: str, headless: bool = False, proxy: str = None):
        
        self.thread = None


        # init the inherited class
        super().__init__(
            headless = headless,
            url = url,
            proxy = proxy,
            from_addr = data["from"],
            to_addr = data["to"],
            date = data["date"],
            service_no = data["service_no"],
            phone = None,
            email = None,
            selected_seats = data["seat"],
            passenger_list = None
        )

        self.unique_id = my_id
        log(f"Init MultiReserver with name = {self.unique_id}")


    def thread_hold_selected_seat(self, parent: "SeatHolder"):
        log(f"Running MultiReserver with name = {self.unique_id}")
        self.thread = Thread(target=self.hold_selected_seat_forver, args=(parent,), daemon=True)
        self.thread.start()



class SeatHolder:
    def __init__(self, headless_mode = False):
        #setting

        self.use_proxy = True
        self.headless_mode = headless_mode

        self.from_addr = None
        self.to_addr = None
        self.journy_date = None
        self.service_no = None

        # time to stop the script
        self.end_time = None
        self.url = "https://online.hrtchp.com/oprs-web/guest/home.do?h=1"


        self.reserver_obj: Dict[str, MutliReserver] = {}
        self.db = PyDb()
        self.proxy_obj = Proxy()


    def run_until(self, date_str, time_str):
        # Combine date and time into a single string
        datetime_str = f"{date_str} {time_str}"

        self.end_time = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M")
        log(f"Script stop time : {self.end_time}")



    def hold_for_multiple_dates(self, data: dict, use_proxy = False):
        log("fun <- hold_for_multiple_dates -> running....")
        log(f"for data --> {data}")

        """
        data = {
            "task_id" : {
                "date" : "25-09-2025",
                "from" : "Shimla isbt",
                "to"   : "kangra",
                "service_no" : "261",
                "seat" : ['20', '25', '30', '21', '31']
            }
            ...
        }
        """
        equal_sleep_time = get_equal_sleep(time_in_minutes=22, num_tasks=len(data))


        for my_id in data:
            if self.is_doomsday(for_this_date=data[my_id]['date']):
                log(f"This date({data[my_id]['date']}) is already passed.. skipping this one", type='warn')
                continue

            proxy = use_proxy and self.proxy_obj.get_my_proxy()

            multi_reserver = MutliReserver(
                my_id = my_id, 
                data = data[my_id], 
                url = self.url,
                headless = self.headless_mode,
                proxy = proxy,
            )

            multi_reserver.thread_hold_selected_seat(parent = self)

            self.reserver_obj[my_id] = multi_reserver
            OBJECT_TO_CLEAN.append(multi_reserver)

            # sleep for eqal gap between task.. to save resources
            if len(data) != 1:
                log(f"Sleeping for {timeCal(int(equal_sleep_time))} to save resurces...")
                #sleep(equal_sleep_time)

        
        # all threads are running
        log(f"All process are running on threads..count = {len(self.reserver_obj)}")

        for obj in self.reserver_obj.values():
            obj.thread.join()

        log(f"MultiReserver task completed successfully.....")


    def is_doomsday(self, for_this_date: str = None):
        #check for script end time
        if self.end_time != None  and datetime.now() >= self.end_time:
            log("Doomsday time! The world is going to end. Bye....", type="warn")
            log("Cleaning everything.....")

            for obj in OBJECT_TO_CLEAN:
                obj.close()
            
            log(f"Goodbye sir....")
            os._exit(0) # close everything....
        
        if for_this_date:
            for_this_date = f"{for_this_date} 23:59"
            this_date = datetime.strptime(for_this_date, "%d-%m-%Y %H:%M")
            
            if datetime.now() >= this_date:
                return True
            
            return False



    def hold_seat(self, selected_seats: list = None, use_proxy = False, upto: datetime  = None):
        """To hold a specific seat...."""
        proxy = None
        fastest_proxy = []
        self.is_doomsday()

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
                        self.service_no, None, None, selected_seats, None)
        
        reserver.hold_selected_seat(self)
        OBJECT_TO_CLEAN.append(reserver) # to close the object incase of fore exit


    def passenger_info(self, count = 5):
        pointer = self.db['namePointer']
        passenger_list = get_passenger_list(count = count, pointer = pointer)

        if len(passenger_list) < count:
            count = count - len(passenger_list)
            passenger_list.extend(get_passenger_list(count = count, pointer = 0))
            self.db['namePointer'] = count

        else:
            self.db['namePointer'] = pointer + count

        return [["Aditya Mukhiya", "Male", "22"]]
    
    



if __name__ == "__main__":

    seat_holder = SeatHolder(headless_mode = False)

    # set time to stop this script
    date_str = "26-10-2025"
    time_str = "01:00"
    seat_holder.run_until(date_str = date_str, time_str = time_str)

    data = {
        "for 26-OCT" : {
            "date" : "26-10-2025",
            "from" : "kangra",
            "to"   : "Shimla isbt",
            "service_no" : "908",
            "seat" : ['25'],
        },

        "for 31-OCT" : {
            "date" : "31-10-2025",
            "from" : "kangra",
            "to"   : "Shimla isbt",
            "service_no" : "1721",
            "seat" : ['25'],
        },

    }

    seat_holder.hold_for_multiple_dates(data=data, use_proxy=False)

    
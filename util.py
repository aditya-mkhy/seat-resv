import random
from time import sleep
import csv
import json
import logging
from datetime import datetime
from typing import Literal

# Create log file with current date
log_filename = f"logs/server_{datetime.now().strftime('%Y-%m-%d')}.log"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",  # <== time format here
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

def log(*args, type: Literal["info", "error", "warn"] = "info", **kwargs):
    if type == "info":
        logging.info(*args, **kwargs)

    elif type == "error":
        logging.error(*args, **kwargs)

    elif type == "warn":
        logging.warning(*args, **kwargs)


class PyDb(dict):
    def __init__(self):
        self.file_name = "data.dt"
        self.read()
        
    def read(self) -> dict:
        with open(self.file_name, "r") as ff:
            try:
                self.update(json.loads(ff.read()))
                return self
            except:
                print("ErrorInDataBase: Can't read it..")
                return self.write(refresh = True)

    def write(self, refresh = False) -> dict:
        if refresh:
            self.update({
                "namePointer" : 0,
                "emailPointer" : 0,
            })

        with open(self.file_name, "w") as tf:
            tf.write(json.dumps(self))

    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.write()
        
def get_email(passengers : list):
    one_passenger = random.choice(passengers)
    one_passenger = one_passenger[0].replace(" ", "").lower()

    num = random.randint(100, 100304)

    domain = random.choice(["gmail", "yahoo", "hotmail"])

    return f"{one_passenger}{num}@{domain}.com"

def get_phone():
    number = str(random.randint(6, 9))
    for i in range(9):
        number += str(random.randint(0, 9))

    return number


def get_passenger_list(count = 5, pointer = 1) -> list:
    with open('name_list.csv', 'r') as csv_file:
        skip_count = 0
        reader = csv.reader(csv_file)

        #skip to that line
        for row in reader:
            if skip_count == pointer:
                break
            skip_count += 1


        passenger_list = []
        total = 0
        for row in reader:
            row.append(get_age())
            passenger_list.append(row)

            total += 1
            if total == count:
                break
        
    return passenger_list


def write(path, word):
    for w in word:
        if w == " ":
            sleep(random.uniform(0.2, 0.9))
        else:
            sleep(random.uniform(0.03, 0.09))
        path.send_keys(w)

def get_age():
    return str(random.randint(14, 50))

def timeCal(sec):
    if sec < 60:
        return f"{int(sec)} Sec"
    elif sec < 3600:
        return f"{sec//60}:{ str(sec%60)[:2]} Mint"
    elif sec < 216000:
        return f"{sec//3600}:{ str(sec%3600)[:2]} Hrs"
    elif sec < 12960000:
        return f"{sec//216000}:{ str(sec%216000)[:2]} Days"
    else:
        return "CE"
    
def get_equal_sleep(time_in_minutes: int, num_tasks: int) -> float:
    if num_tasks <= 0:
        raise ValueError("Number of tasks must be greater than 0")

    return (time_in_minutes * 60) / num_tasks



if __name__ == "__main__":
    pass
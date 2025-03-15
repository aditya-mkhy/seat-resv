import random
from time import sleep
import csv
import json

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


if __name__ == "__main__":
    pass
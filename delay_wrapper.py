import time
import datetime

default_clock_minutes = 5 
default_clock_hour = 0

"""
#executes function as soon as next multiple of clock_minutes is reached
class wait_multiple_of_minutes: #class that returns wrapper with passed default_clock_minutes parameter
    def __init__(self, clock_minutes = default_clock_minutes): #set default value, gets replaced if kwarg with different value is passed in
        self.clock_minutes = clock_minutes

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            while not datetime.datetime.now().minute % self.clock_minutes == 0: #do nothing until current minutes is multiple of clock_minutes
                time.sleep(1)
            func(*args, **kwargs)

        return wrapper
"""

class wait_multiple:
    def __init__(self, minute = None, hour = None):
        self.minute = minute
        self.hour = hour

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            while True:
                if self.minute: 
                    if datetime.datetime.now().minute % self.minute == 0:
                        break
                if self.hour:
                    if datetime.datetime.now().hour % self.hour == 0:
                        break
                time.sleep(1)
            func(*args, **kwargs)

     

class wait_exact:
    def __init__(self, minute = None, hour = None):
        self.minute = minute
        self.hour = hour

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            while not (self.minute == datetime.datetime.now().minute or self.hour == datetime.datetime.now().hour):
                time.sleep(1)
            func(*args, **kwargs)

            

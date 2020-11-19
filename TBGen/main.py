#!/bin/python3.6
import os
from Testbench import Testbench
from time import sleep


# The screen clear function
def screen_clear():
    sleep(2)
    # for mac and linux(os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
    # for windows platfrom
        _ = os.system('cls')


my_testench = Testbench()
response = "Y"
while(response != "N" and response != "n"):
    screen_clear()
    if(my_testench.getFile()):
        screen_clear()
        my_testench.getData()
        screen_clear()
        my_testench.createTB()
        break
    else:
        response = input("\nDo you want to try again? (Y/N)\n")
        
    
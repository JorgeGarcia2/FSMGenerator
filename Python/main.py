#!/bin/python3

from FSM import FSM

my_FSM = FSM()

response = "Y"
#Check if the user wants to continue trying new file names
while(response != "N" and response != "n"):
    #If the program finds the file, continue
    if(my_FSM.getFile()):
        #Get data from verilog source file
         my_FSM.getData()
         #Print contents of translator
         my_FSM.print()
         #Create testbench with information found
         my_FSM.createTB()
         #Do not iterate again (Purpose finished)
         response="n"
    else:
    #If the program does not find the file, ask to try again
        response = input("\nDo you want to try again? (Y/N)\n")
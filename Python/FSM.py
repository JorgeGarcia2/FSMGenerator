#!/bin/python3

import re
import os
import datetime 

"""

States[match(1)]=
                [[match(1).split()]
                ,match(2),
                [match(3).slpit()]]
"""
class FSM:
    

    def getFile(self):
        noError = True
        
        #Ask for the verilog source code file name
        fileName = input("\nWhat is the table's filename?\n(It should be a csv file) ")

        #Append ".sv" suffix if not found
        if (not re.match(r"\.csv",fileName)): 
            fileName = fileName + ".csv"

        #Try to open file
        try: 
            f = open(fileName,"r")
        except:
            print(f"The {fileName} file was not found or you do not have read permissions\n")
            fileName=""

            #If cannot open file, check in working directory for other sv files that do not contain "_testbench"
            for fil in os.listdir("."):
                if ".sv" in fil and not "_testbench" in fil:
                    fileName=fil

                    #If a file is found, ask if the user wants to use it
                    print("sv file found, do you want to use: "+fil+"?(Y,N)\n")
                    t=input()
                    #If answer is no, search for more files, else use the file
                    if t!="n" and t!="N":
                        print(f"File {fileName} will be used!\n")
                        f = open(fileName,"r")
                        break
                    else:
                        fileName=""
                        print("File not used")
            #If user does not use any file, send error
            if fileName=="":
                noError = False
        #If there is no error, read the file contents and close file
        if(noError):
            self.designCode = " " + f.read()
            print(f"File {fileName} read successfully")
            f.close()
        return noError
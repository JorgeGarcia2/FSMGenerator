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
        fileName = input("\nWhat is the top model's filename? ")
        #If file has no extension, apend ".v"
        if (fileName.find(".") == -1): 
            fileName = fileName + ".v"
        try: 
            f = open(fileName,"r")
            self.designCode = f.read()
            print("File read successfully")
            f.close()
        except:
            match = re.search(r"^((\w+\/)*).*$", fileName)
            print(match.group(1))
            print(f"The {fileName} file was not found or you do not have read permissions")
            if(match.group(1) != ""): fileName=match.group(1)
            else: fileName = "./"
            if(os.path.isdir(fileName)):
                for file in os.listdir(fileName):
                    if(re.search(r"^\w((?!_testbench).)*\.+(sv|v)$", file)):
                        fileName += file
                        print("\nDesign file found, do you want to use: "+fileName+"?(Y,N)")
                        t=input()
                        if t!="n" and t!="N":
                            print(f"File {fileName} will be used!")
                            f = open(fileName,"r")
                            self.designCode = " "+f.read()
                            print(f"File {fileName} read successfully")
                            f.close()
                            break
                        else:
                            if(match.group(1) != ""): fileName=match.group(1)
                            else: fileName = "./"
                            print("File not used")
                if fileName=="./":
                    noError = False
            else: 
                print("The specified path was not found")
                noError = False
        return noError
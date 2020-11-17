#!/bin/python3

import re
import os

def getString():
    fileName = input("\nWhat is the table's filename?\n(It must be a csv file) ")
    #If file has no extension, apend ".csv"
    if (fileName.find(".") == -1): 
        fileName = fileName + ".csv"
    try: 
        f = open(fileName,"r")
        fileCont = f.read()
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
                if(re.search(r"^\w((?!FSM_Design).)*\.+(sv|v)$", file)):
                    fileName += file
                    print("\nDesign file found, do you want to use: "+fileName+"?(Y,N)")
                    t=input()
                    if t!="n" and t!="N":
                        print(f"File {fileName} will be used!")
                        f = open(fileName,"r")
                        fileCont = f.read()
                        print(f"File {fileName} read successfully")
                        f.close()
                        break
                    else:
                        if(match.group(1) != ""): fileName=match.group(1)
                        else: fileName = "./"
                        print("File not used")
            if fileName=="./":
                fileCont = ""
        else: 
            print("The specified path was not found")
            fileCont = ""
    return fileCont

if (__name__=="__main__"):
    print(getString())
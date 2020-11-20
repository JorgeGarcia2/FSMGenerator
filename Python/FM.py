#!/bin/python3

import csv
import re
import os

gsuf = ""
gkey = ""

#Prompts for valid file name and assigns file text to string
def getFileCont(suf,key):
    global gsuf
    global gkey
    gkey = key
    gsuf = suf
    f = open(getFileName())
    fileCon = f.read()
    f.close()
    return fileCon

def getFileName(suf = "",key = ""):
    if (suf == ""):
        suf = gsuf
        key = gkey
    fileCont = "y"
    #Check if the user wants to continue trying new file names
    while(fileCont == "Y" or fileCont == "y"):
        fileCont = ""
        fileName = input("\nWhat is the top model's filename?\n(This program only searches for "+suf+" estensions) ")
        #If file has no extension, apend .suf
        if (fileName.find(".") == -1): 
            fileName = fileName + "." + suf
        try: 
            f = open(fileName,"r")
            fileCont = "Hola"
            f.close()
        except:
            match = re.search(r"^((\w+\/)*).*$", fileName)
            print(match.group(1))
            print(f"The {fileName} file was not found or you do not have read permissions")
            if(match.group(1) != ""): fileName=match.group(1)
            else: fileName = "./"
            if(os.path.isdir(fileName)):
                for file in os.listdir(fileName):
                    if(re.search(r"^\w((?!"+key+r").)*\."+suf+"$", file)):
                        fileName += file
                        print("\nDesign file found, do you want to use: "+fileName+"?(Y,N)")
                        t=input()
                        if t!="n" and t!="N":
                            print(f"File {fileName} will be used!")
                            f = open(fileName,"r")
                            fileCont = "Hola"
                            f.close()
                            break
                        else:
                            if(match.group(1) != ""): fileName=match.group(1)
                            else: fileName = "./"
                            print("File not used!")
            else: 
                print("The specified path was not found")
        
        #If the program does not find the file, ask to try again
        if (fileCont == ""):
            fileCont = input("\nDo you want to try again? (Y/N)\n")
            if (fileCont == "N" or fileCont == "n"):
                fileName = ""
                fileCont = ""
            else: fileCont = "y"
    return fileName

def getFSMData(path):
    states = {}     #Dictionary for states: [inputs, Next state, outputs]  
    NameInputs = []    #List of 
    NameOutputs = []
    fistState = ""
    regex = r"^(\w+)\((\d+)((b|h|d)|.*)\)$"
    tempIn = []
    tempOut = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            i += 1
            tempIn = row[0].split("|")
            tempOut = row[3].split("|")
            
            if (i==2): 
                for elemet in tempIn:
                    match = re.search(regex,elemet)
                    NameInputs.append([match.group(1), match.group(2), match.group(4)])
                for elemet in tempOut:
                    match = re.search(regex,elemet)
                    NameOutputs.append([match.group(1), match.group(2), match.group(4)])
            if (i>2):
                if(i == 3): fistState = row[2]
                #InputValue = [size]'[radix][value]
                for j in range(len(tempIn)):
                    #if radix was not specified, "d" by default
                    if (tempIn[j] != "x" and tempIn[j] != "X"):
                        if (NameInputs[j][2] == None): NameInputs[j][2] = "d"
                        tempIn[j] = NameInputs[j][1] + "'" + NameInputs[j][2] + tempIn[j]
                #OutputValue = [size]'[radix][value]
                for j in range(len(tempOut)):
                    if (tempOut[j] != "x" and tempOut[j] != "X"):
                        if (NameOutputs[j][2] == None): NameOutputs[j][2] = "d"
                        tempOut[j] = NameOutputs[j][1] + "'" + NameOutputs[j][2] + tempOut[j]
                #If key doesn't exist
                if(states.get(row[1]) == None): 
                    states[row[1]] = [[tempIn, row[2], tempOut]]
                else: 
                    states[row[1]].append([tempIn, row[2], tempOut])
    return states, NameInputs, NameOutputs, fistState
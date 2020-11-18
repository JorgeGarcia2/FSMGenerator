#!/bin/python3

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
    st = f.read()
    f.close()
    return st

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
            #fileCont = f.read()
            #print(f"File {fileName} read successfully")
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
                            #fileCont = f.read()
                            #print(f"File {fileName} read successfully")
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

#Makes the output logic for the machine
def getFSMOLogic(dicS,dicK):
    FSMSLogic="\n  //Next State Logic Block\n  always@(state"
    
    for i in dicK["inputs"]: FSMSLogic += " or " + i
    FSMSLogic += ")\n  begin\n    case(state)\n"

    for S in dicS.keys():
        FSMSLogic += "      " + S + ":\n"
        IF = False
        for i in range(len(dicS[S])):
            if (IF): Temp = "        else if("
            else: Temp = "        if("
            f=False
            for j in range(len(dicS[S][i][0])):
                if (dicS[S][i][0][j] != "x" and dicS[S][i][0][j] != "X"):
                    if (f): Temp += " && "
                    Temp += dicK["inputs"][j] + " == " + dicS[S][i][0][j]
                    f=True
            if (Temp != "        if("):
                IF = True
                FSMSLogic += Temp + ") "
            else:
                FSMSLogic += "        "
            FSMSLogic += "nextstate = " + dicS[S][i][1] + ";\n"
        if (IF):
            FSMSLogic += "        else nextstate = " + dicK["ppal"] + ";"
        FSMSLogic += "\n"
    FSMSLogic += "      default:\n        nextstate = " + dicK["ppal"] + ";\n    endcase\n  end\n"
    return FSMSLogic
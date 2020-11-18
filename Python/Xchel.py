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

#Prompts for valid file name and assigns file text to string
def getFSMSLogic(dic,ppal):
    FSMSLogic="\n  //Next State Logic Block\n  always@(state"
    
    for i in range(len(dic["S0"][0][0])): FSMSLogic += " or in" + str(i)
    FSMSLogic += ")\n  begin\n    case(state)\n"

    for S in dic.keys():
        FSMSLogic += "      " + S + ":\n"
        for i in range(len(dic[S])):
            Temp = "        if("
            f=False
            for j in range(len(dic[S][i][0])):
                if (dic[S][i][0][j] != "x" and dic[S][i][0][j] != "x"):
                    if (f): Temp += " && "
                    Temp += "in" + str(j) + " == " + dic[S][i][0][j]
                    f=True
            if (Temp != "        if("):
                FSMSLogic += Temp + ") "
            else:
                FSMSLogic += "        "
            FSMSLogic += "nextstate = " + dic[S][i][1] + ";\n"
        FSMSLogic += "\n"
    FSMSLogic += "      default:\n        nextstate = " + ppal + ";\n    endcase\n  end"
    return FSMSLogic

if (__name__=="__main__"):
    import Jorch
    import Fers

    fileName = getFileName("csv","_Design")
    
    if (fileName == ""):
        print("There is no table!")
    else:
        print("Here's the table!\n\n"+fileName+"\n\n")
        dictio = Jorch.getFSMDic(fileName)
        #dictio = {"S0":[[[0],"S1",[0]],[[1],"S2",[1]]],"S1":[[[0],"S2",[1]],[[1],"S1",[0]]],"S2":[[[0],"S0",[1]],[[1],"S0",[1]]]}
        print(Fers.getFSMHead(dictio,"FSM"))
        print(getFSMSLogic(dictio,"S0"))
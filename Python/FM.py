#!/bin/python3

import csv
import re
import os

#**************************************************************************************************
#   Function:
#       getFileName(suf = "",key = "").
#
#   Description:
#       This function asks for a file name and search for it in the directory given. 
#       If the file was not found, it will search for other files in the current directory 
#       and give the user the option to use them.
#       Additionally, a file extension and a keyword can be passed as a parameter, this will
#       limit the search to files with the extension and without the keyword.
#
#   Precondition:
#       None.
#
#   Parameters:
#       * suf - File extention to use.
#       * key - Ignored files Keyword.
#
#    Return Values:
#       * fileName - File name to use.
#**************************************************************************************************
def getFileName(suf = "",key = ""):
    
    fileCont = True
    # Check if the user wants to continue trying new file names
    while(fileCont):
        fileCont = False
        fileName = input("\nWhat is your "+suf.upper()+"'s filename? ")
        
        # If file has no extension, apend .suf
        if (fileName.find(".") == -1): 
            fileName = fileName + "." + suf

        # Try to open the file
        try: 
            f = open(fileName,"r")
            fileCont = True
            f.close()
        except:
            # Get the path of the file the user is trying to access and warn of inexistent file
            match = re.search(r"^((\w+\/)*).*$", fileName)
            print(match.group(1))
            print(f"The {fileName} file was not found or you do not have read permissions")

            # If there was a path, use it
            # else, use working directory
            if(match.group(1) != ""): fileName=match.group(1)
            else: fileName = "./"
            # Check if the path entered is found
            if(os.path.isdir(fileName)):
                # Get files in the directory
                for file in os.listdir(fileName):

                    # Check if there are files that do not contain the key of the program's output
                    # but do contain the same extension as the needed input
                    if(re.search(r"^\w((?!"+key+r").)*\."+suf+"$", file)):
                        fileName += file

                        # Ask user if he wants to use the file
                        t=input("\n"+suf.upper()+" file found, do you want to use: "+fileName+" (Y,N)? ")
                        
                        if t!="n" and t!="N":

                            # If it's going to be used, fill fileCont with a non-empty string
                            print(f"File {fileName} will be used!")
                            fileCont = True
                            break
                        else:
                            # If file is not going to be used, keep searching for files
                            if(match.group(1) != ""): fileName=match.group(1)
                            else: fileName = "./"
                            print("File not used!")
            else:
                print("The specified path was not found")
        
        # If the program does not find the file, ask to try again
        if (fileCont == False):
            t = input("\nDo you want to try again (Y/N)? ")
            if (t == "N" or t == "n"):
                fileName = ""
                fileCont = False
            else: fileCont = True
        else: fileCont = False
    return fileName

#**************************************************************************************************
#   Function:
#       getFSMData(path).
#
#   Description:
#       This function opens a csv file with the description of a finite state machine and gets 
#       the information of the state transitions, the input and output names and the start state, 
#       and places it in containers to finally return them. 
#
#   Precondition:
#       This function must be called with an existing path. Otherwise it will produce fail.
#
#   Parameters:
#       * path - Path of the csv file to use.
#
#    Return Values:
#       * states - Dictionary for states transitions: [state:[inputs, Next state, outputs]]  
#       * NameInputs - List of inputs names with its radix and bus size.
#       * NameOutputs - List of outputs names with its radix and bus size.
#       * firstState - Name of the fist state.
#**************************************************************************************************
def getFSMData(path):
    states = {}                             # Dictionary for states transitions: [state:[inputs, Next state, outputs]]
    NameInputs = []                         # List of inputs names with its radix and bus size.
    NameOutputs = []                        # List of outputs names with its radix and bus size.
    firstState = ""                         # Name of the fist state.
    regex = r"^(\w+)($|\((\d+)((b|h|d)|.*)\)$)" # RegEx for the table header
    tempIn = []                             # Auxilary list for inputs values
    tempOut = []                            # Auxilary list for outputs values

    # Open the file for reading
    with open(path, 'r') as file:

        # Read the file as a csv table
        reader = csv.reader(file)
        i = 0

        # Iterate over rows
        for row in reader:
            i += 1

            # Get inputs and outputs values and split them into their list
            tempIn = row[0].split("|")
            tempOut = row[3].split("|")
            
            # If the second row is being read, get information about inputs and outputs
            if (i==2): 

                # Get input names, size and radix
                for elemet in tempIn:
                    match = re.search(regex,elemet)
                    # If the FSM has inputs, append the corresponding data
                    if (match != None):
                        NameInputs.append([match.group(1), match.group(3), match.group(5)])              

                # Get output names, size and radix
                for elemet in tempOut:
                    match = re.search(regex,elemet)
                    NameOutputs.append([match.group(1), match.group(3), match.group(5)])

            # If the read row is below the second row, get values
            if (i>2):
                #Get the first state read
                if(i == 3): firstState = row[2]
                # InputValue = [size]'[radix][value]
                # OutputValue = [size]'[radix][value]
                    # if size was not specified, "1" by default
                    # if radix was not specified, "d" by default
                for j in range(len(tempIn)):
                    if (tempIn[j] != "x" and tempIn[j] != "X"):
                        if (NameInputs[j][1] == None): NameInputs[j][1] = "1"
                        if (NameInputs[j][2] == None): NameInputs[j][2] = "d"
                        tempIn[j] = NameInputs[j][1] + "'" + NameInputs[j][2] + tempIn[j]
                for j in range(len(tempOut)):
                    if (tempOut[j] != "x" and tempOut[j] != "X"):
                        if (NameOutputs[j][1] == None): NameOutputs[j][1] = "1"
                        if (NameOutputs[j][2] == None): NameOutputs[j][2] = "d"
                        tempOut[j] = NameOutputs[j][1] + "'" + NameOutputs[j][2] + tempOut[j]

                # If key doesn't exist, create
                # else, append the values read
                if(states.get(row[1]) == None): 
                    states[row[1]] = [[tempIn, row[2], tempOut]]
                else: 
                    states[row[1]].append([tempIn, row[2], tempOut])

    # Return states dictionary, nameInputs matrix, NameOutputs matrix and firstState string
    return states, NameInputs, NameOutputs, firstState
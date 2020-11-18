#!/bin/python3
import csv
import re

def getFSMDic(path):
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
            print(row)
    return states, NameInputs, NameOutputs, fistState

if (__name__=="__main__"):
    print(getFSMDic('D:\Bibliotecas\Documents\Repositorios\FSMGenerator\MultiFSM.csv'))
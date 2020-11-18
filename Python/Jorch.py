#!/bin/python3
import csv
def getFSMDic():
    states = {}
    with open('D:\Bibliotecas\Documents\Repositorios\FSMGenerator\FSMTable.csv', 'r') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            i += 1
            if (i>2):
                if(states.get(row[1]) == None): states[row[1]] = [[row[0].split("|"), row[2], row[3].split("|")]]
                else: states[row[1]].append([row[0].split("|"), row[2], row[3].split("|")])
            print(row)
    return states

if (__name__=="__main__"):
    print(getFSMDic())


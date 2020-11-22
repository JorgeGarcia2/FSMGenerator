#!/bin/python3

# import custom FSM and file manager modules
import FSM
import FM

# Get a valid file name prompting the user and
# searching in directories
fileName = FM.getFileName("csv","_Design")

# If a valid file was found, continue
if (fileName == ""):
		print("There is no table!")
else:
		# Get data from file
		dictio, NI, NO, ppal = FM.getFSMData(fileName)
		# Get the path of the file and the name without extension
		name = fileName[:-4]
		# Get the string value of the code header
		FSMstr = FSM.getFSMHead(dictio,name,NI,NO)
		# Get the string value of the logic code
		FSMstr += FSM.getFSMLogic(dictio,NI,NO,ppal)
		# Write the code to a new file
		FSM.writeFSM(name,FSMstr)
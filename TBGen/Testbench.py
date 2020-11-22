#!/bin/python3

import re
import os
import datetime
from PortTB import Port
from PortTB import Input


class Testbench:
    def __init__(self):
        self.designCode = None
        self.module_name = ""
        self.inputs = []
        self.outputs = []
        self.clock = None
        self.reset = None
        self.time = 0
        self.iters = 1
        self.radix = "dec"
        self.types = {"C":0,"R":0,"d":0,"i":0,"s":0, "c":0, "r":0} #Stores how many bits of every input type there is
        self.Auto = True

    #Prompts for valid file name and assigns file text to string
    def getFile(self):
        noError = True
        
        #Ask for the verilog source code file name
        fileName = input("\nWhat is the top model's filename? ")

        #If file has no extension, apend ".v"
        if (fileName.find(".") == -1): 
            fileName = fileName + ".v"

        #Try to open file
        try: 
            f = open(fileName,"r")
            self.designCode = " " + f.read()
            print("File read successfully")
            f.close()
        except:
            match = re.search(r"^((\w+\/)*).*$", fileName)
            print(match.group(1))
            print(f"The {fileName} file was not found or you do not have read permissions\n")
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
                            self.designCode = " " + f.read()
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

    def getData(self):
        data = {"input": [],
                "output": []}
        #Remove all the comments
        self.designCode = re.sub(r"(//.*)", "", self.designCode) #erase comment line
        self.designCode = re.sub(r"(/\*)(.|\n)*?(\*\/)", "", self.designCode) #erase block comment
        
        for i in re.finditer(r"parameter\s*\w*\s*=\s*\d+\s*(,\s*\w*\s*=\s*\d*\s*)*", self.designCode): #modify Parameters to their values
            for j in re.findall(r"\w*\s*=\s*\d+",i.group()):
                k=re.split(r"=",j.replace(" ",""))
                self.designCode = self.designCode.replace(k[0],k[1])

        pattern = r"\W+((module|input|output|inout)\s*(reg|wire|\s*)\s*(\[[\w\s\+\-\*]+:[\w\s\+\-\*]+\]\s*|\s+)\s*(((,\s*|\s*)((?!input|output|inout)[_a-zA-Z]\w*))*))"
        
        #Find match and delete it from main code
        match = re.search(pattern, self.designCode)
        self.designCode = re.sub(pattern, "", self.designCode, 1)
        
        #Iterate over found patterns
        while match:
            #Get names
            names = match.group(5).replace(" ","").split(",")

            #Get range
            if re.search(":",match.group(4)): 
                ran = re.split(r"[:\[\] ]",match.group(4))
            else: 
                ran=["","0","0",""]
                
            #If it's the module, get name
            print(match.group(2) + names[0])
            if (match.group(2).replace(' ','') == "module"): self.module_name = names[0]
            else:
                #Else, check if there are operations in the range, if so, calculate them and get vinteger values
                for j in range(2):
                    if "-" in str(ran[j+1]):
                        arg1=ran[j+1].split("-")[0]
                        arg2=ran[j+1].split("-")[1]
                        ran[j+1]=int(arg1)-int(arg2)
                    elif "+" in str(ran[j+1]):
                        arg1=ran[j+1].split("+")[0]
                        arg2=ran[j+1].split("+")[1]
                        ran[j+1]=int(arg1)+int(arg2)
                    elif "*" in str(ran[j+1]):
                        arg1=ran[j+1].split("*")[0]
                        arg2=ran[j+1].split("*")[1]
                        ran[j+1]=int(arg1)*int(arg2)
                    else: ran[j+1]=int(ran[j+1])
                #Store a default value for each name
                for i in range(0,len(names)):
                        data[match.group(2).replace(' ','')].append([names[i], ran[1], ran[2], 'C', 1]) 
            
            #Search for matches and delete them
            match = re.search(pattern, self.designCode)
            self.designCode = re.sub(pattern, "", self.designCode, 1)

        #Ask for automatic translation
        self.Auto=input("\nDo you want a fully automated translation?(Y,n)\n"
        "If so, the program will ask if clock and reset signals are correct\n"
        "and go through all signal combinations for the others, if the cycles number in this case is bigger than 16, for cycles will be used\n"
        "random values will be used instead\n")
        if(self.Auto=="N" or self.Auto=="n"): self.Auto = False
        else: self.Auto = True

        #Ask for values and steps of inputs
        if (not self.Auto): print("\nEnter the initial value and the steps for the entries listed below separated by an enter.\n"
            "(The default values ​​will be a random numbering and steps of 1).\n")
        for e in data["input"]:
            e.append(1)
            e[3]=""
            #heck size of signal for clocks and resets
            if (e[1]==e[2]):
                #If c,l,k detected, ask if correct
                if (re.search(r"\w*[cC][lL]\w*[kK]\w*",e[0]) and self.clock == None):
                    res = input(f"\nInput {e[0]} has been detected as a possible clock signal. Is this correct? (Y/N)\n")
                    if (res != "N" or res != "n"): e[3] = 'c' 
                #If r,s,t detected, ask if correct
                elif (re.search(r"\w*[rR]\w*[sS]\w*[tT]\w*", e[0]) and self.reset == None):
                    res = input(f"\nInput {e[0]} has been detected as a possible reset signal. Is this correct? (Y/N)\n")
                    if (res != "N" or res != "n"): e[3] = 'r'
            #Operations if no automatic translation
            if (not self.Auto):
                if (e[3]!='c' and e[3]!='r'):
                    
                    #Ask for type of value and check for problems
                    e[3] = input(f"\n{e[0]} [{e[1]}:{e[2]}]\n\tType of value([i]ncreasing, [d]ecreasing, [R]andom, [s]tatic, [c]lock, [r]eset)\n"
                    "(Default is Random): ")
                    if(e[3]=="c" and self.clock!=None): e[3]="R"
                    if(e[3]=="r" and self.reset!=None): e[3]="R"
                    if(e[3]!="i" and e[3]!="d" and e[3]!="R" and e[3]!="s" and e[3]!="c" and e[3]!="r"): e[3]="R"

                    #Ask for step value
                    if(e[3]=="i" or e[3]=="d"):
                        res = input(f"\tStep: ")
                        if (res.isdecimal()): e[5] = int(res)
                        else: e[5]=1
                    elif (e[3] == "s"): e[5]=0
                    else: e[5]=1

                #ask for initial value
                res = 0
                if (e[3]!="R" and e[3]!="r" and e[3]!="C"):
                    res = input(f"\n{e[0]} [{e[1]}:{e[2]}]\n\tInitial value: ")
                    if (res.isdecimal()): e[4] = int(res)
                    else: e[4]=0

                #In case of reset, ask for active value
                if (e[3]=="r"):
                    res = input(f"\n{e[0]} [{e[1]}:{e[2]}]\n\tActive value: ")
                    if (res.isdecimal()): e[4] = int(res)
                    else: e[4]=1
            else:
                #Give default values when auto translation enabled
                if (e[3]!='c' and e[3]!='r'): e[3]="C"
                if (e[3]=="r"): e[4] = 1
                else: e[4] = 0
                e[5] = 1

            #Store data and increment number of bytes in value type
            self.types[e[3]] += 1
            if (e[3] == 'c'): self.clock = Input(e)
            elif (e[3] == 'r'): self.reset = Input(e)
            else:
                self.inputs.append(Input(e))
                self.types[e[3]] += self.inputs[-1].rangePort

        #Get outputs
        for o in data["output"]:
            self.outputs.append(Port(o))

        #  Check if combinational aproach is viable or if it's better
        #  to use Random values based in the number of iterations
        if (self.types["C"] > 10):
            print("It will iterate more than 1024 times! for the simulation's safety,\ncombinational results will not be used and random values are used instead!")
            self.types["R"] = self.types["C"]
            self.types["C"] = 0
            for i in self.inputs: i.type= "R"
        else: self.time = 2**self.types["C"]
        if (not self.Auto or self.types["C"] == 0):
            try:
                #Ask for time intervals, catch problems
                self.time = int(input("How many time intervals do you want? "))
                if(self.time>1000): raise ArithmeticError
            except ArithmeticError: print("Value too big, using default: 10\n")
            except: print("Value not understood, using default: 10\n")
            finally: self.time = 10

        #Ask for radix
        self.radix = input("Choose the test vectors radix ('bin', 'dec' or 'hex')\n")

    def writeTB(self):

        #Store code in string, Store header with names, comments, information about the program and the testbench
        date = datetime.datetime.now()
        textTB =  ("/*"+ 80*"*"+"\n"
            "* Testbench created automatically with a program written in Python 3.8 by:\n"
            "*\t - Garcia Vidal Jorge Alberto\n"
            "*\t - Morales Hurtado David Xchel\n"
            "*\t - Rodriguez Contreras Luis Fernando\n*\n"
            "* For the first project in the class of professor:\n"
            "*\t - Carolina Rosas Huerta\n"
            "* In the Silicon Verification Program\n*\n"
            f"* \tDesign Name : {self.module_name}\n"
            f"* \tFile Name : {self.module_name}_testbench.sv\n"
            f"* \tDate: {date.strftime('%B %d, %Y')}\n")
        textTB += ("" + 80*"*"+"*/\n\n"
            "//time scale\n"
            "`timescale 1ns/1ps\n\n"
            "//Main Testbench Starts here\n"
            f"module {self.module_name}_TB;\n\n"
            "//Signal instantiation\n")

        #Instantiate signals
        if (self.clock != None):
            textTB += f"reg {self.clock.namePort}_TB;\n"
        if (self.reset != None):
            textTB += f"reg {self.reset.namePort}_TB;\n"
        for i in self.inputs:
            textTB += f"reg {i.rangePortTB()}{i.namePort}_TB;\n"
        for i in self.outputs:
            textTB += f"wire {i.rangePortTB()}{i.namePort}_TB;\n"
            
        #Instantiate module
        textTB += f"\n{self.module_name} UUT("
        if (self.clock != None):
            textTB += f".{self.clock.namePort}({self.clock.namePort}_TB), "
        if (self.reset != None):
            textTB += f".{self.reset.namePort}({self.reset.namePort}_TB), "
        for i in self.inputs:
            textTB += f".{i.namePort}({i.namePort}_TB), "
        for i in self.outputs:
            textTB += f".{i.namePort}({i.namePort}_TB)"
            if(i != self.outputs[-1]):
                textTB += ", "
            else: 
                textTB += ");\n\n"
        
        #Instantiate clock commutation
        if (self.clock != None): textTB += f"//Clock initialization as commuter\nalways forever #1 {self.clock.namePort}_TB = ~{self.clock.namePort}_TB;\n\n"
        
        #Start initial
        textTB += ("initial\n"
        "\tbegin\n"
        f'\t\t$dumpfile("{self.module_name}.vcd");\n'
        f"\t\t$dumpvars(1, {self.module_name}_TB);\n\n\t\t")

        #Initialize all the ports
        textTB += "//Initializing values\n"
        if (self.clock != None):
            textTB += f"\t\t{self.clock.printValue()};\n"

        if (self.reset != None):
            textTB += f"\t\t{self.reset.printValue()};\n"
        for i in self.inputs:
            textTB += f"\t\t{i.printValue(self.radix)};\n"
        
        if (self.reset != None):
            textTB += "\n\t\t#2\n\t\t//Deactivating reset\n"
            textTB += f"\t\t{self.reset.namePort}_TB = ~ {self.reset.namePort}_TB;\n"
        
        #Print number of iterations
        textTB += f"\n\t\t//The program will iterate {self.time} times\n"

        #Check if combinational mode is used
        if (self.types["C"]==0):
            for times in range(self.time):
                textTB += f"\n\t\t//Iteration: {times+1}\n\t\t#1\n"
                for i in self.inputs:
                    #If combinational mode not used, change value according to value type and print it
                    i.chValue()
                    textTB += f"\t\t{i.printValue(self.radix)};\n"
            textTB += f"\n\t\t//Ending iteration\n\t\t#1"
        else:
                #If combinational mode enabled, use recursive function
                textTB += f"\n\t\t//Iteration: 1\n\t\t#1\n"
                textTB += self.recuFun()
                textTB += f"\n\t\t//Ending iteration\n\t\t#1"

        #Finish testbench code
        textTB += "\n\t\t$finish;\n\tend\nendmodule"
        
        return textTB

    def recuFun(self, val=0, st=""):
        #If the cycles are less than 32, do not use "for" cycles
        if (self.types["C"]<5):
            for i in range(2**(self.inputs[val].rangePort + 1)):
                if (self.inputs[val].value != 0):
                    self.iters += 1
                    st += f"\n\t\t//Iteration: {self.iters}\n\t\t#1\n"
                self.inputs[val].chValue()
                if (val+1 < len(self.inputs)): st += self.recuFun(val + 1)
                st += f"\t\t{self.inputs[val].printValue()};\n"
        else:
            #Else, use "for" cycles in the testbench code
            if (val < len(self.inputs)):
                st += "" + self.iters * "\t" + f"\tfor(integer i{str(self.iters)}=0;i{str(self.iters)}<{2**(self.inputs[val].rangePort + 1)};i{str(self.iters)}++) begin\n"
                self.iters += 1
                st += self.recuFun(val+1)
                self.iters -= 1
                st += "" + self.iters * "\t" + f"\t\t{self.inputs[val].namePort}_TB += 1;\n" + self.iters * "\t" + "\tend\n"
            else:
                st += "" + self.iters * "\t" + f"\t#1\n"
        return st
    
    #Function to open file and write to it
    def createTB(self):
        f = open(self.module_name + "_testbench.sv", "w")
        f.write(self.writeTB())
        f.close()
        print(f"\n{self.module_name}_testbench.sv file has been created successfully")

    #Function to give an easy to read tree ofthe elements in the translation
    def print(self):
        print(f"\nModule: {self.module_name}\n|\n|->Inputs")
        for i in self.inputs:
            print("|  |")
            i.print()
        print("|\n|")
        print(f"|->Outputs")
        for i in self.outputs:
            print("|  |")
            i.print()
        print("|->Clock\n|")
        self.clock.print()
        print("|->Reset\n|")
        self.reset.print()
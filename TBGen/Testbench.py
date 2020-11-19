#!/bin/python3.6
 # !/bin/python3.8 --> From Jorge
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
        self.time = 10
        self.radix = "dec"

    #Prompts for valid file name and assigns file text to string
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

    def getData(self):
        data = {"input": [],
                "output": []}
        #Remove all the comments
        self.designCode = re.sub(r"(//.*)", "", self.designCode) #erase comment line
        self.designCode = re.sub(r"(/\*)(.|\n)*?(\*\/)", "", self.designCode) #erase block comment
        
        for i in re.finditer(r"parameter\s*\w*\s*=\s*\d+\s*(,\s*\w*\s*=\s*\d*\s*)*", self.designCode): #modify Parameters
            for j in re.findall(r"\w*\s*=\s*\d+",i.group()):
                k=re.split(r"=",j.replace(" ",""))
                self.designCode = self.designCode.replace(k[0],k[1])

        pattern = r"\W+((module|input|output|inout)\s*(reg|wire|\s*)\s*(\[[\w\s\+\-\*]+:[\w\s\+\-\*]+\]\s*|\s+)\s*(((,\s*|\s*)((?!input|output|inout)[_a-zA-Z]\w*))*))"
        
        match = re.search(pattern, self.designCode)
        self.designCode = re.sub(pattern, "", self.designCode, 1)
        
        while match:
            names = match.group(5).replace(" ","").split(",")
            if re.search(":",match.group(4)): 
                ran = re.split(r"[:\[\] ]",match.group(4))
            else: 
                ran=["","0","0",""]
                
            for i in range(0,len(names)):
                if (match.group(2).replace(' ','') == "module"): self.module_name = names[0]
                else:
                    ################Actuar dependiendo de Operación o número
                    for j in range(2):
                        if "-" in str(ran[j+1]):
                            arg1=ran[j+1].split("-")[0]
                            arg2=ran[j+1].split("-")[1]
                            ran[j+1]=int(arg1)-int(arg2)
                            #ran[j+1]=int(ran[j+1].split("-")[0])-int(ran[j+1].split("-")[1])
                        elif "+" in str(ran[j+1]):
                            arg1=ran[j+1].split("+")[0]
                            arg2=ran[j+1].split("+")[1]
                            ran[j+1]=int(arg1)+int(arg2)
                            #ran[j+1]=int(ran[j+1].split("+")[0])+int(ran[j+1].split("+")[1])
                        elif "*" in str(ran[j+1]):
                            arg1=ran[j+1].split("*")[0]
                            arg2=ran[j+1].split("*")[1]
                            ran[j+1]=int(arg1)*int(arg2)
                            #ran[j+1]=int(ran[j+1].split("*")[0])*int(ran[j+1].split("*")[1])
                        else: ran[j+1]=int(ran[j+1])
                    data[match.group(2).replace(' ','')].append([names[i], ran[1], ran[2], 'R', 1]) 
                   
            match = re.search(pattern, self.designCode)
            self.designCode = re.sub(pattern, "", self.designCode, 1)

        for e in data["input"]:
            if (e[1]==e[2]):
                if (re.search(r"\w*[cC][lL]\w*[kK]\w*",e[0])):
                    res = input(f"\nInput {e[0]} has been detected as a possible clock signal. Is this correct? (Y/N)\n")
                    if (res == "Y" or res == "y"): e[3] = 'c' 
                elif (re.search(r"\w*[rR]\w*[sS]\w*[tT]\w*", e[0])):
                    res = input(f"\nInput {e[0]} has been detected as a possible reset signal. Is this correct? (Y/N)\n")
                    if (res == "Y" or res == "y"): e[3] = 'r' 

        print("\nEnter the initial value and the steps for the entries listed below.\n"
              "(The default values ​​will be a random numbering and steps of 1).")
        for e in data["input"]:
            if (e[3]!='c' and e[3]!='r'):
                res = input(f"\n*{e[0]} [{e[1]}:{e[2]}]\n\tInitial value: ")
                if (res.isdecimal()): e[3] = int(res)
                res = input(f"\tStep: ")
                if res != "": e[4] = int(res)
                if (res.isdecimal()): e[4] = int(res)
            if (e[3] == 'c'): self.clock = Input(e)
            elif (e[3] == 'r'): self.reset = Input(e)
            else: self.inputs.append(Input(e))
        if (self.reset != None):
            res = input(f"\nYour Reset signal use negative logic?: ")
            if (res == "N" or res == "n"): self.reset.value = 0
            else: self.reset.value = 1
        if (self.clock != None):
            res = input(f"\nYour Clock signal start on 0?: ")
            if (res == "N" or res == "n"): self.clock.value = 1
            else: self.clock.value = 0
            
            

        for o in data["output"]:
            self.outputs.append(Port(o))
        try:
            self.time = int(input("\nHow many time intervals do you want? "))
        except:
            print("Value not understood, using default: 10")
        self.radix = input("Choose the test vectors radix ('bin', 'dec' or 'hex'): ")
        
        

    def writeTB(self):
        date = datetime.datetime.now()
        textTB =  ("/*"+ 80*"*"+"\n"
            "* Testbench created automatically with a program written in Python 3.8 by:\n"
            "*\t - Garcia Vidal Jorge Alberto\n"
            "*\t - Morales Hurtado David Xchel\n"
            "*\t - Rodriguez Contreras Luis Fernando\n"
            "* For the first project in the class of professor:\n"
            "*\t - Carolina Rosas Huerta\n"
            "* In the Silicon Verification Program\n*\n"
            f"* \tDesign Name : {self.module_name}\n"
            f"* \tFile Name : {self.module_name}_testbench.sv\n"
            f"- \tDate: {date.strftime('%B %d, %Y')}\n"
            "" + 80*"*"+"*/\n"
            "`timescale 1ns/1ps\n\n"
            "//Main Testbench Starts here\n"
            f"module {self.module_name}_TB;\n\n"
            "\t//Signal instantiation\n")

        if (self.clock != None):
            textTB += f"\treg {self.clock.namePort}_TB;\n"
        if (self.reset != None):
            textTB += f"\treg {self.reset.namePort}_TB;\n"
        for i in self.inputs:
            textTB += f"\treg {i.rangePortTB()}{i.namePort}_TB;\n"
        for i in self.outputs:
            textTB += f"\twire {i.rangePortTB()}{i.namePort}_TB;\n"
            
        textTB += ("\t//Module instantiation\n"
                f"\t{self.module_name} UUT(")
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
            
        #Clock bucle
        if (self.clock != None):
            textTB += ("\t//Clock bucle\n"
                f"\talways forever #1 {self.clock.namePort}_TB = ~{self.clock.namePort}_TB;\n\n")
        
        #Main initial block
        textTB += ("\t//Main initial block\n"
            "\tinitial begin\n")
        #Clock and Reset signals initials values 
        if (self.clock != None):
            textTB += ("\t\t//Clock initial values\n"
                f"\t\t{self.clock.namePort}_TB = {self.clock.value};\n")

        if (self.reset != None):
            textTB += ("\t\t//Reset initial values\n"
            f"\t\t{self.reset.namePort}_TB = {self.reset.value};\n")
            self.reset.nextValue()
            textTB +=f"\n\t\t//Reset on\n\t\t#0.5\t{self.reset.namePort}_TB = {self.reset.value};\n"
            self.reset.nextValue()
            textTB +=f"\t\t//Reset off\n\t\t#1\t{self.reset.namePort}_TB = {self.reset.value}; #0.5\n"
        
        #Start iterations
        textTB += f"\n\t\t//The program will iterate {self.time} times"
        for times in range(self.time):
            textTB += f"\n\t\t//Iteration: {times+1}\n"
            for i in self.inputs:
                textTB += f"\t\t{i.printValue(self.radix)};\n" 
                i.nextValue()
            #Display outputs
            textTB += '\t\t$display("|'
            for i in self.outputs:
                textTB += f"{i.namePort} = %b |"
            textTB += '", '
            for i in self.outputs:
                textTB += f"{i.namePort}_TB"
                if(i != self.outputs[-1]): textTB += ", "
            textTB += (");\n"
                       "\t\t#1") 
            
        textTB += ("\n\t\t$finish;\n"
                   "\tend\n\n")
        
        #dumpfile and dumpvars
        textTB += ("\t//dumpfile and dumpvars\n"
        "\tinitial begin\n"
        f'\t\t$dumpfile("{self.module_name}.vcd");\n'
        f"\t\t$dumpvars(1, {self.module_name}_TB);\n"
        "\tend\n"
        "endmodule")
        
        return textTB
    
    def createTB(self):
        f = open(self.module_name + "_testbench.sv", "w")
        f.write(self.writeTB())
        f.close()
        print(f"\n{self.module_name}_testbench.sv file has been created successfully")
        

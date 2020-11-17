#!/bin/python3

import re
import os
import datetime 

"""
Inputs ,    Current State, Next State  ,Output
0|0    ,    S0           ,    S1       ,2|3
0|1    ,    S0           ,    S2       ,2|3
1|0    ,    S0           ,    S1       ,2|3
1|1    ,    S0           ,    S2       ,2|3

1|0    ,    S1           ,    S4       ,5|3
0|1    ,    S1           ,    S3       ,5|3


Inputs ,    Current State, Next State  
0|0    ,    S0           ,    S1       
0|1    ,    S0           ,    S2       
1|0    ,    S0           ,    S1       
1|1    ,    S0           ,    S2       
1|0    ,    S1           ,    S4       
0|1    ,    S1           ,    S3       

dic {"S0":}

Inputs ,    Current State,  Output
0|0    ,    S0           ,    2|3
0|1    ,    S0           ,    2|3
1|0    ,    S0           ,    2|3
1|1    ,    S0           ,    2|3

1|0    ,    S1           ,    5|3
0|1    ,    S1           ,    5|3

Registro --> always@(posedge clk or posedge reset) state <= next_state;
Next state Logic --> case (state or Inputs) next_state = Sx;
Output Logic --> case (state or Inputs) out1 = x, out2 = y;



0,S1,S2,1
1,S1,S1,0
0,S2,S0,1
1,S2,S0,1

* Next state logic f(Inputs, CS) -->  contenedor para NSL
* Output logic f(Inputs, CS)     -->  contenedor para OL

Inputs={"S0":[[0,1][1,0]],"S1":[[1,0][0,1]]}


States=["S0","S1",....]
NState={"S0":["S1","S2"],"S1":["S4","S3"]}
Outputs={"S0":[[2,3][3,4]],"S1":[[3,5][5,3]]}

"""


class FSM:
    

    def getFile(self):
        noError = True
        
        #Ask for the verilog source code file name
        fileName = input("\nWhat is the table's filename?\n(It should be a csv file) ")

        #Append ".sv" suffix if not found
        if (not re.match(r"\.csv",fileName)): 
            fileName = fileName + ".csv"

        #Try to open file
        try: 
            f = open(fileName,"r")
        except:
            print(f"The {fileName} file was not found or you do not have read permissions\n")
            fileName=""

            #If cannot open file, check in working directory for other sv files that do not contain "_testbench"
            for fil in os.listdir("."):
                if ".sv" in fil and not "_testbench" in fil:
                    fileName=fil

                    #If a file is found, ask if the user wants to use it
                    print("sv file found, do you want to use: "+fil+"?(Y,N)\n")
                    t=input()
                    #If answer is no, search for more files, else use the file
                    if t!="n" and t!="N":
                        print(f"File {fileName} will be used!\n")
                        f = open(fileName,"r")
                        break
                    else:
                        fileName=""
                        print("File not used")
            #If user does not use any file, send error
            if fileName=="":
                noError = False
        #If there is no error, read the file contents and close file
        if(noError):
            self.designCode = " " + f.read()
            print(f"File {fileName} read successfully")
            f.close()
        return noError
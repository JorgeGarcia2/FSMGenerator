#!/bin/python3

import FM
import Jorch
import Fers

"""
States=
{
"State0":[[in1,in2,...],"Nstate1",[out1,out2,...]]
         [[in3,in4,...],"Nstate2",[out3,out4,...]]
"State1":[[in1,in2,...],"Nstate1",[out1,out2,...]]
}
"""

class FSM:

    FSMstr = ""

    def __init__(self):
        fileName = FM.getFileName("csv","_Design")

        if (fileName == ""):
            print("There is no table!")
        else:
            print("Here's the table "+fileName+"!!\n\n")
            dictio = Jorch.getFSMDic(fileName)
            self.FSMstr = Fers.getFSMHead(dictio,"FSM")
            dicKey = {"inputs":["Op"],"ppal":"S0","outputs":["X"]}
            self.FSMstr += self.getFSMSLogic(dictio,dicKey)
            print(self.FSMstr)

    #Makes the state logic for the machine
    def getFSMSLogic(self,dicS,dicK):
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
                    if (dicS[S][i][0][j] != "x" and dicS[S][i][0][j] != "x"):
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
        FSMSLogic += "      default:\n        nextstate = " + dicK["ppal"] + ";\n    endcase\n  end"
        return FSMSLogic
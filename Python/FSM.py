#!/bin/python3

import FM
import Xchel
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
            dictio, NI, NO = Jorch.getFSMDic(fileName)
            print(NI)
            print(NO)
            self.FSMstr = Fers.getFSMHead(dictio,"FSM")
            self.FSMstr += self.getFSMLogic(dictio,NI,NO)
            print(self.FSMstr)

    #Makes the state logic for the machine
    def getFSMLogic(self,dicS,Ni,No):
        FSMSLogic="\n  //Next State Logic Block\n  always@(state)\n"
        FSMOLogic="\n  //Output Logic Block\n  always@(state)\n"

        for S in dicS.keys():
            FSMSLogic += "      " + S + ":\n"
            FSMOLogic += "      " + S + ":\n"
            IF = False
            for i in range(len(dicS[S])):
                if (IF): Temp = "        else if("
                else: Temp = "        if("
                f=False
                for j in range(len(dicS[S][i][0])):
                    if (dicS[S][i][0][j] != "x" and dicS[S][i][0][j] != "X"):
                        if (f): Temp += " && "
                        Temp += Ni[j][0] + " == " + dicS[S][i][0][j]
                        f=True
                if (Temp != "        if("):
                    IF = True
                    if (len(No) > 1):
                        FSMOLogic += Temp + ") begin\n"
                    else:
                        FSMOLogic += Temp + ")\n"
                    FSMSLogic += Temp + ")\n"
                FSMSLogic += "          nextstate = " + dicS[S][i][1] + ";\n\n"
                for j in range(len(No)):
                    if (dicS[S][i][2][j] != "x" and dicS[S][i][2][j] != "X"):
                        FSMOLogic += "          " + No[j][0] + " = " + dicS[S][i][2][j] + ";\n"
                if (len(No) > 1):
                    FSMOLogic += "        end\n"
                FSMOLogic += "\n"
            if (IF):
                FSMSLogic += "        else\n          nextstate = " + "S0" + ";\n"
                FSMOLogic += "        else begin\n"
                for j in range(len(No)):
                    if (dicS[S][0][2][j] != "x" and dicS[S][0][2][j] != "X"):
                        FSMOLogic += "          " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n"
                FSMOLogic += "        end\n\n"
            FSMSLogic += "\n"
            FSMOLogic += "\n"
        FSMSLogic += "      default:\n        nextstate = " + "S0" + ";\n"
        FSMOLogic += "      default: begin\n"
        for j in range(len(No)):
            FSMOLogic += "        " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n"
        FSMOLogic += "      end\n"
        FSMSLogic += "    endcase\n  end\n"
        FSMOLogic += "    endcase\n  end\n\nendmodule"
        return FSMSLogic + FSMOLogic

"""
    #Makes the state logic for the machine
    def getFSMLogic(self,dicS,dicK,opt):
        FSMSLogic="\n  //Next State Logic Block\n  always@(state)\n"
        FSMOLogic="\n  //Output Logic Block\n  always@(state)\n"

        for S in dicS.keys():
            FSMSLogic += "      " + S + ":\n"
            FSMOLogic += "      " + S + ":\n"
            IF = False
            for i in range(len(dicS[S])):
                if (IF): Temp = "        else if("
                else: Temp = "        if("
                f=False
                for j in range(len(dicS[S][i][0])):
                    if (dicS[S][i][0][j] != "x" and dicS[S][i][0][j] != "X"):
                        if (f): Temp += " && "
                        Temp += Ni[j] + " == " + dicS[S][i][0][j]
                        f=True
                if (Temp != "        if("):
                    IF = True
                    if (opt == 1 and len(No) > 1):
                        FSMLogic += Temp + ") begin\n"
                    else:
                        FSMLogic += Temp + ")\n"
                if (opt == 0):
                    FSMLogic += "          nextstate = " + dicS[S][i][1] + ";\n\n"
                else:
                    for j in range(len(No)):
                        if (dicS[S][i][2][j] != "x" and dicS[S][i][2][j] != "X"):
                            FSMLogic += "          " + No[j] + " = " + dicS[S][i][2][j] + ";\n"
                    if (opt == 1 and len(No) > 1):
                        FSMLogic += "        end\n"
                    FSMLogic += "\n"
            if (IF):
                if (opt == 0):
                    FSMLogic += "        else\n          nextstate = " + dicK["ppal"] + ";\n"
                else:
                    FSMLogic += "        else begin\n"
                    for j in range(len(No)):
                        if (dicS[S][0][2][j] != "x" and dicS[S][0][2][j] != "X"):
                            FSMLogic += "          " + No[j] + " = " + dicS[S][0][2][j] + ";\n"
                    FSMLogic += "        end\n\n"
            FSMLogic += "\n"
        if (opt == 0):
            FSMLogic += "      default:\n        nextstate = " + dicK["ppal"] + ";\n"
        else:
            FSMLogic += "      default: begin\n"
            for j in range(len(No)):
                FSMLogic += "        " + No[j] + " = 0;\n"
            FSMLogic += "      end\n"
        FSMLogic += "    endcase\n  end\n"
        return FSMLogic"""
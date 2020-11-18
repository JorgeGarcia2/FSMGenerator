#!/bin/python3

import FM
import Xchel
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
            dictio, NI, NO, ppal = FM.getFSMData(fileName)
            name = "FSM"
            self.FSMstr = Fers.getFSMHead(dictio,name,NI,NO)
            self.FSMstr += self.getFSMLogic(dictio,NI,NO,ppal)
            self.writeFSM(name,self.FSMstr)

    #Makes the state logic for the machine
    def getFSMLogic(self,dicS,Ni,No,ppal):
        FSMSLogic="\n  //Next State Logic Block\n  always@(state)\n  begin\n    case(state)\n"
        FSMOLogic="\n  //Output Logic Block\n  always@(state)\n  begin\n    case(state)\n"

        for S in dicS.keys():
            FSMSLogic += "      " + S + ": begin\n"
            FSMOLogic += "      " + S + ": begin\n"
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
                if (IF):
                    FSMOLogic += "        end\n"
                FSMOLogic += "\n"
            if (IF):
                FSMSLogic += "        else\n          nextstate = " + ppal + ";\n"
                FSMOLogic += "        else begin\n"
                for j in range(len(No)):
                    if (dicS[S][0][2][j] != "x" and dicS[S][0][2][j] != "X"):
                        FSMOLogic += "          " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n"
                FSMOLogic += "        end\n"
            FSMSLogic += "      end\n"
            FSMOLogic += "      end\n"
        FSMSLogic += "      default:\n        nextstate = " + ppal + ";\n"
        FSMOLogic += "      default: begin\n"
        for j in range(len(No)):
            FSMOLogic += "        " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n"
        FSMOLogic += "      end\n"
        FSMSLogic += "    endcase\n  end\n"
        FSMOLogic += "    endcase\n  end\n\nendmodule"
        return FSMSLogic + FSMOLogic

    def writeFSM(self,nam,cont):
        f = open(nam + "_Design.v","w")
        f.write(cont)
        f.close()
        print(f"file {nam}_Design.v created succesfully!\n")
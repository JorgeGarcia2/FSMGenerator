#!/bin/python3

# import math and custom file manager modules
import math
import FM

class FSM:

    FSMstr = ""

    # Constructor
    def __init__(self):

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
            self.FSMstr = self.getFSMHead(dictio,name,NI,NO)
            # Get the string value of the logic code
            self.FSMstr += self.getFSMLogic(dictio,NI,NO,ppal)
            # Write the code to a new file
            self.writeFSM(name,self.FSMstr)

    #Creates the Verilog design file's header (TOP module with inputs, outputs and states)
    def getFSMHead(self,dic, name, input_list, output_list):

        keys_list = []      #This list will store the dictionary keys (because the number of states can vary between FSMs)
        for key in dic.keys():
            keys_list.append(key)

        number_of_inputs = len( dic[keys_list[0]][0][0] )
        #number_of_outputs = len( dic[keys_list[0]][0][2] )
        number_of_states = len(keys_list)
        required_state_bits = math.ceil(math.log(number_of_states, 2))  #Required number of bits to encode the different states
        
        FSMHead =   (f"module {name}(\n"
                    "  input reset, clock,")

        current_bus_size = 0        #Create variable for later use
        last_bus_size = 0           #Create variable for later use

        if (number_of_inputs > 0):
            for i in input_list:
                current_bus_size = int(i[1])
                if (current_bus_size != last_bus_size):
                    FSMHead += "\n  input "
                    if (current_bus_size > 1):
                        FSMHead += f"[{current_bus_size-1}:0] "
                FSMHead += f"{i[0]}, "
                last_bus_size = current_bus_size
        
        current_bus_size = last_bus_size = 0

        for i in output_list:
            current_bus_size = int(i[1])
            if (current_bus_size != last_bus_size):
                FSMHead += "\n  output reg "
                if (current_bus_size > 1):
                    FSMHead += f"[{current_bus_size-1}:0] " 
            FSMHead += f"{i[0]}, "
            last_bus_size = current_bus_size

        FSMHead = FSMHead[:-2]                      #Remove the last two characters ", "
        
        delimiter = ', '
        keys_string = delimiter.join(keys_list)     #Pass the states keys to a string for later use

        FSMHead += (");\n\n"
                f"  typedef enum reg [{required_state_bits-1}:0] {{{keys_string}}} statetype;\n"
                f"  statetype state, nextstate;\n\n"    #Should be "  statetype [{required_state_bits-1}:0] state, nextstate;" but EPWave is weird
                    "  //State register\n"
                    "  always@ (posedge clock or posedge reset)\n"
                f"    if (reset) state <= {keys_list[0]};\n"
                    "    else       state <= nextstate;\n")
        
        return FSMHead

    #Makes the state logic for the machine
    def getFSMLogic(self,dicS,Ni,No,ppal):
        FSMSLogic = "\n  //Next State Logic Block\n  always@(state"
        for i in Ni: FSMSLogic += " or " + i[0]
        FSMSLogic += ")\n  begin\n    case(state)\n"
        FSMOLogic = "\n  //Output Logic Block\n  always@(state)\n  begin\n    case(state)\n"

        for S in dicS.keys():
            FSMSLogic += "      " + S + ":\n"
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
                    FSMOLogic += Temp + ") begin\n"
                    FSMSLogic += Temp + ")\n"
                FSMSLogic += "          nextstate = " + dicS[S][i][1] + ";\n\n"
                for j in range(len(No)):
                    if (dicS[S][i][2][j] != "x" and dicS[S][i][2][j] != "X"):
                        FSMOLogic += "          " + No[j][0] + " = " + dicS[S][i][2][j] + ";\n"
                if (IF):
                    FSMOLogic += "        end\n"
                FSMOLogic += "\n"
            if (IF):
                FSMSLogic += "        else\n          nextstate = " + S + ";\n"
                """FSMOLogic += "        else begin\n"
                for j in range(len(No)):
                    if (dicS[S][0][2][j] != "x" and dicS[S][0][2][j] != "X"):
                        FSMOLogic += "          " + No[j][0] + " = " + dicS[S][0][2][j] + ";\n"
                    else:
                        FSMOLogic += "          " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n"
                FSMOLogic += "        end\n" """
            FSMSLogic += "\n"
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
        f = open(nam + "_PyDesign.v","w")
        f.write(cont)
        f.close()
        print(f"file {nam}_PyDesign.v created succesfully!\n")
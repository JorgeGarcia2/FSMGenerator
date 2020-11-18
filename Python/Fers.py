#!/bin/python3.6
import math

"""
States=
{
"State0":[ [[in1,in2,...],"Nstate1",[out1,out2,...]],
           [[in1],        "Nstate2",[out1]] ],
"State1":[ [[in1,in2,...],"Nstate1",[out1,out2,...]] ]
}
______________________________________________________

module Mealy_FSM(
  input clk, reset, A, B,
  output reg y);
  
  typedef enum reg [1:0] {S0, S1, S2} statetype;
  statetype [1:0] state, nextstate;  --> the [1:0] bus is recommended by the Dig. Design book,
                                         but EPWave is weird so I did not include it in the design


dummy_dic = { 
    "S0": [[[], "S1", [1]]],
    "S1": [[[], "S2", [0]]],
    "S2": [[[], "S0", [0]]]
}                                        
"""

dummy_dic = { 
    "S0": [[[1,0,1], "S1", [1]]],
    "S1": [[[0,0,1], "S2", [0]]],
    "S2": [[[1,1,0], "S0", [0]]]
}

#Creates the Verilog design file's header (TOP module with inputs, outputs and states)
def getFSMHead(dic, name):
    print(dic)          #Just to know that the dictionary is correctly passed
    print()             #Just a line break :P

    keys_list = []      #This list will store the dictionary keys (because the number of states can vary between FSMs)
    for key in dic.keys():
        keys_list.append(key)

    number_of_inputs = len( dic[keys_list[0]][0][0] )
    number_of_outputs = len( dic[keys_list[0]][0][2] )
    number_of_states = len(keys_list)
    required_state_bits = math.ceil(math.log(number_of_states, 2))  #Required number of bits to encode the different states
    
    FSMHead =   (f"module {name}(\n"
                  "  input reset, clock,\n")

    if (number_of_inputs > 0):
        FSMHead += "  input "
        for i in range(number_of_inputs):   #For now, only 1-bit inputs considered
            FSMHead += f"in{i}, "
        FSMHead += "\n"
    
    FSMHead += "  output reg "

    for i in range(number_of_outputs):  #For now, only 1-bit outputs considered
        FSMHead += f"out{i}, "

    FSMHead = FSMHead[:-2]                      #Remove the last two characters ", "
    
    delimiter = ' '                      
    keys_string = delimiter.join(keys_list)     #Pass the states keys to a string for later use

    FSMHead += (");\n\n"
               f"  typedef enum reg [{required_state_bits-1}:0] {{{keys_string}}} statetype;\n"
               f"  statetype state, nextstate;\n\n"    #Should be "  statetype [{required_state_bits-1}:0] state, nextstate;" but EPWave is weird
                "  //State register\n"
                "  always@ (posedge clock or posedge reset)\n"
               f"    if (reset) state <= {keys_list[0]};\n"
                "    else       state <= nextstate;\n")

    
    
    return FSMHead


################## MAIN CODE ###################

FSM_name = "FSM_module"             #Dummy module name
if (__name__=="__main__"):
    print(getFSMHead(dummy_dic, FSM_name))
#!/bin/python3

# import math module
import math

#**************************************************************************************************
#   Function:
#       getFSMHead(dic, name, input_list, output_list).
#
#   Description:
#       This function creates the Verilog design file's header.
#       It begins by creating the Finite State Machine's module, then declares
#       the input and output signals. It also creates a statetype variable
#       for the required number of different states.
#       This function finishes by creating the State Register of the FSM design.
#
#   Precondition:
#       None.
#
#   Parameters:
#       * dic - Dictionary for states transitions: [state:[inputs, Next state, outputs]].
#       * name - Name of the FSM module.
#       * input_list - List of inputs names with its radix and bus size.
#       * output_list - List of outputs names with its radix and bus size.
#
#    Return Value:
#       * FSMHead - String containing the verilog module's header and the State Register.
#**************************************************************************************************
def getFSMHead(dic, name, input_list, output_list):

    # keys_list will store the dictionary keys/current-state-names (because the number of states can vary between FSMs)
    keys_list = []
    for key in dic.keys():
        keys_list.append(key)

    # Store the number of inputs and states  
    number_of_inputs = len(dic[keys_list[0]][0][0])
    number_of_states = len(keys_list)

    # Required number of bits to encode the different states (ceil function rounds up to the next integer number)
    required_state_bits = math.ceil(math.log(number_of_states, 2))
    
    # Begin the Verilog header string by calling the module, reset and clock signals
    FSMHead =   (f"module {name}(\n"
                "  input reset, clock,")

    # Initialize two variables for later use
    current_bus_size = 0
    last_bus_size = 0

    # Get the input instantiation
    if (number_of_inputs > 0):
        for i in input_list:
            current_bus_size = int(i[1])

            # If the size of the current signal is different to the last,
            # instantiate a new input size, else append it to current size
            if (current_bus_size != last_bus_size):
                FSMHead += "\n  input "
                if (current_bus_size > 1):
                    FSMHead += f"[{current_bus_size-1}:0] "
            FSMHead += f"{i[0]}, "
            last_bus_size = current_bus_size
    
    # Reset the current and last bus variables to 0
    current_bus_size = last_bus_size = 0

    # Get the output instantiation
    for i in output_list:
        current_bus_size = int(i[1])
        # If the size of the current signal is different to the last,
        # instantiate a new output size, else append it to current size
        if (current_bus_size != last_bus_size):
            FSMHead += "\n  output reg "
            if (current_bus_size > 1):
                FSMHead += f"[{current_bus_size-1}:0] " 
        FSMHead += f"{i[0]}, "
        last_bus_size = current_bus_size

    # Remove the last two characters ", "
    FSMHead = FSMHead[:-2]
    
    # Pass the states keys to a string for later use
    delimiter = ', '
    keys_string = delimiter.join(keys_list)

    # Create the states as a new variable of type statetype, using enum. Then, create the State Register always block
    FSMHead += (");\n\n"
            f"  typedef enum reg [{required_state_bits-1}:0] {{{keys_string}}} statetype;\n"
            f"  statetype state, nextstate;\n\n"    #Should be "  statetype [{required_state_bits-1}:0] state, nextstate;", but works in EPWave
                "  //State register\n"
                "  always@ (posedge clock or posedge reset)\n"
            f"    if (reset) state <= {keys_list[0]};\n"
                "    else       state <= nextstate;\n")
    
    return FSMHead

#**************************************************************************************************
#   Function:
#       getFSMLogic(dicS,Ni,No,ppal).
#
#   Description:
#       This function creates the Verilog code for the next state and output block for a Finite 
#       State Machine based on the information provided by the arguments.
#
#   Precondition:
#       This function must be called after getFSMHead function to continue with the FSM code.
#
#   Parameters:
#       * dicS - Dictionary with information about states transitions.
#       * ppal - FSM Principal state.
#       * Ni - List of inputs names with its radix and bus size.
#       * No - List of outputs names with its radix and bus size.
#
#    Return Values:
#       * FSMSLogic + FSMOLogic - concatenation of the FSMSLogic and FSMOLogic strings 
#           which contain the verilog code for the Next State and Output blocks respectively.
#**************************************************************************************************
def getFSMLogic(dicS,Ni,No,ppal):

    # Initialize state logic block with an always sensitive to the current state and the inputs
    FSMSLogic = "\n  //Next State Logic Block\n  always@(state"
    for i in Ni: FSMSLogic += " or " + i[0]
    FSMSLogic += ")\n  begin\n    case(state)\n"
    # Initialize state logic block with an always sensitive to the current state
    FSMOLogic = "\n  //Output Logic Block\n  always@(state)\n  begin\n    case(state)\n"

    # Iterate over dictionary keys
    for S in dicS.keys():

        # Append the key as a case without begin in state logic for better readability
        FSMSLogic += "      " + S + ":\n"
        FSMOLogic += "      " + S + ": begin\n"

        # Initialize no if found and iterate over input values
        IF = False
        for i in range(len(dicS[S])):

            # If an if was found before, continue with else if instead of an if
            if (IF): Temp = "        else if("
            else: Temp = "        if("

            # Initialize found conditions as false
            f=False
            for j in range(len(dicS[S][i][0])):
                if (dicS[S][i][0][j] != "x" and dicS[S][i][0][j] != "X"):

                    # If there was a condition before, append an "&&"
                    if (f): Temp += " && "
                    Temp += Ni[j][0] + " == " + dicS[S][i][0][j]
                    f=True
            # If conditions were found, append the conditions
            if (f):
                IF = True
                FSMOLogic += Temp + ") begin\n"
                FSMSLogic += Temp + ")\n"
            # Append the next state depending on the current state and the conditions
            FSMSLogic += "          nextstate = " + dicS[S][i][1] + ";\n\n"

            # Append the output values for all outputs depending on the current state and the conditions
            for j in range(len(No)):
                if (dicS[S][i][2][j] != "x" and dicS[S][i][2][j] != "X"):
                    FSMOLogic += "          " + No[j][0] + " = " + dicS[S][i][2][j] + ";\n"
            # If there was an if clause, append the end to the output logic
            if (IF):
                FSMOLogic += "        end\n"
            FSMOLogic += "\n"
        # If there was an if found, finish next state logic with
        # else going to the same current state
        if (IF):
            FSMSLogic += "        else\n          nextstate = " + S + ";\n"
        FSMSLogic += "\n"
        FSMOLogic += "      end\n"
    # Append default state cases
    FSMSLogic += "      default:\n        nextstate = " + ppal + ";\n"
    FSMOLogic += "      default: begin\n"

    # Append all values of outputs
    for j in range(len(No)):
        FSMOLogic += "        " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n"

    # Finish the next state and output logic block strings
    FSMOLogic += "      end\n"
    FSMSLogic += "    endcase\n  end\n"
    FSMOLogic += "    endcase\n  end\n\nendmodule"

    # Return sum of both strings
    return FSMSLogic + FSMOLogic

#**************************************************************************************************
#   Function:
#       writeFSM(nam,cont).
#
#   Description:
#       This function creates the Finite State Machine's Verilog design file.
#       It appends the key '_PyDesign' to make a distinction between the Python
#       and the C++ FSM generators.
#       It begins by Creating a file with the given name for writing purposes.
#       It then writes the contents of all the strings created throughout the program.
#       It finishes by closing the file and printing the successful creation of the file.
#
#   Precondition:
#       None.
#
#   Parameters:
#       * nam - Name of the Verilog file to create.
#       * cont - String containing the entire Verilog file.
#
#    Return Value:
#       None.
#**************************************************************************************************
def writeFSM(nam,cont):
    f = open(nam + "_PyDesign.v","w")
    f.write(cont)
    f.close()
    print(f"file {nam}_PyDesign.v created succesfully!\n")
#include "FSM.hpp"
#include "FM.hpp"
#include <math.h>

using namespace std;

/*
dummy_dic = { 
    "S0": [[[0,0,0], "S1", [1]]],
    "S1": [[[0,0,0], "S2", [1]]],
    "S2": [[[0,0,0], "S0", [1]]]
}

[[["0"], "S1", ["1"]]]  --> vector de objetos tipo FSMLine
 [["0"], "S1", ["1"]]   --> objecto tipo FSMLine
vector de strings, string, vector de strings

FSMdictionary={{key,vector{FSMLine(),FSMLine()}}.{key,vector{FSMLine(),FSMLine()}}} --> How to create a dictionary-like map

*/

string getFSMHead(string& name)
{
    FSMdictionary States = {{"S0",{FSMLine({"0","0","0"},"S1",{"1"})}},
                            {"S1",{FSMLine({"0","0","0"},"S2",{"1"})}},
                            {"S2",{FSMLine({"0","0","0"},"S0",{"1"})}}};

    vector<string> keys_vector;     //Store the dictionary keys inside the keys_vector for later use
    for(map<string, Line_vector>::iterator it = States.begin(); it != States.end(); ++it)
    {
        keys_vector.push_back(it->first);
    }

    //States[keys_vector[i]][j] gets the j-esim object of type FSMLine, whose key is keys_vector[i]
    unsigned int number_of_inputs = States[keys_vector[0]][0].get_inputs().size();
    unsigned int number_of_outputs = States[keys_vector[0]][0].get_outputs().size();
    unsigned int number_of_states = keys_vector.size();
    unsigned int required_state_bits = ceil(log2(number_of_states));

    string FSMHead = "";

    FSMHead += "module " + name + "(\n"
             + "  input reset, clock, \n";

    if (number_of_inputs > 0)
    {
        FSMHead += "  input ";
        for (int i=0; i<number_of_inputs; i++)     //Se actualizará cuando se tenga la input_list
        {
            FSMHead += "in" + to_string(i) + ", ";
        }
        /* for i in input_list:     --> Modelo a seguir
                if (int(i[1]) > 1):
                    FSMHead += f"[{int(i[1])-1}:0] "
                FSMHead += f"{i[0]}, " */
        FSMHead += "\n";
    }

    FSMHead += "  output reg ";

    for (int i=0; i<number_of_outputs; i++)     //Se actualizará cuando se tenga la output_list
    {
        FSMHead += "out" + to_string(i) + ", ";
    }
    /* for i in output_list:     --> Modelo a seguir
            if (int(i[1]) > 1):
                FSMHead += f"[{int(i[1])-1}:0] " 
            FSMHead += f"{i[0]}, " */

    FSMHead.erase(FSMHead.end()-2);             //Remove the last two characters ", "
    FSMHead.pop_back();                         //This function seems necessary

    string keys_string;                         //Pass the states keys to a string for later use
    for (const auto &piece : keys_vector) keys_string += piece + " ";

    FSMHead += ");\n\n";
    FSMHead += "  typedef enum reg [" + to_string(required_state_bits-1) + ":0] " + keys_string + "statetype;\n"
             + "  statetype state, nextstate;\n\n"
             + "  //State register\n"
             + "  always@ (posedge clock or posedge reset)\n"
             + "    if (reset) state <= " + keys_vector[0] + ";\n"
             + "    else       state <= nextstate;\n";

    return FSMHead;
}

int main()
{
    string dummy_module_name = "PEPE";
    cout << getFSMHead(dummy_module_name);

    return 0;
}
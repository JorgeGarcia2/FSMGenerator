#include "FSM.hpp"
#include <math.h>

using namespace std;

/*
dummy_dic = {       --> simple dictionary
    "S0": [[[0,0,0], "S1", [1]]],
    "S1": [[[0,0,0], "S2", [1]]],
    "S2": [[[0,0,0], "S0", [1]]]
}

/*FSMdictionary States = {{"S0",{FSMLine({"0","0","0"},"S1",{"1"})}},       --> simple dictionary C++ version
                        {"S1",{FSMLine({"0","0","0"},"S2",{"1"})}},
                        {"S2",{FSMLine({"0","0","0"},"S0",{"1"})}}};

[[["0"], "S1", ["1"]]]  --> vector de objetos tipo FSMLine
 [["0"], "S1", ["1"]]   --> objecto tipo FSMLine
vector de strings, string, vector de strings

FSMdictionary={{key,vector{FSMLine(),FSMLine()}}.{key,vector{FSMLine(),FSMLine()}}} --> How to create a dictionary-like map

*/

string getFSMHead(string& name, FSMdictionary& States, busInfo& input_list, busInfo& output_list)
{

    for (int i=0; i< input_list.size(); i++)
        cout << "entrada: " << input_list[i][0] << endl;
    for (int i=0; i< output_list.size(); i++)
        cout << "salida: " << output_list[i][0] << endl;

    vector<string> keys_vector;     //Store the dictionary keys inside the keys_vector for later use
    for(map<string, Line_vector>::iterator it = States.begin(); it != States.end(); ++it)
    {
        keys_vector.push_back(it->first);
        //cout << "Key: " << it->first << endl;
    }

    //States[keys_vector[i]][j] gets the j-esim object of type FSMLine, whose key is keys_vector[i]
    unsigned int number_of_inputs = States[keys_vector[0]][0].get_inputs().size();
    unsigned int number_of_outputs = States[keys_vector[0]][0].get_outputs().size();
    unsigned int number_of_states = keys_vector.size();
    unsigned int required_state_bits = ceil(log2(number_of_states));

    string FSMHead = "";

    FSMHead += "module " + name + "(\n"
             + "  input reset, clock, \n";

    unsigned int current_bus_size = 0;          //Create variable for later use
    unsigned int last_bus_size = 0;             //Create variable for later use

    if (number_of_inputs > 0)
    {
        /* for i in input_list:     --> Modelo a seguir
                if (int(i[1]) > 1):
                    FSMHead += f"[{int(i[1])-1}:0] "
                FSMHead += f"{i[0]}, " */
        
        for (unsigned int i = 0; i < input_list.size(); i++)
        {
            current_bus_size = stoi(input_list[i][1]);       //Store the current bus size
            if (current_bus_size != last_bus_size)
            {
                FSMHead += "  input ";
                if (current_bus_size > 1)
                    FSMHead += "[" + to_string(current_bus_size - 1) + ":0] ";
            }
            FSMHead += input_list[i][0] + ",\n";
            last_bus_size = current_bus_size;
        }
    }

    current_bus_size = last_bus_size = 0;
    /* for i in output_list:     --> Modelo a seguir
            if (int(i[1]) > 1):
                FSMHead += f"[{int(i[1])-1}:0] " 
            FSMHead += f"{i[0]}, " */
    for (unsigned int i = 0; i < output_list.size(); i++)
    {
        current_bus_size = stoi(output_list[i][1]);       //Store the current bus size
        if (current_bus_size != last_bus_size)
        {
            FSMHead += "  output reg ";
            if (current_bus_size > 1)
                FSMHead += "[" + to_string(current_bus_size - 1) + ":0] ";
        }
        FSMHead += output_list[i][0] + ",\n";
        last_bus_size = current_bus_size;
    }

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
    vector<string> lineFile{"Hola", "mundo"};
	string fileText, sstate;
    busInfo inputs, outputs;
    FSMdictionary s;
	
    s = getFSMData(sstate, inputs, outputs);

    string dummy_module_name = "PEPE";
    cout << getFSMHead(dummy_module_name, s, inputs, outputs);

    return 0;
}
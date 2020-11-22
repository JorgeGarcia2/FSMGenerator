#include <fstream>
#include <iostream>
#include <map>
#include <vector>
#include <sstream>
#include <regex>
#include <math.h>
#include "FM.hpp"

using namespace std;

class FSMLine{
    public:
        // Constructor
        FSMLine(vector<string> inputs, string next_state, vector<string> outputs)
        {
            line_inputs = inputs;
            line_next_state = next_state;
            line_outputs = outputs;
        }

        // Accessor methods
        vector<string> get_inputs() {return line_inputs;}
        vector<string> get_outputs() {return line_outputs;}
        string get_next_state() {return line_next_state;}
    
    private:
        // Attributes
        vector<string> line_inputs;
        vector<string> line_outputs;
        string line_next_state;
};

typedef vector<FSMLine> Line_vector;
typedef map<string, Line_vector> FSMdictionary;
typedef vector <vector<string>> busInfo;

/**************************************************************************************************
#   Function:
#       getFSMData(string &startState, busInfo &nameInputs, busInfo &nameOutputs, string &tabName).
#
#   Description:
#       This function commands the search of a CSV file and the extraction of its contents.
#       Then, the information of interest is placed in different containers for
#       easier manipulation. The parameters are passed by reference so that this function
#       is able to modify their contents.
#
#   Precondition:
#       None.
#
#   Parameters:
#       * startState - Name of the first state.
#       * nameInputs - A vector of vectors of strings containing the inputs names with its radix and bus size.
#       * nameOutputs - A vector of vectors of strings containing the outputs names with its radix and bus size.
#       * tabName - Name of the CSV file.
#
#    Return Value:
#       * states - Map for states transitions: [state:[inputs, Next state, outputs]]
**************************************************************************************************/
inline FSMdictionary getFSMData(string &startState, busInfo &nameInputs, busInfo &nameOutputs, string &tabName)
{
    string lineCont;
    int countRow = 0;
    
    stringstream ss;
    // Vector to save the row, inputs, and outputs from the current row 
    vector <string> cRow, cInputs, cOutputs, temp;
    
    FSMdictionary states;
    smatch m;
    regex reBus("^(\\w+)\\((\\d+)((b|h|d)|.*)\\)$");

    // Get file name
    tabName = getFileName("csv","_Design","FSMTable.csv");

    // Get the content of the .csv file and save in the string stream ss
    ss.str(getFileCont(tabName));

    // iterate for every row
    while(getline(ss,lineCont)){
        cRow.clear();
        countRow++;
        // Clear cInputs and cOutputs vectors
        cInputs.clear();
        cOutputs.clear();
        // Sperate the row in vectors using commas as delimeters
        split(lineCont,cRow,',');
        // separate inputs and outputs from the current row using "|"as delimiter
        split(cRow[0],cInputs,'|');
        split(cRow[3],cOutputs,'|');
        // obtain size bus and radix
        if(countRow == 2){
            for(int i = 0; i < cInputs.size(); i++){
                regex_search (cInputs[i],m,reBus);
                vector <string> temp {m[1], m[2], m[3]};
                // if no radix is specified, assign "d"
                temp[2] = (temp[2] =="")?"d":temp[2];
                // if no bus size is specified, assign 1
                temp[1] = (temp[1] =="")?"1":temp[1];
                nameInputs.push_back(temp);
            }
            for(int i = 0; i < cOutputs.size(); i++){
                regex_search (cOutputs[i],m,reBus);
                vector <string> temp {m[1], m[2], m[3]};
                // if no radix is specified, assign "d"
                temp[2] = (temp[2] =="")?"d":temp[2];
                // if no bus size is specified, assign 1
                temp[1] = (temp[1] =="")?"1":temp[1];
                nameOutputs.push_back(temp);
            }
        }
        if(countRow > 2){
            // if countRow is equal to 3, startState stores the fist current state
            if(countRow == 3) startState = cRow[1];

            for(int i = 0; i < cInputs.size(); i++){
                if(cInputs[i] != "x" || cInputs[i] != "x")
                    cInputs[i] = nameInputs[i][1] + "'" + nameInputs[i][2] + cInputs[i];
            }
            for(int i = 0; i < cOutputs.size(); i++){
                if(cOutputs[i] != "x" || cInputs[i] != "x")
                    cOutputs[i] = nameOutputs[i][1] + "'" + nameOutputs[i][2] + cOutputs[i];
            }
            // Save the data
            states[cRow[1]].push_back(FSMLine (cInputs,cRow[2],cOutputs));
        }
    }
    return states;
}

/**************************************************************************************************
#   Function:
#       getFSMHead(string& name, FSMdictionary& States, busInfo& input_list, busInfo& output_list).
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
#       * name - Name of the FSM module.
#       * States - map for states transitions: [state:[inputs, Next state, outputs]].
#       * input_list - List of inputs names with its radix and bus size.
#       * output_list - List of outputs names with its radix and bus size.
#
#    Return Value:
#       * FSMHead - String containing the verilog module's header and the State Register.
**************************************************************************************************/
inline string getFSMHead(string& name, FSMdictionary& States, busInfo& input_list, busInfo& output_list)
{
    // keys_vector will store the dictionary keys/current-state-names (because the number of states can vary between FSMs)
    vector<string> keys_vector;
    for(FSMdictionary::iterator it = States.begin(); it != States.end(); ++it)
    {
        keys_vector.push_back(it->first);
    }

    // Call the sort function with the third parameter to accomodate elements in keys_vector in ascending numerical order
    sort(begin(keys_vector), end(keys_vector), [](const string& s1, const string& s2)
    {
        if (s1.size() != s2.size())
            return (s1.length() < s2.length());
        return (s1 < s2);
    });

    // Store the number of inputs and states
    unsigned int number_of_inputs = States[keys_vector[0]][0].get_inputs().size();
    unsigned int number_of_states = keys_vector.size();

    // Required number of bits to encode the different states (ceil function rounds up to the next integer number)
    unsigned int required_state_bits = ceil(log2(number_of_states));

    // Begin the Verilog header string by calling the module, reset and clock signals
    string FSMHead = "module " + name + "(\n"
             + "  input reset, clock,";

    // Initialize two variables for later use
    unsigned int current_bus_size = 0;
    unsigned int last_bus_size = 0;

    // Get the input instantiation
    if (number_of_inputs > 0)
    {
        for (unsigned int i = 0; i < input_list.size(); i++)
        {
            current_bus_size = stoi(input_list[i][1]);

            // If the size of the current signal is different to the last,
            // instantiate a new input size, else append it to current size
            if (current_bus_size != last_bus_size)
            {
                FSMHead += "\n  input ";
                if (current_bus_size > 1)
                    FSMHead += "[" + to_string(current_bus_size - 1) + ":0] ";
                FSMHead += input_list[i][0] + ", ";
            }
            else
                FSMHead += input_list[i][0] + ", ";            
            last_bus_size = current_bus_size;
        }
    }

    // Reset the current and last bus variables to 0
    current_bus_size = last_bus_size = 0;

    // Get the output instantiation
    for (unsigned int i = 0; i < output_list.size(); i++)
    {
        current_bus_size = stoi(output_list[i][1]);

        // If the size of the current signal is different to the last,
        // instantiate a new input size, else append it to current size
        if (current_bus_size != last_bus_size)
        {
            FSMHead += "\n  output reg ";
            if (current_bus_size > 1)
                FSMHead += "[" + to_string(current_bus_size - 1) + ":0] ";
            FSMHead += output_list[i][0] + ", ";
        }
        else
            FSMHead += output_list[i][0] + ", ";
        last_bus_size = current_bus_size;
    }

    // Remove the last two characters ", "
    FSMHead.erase(FSMHead.end()-2);
    FSMHead.pop_back();

    // Pass the states keys to a string for later use
    string keys_string;
    for (const auto &piece : keys_vector) keys_string += piece + ", ";
    keys_string.erase(keys_string.end()-2);
    keys_string.pop_back();

    // Create the states as a new variable of type statetype, using enum. Then, create the State Register always block
    FSMHead += ");\n\n";
    FSMHead += "  typedef enum reg [" + to_string(required_state_bits-1) + ":0] {" + keys_string + "} statetype;\n"
             + "  statetype state, nextstate;\n\n"
             + "  // State register\n"
             + "  always@ (posedge clock or posedge reset)\n"
             + "    if (reset) state <= " + keys_vector[0] + ";\n"
             + "    else       state <= nextstate;\n";

    return FSMHead;
}

/**************************************************************************************************
#   Function:
#       getFSMLogic(FSMdictionary dicS, busInfo Ni, busInfo No,string ppal).
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
#       * Ni - A vector of vectors of strings containing the inputs names with its radix and bus size.
#       * No - A vector of vectors of strings containing the outputs names with its radix and bus size.
#
#    Return Value:
#       * FSMSLogic + FSMOLogic - concatenation of the FSMSLogic and FSMOLogic strings 
#           which contain the verilog code for the Next State and Output blocks respectively.
**************************************************************************************************/
inline string getFSMLogic(FSMdictionary dicS, busInfo Ni, busInfo No,string ppal)
{
    string FSMOLogic, FSMSLogic;

    // Initialize state logic block with an always sensitive to the current state and the inputs
    FSMSLogic = "\n  // Next State Logic Block\n  always@(state";
    for (int i=0;i<Ni.size();i++) FSMSLogic += " or " + Ni[i][0];
    FSMSLogic += ")\n  begin\n    case(state)\n";
    // Initialize state logic block with an always sensitive to the current state
    FSMOLogic = "\n  // Output Logic Block\n  always@(state)\n  begin\n    case(state)\n";

    // Iterate over dictionary keys
    for(FSMdictionary::iterator it = dicS.begin(); it != dicS.end(); ++it){
        
        // Append the key as a case without begin in state logic for better readability
        FSMSLogic += "      " + it->first + ":\n";
        FSMOLogic += "      " + it->first + ": begin\n";
        
        // Initialize no if found and iterate over input values
        bool IF = false, f;
        string Temp = "";
        for (auto i:it->second){
            
            // If an if was found before, continue with else if instead of an if
            if (IF) Temp = "        else if(";
            else Temp = "        if(";
            
            // Initialize found conditions as false
            f = false;
            for(int j=0;j<Ni.size();j++){
                if (i.get_inputs()[j] != "x" and i.get_inputs()[j] != "X"){
                    
                    // If there was a condition before, append an "&&"
                    if (f) Temp += " && ";
                    Temp += Ni[j][0] + " == " + i.get_inputs()[j];
                    IF = true;
                    f = true;
                }
            }
            // If conditions were found, append the conditions
            if (IF){
                FSMOLogic += Temp + ") begin\n";
                FSMSLogic += Temp + ")\n";
            }
            
            // Append the next state depending on the current state and the conditions
            FSMSLogic += "          nextstate = " + i.get_next_state() + ";\n\n";
            
            // Append the output values for all outputs depending on the current state and the conditions
            for (int j=0;j<No.size();j++){
                if (i.get_outputs()[j] != "x" and i.get_outputs()[j] != "X")
                    FSMOLogic += "          " + No[j][0] + " = " + i.get_outputs()[j] + ";\n";
            }
            
            // If there was an if clause, append the end to the output logic
            if (IF) FSMOLogic += "        end\n";
            FSMOLogic += "\n";
        }
        
        // If there was an if found, finish next state logic with
        // else going to the same current state
        if (IF){
            FSMSLogic += "        else\n          nextstate = " + it->first + ";\n";
        }
        FSMOLogic += "      end\n";
    }
    
    // Append default state cases
    FSMSLogic += "      default:\n        nextstate = " + ppal + ";\n";
    FSMOLogic += "      default: begin\n";
    
    // Append all values of outputs
    for (int j=0; j<No.size();j++)
        FSMOLogic += "        " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n";
    
    // Finish the next state and output logic block strings
    FSMOLogic += "      end\n";
    FSMSLogic += "    endcase\n  end\n";
    FSMOLogic += "    endcase\n  end\n\nendmodule";
    
    // Return sum of both strings
    return FSMSLogic + FSMOLogic;
}

// Function for writing the code to a file with termination "_CppDesign.v"
inline bool writeFSM(string name, string code)
{
    bool f = false;
    fstream file;
    file.open(name + "_CppDesign.v",ios::out);
    file << code;
    file.close();
    f = true;
    return f;
}

// Function for printing easy to read format of the dictionary
inline void printFSMDict(FSMdictionary dicS){
    vector<string> tInputs;
    vector<string> tOutputs;
    string tNextState;

    // Iterate over the keys of the fictionary
    for (auto const& pair: dicS) {
        // Print the state and number of transitions
        cout << "State: " <<pair.first << "\tTransitions: " << dicS[pair.first].size()<<endl;

        // Iterate over the vector of each key
        for(int j = 0; j < dicS[pair.first].size(); j++){
            tInputs = dicS[pair.first][j].get_inputs();
            tOutputs = dicS[pair.first][j].get_outputs();
            tNextState = dicS[pair.first][j].get_next_state();
            // Print inputs
            for(int i = 0; i < tInputs.size(); i++) 
                cout << tInputs[i] << "| ";
            // Print next state
            cout << tNextState<<" |";
            // Print outputs
            for(int i = 0; i < tOutputs.size(); i++) 
                cout << tOutputs[i] << " |";
            cout << endl;
            tInputs.clear();
            tOutputs.clear();
        }
        cout << endl;
    }

}
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

inline FSMdictionary getFSMData(string &startState, busInfo &nameInputs, busInfo &nameOutputs, string &tabName)
{
    string lineCont;
    int countRow = 0;
    // , startState;
    stringstream ss;
    // Vector to save the row, inputs, and outputs from the current row 
    vector <string> cRow, cInputs, cOutputs, temp;
    // vector <vector<string>> nameInputs, nameOutputs;
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
        // separate inputs and outputs from the current row using "|"as delimeter
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

inline string getFSMHead(string& name, FSMdictionary& States, busInfo& input_list, busInfo& output_list)
{
    vector<string> keys_vector;     // Store the dictionary keys inside the keys_vector for later use
    for(FSMdictionary::iterator it = States.begin(); it != States.end(); ++it)
    {
        keys_vector.push_back(it->first);
    }

    // States[keys_vector[i]][j] gets the j-esim object of type FSMLine, whose key is keys_vector[i]
    unsigned int number_of_inputs = States[keys_vector[0]][0].get_inputs().size();
    unsigned int number_of_outputs = States[keys_vector[0]][0].get_outputs().size();
    unsigned int number_of_states = keys_vector.size();
    unsigned int required_state_bits = ceil(log2(number_of_states));

    // Initialize string
    string FSMHead = "module " + name + "(\n"
             + "  input reset, clock,";

    unsigned int current_bus_size = 0;          // Create variable for later use
    unsigned int last_bus_size = 0;             // Create variable for later use

    if (number_of_inputs > 0)
    {
        for (unsigned int i = 0; i < input_list.size(); i++)    // For all the inputs of the FSM
        {
            current_bus_size = stoi(input_list[i][1]);      // Store the current bus size
            if (current_bus_size != last_bus_size)          // In case that the bus size has changed...
            {
                FSMHead += "\n  input ";                    // ...a new input declaration is needed
                if (current_bus_size > 1)
                    FSMHead += "[" + to_string(current_bus_size - 1) + ":0] ";
                FSMHead += input_list[i][0] + ", ";
            }
            else
                FSMHead += input_list[i][0] + ", ";            
            last_bus_size = current_bus_size;               // Now store the used bus size as "last bus size"
        }
    }

    current_bus_size = last_bus_size = 0;

    for (unsigned int i = 0; i < output_list.size(); i++)       // For all the outputs of the FSM
    {
        current_bus_size = stoi(output_list[i][1]);         // Store the current bus size
        if (current_bus_size != last_bus_size)              // In case that the bus size has changed...
        {
            FSMHead += "\n  output reg ";                   // ...a new output reg declaration is needed
            if (current_bus_size > 1)
                FSMHead += "[" + to_string(current_bus_size - 1) + ":0] ";
            FSMHead += output_list[i][0] + ", ";
        }
        else
            FSMHead += output_list[i][0] + ", ";
        last_bus_size = current_bus_size;                   // Now store the used bus size as "last bus size"
    }

    FSMHead.erase(FSMHead.end()-2);             // Remove the last two characters
    FSMHead.pop_back();                         // This function seems necessary

    string keys_string;                         // Pass the states keys to a string for later use
    for (const auto &piece : keys_vector) keys_string += piece + ", ";
    keys_string.erase(keys_string.end()-2);     // Remove the last two characters
    keys_string.pop_back();                     // This function seems necessary

    FSMHead += ");\n\n";                        // Add the information to the head string
    FSMHead += "  typedef enum reg [" + to_string(required_state_bits-1) + ":0] {" + keys_string + "} statetype;\n"
             + "  statetype state, nextstate;\n\n"
             + "  // State register\n"
             + "  always@ (posedge clock or posedge reset)\n"
             + "    if (reset) state <= " + keys_vector[0] + ";\n"
             + "    else       state <= nextstate;\n";

    return FSMHead;
}

inline string getFSMLogic(FSMdictionary dicS, busInfo Ni, busInfo No,string ppal){
    string FSMOLogic, FSMSLogic;
    FSMSLogic = "\n  // Next State Logic Block\n  always@(state";
    for (int i=0;i<Ni.size();i++) FSMSLogic += " or " + Ni[i][0];
    FSMSLogic += ")\n  begin\n    case(state)\n";
    FSMOLogic = "\n  // Output Logic Block\n  always@(state)\n  begin\n    case(state)\n";

    for(FSMdictionary::iterator it = dicS.begin(); it != dicS.end(); ++it){
        FSMSLogic += "      " + it->first + ":\n";
        FSMOLogic += "      " + it->first + ": begin\n";
        bool IF = false, f;
        string Temp = "";

        for (auto i:it->second){
            if (IF) Temp = "        else if(";
            else Temp = "        if(";
            f = false;
            for(int j=0;j<Ni.size();j++){
                if (i.get_inputs()[j] != "x" and i.get_inputs()[j] != "X"){
                    if (f) Temp += " && ";
                    Temp += Ni[j][0] + " == " + i.get_inputs()[j];
                    f = true;
                }
            }
            if (Temp != "        if("){
                IF = true;
                FSMOLogic += Temp + ") begin\n";
                FSMSLogic += Temp + ")\n";
            }
            FSMSLogic += "          nextstate = " + i.get_next_state() + ";\n\n";
            for (int j=0;j<No.size();j++){
                if (i.get_outputs()[j] != "x" and i.get_outputs()[j] != "X")
                    FSMOLogic += "          " + No[j][0] + " = " + i.get_outputs()[j] + ";\n";
            }
            if (IF) FSMOLogic += "        end\n";
            FSMOLogic += "\n";
        }
        if (IF){
            FSMSLogic += "        else\n          nextstate = " + it->first + ";\n";
        }
        FSMOLogic += "      end\n";
    }
    FSMSLogic += "      default:\n        nextstate = " + ppal + ";\n";
    FSMOLogic += "      default: begin\n";
    for (int j=0; j<No.size();j++)
        FSMOLogic += "        " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n";
    FSMOLogic += "      end\n";
    FSMSLogic += "    endcase\n  end\n";
    FSMOLogic += "    endcase\n  end\n\nendmodule";
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
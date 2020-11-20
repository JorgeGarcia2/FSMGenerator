#include "FSM.hpp"

using namespace std;

int main(){
	string fileText, sstate, FSMCode,name;
    busInfo inputs, outputs;
    FSMdictionary States;
	
    // Get data from the table, this includes the name of the inputs,
    // outputs, states, table and its values
    States = getFSMData(sstate, inputs, outputs,name);
    // Get the path and name of the table without extension
    name = string(name.substr(0,name.size()-4));
    vector<string> dv;

    // Get the table name for the module name
    split(name,dv,'/');
    string nameM=dv[dv.size()-1];

    // Get the head and logic code from the data in string format
    FSMCode = getFSMHead(nameM, States, inputs, outputs);
    FSMCode += getFSMLogic(States,inputs,outputs,sstate);

    // Write the file with the code string
    writeFSM(name, FSMCode);
}
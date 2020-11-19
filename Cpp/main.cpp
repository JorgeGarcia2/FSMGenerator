#include "FSM.hpp"

using namespace std;

int main(){
	string fileText, sstate, FSMCode,name;
    busInfo inputs, outputs;
    FSMdictionary States;
	
    States = getFSMData(sstate, inputs, outputs,name);
    name = string(name.substr(0,name.size()-4));
    vector<string> dv;

    split(name,dv,'/');

    string nameM=dv[dv.size()-1];

    FSMCode = getFSMHead(nameM, States, inputs, outputs);
    FSMCode += getFSMLogic(States,inputs,outputs,sstate);
    writeFSM(name, FSMCode);
}
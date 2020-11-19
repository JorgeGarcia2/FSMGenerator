#include "FSM.hpp"

using namespace std;

int main(){
	string fileText, sstate, FSMCode,name;
    busInfo inputs, outputs;
    FSMdictionary States;
	
    States = getFSMData(sstate, inputs, outputs,name);

    FSMCode = getFSMHead(sstate, States, inputs, outputs);
    FSMCode += getFSMLogic(States,inputs,outputs,sstate);
    name = name.substr(0,name.size()-4);
    writeFSM(name, FSMCode);
}
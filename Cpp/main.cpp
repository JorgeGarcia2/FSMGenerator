#include <iostream>
#include "FSM.hpp"

using namespace std;

int main(){
	string fileText, sstate, FSMCode,name;
    busInfo inputs, outputs;
    FSMdictionary s;
	
    s = getFSMData(sstate, inputs, outputs,name);

    FSMCode = "";
    FSMCode += getFSMLogic(s,inputs,outputs,sstate);
    name = name.substr(0,name.size()-4);
    writeFSM(name, FSMCode);
}
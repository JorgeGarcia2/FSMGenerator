#include <iostream>
#include "FSM.hpp"

using namespace std;

int main(){
	string fileText, sstate, FSMCode;
    busInfo inputs, outputs;
    FSMdictionary s;
	
    s = getFSMData(sstate, inputs, outputs);

    FSMCode = "";
    FSMCode = getFSMLogic(s,inputs,outputs,sstate);

    cout << endl << FSMCode;
}
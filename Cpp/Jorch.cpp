#include "FSM.hpp"
using namespace std;


int main(){
	vector<string> lineFile{"Hola", "mundo"};
	string fileText, sstate;
    busInfo inputs, outputs;
    FSMdictionary s;
	for(int i = 0; i < lineFile.size(); i++) {
        cout << lineFile[i] << endl;
    }
    cout << endl;
	
    s = getFSMData(sstate, inputs, outputs);
    //printFSMDict(s);

    for (int i=0; i< inputs.size(); i++){
        cout << "Input: "<< i <<endl;
        cout << inputs[i][0] << endl;
        cout << inputs[i][1] << endl;
        cout << inputs[i][2] << endl;
    }
    for (int i=0; i< outputs.size(); i++){
        cout << "Output: "<< i <<endl;
        cout << outputs[i][0] << endl;
        cout << outputs[i][1] << endl;
        cout << outputs[i][2] << endl;
    }
}
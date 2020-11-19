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
    printFSMDict(s);
}
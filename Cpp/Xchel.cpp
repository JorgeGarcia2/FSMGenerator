#include "FSM.hpp"
#include <map>



int main(){
	string fileText, sstate, FSMCode;
    busInfo inputs, outputs;
    FSMdictionary s;
	
    s = getFSMData(sstate, inputs, outputs);

    system("clear");

    for(auto i:s){
        cout << i.first << ":\nOutputs: \n";
        for(auto j:i.second){
            for (auto k:j.get_outputs())  cout << "\t" << k << ", ";
            cout << endl;
        }
        cout << endl;
    }
    FSMCode = "";
    FSMCode = getFSMLogic(s,inputs,outputs,sstate);

    cout << endl << FSMCode;
}
#include "Jorch.hpp"
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
    cout<<endl<<s["S2"].size()<<endl;
    for(int j = 0; j < s["S2"].size(); j++){
        lineFile = s["S2"][j].get_inputs();
        for(int i = 0; i < lineFile.size(); i++) {
            cout << lineFile[i] << " |";
        }
        cout <<endl<<sstate<< endl;
        lineFile.clear();
    }
}
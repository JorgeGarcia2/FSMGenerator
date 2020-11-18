#include "FSM.hpp"
#include "FM.hpp"

using namespace std;

/*
dummy_dic = { 
    "S0": [[[0,0,0], "S1", [1]]],
    "S1": [[[0,0,0], "S2", [1]]],
    "S2": [[[0,0,0], "S0", [1]]]
}

dummy_dic = { 
"S0": [[[], "S1", [1]], [[], "S1", [0]]],
"S1": [[[], "S2", [0]]],
"S2": [[[], "S0", [0]]]
}

[[["0"], "S1", ["1"]]]  --> vector de objetos tipo FSMLine
 [["0"], "S1", ["1"]]   --> objecto tipo FSMLine
vector de strings, string, vector de strings

FSMdictionary={{key,vector{FSMLine(),FSMLine()}}.{key,vector{FSMLine(),FSMLine()}}} --> Manera de crear diccionario :D

*/

string getFSMHead()
{
    FSMdictionary States = {{"S0",{FSMLine({"1","2","3"},"S0",{"11","12","13"}),FSMLine({"4","5","6"},"S1",{"14","15","16"})}},
                      {"S1",{FSMLine({"7","8","9"},"S1",{"17","18","19"}),FSMLine({"0","a","b"},"S0",{"10","1a","1b"})}}};
    
   

    return "holis";
}

int main()
{

    cout << getFSMHead();

    return 0;
}
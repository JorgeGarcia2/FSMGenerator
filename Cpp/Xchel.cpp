#include "FSM.hpp"
#include "FM.hpp"

string getFSMLogic(dictionary dicS)
{
    
    return "";
}

string writeFSM()
{
    
    return "";
}

int main (){
    string FSMCode, tabName, tabCont;
    dictionary States = {{"S0",{Line({"1","2","3"},{"11","12","13"},"S0"),Line({"4","5","6"},{"14","15","16"},"S1")}},
                      {"S1",{Line({"7","8","9"},{"17","18","19"},"S1"),Line({"0","a","b"},{"10","1a","1b"},"S0")}}};
    tabName = getFileName("csv","_Design","Table.csv");
    tabCont = getFileCont(tabName);
    FSMCode = getFSMLogic(States);
    cout << tabCont;
    cout << endl << FSMCode;
    return 0;
}
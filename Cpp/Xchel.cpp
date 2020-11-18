#include "FSM.hpp"
#include "FM.hpp"

string getFSMLogic(FSMdictionary dicS)
{
    
    return "";
}

string writeFSM()
{
    
    return "";
}

int main (){
    string FSMCode, tabName, tabCont;
    FSMdictionary States = {{"S0",{FSMLine({"1","2","3"},"S0",{"11","12","13"}),FSMLine({"4","5","6"},"S1",{"14","15","16"})}},
                      {"S1",{FSMLine({"7","8","9"},"S1",{"17","18","19"}),FSMLine({"0","a","b"},"S0",{"10","1a","1b"})}}};
    tabName = getFileName("csv","_Design","Table.csv");
    tabCont = getFileCont(tabName);
    FSMCode = getFSMLogic(States);
    cout << tabCont;
    cout << endl << FSMCode;
    return 0;
}
#include "FSM.hpp"
#include "FM.hpp"
#include <map>

string getFSMLogic(FSMdictionary dicS, string Ni[], string No[],string ppal){
    string FSMOLogic, FSMSLogic;
    FSMSLogic = "\n  //Next State Logic Block\n  always@(state";
    for (int i=0;i<Ni->size();i++) FSMSLogic += " or " + Ni[i];
    FSMSLogic += ")\n  begin\n    case(state)\n";
    FSMOLogic = "\n  //Output Logic Block\n  always@(state)\n  begin\n    case(state)\n";

    for(FSMdictionary::iterator it = dicS.begin(); it != dicS.end(); ++it){
        FSMSLogic += "      " + it->first + ": begin\n";
        FSMOLogic += "      " + it->first + ": begin\n";
        bool IF = false, f;
        string Temp = "";

        for (auto i:it->second){
            if (IF) Temp = "        else if(";
            else Temp = "        if(";
            f = false;
            for(int j=0;j<Ni->size();j++){
                if (i.get_inputs()[j] != "x" and i.get_inputs()[j] != "X"){
                    if (f) Temp += " && ";
                    Temp += Ni[j] + " == " + i.get_inputs()[j];
                    f = true;
                }
            }
            if (Temp != "        if("){
                IF = true;
                if (No->size() > 1) FSMOLogic += Temp + ") begin\n";
                else FSMOLogic += Temp + ")\n";
                FSMSLogic += Temp + ")\n";
            }
            FSMSLogic += "          nextstate = " + i.get_next_state() + ";\n\n";
            for (int j;j<No->size();j++){
                if (i.get_outputs()[j] != "x" and i.get_outputs()[j] != "X")
                    FSMOLogic += "          " + No[j] + " = " + i.get_outputs()[j] + ";\n";
            }
            if (IF) FSMOLogic += "        end\n";
            FSMOLogic += "\n";
        }
        if (IF){
            FSMSLogic += "        else\n          nextstate = " + ppal + ";\n";
            FSMOLogic += "        else begin\n";
            for (int j=0;j<No->size();j++){
                if (it->second[0].get_outputs()[0] != "x" and it->second[0].get_outputs()[0] != "X")
                    FSMOLogic += "          " + No[j] + " = " + No[j] + "'" + No[j] + it->second[0].get_outputs()[0] + ";\n";
                else FSMOLogic += "          " + No[j] + " = " + No[j] + "'" + No[j] + "0;\n";
            }
            FSMOLogic += "        end\n";
        }
        FSMSLogic += "      end\n";
        FSMOLogic += "      end\n";
    }
    FSMSLogic += "      default:\n        nextstate = " + ppal + ";\n";
    FSMOLogic += "      default: begin\n";
    for (int j; j<No->size();j++)
        FSMOLogic += "        " + No[j] + " = " + No[j] + "'" + No[j] + "0;\n";
    FSMOLogic += "      end\n";
    FSMSLogic += "    endcase\n  end\n";
    FSMOLogic += "    endcase\n  end\n\nendmodule";
    return FSMSLogic + FSMOLogic;
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
    string NI[] = {"In1","In2","In3"};
    string NO[] = {"Out1","Out2","Out3"};
    FSMCode = getFSMLogic(States,NI,NO,"S0");
    cout << tabCont;
    cout << endl << FSMCode;
    return 0;
}
#include "FSM.hpp"
#include <map>

string getFSMLogica(FSMdictionary dicS, busInfo Ni, busInfo No,string ppal){
    string FSMOLogic, FSMSLogic;
    FSMSLogic = "\n  //Next State Logic Block\n  always@(state";
    for (int i=0;i<Ni.size();i++) FSMSLogic += " or " + Ni[i][0];
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
            for(int j=0;j<Ni.size();j++){
                if (i.get_inputs()[j] != "x" and i.get_inputs()[j] != "X"){
                    if (f) Temp += " && ";
                    Temp += Ni[j][0] + " == " + i.get_inputs()[j];
                    f = true;
                }
            }
            if (Temp != "        if("){
                IF = true;
                if (No.size() > 1) FSMOLogic += Temp + ") begin\n";
                else FSMOLogic += Temp + ")\n";
                FSMSLogic += Temp + ")\n";
            }
            FSMSLogic += "          nextstate = " + i.get_next_state() + ";\n\n";
            cout << "Haya" << endl;
            for (int j=0;j<No.size();j++){
                //PROBLEMAAAAAAAAAAAAAAAAAAAAAAAAAa
                cout << "Halp!!: " << i.get_outputs()[j] << endl;
                if (i.get_outputs()[j] != "x" and i.get_outputs()[j] != "X")
                    FSMOLogic += "          " + No[j][0] + " = " + i.get_outputs()[j] + ";\n";
            }
            if (IF) FSMOLogic += "        end\n";
            FSMOLogic += "\n";
        }
        if (IF){
            FSMSLogic += "        else\n          nextstate = " + ppal + ";\n";
            FSMOLogic += "        else begin\n";
            for (int j=0;j<No.size();j++){
                if (it->second[0].get_outputs()[0] != "x" and it->second[0].get_outputs()[0] != "X")
                    FSMOLogic += "          " + No[j][0] + " = " + it->second[0].get_outputs()[0] + ";\n";
                else FSMOLogic += "          " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n";
            }
            FSMOLogic += "        end\n";
        }
        FSMSLogic += "      end\n";
        FSMOLogic += "      end\n";
    }
    FSMSLogic += "      default:\n        nextstate = " + ppal + ";\n";
    FSMOLogic += "      default: begin\n";
    for (int j; j<No.size();j++)
        FSMOLogic += "        " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + "0;\n";
    FSMOLogic += "      end\n";
    FSMSLogic += "    endcase\n  end\n";
    FSMOLogic += "    endcase\n  end\n\nendmodule";
    return FSMSLogic + FSMOLogic;
}

string writeFSM()
{
    
    return "";
}

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
    FSMCode = getFSMLogica(s,inputs,outputs,sstate);

    cout << endl << FSMCode;
}
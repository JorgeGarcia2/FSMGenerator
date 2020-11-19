#include <fstream>
#include <iostream>
#include <map>
#include <vector>
#include <sstream>
#include <regex>
#include "FM.hpp"

using namespace std;

class FSMLine{
    public:
        //Constructor
        FSMLine(vector<string> inputs, string next_state, vector<string> outputs)
        {
            line_inputs = inputs;
            line_next_state = next_state;
            line_outputs = outputs;
        }

        //Accessor methods
        vector<string> get_inputs() {return line_inputs;}
        vector<string> get_outputs() {return line_outputs;}
        string get_next_state() {return line_next_state;}
    
    private:
        //Attributes
        vector<string> line_inputs;
        vector<string> line_outputs;
        string line_next_state;
};

typedef vector<FSMLine> Line_vector;
typedef map<string, Line_vector> FSMdictionary;
typedef vector <vector<string>> busInfo;

inline void split(const string& str, vector<string> &cont, char delim)
{
    stringstream ss(str);
    string token;
    while (getline(ss, token, delim)) {
        cont.push_back(token);
    }
}


inline FSMdictionary getFSMData(string &startState, busInfo &nameInputs, busInfo &nameOutputs)
{
    string tabName, lineCont;
    int countRow = 0;
    //, startState;
    stringstream ss;
    //Vector to save the row, inputs, and outputs from the current row 
    vector <string> cRow, cInputs, cOutputs, temp;
    //vector <vector<string>> nameInputs, nameOutputs;
    FSMdictionary states;
    smatch m;
    regex reBus("^(\\w+)\\((\\d+)((b|h|d)|.*)\\)$");

    //Get file name
    tabName = getFileName("csv","_Design","FSMTable.csv");

    //Get the content of the .csv file and save in the string stream ss
    ss.str(getFileCont(tabName));

    //iterate for every row
    while(getline(ss,lineCont)){
        cRow.clear();
        countRow++;
        //Clear cInputs and cOutputs vectors
        cInputs.clear();
        cOutputs.clear();
        //Sperate the row in vectors using commas as delimeters
        split(lineCont,cRow,',');
        //separate inputs and outputs from the current row using "|"as delimeter
        split(cRow[0],cInputs,'|');
        split(cRow[3],cOutputs,'|');
        cout <<endl<< "Linea "<<countRow<<endl;
        for(int i = 0; i < cRow.size(); i++)
            cout << cRow[i] << "|";
        cout <<endl<< "Entradas "<<endl;
        for(int i = 0; i < cInputs.size(); i++)
            cout << cInputs[i] << endl;            
        cout <<endl<< "Salidas "<<endl;
        for(int i = 0; i < cOutputs.size(); i++)
            cout << cOutputs[i] << endl;
        //obtain size bus and radix
        if(countRow == 2){
            for(int i = 0; i < cInputs.size(); i++){
                regex_search (cInputs[i],m,reBus);
                vector <string> temp {m[1], m[2], m[3]};
                //if no radix is specified, assign "d"
                temp[2] = (temp[2] =="")?"d":temp[2];
                //if no bus size is specified, assign 1
                temp[1] = (temp[1] =="")?"1":temp[1];
                nameInputs.push_back(temp);
                cout << nameInputs[i][0] << nameInputs[i][1] << nameInputs[i][2] << endl;
            }
            for(int i = 0; i < cOutputs.size(); i++){
                regex_search (cOutputs[i],m,reBus);
                vector <string> temp {m[1], m[2], m[3]};
                //if no radix is specified, assign "d"
                temp[2] = (temp[2] =="")?"d":temp[2];
                //if no bus size is specified, assign 1
                temp[1] = (temp[1] =="")?"1":temp[1];
                nameOutputs.push_back(temp);
                cout << nameOutputs[i][0] << nameOutputs[i][1] << nameOutputs[i][2] << endl;
            }
        }
        if(countRow > 2){
            //if countRow is equal to 3, startState store the fist current state
            if(countRow == 3) startState = cRow[1];

            for(int i = 0; i < cInputs.size(); i++){
                if(cInputs[i] != "x" || cInputs[i] != "x")
                    cInputs[i] = nameInputs[i][1] + "'" + nameInputs[i][2] + cInputs[i];
            }
            for(int i = 0; i < cOutputs.size(); i++){
                if(cOutputs[i] != "x" || cInputs[i] != "x")
                    cOutputs[i] = nameOutputs[i][1] + "'" + nameOutputs[i][2] + cOutputs[i];
            }

            states[cRow[1]].push_back(FSMLine (cInputs,cRow[2],cOutputs));
        }
    }
    return states;
}

string getFSMLogic(FSMdictionary dicS, busInfo Ni, busInfo No,string ppal){
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
            for (int j;j<No.size();j++){
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
                    FSMOLogic += "          " + No[j][0] + " = " + No[j][1] + "'" + No[j][2] + it->second[0].get_outputs()[0] + ";\n";
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
/*
inline string printFSMDict(FSMdictionary dicS){
    for (auto const& pair: dicS) {
            
            output_M.push_back(Port(pair.first,pair.second));
        }
}*/
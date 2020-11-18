#include <fstream>
#include <iostream>
#include <map>
#include <vector>

using namespace std;

class Line
{
    public:
        //Constructor
        Line(vector<string> inputs, vector<string> outputs, string next_state)
        {
            line_inputs = inputs;
            line_outputs = outputs;
            line_next_state = next_state;
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

typedef vector<Line> Line_vector;
typedef map<string, Line_vector> dictionary;

string getFileName(string suf, string key, string def)
{
    ifstream file;
    string fName;
    while (1){
        //Ask for file name
        cout << "What's the file name?\n";
        cin >> fName;
        //Check if the name has suffix "suf", if not, append it
        if (fName.find("."+suf)==string::npos)fName += "." + suf;
        //Try to open file
        file.open(fName, ios::in);
        if (!file) {
            //If file cannot be opened, try to open default "def" file
            cout << "Cannot open file \"" + fName + "\"!\n";
            file.open(def, ios::in);
            //If default file is found, break the cycle, if not ask again
            if (!file) cout << "default file \"" + def + "\" not found!\n";
            else{
                cout << "default file \"" + def + "\" found, using it!\n";
                break;
            }
        }else{
            //Break while if file is found
            cout << "file " + fName + " found!\n\n";
            break;
        }
    }
    file.close();
    return fName;
}

string getFileCont(string fileName){
    ifstream file;
    file.open(fileName,ios::in);
    string fileCont = " " + string((istreambuf_iterator<char>(file) ),(istreambuf_iterator<char>()));
    file.close();
    return fileCont;
}

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
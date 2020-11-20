#include <fstream>
#include <iostream>
#include <vector>
#include <sstream>

using namespace std;

inline string getFileName(string suf, string key, string def){
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
                fName = def;
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

//Function to get the contents of a file in string format
inline string getFileCont(string fileName){
    ifstream file;

    //Open file
    file.open(fileName,ios::in);

    //Get content
    string fileCont = string((istreambuf_iterator<char>(file) ),(istreambuf_iterator<char>()));

    //Close file
    file.close();
    return fileCont;
}

//Function to get vector of strings by splitting a string using delimeter
inline void split(const string& str, vector<string> &cont, char delim)
{
    stringstream ss(str);
    string token;

    //Get the vector elements from the values before the delimeter
    while (getline(ss, token, delim)) {
        cont.push_back(token);
    }
}
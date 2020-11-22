#include <fstream>
#include <iostream>
#include <vector>
#include <sstream>

using namespace std;

/***************************************************************************************************
#   Function:
#       string getFileName(string suf, string def)
#
#   Description:
#       This function requests a file name and looks for it in the specified directory. if the 
#       file has no extension, add the extension given by the suff parameter. If the file cannot 
#       be found, it will search for a default file.
#
#   Precondition:
#       None.
#
#   Parameters:
#       * suf - extension to add to the file name in case it doesn't have one.
#       * def - default filename to search in case the file name given by the user is not found.
#
#    Return Values:
#       * fName - File name to use.
**************************************************************************************************/
inline string getFileName(string suf, string def){
    ifstream file;
    string fName;
    while (1){
        // Ask for file name
        cout << "What's the file name?\n";
        cin >> fName;
        // Check if the name has suffix "suf", if not, append it
        if (fName.find("."+suf)==string::npos)fName += "." + suf;
        // Try to open file
        file.open(fName, ios::in);
        if (!file) {
            // If file cannot be opened, try to open default "def" file
            cout << "Cannot open file \"" + fName + "\"!\n";
            file.open(def, ios::in);
            // If default file is found, break the cycle, if not ask again
            if (!file) cout << "default file \"" + def + "\" not found!\n";
            else{
                cout << "default file \"" + def + "\" found, using it!\n";
                fName = def;
                break;
            }
        }else{
            // Break while if file is found
            cout << "file " + fName + " found!\n\n";
            break;
        }
    }
    file.close();
    return fName;
}

/***************************************************************************************************
#   Function:
#       string getFileCont(string fileName).
#
#   Description:
#       This function gets the content of a file and returns it in a string.
#
#   Precondition:
#       This function must be called with an existing path obtain for getFileName function.
#
#   Parameters:
#       * fileName - extension to add to the file name in case it doesn't have one.
#
#    Return Values:
#       * fileCont - String with the content of the file read.
**************************************************************************************************/
inline string getFileCont(string fileName){
    ifstream file;

    // Open file
    file.open(fileName,ios::in);

    // Get content
    string fileCont = string((istreambuf_iterator<char>(file) ),(istreambuf_iterator<char>()));

    // Close file
    file.close();
    return fileCont;
}

/***************************************************************************************************
#   Function:
#       void split(const string& str, vector<string> &cont, char delim).
#
#   Description:
#       This function splits a string using a character as a delimiter and stores the 
#       substrings in a vector of strings.
#
#   Precondition:
#       None.
#
#   Parameters:
#       * str - string to split.
#       * cont - memory address of the string vector to store the substrings.
#       * delim - delimiter character.
#
#    Return Values:
#       * None.
**************************************************************************************************/
inline void split(const string& str, vector<string> &cont, char delim)
{
    stringstream ss(str);
    string token;

    // Get the vector elements from the values before the delimeter
    while (getline(ss, token, delim)) {
        cont.push_back(token);
    }
}
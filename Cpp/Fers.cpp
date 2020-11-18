#include <iostream>
#include <map>
#include <vector>
#include <string>

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

string getFSMHead()
{
    /*
    dummy_dic = { 
    "S0": [[[], "S1", [1]], [[], "S1", [0]]],
    "S1": [[[], "S2", [0]]],
    "S2": [[[], "S0", [0]]]
    }

    [[[], "S1", [1]], [[], "S1", [0]]]  --> vector de vector de vector
    [[], "S1", [1]], [[], "S1", [0]]    --> vector de vector
    [], "S1", [1]   --> vector de listS, S, listS
    lista de strings, string, lista de strings
    */


    
   

    return "";
}

int main()
{

    cout << getFSMHead();

    return 0;
}
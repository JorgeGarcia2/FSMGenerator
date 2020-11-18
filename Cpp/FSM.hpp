#include <fstream>
#include <iostream>
#include <map>
#include <vector>

using namespace std;

class FSMLine
{
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
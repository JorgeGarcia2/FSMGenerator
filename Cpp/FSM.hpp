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
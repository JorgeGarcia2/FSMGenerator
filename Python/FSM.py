#!/bin/python3

import Xchel
import Jorch
import Fers

"""
States=
{
"State0":[[in1,in2,...],"Nstate1",[out1,out2,...]]
         [[in3,in4,...],"Nstate2",[out3,out4,...]]
"State1":[[in1,in2,...],"Nstate1",[out1,out2,...]]
}
"""

class FSM:

    def __init__(self):
        self.FContents=""
        self.States={}
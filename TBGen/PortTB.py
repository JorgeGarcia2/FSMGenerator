#!/bin/python3

import random
import string

class Port:
    #Constructor with information from list
    def __init__(self, port_def):
        self.namePort = port_def[0]                     #Port Name
        self.rangePort = abs(port_def[1] - port_def[2]) #Bus size -1
        self.rangePorta = port_def[1]                   #first bit
        self.rangePortb = port_def[2]                   #last bit

    #Method to get range representation
    def rangePortTB(self):
        strRange = ""
        if (self.rangePort != 0):
            strRange = f"[{self.rangePorta}:{self.rangePortb}] "
        return strRange

    #Method to print Port's attributes
    def print(self):
        print(f"|  |->{self.namePort}\n|  |  |->Range: {self.rangePortTB()}\n|  |  \\->Size: {self.rangePort+1}")
        
        
class Input(Port):
    def __init__(self, port_def):
        Port.__init__(self, port_def)
        self.type = port_def[3]                               #Initial value for the type of value
        self.value = port_def[4]%(2**(self.rangePort) + 1)    #Initial value in range of the bus values
        self.step = port_def[5]                               #Initial value for step

        #If the type is random, use a random value instead
        if (self.type == 'R'):
            self.value = random.randint(0, 2**(self.rangePort + 1) - 1)

    #Polimorfed print method for input data
    def print(self):
        print(f"|  |->{self.namePort}\n|  |  |->Type: {self.type}\n|  |  |->Value: {self.value}\n|  |  |->Step: {self.step}\n|  |  |->Range: {self.rangePortTB()}\n|  |  \\->Size: {self.rangePort+1}") 
    
    #Method to print the port's value depending of a radix
    def printValue(self, base = "dec"):
        if (base == "bin"):
            valueStr = f"b{int2base(self.value, 2)}"
        elif (base == "hex"):
            valueStr = f"h{int2base(self.value, 16)}"
        else:
            valueStr = f"d{int2base(self.value, 10)}"
        return f"{self.namePort}_TB = {self.rangePort + 1}'{valueStr}"
    
    #Method to change the value of the input object, according to its value type
    def chValue(self):
        if (self.type=="d"): self.value = (self.value-self.step)%(2**(self.rangePort + 1))
        elif (self.type=="R"): self.value = random.randint(0, 2**(self.rangePort + 1) - 1)
        else: self.value = (self.value+self.step)%(2**(self.rangePort + 1))
        return

#Method for changing from a decimal value to another radix in string form
def int2base(x, base):
    digs = string.digits + string.ascii_letters
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)
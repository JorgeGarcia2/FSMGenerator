#!/bin/python3.6
 # !/bin/python3.8 --> From Jorge
import random
import string

class Port:
    def __init__(self, port_def):
        self.namePort = port_def[0]     #Port Name
        self.rangePort = port_def[1] - port_def[2] #Bus size -1
        if (self.rangePort > 0):
            self.downtoPort = True      #Down to 
        else:
            self.rangePort *= -1        #To
            self.downtoPort = False
            
        self.print    

    #Metodo para obtener la representacion del rango
    def rangePortTB(self):
        strRange = ""
        if (self.rangePort != 0):
            if(self.downtoPort): 
                strRange = f"[{self.rangePort}:0]"
            else: 
                strRange = f"[0:{self.rangePort}]"
        return strRange

    #Metodo para imprimir los atributos del objeto Port
    def print(self):
        print(f"\nPort name: {self.namePort}\nBus size: {self.rangePort}\nPort value: {self.value}\n")
        
        
class Input(Port):
    def __init__(self, port_def):
        Port.__init__(self, port_def)
        if(type(port_def[3]) == int):
            self.value = port_def[3]
        else: self.value = 'R'
        if (port_def[4] != 0): self.step = port_def[4] #Initial values
        else: self.step = 1

        if (self.value == 'R'):                          
            self.value = random.randint(0, 2**(self.rangePort)) #Asigna valor random al valor inicial
        elif (self.value != 'c' and self.value != 'r'):
            self.value = int(self.value)                        #Asigna valor preestablecido al valor inicial
        
    def printValue(self, base = "dec"):
        if (base == "bin"):
            if(self.downtoPort): valueStr = f"b{int2base(self.value, 2)}"
            else: valueStr = f"b{int2base(self.value, 2)[::-1]}"
        elif (base == "hex"):
            valueStr = f"h{int2base(self.value, 16)}"
        else:
            valueStr = f"d{int2base(self.value, 10)}"
        
        return f"{self.namePort}_TB = {self.rangePort + 1}'{valueStr}"
    
    def nextValue(self):
        if((self.value + self.step) < 2**(self.rangePort + 1)):
            self.value += self.step
        else:
            temp = self.value + self.step
            while(temp>=2**(self.rangePort + 1)): temp -= 2**(self.rangePort + 1)
            self.value = temp
        
    
    

               
                 
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
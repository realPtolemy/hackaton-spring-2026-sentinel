import os, sys, math
def MyFunction(X,y):
    Global_Var = 10
    if X>y:
      return X
    else:
                return y

def calculate(a):
    l = [1,2,3,4,5]
    for i in range(len(l)):
        print(l[i])
    

    try:
        list = a + 10 
    except:
        print("it failed")

class person:
    def __init__(self, n):
        self.name=n
    def Greet(self):
        print("Hi "+self.name)

x = MyFunction( 5,10 )
c = calculate(10)
p = person("Bob")
p.Greet()
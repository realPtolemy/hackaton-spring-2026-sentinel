import os, sys, math # Multiple imports on one line
def MyFunction(X,y): # Poor naming (CamelCase for functions)
    Global_Var = 10 # Unused variable and bad naming
    if X>y:
      return X # 2-space indent
    else:
                return y # 16-space indent!

def calculate(a):
    l = [1,2,3,4,5]
    for i in range(len(l)): # Using range(len()) instead of iterating
        print(l[i])
    
    # Shadowing a built-in name and using a 'naked' except
    try:
        list = a + 10 
    except:
        print("it failed")

class person: # No capital letter for class
    def __init__(self, n):
        self.name=n
    def Greet(self):
        print("Hi "+self.name) # Manual string concatenation instead of f-strings

x = MyFunction( 5,10 ) # Weird spacing inside parentheses
c = calculate(10)
p = person("Bob")
p.Greet()

# No if __name__ == "__main__": block
# No docstrings
# No comments explaining the logic
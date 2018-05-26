# -*- coding:utf-8 -*-



class A(object):
    def __new__(self):
        print(self)
        print("new")
        
    
class B(A):
    def __init__ (self):
        print(self)
        print("Hello")
    
    def __new__ (self):
        A.__new__(self)
        self.__init__(self)

        





def main():
    b = B()



if __name__ == '__main__':
    main()
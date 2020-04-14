#python3 广度优先 python2 深度优先

class A(object):
    def __init__(self):
        print('A')

class B(A):
    pass
    # def __init__(self):
    #     print('B')

class C(A):
    def __init__(self):
        print('C')

class D(B,C):
    pass
    # def __init__(self):
    #     print('D')

a = D()
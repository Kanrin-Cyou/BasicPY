class dog(object):

    def __init__(self,name):
        self.name = name
    
    @staticmethod #静态方法=切断与类的关系，相当于一个单纯的函数，外部调用需要传入self
    def eat(self,food):
        print('{} is eating {}'.format(self.name,food))
        #掉用不了self.name了

d = dog('ChenRonghua')
d.eat(d,'包子')

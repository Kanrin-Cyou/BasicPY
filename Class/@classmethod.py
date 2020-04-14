class dog(object):

    #n=123
    #name = 'huazai'
    def __init__(self,name):
        self.name = name
        #self.n=123
        
    @classmethod #类方法只能访问类变量，不能访问实例变量
    def eat(self,food):
        print('{} is eating {}'.format(self.name,food))

    def talk(self):
        print('%s is talking'%self.name)

d = dog('ChenRonghua')
d.eat('包子')

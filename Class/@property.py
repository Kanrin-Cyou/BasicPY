class dog(object):

    #n=123
    #name = 'huazai'
    def __init__(self,name):
        self.name = name
        #self.n=123

    @property #变成一个属性了，函数不能再传入额外参数了
    def eat(self):
        print('{} is eating {}'.format(self.name,'food'))

    @eat.setter    
    def eat(self,food):
        print('set to food:',food)

    def talk(self):
        print('%s is talking'%self.name)

d = dog('ChenRonghua')
d.eat
d.eat='baozi'

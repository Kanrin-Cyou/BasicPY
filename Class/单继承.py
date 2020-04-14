class people(object):

    def __init__(self,name,age):
        self.name = name
        self.age = age

    def eat(self):
        print('{} is eating'.format(self.name))

    def sleep(self):
        print('{} is sleeping'.format(self.name))

    def talk(self):
        print('{} is talking'.format(self.name))

class relation(object):

    def make_friend(self,obj):
        print('{}is making firend with {}'.format(self.name,obj.name))


class man(people,relation):
    
    def __init__(self,name,age,money): #重构
        #people.__init__(self,name,age)  #调用父类的方法(经典类) class people
        super(man,self).__init__(name,age) #调用父类的方法(新式类) class people(object)
        # super(animal,self).__init__(name,age) 多继承
        self.money = money
        print('{}一出生就有{}块钱'.format(self.name,self.money))

    def piao(self):
        print('{}is piaoing...20s...done'.format(self.name))

    def sleep(self):
        people.sleep(self)
        print('man is sleeping')

class women(people):

    def give_birth(self):
        print('{}is giving birth to a baby'.format(self.name))

m1 = man('niuhanyang',22,10)

# m1.eat()
# m1.piao()
# m1.sleep()

# print('\n')
w1 = women('chenronghua',26)
# w1.give_birth()

m1.make_friend(w1)
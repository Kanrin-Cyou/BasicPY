class Animal(object):
    def __init__(self, name):  # Constructor of the class
        self.name = name
 
    def talk(self):              # Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")
    
    @staticmethod
    def animal_talk(obj):
        obj.talk()

 
class Cat(Animal):

    def talk(self):
        print('%s: Meow!' %self.name)
 
 
class Dog(Animal):

    def talk(self):
        print('%s: Woof!' %self.name)

# def animal_talk(obj): #变成了统一的接口，根据传入不同实现了不同的状态。具体如何实现，在子类里定义。
#     obj.talk()
 
c1 = Cat('小晴')
d1 = Dog('李磊')
 
# animal_talk(c1)
# animal_talk(d1)
Animal.animal_talk(c1) #只给用户一个统一的接口
Animal.animal_talk(d1)
# 上述代码中，obj 是通过 Foo 类实例化的对象，其实，不仅 obj 是一个对象，Foo类本身也是一个对象，因为在Python中一切事物都是对象。
# 如果按照一切事物都是对象的理论：obj对象是通过执行Foo类的构造方法创建，那么Foo类对象应该也是通过执行某个类的 构造方法 创建。

class Foo(object):

    def __init__(self,name):
        self.name = name

f = Foo('alex')
# print(type(f)) #<class '__main__.Foo'>
# print(type(Foo)) #<class 'type'> 类就是type

#来看一下type是如何创造类的, type 称为 class 的 class

#1.普通方法

class Foo1(object):

    def func1(self):
        print('hello alex')

#2.特殊方式 

def func2(self):
    print('hello wupeiqi')

Foo2 = type('Foo',(object,), {'talk': func2})
#type第一个参数：类名
#type第二个参数：当前类的基类
#type第三个参数：类的成员
 
# print(type(Foo2)) #<class 'type'>
# f2 = Foo2() #实例化
# f2.talk() #调用函数

#3.自创

def func3(self):
    print('hello alex')

def __init__(self,name,age):
    self.name = name
    self.age = age

Foo3 = type('Foo3',(object,),{'talk':func3,'__init__':__init__})

f3 = Foo3('alex',35)
f3.talk()
print(f3.name)

#那么问题来了，类默认是由 type 类实例化产生，type类中如何实现的创建类？类又是如何创建对象？
#答：类中有一个属性 __metaclass__，其用来表示该类由 谁 来实例化创建
#所以，我们可以为 __metaclass__ 设置一个type类的派生类，从而查看 类 创建的过程。
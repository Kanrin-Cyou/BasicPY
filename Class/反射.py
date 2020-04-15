
def bulk(self):
    print('%s is yelling'%self.name)

class dog(object):

    def __init__(self,name):
        self.name = name

    def eat(self,food):
        print("%s is eating %s"%(self.name,food))


d = dog('NiuHanyang')
choice = input('>>:').strip()

# if 'choice' == 'eat' : 如果有很多方法那就难办了

#我们使用反射来实现

# print(hasattr(d,choice)) #hasattr返回布尔值，是否有该方法

# print(getattr(d,choice)) #getattr返回该方法的内存地址

# getattr(d,choice)('bacon') #()调用

# ---------------------------

if hasattr(d,choice):
    attr = getattr(d,choice) #d里面对应的东西,可以是name，eat
    setattr(d,choice,"Ronghua") #修改名字
else:
    setattr(d,choice,bulk) #类, choice(输入talk) = bulk()
    d.talk(d)
    # setattr(d,choice,22)
    # print(getattr(d,choice))

print(d.name)

# ---------------------------

# if hasattr(d,choice): 
#     delattr(d,choice) #删除元素
# else:
#     pass

# print(d.name)

# ---------------------------
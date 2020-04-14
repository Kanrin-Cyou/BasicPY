# 面向对象：封装（私有），继承（父子），多态(一种接口，多种形态，实现接口的重用)
# 封装：把一些功能的实现细节不对外暴露
# 继承：代码的重用
    #单继承 调用父类的方法 super(自身,self).__init__(name,age)
    #多继承 
    #组合 self.person = Person(self,job) 直接继承功能
# 多态：接口重用

#对象：实例化一个类之后的对象
#类： 
    #属性：实例变量，类变量，私有属性(__var)
    #方法：构造方法(__init__),析构函数(__del__),私有方法(__method)

#静态方法 @staticmethod 只是名义上归类管理，实际上切断了和类的关联，作为独立的内容
#类方法 @classmethod #类方法只能访问类变量，不能访问实例变量
#属性方法 @property #变成一个属性了，函数不能再传入额外参数了

class role(object):
    
    n = 123 #类变量,大家共用的属性,节省开销（防止每一次都赋值）
    
    def __init__(self,name,role,weapon,life_value=100,money=15000):
        #构造函数
        #在实例化时做一些类的初始化的工作
        self.name = name #实例变量（静态属性），作用域就是实例本身
        self.role = role
        self.weapon = weapon
        self.__life_value = life_value #私有属性
        self.money = money
    
    def __del__(self):
        #析构函数
        #在实例释放、销毁的时候执行
        #通常用于做一些收尾工作，如关闭一些数据库链接，打开的临时文件
        #print('{:s} is dead'.format(self.name))
        pass
    
    def show_statues(self):
        print('name:{}\nlife_value:{}'.format(self.name,self.__life_value))

    def __gotname(self): #私有方法
        print("nice try")

    def shot(self): #类的方法，功能（动态属性）
        print('{:s} is shooting'.format(self.name))

    def get_shot(self):
        print('{:s}: ah..., I got shot.'.format(self.name))

    def buy_gun(self, gun_name):
        print('{:s} just brought {:s}'.format(self.name,gun_name))
    

r1=role('alex','police','ak47')
r1.show_statues()

r2=role('jack','terrorist','B22') 

# r1.name = '陈荣华'
# r1.bulletproof = True
# r1.n = 'abc'

# #r1.shot(),r1.get_shot(),
# #print(r1.name,'has bulletproof is',r1.bulletproof)


# r2.name = '徐良伟'

#r2.shot(),r2.get_shot()

        
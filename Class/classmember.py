from lib.aa import C

obj=C()

print(obj.__doc__) #表示类的描述信息

print(obj.__module__) # 表示当前操作的对象从哪个模块导出的

print(obj.__class__) #表示当前操作的对象的类是什么

# __dict__ 查看类或对象中的所有成员 　

# __str__ 如果一个类中定义了__str__方法，那么在打印 对象 时，默认输出该方法的返回值。
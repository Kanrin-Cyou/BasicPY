#动态导入模块: 导入的模块名是变量

# mod = __import__('lib.aa') #这是解释器自己用的
# obj = mod.aa.C()
# print(obj.name)

import importlib
aa = importlib.import_module('lib.aa')
print(aa.C().name)
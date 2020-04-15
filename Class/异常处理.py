
#异常处理：虽然出了问题，但不想让用户看到该错误
#提前做好预处理，提示用户重新输入

names = ['alex','jack']
data={}
#names[3]

try:   
    # names[3]
    # data['name']
    a=1
    print(a)
except (KeyError,IndexError) as e:  #一直执行上面命令，除非出现该错误，执行下面命令
    print('没有这个Key',e)

except Exception: #抓所有错误
    print("未知错误")

else:
    print("一切正常")

finally: #不管有没有错，都执行
    print("结束")


# except IndexError as e:
#     print('列表操作错误',e)

# except Exception as e : #所有错误，不推荐使用



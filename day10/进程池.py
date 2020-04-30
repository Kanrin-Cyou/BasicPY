#进程池，限制同一时间的进程数量，否者影响OS。
#线程对性能影响小，但过多会导致cpu切换过于频繁。

from  multiprocessing import Process, Pool,freeze_support
import time
import os

def Foo(i):
    time.sleep(2)
    print("in process",os.getpid())
    return i + 100

def Bar(arg):
    print('-->exec done:', arg,os.getpid()) #主进程执行的callback 
    #主进程写，只需要连接一次，如果每个子进程都连接，效率低

if __name__ == '__main__': #手动执行就执行，不手动执行当作模块脚本就不执行（模块名）
    #freeze_support()
    pool = Pool(processes=3) #允许进程池同时放入5个进程
    
    print("主进程",os.getpid())
    
    for i in range(10):
        pool.apply_async(func=Foo, args=(i,), callback=Bar) #callback=回调，执行完前面的func，执行callback的
        #pool.apply(func=Foo, args=(i,)) #串行
        #pool.apply_async(func=Foo, args=(i,)) #并行（异步执行）
    print('end')
    pool.close()
    pool.join() #进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。.join()
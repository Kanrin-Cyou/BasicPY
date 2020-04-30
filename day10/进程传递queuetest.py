from multiprocessing import Process, Queue #进程Q
#import threading
#import queue #线程q

#两个进程之间，内存独立
#两个线程之间，内存共享

def f(qq):
    qq.put([42,None,'hello'])

#并不是两个进程共享q 而是克隆了一个q
#然后通过pickel联系更新，实现了数据的传递

if __name__ == '__main__': #主进程

    #q = queue.Queue()
    #p = threading.Thread(target=f,)

    q = Queue() #生成一个Queue
    p = Process(target=f,args=(q,)) #把主进程q传递给子进程，子进程克隆q
    p.start() #启动子进程
    print(q.get()) 
    p.join()
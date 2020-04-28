import threading, time

import queue

q = queue.Queue(maxsize=10) #实例化

def Producer(name):
    count = 1
    while True:
        q.put('%s包子%i'%(name,count))
        print('生产了包子',count)
        time.sleep(0.5)
        count += 1


def Consumer(name):
    while True:
        print('[%s] 取到了[%s]并且吃了它'%(name,q.get()))

p = threading.Thread(target=Producer,args=('Alex',))
p1 = threading.Thread(target=Producer,args=('Boson',))
c = threading.Thread(target=Consumer,args=('ChengRonghua',))
c1 = threading.Thread(target=Consumer,args=('王森',))

p.start()
p1.start()
c.start()
c1.start()

__author__ = "Alex Li"

from multiprocessing import Process, Lock

#进程为什么需要锁？
#但是有没有共用同一块屏幕(print)？保证print不会乱


def f(l, i):
    l.acquire()
    print('hello world', i)
    l.release()


if __name__ == '__main__':
    lock = Lock()

    for num in range(100):
        Process(target=f, args=(lock, num)).start()
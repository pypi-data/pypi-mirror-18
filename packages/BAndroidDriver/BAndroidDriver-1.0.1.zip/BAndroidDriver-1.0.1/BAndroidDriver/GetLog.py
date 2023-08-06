# coding=utf-8
import threading
import time

class GetLog(threading.Thread):

    def __init__(self, thread_num=0, timeout=1.0):
        super(GetLog, self).__init__()
        self.thread_num = thread_num
        self.stopped = False
        self.timeout = timeout

    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        while True:
            print "Test"
        while not self.counter:
            subthread.join(self.name)
        print('Thread stopped')

    def stop(self):
        self.stopped = True

    def isStopped(self):
        return self.stopped
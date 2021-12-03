import threading
import queue
import time
import random

buffer = queue.Queue()


def Producer(name):
    cnt = 0
    while cnt < 10:
        while buffer.qsize() < 10:
            element = chr(random.randint(0, 25) + 65)
            buffer.put(element)
            print(f"{name} has put '{element}' in the buffer\n")
            cnt += 1
            time.sleep(1)


def Consumer(name):
    cnt = 0
    while cnt < 10:
        while buffer.qsize():
            print(f'{name} get {buffer.get()} from buffer\n')
            time.sleep(1)
            cnt += 1


t1 = threading.Thread(target=Producer, args=("p1",))
t2 = threading.Thread(target=Producer, args=("p2",))
t3 = threading.Thread(target=Consumer, args=("c1",))
t4 = threading.Thread(target=Consumer, args=("c2",))

t1.start()
t2.start()
t3.start()
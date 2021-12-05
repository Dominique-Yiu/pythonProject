"""生产者-消费者模型"""
import time
import random
from multiprocessing import Process, Semaphore, Manager
import multiprocessing
import argparse
import os
import pandas as pd

"""消费者模型"""


def consumer(mydict: dict, mylist: list, Mutex, Empty, Full, Out):
    # cnt统计消费者的消费次数
    cnt = 0
    # 每个消费者，进行十次的消费行为
    while cnt < 10:
        # 这个变量的意义是为了防止while打印非常多次的提示语句，一次就行了
        if Full.get_value() <= 0:
            Nothing = None  # Do nothing
            # 如果是因为同步信号量，输出：{} seconds | Buffer empty! Consumer: {} is waiting... print(f"{time.strftime('%H:%M:%S')}
            # seconds | Buffer empty! Consumer: {multiprocessing.current_process().name} is waiting...")
        Full.acquire()
        if Mutex.get_value() <= 0:
            Nothing = None  # Do nothing
            # 如果是因为互斥信号量，输出：{} seconds | A process is executing! Consumer: {} is waiting... print(f"{time.strftime(
            # '%H:%M:%S')} seconds | A process is executing! Consumer: {multiprocessing.current_process().name} is
            # waiting...")
        Mutex.acquire()
        # 随机一个消费操作的耗时
        time.sleep(random.randint(1, 2))
        # print(f"{time.strftime('%H:%M:%S')} seconds | Consumer: {multiprocessing.current_process().name} has
        # consumed a product ({mylist[mydict['fot']]}) that located in the {mydict['fot']}th position of the buffer.")

        # print('Executing Time\t\tBuffer Data\t\t\t\t\t\t\tProcess Name\t\tConsume/Produce')
        print(
            f"{time.strftime('%H:%M:%S')}\t\t{mylist}\t\t{multiprocessing.current_process().name}-C\t\t{mylist[mydict['fot']]}")
        Out.append([time.strftime('%H:%M:%S'), list(mylist), multiprocessing.current_process().name + '-C', mylist[mydict['fot']]])

        # 对消费后的内容重置，同时cnt自增一表示消费者执行一次消费操作，另外更新fot即out的位置
        mylist[mydict['fot']] = chr(48)

        cnt += 1
        mydict['fot'] = (mydict['fot'] + 1) % mydict['buffer_size']
        # 最后一步做V操作，没有顺序
        Mutex.release()
        Empty.release()

        # 在下次操作前，随机等待一段时间
        time.sleep(random.randint(1, 4))


"""生产者模型"""


def producer(mydict: dict, mylist: list, Mutex, Empty, Full, Out):
    # 生产者的生产操作的次数
    cnt = 0
    # 每个生产者生产十次产品
    while cnt < 10:
        # 首先进行同步信号的判断，看有没有空位供存放
        if Empty.get_value() <= 0:
            Nothing = None  # Do nothing
            # print(f"{time.strftime('%H:%M:%S')} seconds | Buffer full! Producer: {multiprocessing.current_process(
            # ).name} is waiting...")
        Empty.acquire()
        if Mutex.get_value() <= 0:
            Nothing = None  # Do nothing
            # print(f"{time.strftime('%H:%M:%S')} seconds | A process is executing! Producer: {
            # multiprocessing.current_process().name} is waiting...")
        Mutex.acquire()
        # 随机一个生产时间，一般长于消费时间
        time.sleep(random.randint(2, 4))
        # 随机产生一个A~Z的字符
        element = chr(random.randint(0, 25) + 65)
        # print(f"{time.strftime('%H:%M:%S')} seconds | Producer: {multiprocessing.current_process().name} has
        # produced a product ({element}) that put in the {mydict['fin']}th position of the buffer.")

        # 更新mylist, cnt, fin等等
        mylist[mydict['fin']] = element

        # print('Executing Time\t\tBuffer Data\t\t\t\t\t\t\tProcess Name\t\tConsume/Produce')
        print(f"{time.strftime('%H:%M:%S')}\t\t{mylist}\t\t{multiprocessing.current_process().name}-P\t\t{element}")
        Out.append([time.strftime('%H:%M:%S'), list(mylist), multiprocessing.current_process().name + '-P', element])

        cnt += 1
        mydict['fin'] = (mydict['fin'] + 1) % mydict['buffer_size']
        # 最后做V操作，没有顺序
        Mutex.release()
        Full.release()

        # 在下次操作前，随机等待一段时间
        time.sleep(random.randint(1, 4))


if __name__ == '__main__':
    # 创建一个命令行解析器对象
    parser = argparse.ArgumentParser(description='Producer-Consumer-Model')
    # 添加参数
    parser.add_argument('buffer_size', type=int, default=10,
                        help='The size of buffer area.')
    parser.add_argument('--exe', action='store_true',
                        help="Execute the Producer-Consumer-Model with the user's <input argument> or default <10>")
    # 参数解析到agrs中
    args = parser.parse_args()
    if args.exe:
        os.system('cls')
        print(f'\n{args}\n')
        # 打印以下详细信息，这个consumer_producerModel.py是该程序的文件名，可自行修改
        os.system('python consumer_producerModel.py -h')
        print()
        # 缓冲区大小
        buffer_size = args.buffer_size
        
        # 缓冲区下一个存放/取出的索引
        fin = fot = 0
        buffer = [chr(48) for _ in range(buffer_size)]

        # 互斥信号量
        mutex = Semaphore(1)

        # 同步信号量
        empty = Semaphore(buffer_size)
        full = Semaphore(0)

        # 将有关buffer缓冲区的内容通过Manager的方法进行共享
        mydict = Manager().dict()
        mylist = Manager().list(buffer)
        output = Manager().list()
        mydict['buffer_size'] = buffer_size
        mydict['fin'] = fin
        mydict['fot'] = fot

        # 创建消费者进程
        consumer1 = Process(target=consumer, args=(mydict, mylist, mutex, empty, full, output))
        consumer2 = Process(target=consumer, args=(mydict, mylist, mutex, empty, full, output))

        # 创建生产者进程
        producer1 = Process(target=producer, args=(mydict, mylist, mutex, empty, full, output))
        producer2 = Process(target=producer, args=(mydict, mylist, mutex, empty, full, output))

        print('Executing Time\t\tBuffer Data\t\t\t\t\t\t\tProcess Name\t\tConsume/Produce')
        # 进程开始运行，相当于fork()
        producer1.start()
        producer2.start()
        consumer1.start()
        consumer2.start()

        # 等待进程结束
        producer1.join()
        producer2.join()
        consumer1.join()
        consumer2.join()

        df = pd.DataFrame(list(output), columns=['Executing Time', 'Buffer Data', 'Process Name', 'Consume/Produce'])
        df.to_csv('./output.csv')

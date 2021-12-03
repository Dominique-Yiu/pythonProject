import os
import argparse
import time


class Banker_Algorithm:

    """初始化函数"""

    def __init__(self):

        #   Available列表，用来保存当前可利用资源
        self.Available = [0 for _ in range(args.ResourceNum)]

        #   Work列表，系统可提供给进程继续运行所需的各类资源数目，初始时和Available一致
        self.Work = [0 for _ in range(args.ResourceNum)]

        #   MaxRequest列表，进程最大需求
        self.MaxRequest = [[0] * args.ResourceNum for _ in range(args.ProcessNum)]

        #   Allocation列表，系统已经分配的资源
        self.Allocation = [[0] * args.ResourceNum for _ in range(args.ProcessNum)]

        #   Need列表，进程还需要的资源
        self.Need = [[0] * args.ResourceNum for _ in range(args.ProcessNum)]

        #   是否安全
        self.Finish = [False for _ in range(args.ProcessNum)]

        #   安全序列号
        self.SafeSeries = [0 for _ in range(args.ProcessNum)]

        #   5
        self.Request = [0 for _ in range(args.ResourceNum)]

        #   资源数量计数
        self.num = 0

    '''数据输入函数'''

    def data_input(self):

        self.Available = [int(item) for item in input('输入初始资源可利用数：').split(' ')]
        for i in range(args.ResourceNum):
            self.Work[i] = self.Available[i]

        for i in range(args.ProcessNum):
            self.MaxRequest[i] = [int(item) for item in input(f'输入第{i + 1}个进程的最大需求：').split(' ')]

        for i in range(args.ProcessNum):
            self.Allocation[i] = [int(item) for item in input(f'输入第{i + 1}个进程的已分配资源：').split(' ')]

        for i in range(args.ProcessNum):
            for j in range(args.ResourceNum):
                self.Need[i][j] = self.MaxRequest[i][j] - self.Allocation[i][j]

    '''打印输出系统信息'''

    def ShowInfo(self):

        os.system('cls')
        print('-' * 60)
        print('当前系统各类资源剩余：', self.Available)

        print('当前系统资源情况：')
        print('PID\t  Max\t\tAllocation\t  Need')
        for i in range(args.ProcessNum):
            print(f'P{i}\t', end=' ')
            for j in range(args.ResourceNum):
                print('%2d' % (self.MaxRequest[i][j]), end=' ')
            print('\t', end=' ')
            for j in range(args.ResourceNum):
                print('%2d' % (self.Allocation[i][j]), end=' ')
            print('\t', end=' ')
            for j in range(args.ResourceNum):
                print('%2d' % (self.Need[i][j]), end=' ')
            print('')

    '''打印安全检查信息'''

    def SafeInfo(self, idx: int):

        print(f'P{idx}\t', end=' ')
        for i in range(args.ResourceNum):
            print('%2d' % (self.Work[i]), end=' ')
        print('\t', end=' ')
        for i in range(args.ResourceNum):
            print('%2d' % (self.Allocation[idx][i]), end=' ')
        print('\t', end=' ')
        for i in range(args.ResourceNum):
            print('%2d' % (self.Need[idx][i]), end=' ')
        print('\t', end=' ')
        # for i in range(args.ResourceNum):
        #     print('%2d' % (self.Allocation[idx][i] + self.Work[i]), end=' ')
        print('')

    '''判断一个进程的还需要的资源是否全为0'''

    def isAllZero(self, idx: int) -> bool:

        self.num = 0
        for i in range(args.ResourceNum):
            if self.Need[idx][i] == 0:
                self.num += 1

        if self.num == args.ResourceNum:
            return True
        return False

    '''安全检查'''

    def isSafe(self) -> bool:

        safeIndex = 0
        allFinish = 0
        r = temp = pNum = 0

        #   预分配
        for i in range(args.ResourceNum):
            self.Work[i] = self.Available[i]
        #   未完成进程设置为False
        for i in range(args.ProcessNum):
            result = self.isAllZero(i)
            if result:
                self.Finish[i] = True
                allFinish += 1
            else:
                self.Finish[i] = False
        #   预分配开始
        while allFinish != args.ProcessNum:
            self.num = 0
            for i in range(args.ResourceNum):
                if self.Need[r][i] <= self.Work[i] and (not self.Finish[r]):
                    self.num += 1
            #   如果可以分配资源，则运行直至完成，最后释放资源
            if self.num == args.ResourceNum:
                for i in range(args.ResourceNum):
                    self.Work[i] += self.Allocation[r][i]  # 释放资源
                allFinish += 1
                self.SafeInfo(r)
                self.SafeSeries[safeIndex] = r
                safeIndex += 1
                self.Finish[r] = True
            r += 1
            if r >= args.ProcessNum:
                r = r % args.ProcessNum
                # 第k轮结束之后，allFinish还是和k-1轮一样，说明发生死锁
                if temp == allFinish:
                    break
                temp = allFinish
            pNum = allFinish
        #   判断系统是否安全
        for i in range(args.ProcessNum):
            if not self.Finish[i]:
                print('当前系统不安全！\n\n')
                return False
        #   打印安全序列
        print('当前系统安全！\n\n安全序列为：')
        #   除去之前已经完成的进程
        for i in range(args.ProcessNum):
            result = self.isAllZero(i)
            if result:
                pNum -= 1
        for i in range(pNum):
            print('%d' % (self.SafeSeries[i]), end=' ')
        print('')
        return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Banker's Algorithm")
    #   资源数量
    parser.add_argument('ResourceNum', type=int, default=3, help='The number of the resource.')
    #   进程数量
    parser.add_argument('ProcessNum', type=int, default=5, help='The number of the process.')
    parser.add_argument('--exe', help='Execute the algorithm.', action='store_true')

    args = parser.parse_args()

    if args.exe:
        over_num = 0    # 完全处理完成的进程总数
        curProcess = 0  # 当前考虑的进程
        bank = Banker_Algorithm()
        # 用户进行输入
        bank.data_input()
        # 首先打印一下资源信息
        bank.ShowInfo()
        print('系统安全情况分析：')
        print("PID\t  Work\t\tAllocation\t  Need")
        isStart = bank.isSafe()
        # 如果在未分配前就是个不安全的系统，直接结束程序
        while isStart:
            print('-' * 60)
            # 这部分是用户进行输入，包括需要分配的进程和资源的指定内容
            while True:
                curProcess = eval(input('输入要分配的进程：'))
                if 0 <= curProcess < args.ProcessNum:
                    break
                os.system('cls')
                print('输入有误，重新输入！')

            for i in range(args.ResourceNum):
                bank.Request[i] = eval(input(f'请输入要分配给进程 P{curProcess} 的第 {i + 1} 类资源：'))

            # 判断用户输入的分配是否合理，如果合理，开始分配
            bank.num = 0
            for i in range(args.ResourceNum):
                if bank.Request[i] <= bank.Need[curProcess][i] and bank.Request[i] <= bank.Available[i]:
                    bank.num += 1
                else:
                    print('发生错误！可能原因如下：\n(1)您请求分配的资源可能大于该进程的某些资源的最大需要！\n(2)系统所剩的资源已经不足了！')
                    break

            if bank.num == args.ResourceNum:
                bank.num = 0
                for i in range(args.ResourceNum):
                    # 分配资源
                    bank.Available[i] -= bank.Request[i]
                    bank.Allocation[curProcess][i] += bank.Request[i]
                    bank.Need[curProcess][i] -= bank.Request[i]
                    # 如果该资源分配完全，不再需要该资源
                    if bank.Need[curProcess][i] == 0:
                        bank.num += 1
                # 如果该进程所有的需求都得到满足，执行后释放
                if bank.num == args.ResourceNum:
                    for i in range(args.ResourceNum):
                        bank.Available[i] += bank.Allocation[curProcess][i]
                    over_num += 1
                    print(f'\n\n本次分配进程 P{curProcess} 完成,该进程占用资源全部释放完毕！')
                else:
                    print(f'\n\n本次分配进程 P{curProcess} 未完成！')
                time.sleep(3.0)
                os.system('pause')
                bank.ShowInfo()
                print('系统安全情况分析：')
                print("PID\t  Work\t\tAllocation\t  Need")
                # 虽然能够在资源足够的时候进行分配，但不能保证之后不发生死锁，这里先做判断
                if not bank.isSafe():
                    for i in range(args.ResourceNum):
                        bank.Available[i] += bank.Request[i]
                        bank.Allocation[curProcess][i] -= bank.Request[i]
                        bank.Need[curProcess][i] += bank.Request[i]
                    print('资源不足，等待中...\n\n分配失败！')
                    time.sleep(3.0)
                    os.system('pause')
            # 如果所有进程执行完成，跳出循环即可
            if over_num == args.ProcessNum:
                break
        os.system('cls')
        print('-' * 20, '程序运行结束', '-' * 20)
        for i in range(10):
            print('-', ' ' * 50, '-')
        print('-' * 54)
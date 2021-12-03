import os
import argparse
def d_ClearScreen():
    if os.name=='nt':#如果当前系统为WINDOWS
        os.system('cls')#执行cls清屏命令
    else:
        os.system('clear')#其它linux等系统执行clear命令
    return

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="Banker's Algorithm")
    # #   资源数量
    # parser.add_argument('ResourceNum', type=int, default=3, help='The number of the resource.')
    # #   进程数量
    # parser.add_argument('ProcessNum', type=int, default=5, help='The number of the process.')
    # parser.add_argument('--exe', help='Execute the algorithm.',
    #                     action='store_true')
    #
    # args = parser.parse_args()

    ResourceNum = eval(input())
    ProcessNum = eval(input())

    #   Available列表，用来保存当前可利用资源
    Available = [[0] * ResourceNum]
    Available = [int(item) for item in input('输入初始资源可利用数：').split(' ')]

    #   MaxRequest列表，进程最大需求
    MaxRequest = [[0] * ResourceNum for _ in range(ProcessNum)]
    for i in range(ProcessNum):
        MaxRequest[i] = [int(item) for item in input(f'输入第{i + 1}个进程的最大需求：').split(' ')]

    #   Allocation列表，系统已经分配的资源
    Allocation = [[0] * ResourceNum for _ in range(ProcessNum)]
    for i in range(ProcessNum):
        Allocation[i] = [int(item) for item in input(f'输入第{i + 1}个进程的已分配资源：').split(' ')]

    #   Need列表，进程还需要的资源
    Need = [[0] * ResourceNum for _ in range(ProcessNum)]
    for i in range(ProcessNum):
        for j in range(ResourceNum):
            Need[i][j] = MaxRequest[i][j] - Allocation[i][j]

    print(MaxRequest)
    print(Allocation)
    print(Need)


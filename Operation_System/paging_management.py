#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 20:34
# @Author  : Yiu
# @Site    : 
# @File    : paging_management.py
# @Software: PyCharm
import argparse
import os
import numpy as np
import random


class job_C:
    def __init__(self, size: int):
        self.page_num = np.linspace(0, size - 1, size).astype(np.int32)
        self.block_num = np.zeros(size).astype(np.int32)
        self.size = size

    def page_table(self):
        print(f'页号\t\t\t块号')
        for i in range(self.size):
            print(f'{self.page_num[i]}\t\t\t{self.block_num[i]}')


class paging_management:
    def __init__(self, size: int):
        self.block = np.array([[0 for _ in range(size)] for _ in range(size)])
        # 当前空闲块数
        self.free_num = size * size
        self.size = size

    def fill_block(self, pos_x: int, pos_y: int):
        if self.block[pos_x][pos_y] != 1:
            self.free_num -= 1
        self.block[pos_x][pos_y] = 1

    def retrieve_block(self, pos_x: int, pos_y: int):
        if self.block[pos_x][pos_y] != 0:
            self.free_num += 1
        self.block[pos_x][pos_y] = 0

    def display_block(self):
        print(self.block)

    def allocate_job(self, task: job_C) -> bool:
        idx = 0
        # 首先判断能否装下
        if self.free_num >= task.size:
            for i in range(self.size):
                for j in range(self.size):
                    if self.block[i][j] == 0:
                        self.fill_block(i, j)
                        task.block_num[idx] = i * 8 + j
                        idx += 1
                    if idx == task.size:
                        print("位视图如下：")
                        self.display_block()
                        print('-' * 100)
                        print(f'当前空闲块数：{self.free_num}')
                        print('-' * 100)
                        print("任务页表如下：")
                        task.page_table()
                        return True
        else:
            print("该任务无法放入，请进行其他操作.")
            return False

    def recycle_job(self, task: job_C):
        for i in range(task.size):
            pos_x = int(task.block_num[i] / 8)
            pos_y = task.block_num[i] % 8
            self.retrieve_block(pos_x, pos_y)
        print('-' * 100)
        print("归还的页表如下：")
        task.page_table()
        print('-' * 100)
        print("回收任务后的位视图如下：")
        self.display_block()
        print('-' * 100)
        print(f"当前空闲块数：{self.free_num}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='分页管理')
    parser.add_argument('block_size', type=int, default=8, help='位视图的边长大小')
    parser.add_argument('rand_num', type=int, default=10, help='初始块被占用的最大个数')
    parser.add_argument('--exe', help='执行程序', action='store_true')
    args = parser.parse_args()

    if args.exe:
        task_num = 0
        task_dic = {}
        manager = paging_management(args.block_size)
        for _ in range(args.rand_num):
            manager.fill_block(random.randint(0, args.block_size - 1), random.randint(0, args.block_size - 1))
        manager.display_block()
        print(f"当前空闲块数：{manager.free_num}")
        os.system('pause')
        while True:
            os.system('cls')
            operation = eval(input("请输入操作数（0：分配任务 1：回收任务 2：退出）："))

            if operation == 2:
                print("-" * 100)
                print("-" * 100)
                print("-" * 100)
                print("-" * 100)
                print('-' * 42, "欢迎下次使用！", '-' * 42)
                print("-" * 100)
                print("-" * 100)
                print("-" * 100)
                print("-" * 100)
                break
            elif operation == 0:
                task = job_C(eval(input("请输入分配任务所需要的块总数：")))
                # 分配任务
                flag = manager.allocate_job(task)
                if flag:
                    task_num += 1
                    task_dic['task' + str(task_num)] = task
                print(f'当前任务有：{task_dic}')

            elif operation == 1:
                name = input("请输入回收任务的名称：")
                if name in task_dic:
                    task = task_dic[name]
                    manager.recycle_job(task)
                    del task_dic[name]
                else:
                    print("请输入合法的回收任务名称！")
                print(f'当前任务有：{task_dic}')
            else:
                print("请按要求进行输入！")
            os.system('pause')

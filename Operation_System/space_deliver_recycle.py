#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 18:32
# @Author  : Yiu
# @Site    :
# @File    : sample.py
# @Software: PyCharm

import argparse
import os

sort_dic = {'未分配': 0, '空表目': 1}
str_list = ['空表目', '未分配']


class table:
    def __init__(self, start: int, length: int, status: str):
        self.start = start
        self.length = length
        self.status = status


class space_deliver_recycle:
    def __init__(self):
        # 正在内存中的任务字典
        self.dic = {}
        # 分配成功的任务数目，即每个任务的任务编号
        self.num = 1

    def deliver_space(self, data: list, length: int) -> list:
        for idx, it in enumerate(data):
            # 判断状态是否为未分配
            if it.status is str_list[1]:
                if it.length > length:
                    # 将任务放入到字典中
                    self.dic['task' + str(self.num)] = [it.start, length]
                    self.num += 1

                    it.length -= length
                    it.start += length
                    # 输出分配情况
                    data = sorted(data, key=lambda x: (sort_dic.get(x.status, 999), x.start))
                    print_table(data)
                    print(f'当前正在主存的任务为：', self.dic)
                    return data
                elif it.length == length:
                    # 将任务放入到字典中
                    self.dic['task' + str(self.num)] = [it.start, length]
                    self.num += 1
                    # 设置成空表目
                    it.length = it.start = 0
                    it.status = str_list[0]
                    # 输出分配情况
                    data = sorted(data, key=lambda x: (sort_dic.get(x.status, 999), x.start))
                    print_table(data)
                    print(f'当前正在主存的任务为：', self.dic)
                    return data
                else:
                    # 如果使空闲区的最后一栏
                    if idx == len(data) - 1:
                        print('作业不能装入.')
            else:
                # 如果使空闲区的最后一栏
                if idx == len(data) - 1:
                    print('作业不能装入.')
        return sorted(data, key=lambda x: (sort_dic.get(x.status, 999), x.start))

    def recycle(self, data: list, name: str) -> list:
        task = 'task' + name
        # 判断是否存在这个任务
        if task in self.dic:  # 任务存在在这个字典中
            data = self.modify(data, task)
            data = sorted(data, key=lambda x: (sort_dic.get(x.status, 999), x.start))
            del self.dic[task]
            print(f"成功删除task{name}.")
            # 打印空闲表
            print_table(data)
            print(f'当前正在主存的任务为：', self.dic)
        else:
            print("不存在改任务，输入有效任务，有效任务如下：")
            # 打印有效任务
            print(self.dic)
        return data

    def modify(self, data: list, task: str) -> list:
        flag_bottom = False  # 不存在下空闲区
        for idx, it in enumerate(data):
            # 是否存在下邻的空闲区
            if self.dic[task][0] + self.dic[task][1] == it.start:  # 存在下邻的空闲区
                flag_bottom = True
                # 是否存在上邻空闲区
                flag = False  # 不存在上邻空闲区
                for idx_1, it_1 in enumerate(data):
                    if it_1.start + it_1.length == self.dic[task][0] and it_1.status == str_list[1]:  # 存在上邻空闲区
                        flag = True
                        # 上邻区长度增加 it.length + self.dic[task][1]
                        it_1.length += it.length + self.dic[task][1]
                        # 将下邻设置为空表目
                        it.length = it.start = 0
                        it.status = str_list[0]
                        break

                if not flag:  # 不存在上邻区
                    it.start = self.dic[task][0]
                    it.length += self.dic[task][1]
                return data
        if not flag_bottom:  # 不存在下邻区
            flag = False  # 假设不存在上邻空闲区
            for idx_1, it_1 in enumerate(data):
                if it_1.start + it_1.length == self.dic[task][0] and it_1.status == str_list[1]:  # 存在上邻空闲区
                    flag = True
                    # 上邻区长度增加 self.dic[task][1]
                    it_1.length += self.dic[task][1]
                    break

            if not flag:  # 不存在上邻区
                # 找个空表目
                for idx_1, it_1 in enumerate(data):
                    if it_1.status == str_list[0]:
                        it_1.start = self.dic[task][0]
                        it_1.length = self.dic[task][1]
                        it_1.status = str_list[1]
                        break
            return data
        return data


def print_table(data: list):
    print("起止\t\t长度\t\t状态")
    for it in data:
        print(f'{it.start}\t\t{it.length}\t\t{it.status}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='主存储器的分配和回收')
    parser.add_argument('list_size', type=int, default=5, help='空闲区总栏数')
    parser.add_argument('--exe', help='执行程序', action='store_true')
    args = parser.parse_args()
    data_list = []
    if args.exe:
        for _ in range(args.list_size):
            os.system("cls")
            status = str_list[eval(input("请输入状态（1：未分配或0：空表目）："))]
            start = eval(input("请输入起始位置（如果是空表目，请输入0）："))
            length = eval(input("请输入长度（如果是空表目，请输入0）："))
            data_list.append(table(start, length, status))

        data_list = sorted(data_list, key=lambda x: (sort_dic.get(x.status, 999), x.start))
        print_table(data_list)
        os.system("pause")

        method = space_deliver_recycle()
        while True:
            os.system("cls")
            operation = eval(input("请输入操作数（1: 分配 2: 回收 3: 退出）："))
            if operation == 3:
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
            elif operation == 1:
                space_size = eval(input("请输入分配的空间大小："))
                data_list = method.deliver_space(data_list, space_size)
            elif operation == 2:
                name = input("请输入需要回收的任务编号：")
                data_list = method.recycle(data_list, name)
            else:
                print("请按要求进行输入！")
            os.system("pause")
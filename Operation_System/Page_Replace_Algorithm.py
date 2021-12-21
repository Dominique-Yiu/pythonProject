#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 9:50
# @Author  : Yiu
# @Site    : 
# @File    : Page_Replace_Algorithm.py
# @Software: PyCharm
import numpy as np
import argparse
import random
import matplotlib.pyplot as plt


class page_replace_lru:
    # 初始化函数
    def __init__(self, size: int):
        # 页块数地大小
        self.size = size
        # 缺页次数统计
        self.count_lru = 0
        # 当前使用的块大小
        self.current_size = 0
        # 内存
        self.memory = ['-' for _ in range(self.size)]
        # 记录优先级
        self.priority = np.array([0 for _ in range(self.size)])

    # 处理
    def lru(self, page: chr, flag: bool):
        # 首先判断有没有空间
        if self.current_size < self.size:  # 有空间
            if page not in self.memory:
                self.count_lru += 1
                for idx, item in enumerate(self.memory):
                    if item == '-':
                        self.memory[idx] = page
                        self.current_size += 1
                        action = f'页面缺失并内存有空间，将page:({page})放入Memory的[{idx}]位置处.'
                        break
                    else:
                        self.priority[idx] += 1
            else:
                idx = self.memory.index(page)
                action = f'页面未缺失，可直接在Memory进行访问({page}).'
                for i in range(self.current_size):
                    self.priority[i] += 1
            self.priority[idx] = 0
        # 如果空间已满，使用LRU算法
        else:
            # 首先判断内存是否存在这个页
            if page not in self.memory:  # 如果不在，需要替换
                idx = np.argmax(self.priority)
                action = f'页面缺失但内存已满，将page:({page})放入Memory的[{idx}]位置处，替换page:({self.memory[idx]}).'
                self.memory[idx] = page
                self.count_lru += 1
            else:
                idx = self.memory.index(page)
                action = f'页面未缺失，可直接在Memory进行访问({page}).'
            self.priority += 1
            self.priority[idx] = 0
        if flag:
            print(page, "\t\t",*self.memory, "\t\t", *self.priority, "\t\t", action)


def generate_page_sequence(length: int) -> str:
    result = ""
    for _ in range(length):
        result += chr(random.randint(48, 48 + 9))
    return result


def plot(PBlocksNumber: int, PSequencesLength: int):
    epoch = 10
    result = []
    for num in range(10, 200):
        percent = 0
        for _ in range(epoch):
            LRU = page_replace_lru(PBlocksNumber)
            sequence = generate_page_sequence(num)
            for item in sequence:
                LRU.lru(item, False)
            percent += float(LRU.count_lru / num)
        result.append(float(percent / epoch))
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.plot(np.linspace(10, 199, 190), result)

    result = []
    for num in range(1, 15):
        percent = 0
        for _ in range(epoch):
            LRU = page_replace_lru(num)
            sequence = generate_page_sequence(PSequencesLength)
            for item in sequence:
                LRU.lru(item, False)
            percent += float(LRU.count_lru / PSequencesLength)
        result.append(float(percent / epoch))
    plt.subplot(1, 2, 2)
    plt.plot(np.linspace(1, 15, 14), result)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='内存页面置换算法')
    parser.add_argument('PBlocksNumber', type=int, default=3, help='页块数')
    parser.add_argument('PSequencesLength', type=int, default=20, help='页访问序列的长度')
    parser.add_argument('--exe', help='Execute the algorithm.', action='store_true')
    parser.add_argument('--plt', help='Draw a picture.', action='store_true')
    args = parser.parse_args()
    print('-' * 80)
    print('页块数\t\t页访问序列的长度\t\t访问页面序列')

    if args.exe:
        LRU = page_replace_lru(args.PBlocksNumber)
        sequence = generate_page_sequence(args.PSequencesLength)
        print(f'{args.PBlocksNumber}\t\t{args.PSequencesLength}\t\t\t\t{sequence}')
        print('-' * 80)
        print('Page\t\tMemory\t\tPriority\t\tAction')
        for item in sequence:
            LRU.lru(item, True)
        print(f'缺页率：{float(LRU.count_lru / args.PSequencesLength)}')
        print('-' * 80)
    if args.plt:
        PBlocksNumber = eval(input("请输入固定长度的页块数(以观察在页块数不变情况下，缺页率和访问页数长度的关系)："))
        PSequencesLength = eval(input("请输入固定长度的访问页面长度(以观察在访问页面长度固定时，缺页率和页块数的关系)："))
        plot(PBlocksNumber, PSequencesLength)


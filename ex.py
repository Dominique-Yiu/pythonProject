import argparse
from math import *
import time

time1, time2 = 0, 0

class Solution:
    '''初始化函数'''
    def __init__(self, N: int, A: int):
        self.primality = N
        self.integer = A

    '''返回所有的因数'''
    def return_AllFactors(self) -> list:
        ls = []
        number = self.euler_phi(self.primality)
        for i in range(1, number + 1):
            if number % i == 0:
                ls.append(i)
        print('p-1所有的因数列表：',ls)
        return ls

    '''计算a模p的指数'''
    def get_aMp_exponent(self):
        gcd = self.Euclidean_gcd(self.primality, self.integer)
        if gcd != 1:
            print(f'{self.primality}与{self.integer}不互素，没有指数')
            return None

        AllFactors = self.return_AllFactors()
        for item in AllFactors:
            if self.Muldular_Repeated_Square_calMethod(self.integer, item, self.primality) == 1:
                print(f'{self.primality}模{self.integer}的指数是{item}')
                return item

    '''
    公式：phi(n) = n * product[if p|m](1 - 1/p)
    '''
    def euler_phi(self, n: int) -> int:
        m = int(sqrt(n + 0.5))
        ans = n
        for i in range(2, m + 1):
            if (n % i == 0):
                ans = ans / i * (i - 1)
                while (n % i == 0):
                    n /= i
        if (n > 1):
            ans = ans / n * (n - 1)
        return int(ans)

    '''利用模平方方法计算余数'''
    def Muldular_Repeated_Square_calMethod(self, b: int, n: int, m: int) -> int:
        a = 1
        result = 0
        while n:
            #   temp is used to reserve n[i]
            temp = n & 1
            #   if temp equals one, a[i] = (a[i-1] * b[i]) mod m
            if temp:
                a = (a * b) % m
            #   else a[i] stays the same, no operations
            result = a
            #   b[i] = b[i-1]^2 mod m
            b = b ** 2 % m
            n >>= 1
        return result

    '''Step 1: 求出第一个最小的原根'''
    def find_theMinestRoot(self) -> int:
        exponent = self.return_exponent()
        flag = False
        g = 1
        while not flag:
            g += 1
            flag = True
            for item in exponent:
                if self.Muldular_Repeated_Square_calMethod(g, item, self.primality) == 1:
                    flag = False
                    break
        return g

    '''Step 2: 得到原根的总数'''
    def return_theNumberof_primaryRoot(self):
        return self.euler_phi(self.euler_phi(self.primality))

    '''利用广义欧几里得求出最大公因数'''
    def Euclidean_gcd(self, a: int, b: int) -> int:
        if b > a:
            temp = a
            a = b
            b = temp
        r = b
        while r:
            r = a % b
            a = b
            b = r
        return a

    '''得到简化剩余系'''
    def return_simpleResidualClass(self) -> list:
        number = self.euler_phi(self.primality)
        ls = []
        for i in range(1, number):
            if self.Euclidean_gcd(i, number) == 1:
                ls.append(i)
        return ls

    '''返回g的指数的list'''
    def return_exponent(self) -> list:
        ls = []
        number = self.euler_phi(self.primality)
        for i in range(2, number):
            if number % i == 0:
                ls.append(int((self.primality - 1) / i))
                while number % i == 0:
                    number /= i
        return ls

    '''Step 3: 返回所有的原根'''
    def return_AllPrimaryRoot(self) -> list:
        global time1, time2
        simpleClss = self.return_simpleResidualClass()
        ls = []
        minestRoot = self.find_theMinestRoot()
        print(f'找到一个原根{minestRoot}')
        for item in simpleClss:
            ls.append(self.Muldular_Repeated_Square_calMethod(minestRoot, item, self.primality))
        time1 = time.time()
        print(f'Step 1,2,3花费的时间为{time1 - starttime}秒')
        return ls

    def Method1(self):
        global time1, time2
        number = self.return_theNumberof_primaryRoot()
        count = 0
        exponent = self.return_exponent()
        g = 1
        while count != number:
            g += 1
            count += 1
            for item in exponent:
                if self.Muldular_Repeated_Square_calMethod(g, item, self.primality) == 1:
                    count -= 1
                    break
        time2 = time.time()
        print(f'Step 1花费的时间为{time2 - time1}秒')


if __name__=='__main__':
    starttime = time.time()
    S = Solution(837379, 5)    #(2847379, 5) (837379, 5)
    S.get_aMp_exponent()
    print(S.return_AllPrimaryRoot()[0:10])
    S.Method1()

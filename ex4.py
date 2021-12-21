import argparse
import random

class Solution:
    #   Using Euclidean algorithm to work out the result of gcd(a,b)
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

    def Fermat_detection(self, N: int):
        index = 0
        while index < args.K:
            random_number = random.randint(1, N-1)
            index += 1
            factor = self.Euclidean_gcd(N, random_number)
            reminder = self.Muldular_Repeated_Square_calMethod(random_number, N - 1, N)
            if factor > 1 or reminder != 1:
                print(f'{N} is not a primality.')
                return None
        likelihood = 1 - (1/2) ** args.K
        print(f'We have {likelihood}% to ensure this number is a primarity.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fermat Primality Detection Algorithm.')
    parser.add_argument('N', type=int, default=None, help='The primality that you need to detect.')
    parser.add_argument('K', type=int, default=10, help='iteration count.')
    parser.add_argument('-F', '--FermatDetection', help='Use Fermat-Detection to judge.',
                        action='store_true')
    args = parser.parse_args()

    print(args)

    if args.FermatDetection:
        solution = Solution()
        solution.Fermat_detection(args.N)


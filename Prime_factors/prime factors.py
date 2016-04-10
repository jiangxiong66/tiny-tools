import random

class Factor(object):
    def __init__(self, randLoops = 20, randSeed = 0):
        self.randLoops = randLoops
        random.seed(randSeed)

    def isPrime(self, n):
        return self.Miller_Rabin(n)

    def getOneFactor(self, n):
        if n < 2:
            return n
        if self.isPrime(n):
            return n
        p = n
        while p >= n:
            p = self.Pollard_rho(p, random.randint(1,n-1))
        return self.getOneFactor(p)
    
    def getAllFactors(self, n):
        if n < 2:
            return [n]
        ans = []
        self.findfac(n, ans)
        return ans

    def mult_mod(self, a, b, c):
        a = a % c
        b = b % c
        ret = 0
        while b:
            if b & 1:
                ret = ret + a
                ret = ret % c
            a= a << 1
            if a >= c:
                a= a % c
            b = b >> 1
        return ret
    
    def pow_mod(self, x, n, mod):
        if n == 1:
            return x % mod
        x = x % mod
        tmp = x
        ret = 1
        while n:
            if n & 1:
                ret = self.mult_mod(ret,tmp,mod)
            tmp = self.mult_mod(tmp,tmp,mod)
            n= n >> 1
        return ret

    def check(self, a, n, x, t):
        ret = self.pow_mod(a,x,n)
        last = ret
        for i in range(1, t+1):
            ret = self.mult_mod(ret,ret,n)
            if ret==1 and last!=1 and last!=n-1:
                return True
            last=ret
        if ret != 1:
            return True
        else:
            return False

    def Miller_Rabin(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if (n & 1) == 0:
            return False
        x = n-1
        t = 0
        while (x & 1) == 0:
            x = x >> 1
            t = t + 1
        for i in range(self.randLoops):
            a = random.randint(1, n-1)
            if self.check(a,n,x,t):
                return False
        return True

    def gcd(self, a, b):
        if a == 0:
            return 1
        if a < 0:
            return self.gcd(-a,b)
        while b:
            t = a % b
            a = b
            b = t
        return a

    def Pollard_rho(self, x, c):
        i = 1
        k = 2
        x0 = random.randint(0, x-1);
        y = x0
        while True:
            i = i + 1
            x0 = (self.mult_mod(x0,x0,x) + c) % x
            d = self.gcd(y-x0,x)
            if d!=1 and d!=x:
                return d
            if y == x0:
                return x;
            if i == k:
                y = x0
                k = k + k

    def findfac(self, n, factors):
        if self.isPrime(n):
            factors.append(n)
            return
        p = n
        while p >= n:
            p = self.Pollard_rho(p, random.randint(1,n-1))
        self.findfac(p, factors)
        self.findfac(n/p, factors)

def testFactor(x):
    f = Factor()
    if f.isPrime(x):
        print "%d is prime." % (x)
    else:
        print "%d is not prime." % (x)
    print "%d is a prime factor of %d" % (f.getOneFactor(x), x)
    ans = f.getAllFactors(x)
    for factor in ans:
        print "%d " % (factor),
    print
    print

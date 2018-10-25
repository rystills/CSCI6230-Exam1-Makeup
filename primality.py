import random

k = 100

"""miller-robin primality check
@param n: the number to test for primality
@returns: whether the miller-robin primality check yielded true or false
"""
def millerRobin(n):
    """main test component of the primality check; performed k times
    @param d: the value calculated in step 3 st d*2^r = n-1
    """
    def millerTest(d):
        """calculate modular exponentiation of (x^y)%p
        @param x: copy of a
        @param y: copy of d
        @param p: copy of n
        """
        def power(x,y,p):
            res = 1 #Initialize result
            #Update x if it is more than or equal to p
            x = x % p;
            while (y > 0):
                #If y is odd, multiply x with result
                if ((y & 1) == 1):
                    res = (res * x) % p

                #y must be even now
                y = y >> 1; # y = y/2
                x = (x * x) % p
            return res
        
        #Pick a random number in [2..n-2]
        #Corner cases make sure that n > 4
        a = 2 + int((random.random() % (n - 4)))
      
        #Compute a^d % n
        x = power(a, d, n)
      
        if (x == 1 or x == n - 1):
            return True
      
        #Keep squaring x while one of the following doesn't happen
        #(i) d does not reach n-1
        #(ii) (x^2) % n is not 1
        #(iii) (x^2) % n is not n-1
        while (d != n - 1):
            x = x**2 % n
            d *= 2
          
            if (x == 1):
                return False
            if (x == n - 1):
                return True
      
        #Return composite
        return False
    
    #1. base case: small #'s
    if (n <= 3):
        return True if n > 1 else False
    
    #2. base case: even #'s
    if (n%2 == 0):
        return False
    
    #3. search for value d*2^r = n-1
    d = n - 1 
    while (d % 2 == 0): 
        d //= 2 
    
    #4. apply miller test k times
    for _ in range(k):
        if (not millerTest(d)):
            return False
    return True

"""pollard-rho factorization algorithm
@param n: the number to factorize
@returns: a factor of n or None, if no such factor was discovered
"""
def pollardRho(n):
    """hard-coded polynomial; here we use (x^2+1)%n
    @param v: the value to run through the polynomial
    @returns: the result of applying v to g
    """
    def g(v):
        return (v**2+1)%n
    
    """calculate the greatest common divisor of two numbers
    @param a: the first number
    @param b: the second number
    @returns: the greatest common divisor of a and b
    """
    def gcd(a, b):
        while b:
            a, b = b, a%b
        return a

    x = 2
    y = 2
    d = 1
    while (d == 1):
        x = g(x)
        y = g(g(y))
        d = gcd(abs(x - y), n)
    return None if (d == n) else d

def main():
    ints = [31531, 520482, 485827]
    for i in ints:
        mr = millerRobin(i)
        print("{0} is {1}prime".format(i,"" if mr else "not "))
        if (not mr):
            print("{0} factored is {1}".format(i,pollardRho(i)))

if __name__ == "__main__":
    main()
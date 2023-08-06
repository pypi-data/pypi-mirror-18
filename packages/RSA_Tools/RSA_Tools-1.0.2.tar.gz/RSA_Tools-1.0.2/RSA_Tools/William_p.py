#! /usr/bin/env python
#-*- encoding: utf-8 -*-
import time
from inverse_mod import inverse_mod
'''
larmod（a，b，c）计算的是a的b次方模c
gcd（a，b）计算的是a和b的公因数
'''
def largemod(a,b,c):
    list=[]
    for i in range(2000):
        if(b%2==0):
            list.append(0)
        else:
            list.append(1)
        b>>=1
        if(b==0):
            break
    #print list
    y=a%c
    z=len(list)-1
    ran=len(list)
    for i in range(ran-1):
        z=z-1
        if(list[z]):
            y=(y*y)*a%c
        else:
            y=(y*y)%c
    return y
################################################################

#算最大公约数：
def gcd(a,b):
    if a%b == 0:
        return b
    else :
        return gcd(b,a%b)


def William_alg(L,n,N):
    d = L[:]
    if(n==1):
        return L
    else:
        for i in range(1,n):
            d = [(d[0]*L[0]+21*d[1]*L[1])%N,(d[0]*L[1]+d[1]*L[0])%N]
    return d
def William_p(N,num = 200):
    L_0 = [5, 1]
    L_1 = [5, -1]

    d_0 = L_0[:]
    d_1 = L_1[:]
    x = 2
    for i in range(1, num):
        d_0 = William_alg(d_0, i, N)
        d_1 = William_alg(d_1, i, N)
        x = largemod(x, i, N)
        inv = inverse_mod(x, N)
        gg = (((d_0[0] + d_1[0]) % N) * inv) % N
        if(gcd(gg - 2, N) != 1):
            xx = gcd(gg-2,N)
            print('************success***********')
            print('the prime is %d'%gcd(gg - 2, N))
            break
        else:
            pass
    return xx



if __name__ == '__main__':
    start = time.time()
    print(William_p(13*19))
    print('William p+1 Algorithm ends with %s s'%(time.time()-start))
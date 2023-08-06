#! /usr/bin/env python
#-*- encoding: utf-8 -*-
import time

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
        b >>= 1
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
def gcd(a, b):
    if a == 0:
        return b
    r = b % a
    return gcd(r, a)

#Pollard_p函数默认最大算到2的十万的阶乘，你也可以自己更改

def Pollard_p(N,num = 100000):
    x = largemod(2,N,N)
    for i in range(1,num):
        x = largemod(x,i,N)
        if(gcd(x-1,N)!=1):
            xx = gcd(x-1,N)
            print('*****success*********')
            print('The prime is %d'%(gcd(x-1,N)))

            break
        else:
            pass

    return xx

if __name__ == '__main__':
    start = time.time()
    #计算一个1024bit的数的因子
    Pollard_p(0x808627CED38A980D765454AC5DFEFC10195F6FEF9B35B52B742DBCE2419C34080A3EF3E9673FEA4DD629FF382155031EA6DCBA8372D42C1862F32B2BEE47E157FA7150C544635035F366F7D68234F56FA24180EB6A00A0F85C65AAEB455B8ED28F2285376CDA786F8C658CFEB3752F3504A7256EA3DBD22EEF20267D156FAB51)
    print('Pollard p-1 Algorithm ends with %s s'%(time.time()-start))


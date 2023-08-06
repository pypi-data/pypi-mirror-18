#! /usr/bin/env python
#-*- encoding: utf-8 -*-
from math import sqrt

def Fermat_alg(N, num = 1000):
    for i in range(1,num):
        ss = (int)(sqrt(N)) + i
        # print(ss)
        ee = ss**2 - N
        # print(ee)
        sqrt_ee = (int)(sqrt(ee))
        if (sqrt_ee ** 2 == ee):
            xx = (int)(sqrt(ee))
            print('**********success**********')
            print('the prime is %d' % (int)(ss-(int)(sqrt(ee))))
            break
        else:
            pass
    return xx

if __name__ == '__main__':
    Fermat_alg(65535*65547)
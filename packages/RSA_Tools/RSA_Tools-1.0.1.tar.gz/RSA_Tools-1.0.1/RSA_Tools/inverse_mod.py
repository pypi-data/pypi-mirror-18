#! /usr/bin/env python
#-*- encoding: utf-8 -*-

def gcd(a, b):
    if a == 0:
        return b
    r = b % a
    return gcd(r, a)

def extended_gcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return b, x0, y0


def print_extended_gcd(a, x, b, y, g):
    print("(%d)(%d) + (%d)(%d) = %d" % (a, x, b, y, g))


# Prints the modular inverse of a,b both ways:
def print_inverse_mod(a, b):
    if gcd(a, b) == 1:
        print("a^-1 mod b = " + str(mod_inverse(a, b)))


# Finds the modular multiplicative inverse using the reverse Euclidean algo.
def inverse_mod(b, n):
    g, x, ignore = extended_gcd(b, n)
    if g == 1:
        return x % n


if __name__ == '__main__':
    print(inverse_mod(4,5))


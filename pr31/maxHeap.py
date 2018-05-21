import os
import sys
import math

def maxheap(list, root):
    if 2*root+1 < len(list):
        k = 2*root+2 if 2*root+2 < len(list) and list[2*root+2] > list[2*root+1] else 2*root+1     #让k成为较小的子节点的index
        if list[root] < list[k]:
            (list[root],list[k]) = (list[k],list[root])     #交换值
            maxheap(list,k)              #对子节点为根节点的子树建堆

def beginMin(a, b):
    for i in range(len(a)//2-1,-1,-1):
        maxheap(a, i)
    for i in b:
        if i < a[0]:
            a[0] = i
            maxheap(a, 0)

def e_maxHeap(list, root):
    if 2*root+1 < len(list):
        k = 2*root+2 if 2*root+2 < len(list) and list[2*root+2] > list[2*root+1] else 2*root+1     #让k成为较小的子节点的index
        if list[root] < list[k]:
            (list[root],list[k]) = (list[k],list[root])     #交换值
            maxheap(list,k)              #对子节点为根节点的子树建堆

def beginMin(a, b):
    for i in range(len(a)//2-1,-1,-1):
        maxheap(a, i)
    for i in b:
        if i < a[0]:
            a[0] = i
            maxheap(a, 0)

if __name__ == "__main__":
    a = [49, 38, 65, 97, 76, 13, 27]
    b = [101, 100, 24, 7, 8, 9, 50, 1, 2, 3, 4, 999, 6]
    beginMin(a, b)
    print(a)

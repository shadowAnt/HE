import os
import sys
import math

def heap(list):
    n = len(list)
    for i in range(0,int(math.log(n,2))):                #每循环依次就完成了一层的建堆
        for j in range(0,n//2):
            k = 2*j+2 if 2*j+2 < n and list[2*j+2] < list[2*j+1] else 2*j+1    #让k成为较小的子节点的index
            if list[j] > list[k]:
                (list[j],list[k]) = (list[k],list[j])         #交换值

def sink(list, root):
    '''
    从最后一个拥有子节点的节点向上遍历，使用下沉算法将遍历到的每一个子树变成二叉堆。最终整个二叉树就成为一个二叉堆
    :param list:
    :param root:
    :return:
    '''
    if 2*root+1 < len(list):
        k = 2*root+2 if 2*root+2 < len(list) and list[2*root+2] < list[2*root+1] else 2*root+1     #让k成为较小的子节点的index
        if list[root] > list[k]:
            (list[root],list[k]) = (list[k],list[root])     #交换值
            sink(list,k)              #对子节点为根节点的子树建堆

def begin(a):
    for i in range(len(a)//2-1,-1,-1):
        sink(a, i)

def findWhere(a, b):
    '''
    a是b的子集，返回a中元素在b中的位置
    :param a:
    :param b:
    :return:
    '''
    alen = len(a)
    blen = len(b)
    ind = []
    for i in range(alen):
       for j in range(blen):
           if a[i] == b[j]:
                ind.append(j)
                break
    return ind

def mink(list, root):
    if 2*root+1 < len(list):
        k = 2*root+2 if 2*root+2 < len(list) and list[2*root+2] > list[2*root+1] else 2*root+1     #让k成为较小的子节点的index
        if list[root] < list[k]:
            (list[root],list[k]) = (list[k],list[root])     #交换值
            mink(list,k)              #对子节点为根节点的子树建堆

def beginMin(a):
    for i in range(len(a)//2-1,-1,-1):
        mink(a, i)

if __name__ == "__main__":
    # a = [49, 38, 65, 97, 76, 13, 27]
    # b = [101, 100, 24,7,8,9, 50,1,2,3,4,999,6]
    # begin(a)
    # for i in b:
    #     if i > a[0]:
    #         a[0] = i
    #         sink(a, 0)
    # print(a)
    a = [49, 38, 65, 97, 76, 13, 27]
    b = [101, 100, 24, 7, 8, 9, 50, 1, 2, 3, 4, 999, 6]
    beginMin(a)
    for i in b:
        if i < a[0]:
            a[0] = i
            mink(a, 0)
    print(a)

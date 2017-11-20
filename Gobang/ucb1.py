from math import *
from random import *

#设置赌博机
node={1:[1,2,3,4,9],2:[2,3,4,5,6],3:[3,5,6,2,7],4:[9,1,1,2,6]}
#ucb记录数据
ucbNode={}
def usb1():
    for key,value in node.items():
        ucbNode[key]=[1,choice(value)]

    for i in range(0,10000):
        totalCount=sum(value[0] for key,value in ucbNode.items())
        bonus,key=max(
            (value[1]/value[0]+sqrt(2*log(totalCount)/value[0])
            ,key) 
            for key,value in ucbNode.items())
        ucbNode[key][0]+=1
        ucbNode[key][1]+=choice(value)
        print(i,key,ucbNode[key][0],ucbNode[key][1])
        
usb1()
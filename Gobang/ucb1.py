'''
这是一个ucb1算法的实现
处理的是多臂赌博机问题
拉一次拉杆，获得一个随机数，然后更新节点
'''
from math import *
from random import *
#臂杆节点
#id:[count,value]
ucbNode={}
#生成一组未初始化node节点id
nodeList=list(range(0,10))

#选择
def select_arm():
    #如果全部选择过了
    if len(nodeList)==0:
        totalCount=sum(value[0] for key,value in ucbNode.items())
        bonus,id=max(
            #
            (value[1]/value[0]+sqrt(2 * log(totalCount) / value[0])
            ,key) 
            for key,value in ucbNode.items())
        return id
    else:
        #随机出来一个节点
        id=choice(nodeList)
        #清除一个节点
        nodeList.remove(id)
        return id
#模拟
def simulation(id):
    return uniform(0,id)

#反向更新节点
def update(id,value):
    if id not in ucbNode:
        ucbNode[id]=[1,value]
    else:
        ucbNode[id][0]+=1
        ucbNode[id][1]+=value


def ucb():
    for _ in range(0,1000):
        #选择
        id=select_arm()
        #模拟
        value=simulation(id)
        #反向更新
        update(id,value)
        print(id,"  ",ucbNode[id][0],"  ",ucbNode[id][1])
    #训练结果
    id=select_arm()
    print(id)

ucb()




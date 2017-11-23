'''
mcst
一个mcst树树状结构
          1
      2        3
    4   5    6    7
这是为了理解mcst而写的一个例子
到达一关需要roll点，
大于某个值的话可以继续深入，
求那条路径最容易通过
'''
from math import *
from random import *

#节点
class node(object):
    def __init__(self,id,roll):
        self.id=id
        self.roll=roll
        self.c=0
        self.v=0
        self.pe=None
        self.nt=None
    def peNode(self,pe):
        self.pe=pe
    def ntNodes(self,nt):
        self.nt=nt
    def addCount(self):
        self.c+=1
    def subCount(self):
        self.c-=1
    def visit(self):
        self.v=1

    
#尝试找出一个结果，保存这个树
#如果所有子节点都在树上，就进行选择一直到产生结果
#例如 1-2.3都有数据则需要根据max取值，但是此时还没有结果，需要继续寻找下一个节点
def simTree(node):
    # #这里是递归调用
    # #如果到达叶子节点了
    # if node.nt is None:
    #     return node,True
    # #如果都访问过了
    # elif all(n.v for n in node.nt):
    #     #贪婪算法在这里不适合
    #     chose=max(node.nt , key=lambda x: x.c)
    # else:
    #     #扩展出来一个新的节点，进行访问
    #     ns = list(filter(lambda x: x.v==0,node.nt))
    #     chose=choice(ns)
    #     #标记节点
    #     chose.visit()
    #     #模拟是否结束
    #     #未结束则寻找下一个节点
    # if(not chose.nt is None and simulation(chose)):
    #     return select_arm(chose)
    # return chose,False
    while not node.nt is None:
        if all(n.v for n in node.nt):
            #贪婪算法在这里不适合
           chose=max(node.nt , key=lambda x: x.c)
        else:
            ns=list(filter(lambda x: x.v==0,node.nt))
            chose=choice(ns)
            #标记节点
            chose.visit()
        #如果中途结束了
        if simulation(chose)==False:
            return chose,False
    return chose,simulation(chose)

    
#模拟,获得结果
def simulation(node):
    #如果是叶子节点，获得结果
    if node.nt is None:
        v=choice(node.roll)>5
        # print("none " ,v)
        return v
    else:
        #判断结果，如果可以，则模拟节点
        v=choice(node.roll)<=5
        # print("node " ,v)
        if v:
            return False
        else:
            return True
    

#反向更新节点
def update(subNode,value):
    if value==True :
        subNode.addCount()
    else:
        subNode.subCount()
    if not subNode.pe is None:
            update(subNode.pe,value)
        

#simulate模拟算法
def mcst(node):
    #构建访问信息节点
    #print("正在访问节点: " , node.id)
    for _ in range(0,100):
        #决策树
        #目前设计的是分为两个阶段，
        #第一阶段是模拟数据，产生基础值
        #第二阶段是根据数据产生决策并更新树
        #这棵树可以自己扩展，自己模拟
        #并根据数据决策选择的节点
        subNode,value=simTree(node)
        print("模拟节点：",subNode.id)
        #更新
        update(subNode,value)
        print("获得模拟结果2：",value)
        #print("正在反向更新节点:" , subNode.id , value)
    #if not node.nt is None:
    #    k,v=max((n.c , n.id) for n in node.nt)
    #   print(node.id,"选择节点：",v)



node1=node(1,[1,6,9])
node2=node(2,[8,2,8])
node3=node(3,[3,4,9])

node1.ntNodes([node2,node3])
node2.peNode(node1)
node3.peNode(node1)

node4=node(4,[3,5,2])
node5=node(5,[8,2,6])

node2.ntNodes([node4,node5])
node3.peNode(node2)
node4.peNode(node2)

node6=node(6,[5,5,8])
node7=node(7,[1,1,2])

node3.ntNodes([node6,node7])
node6.peNode(node3)
node7.peNode(node3)

mcst(node1)

#寻找树的节点
def find(node):
    print("find: ",node.id)
    if not node.nt is None:
        v=max(node.nt,key=lambda x: x.c)
        find(v)
find(node1)




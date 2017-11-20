'''
mcst
一个mcst树，使用随机来进行模拟
一般来说mcst的每层节点应该是独立的，即树状结构
          1
      2        3
    4   5    6    7
这样的结构，各个节点是相互独立的
还有不独立的，这里不做讨论
'''
from math import *
from random import *

#节点
class node:
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
    def visit(self):
        self.v=1

    
#选择
def select_arm(node):
    #如果到达叶子节点了
    if node.nt is None:
        return node
    #如果都访问过了
    elif all(n.v for n in node.nt):
        return max(node.nt , key=lambda x: x.c)
    else:
        #扩展出来一个新的节点，进行访问
        chose=choice(node.nt)
        #标记节点
        chose.visit()
        return chose
#模拟
def simulation(node):
    #如果是叶子节点，获得结果
    if node.nt is None:
        return choice(node.roll)>5
    else:
        #判断结果，如果可以，则模拟节点
        if choice(node.roll)<=5:
            return False
        else:
            return mcst(node)
    

#反向更新节点
def update(subNode,value):
    if value :
        subNode.addCount()
        if not subNode.pe is None:
            update(subNode.pe,value)


def mcst(node):
    #构建访问信息节点
    #print("正在访问节点: " , node.id)
    for _ in range(0,1000):
        #选择
        subNode=select_arm(node)
        #模拟
        value=simulation(subNode)
        #反向更新
        update(subNode,value)
        #print("正在反向更新节点:" , subNode.id , value)
    #if not node.nt is None:
    #    k,v=max((n.c , n.id) for n in node.nt)
    #   print(node.id,"选择节点：",v)



node1=node(1,[1,6,9])
node2=node(2,[2,8,8])
node3=node(3,[3,4,9])

node1.ntNodes([node2,node3])
node2.peNode(node1)
node3.peNode(node1)

node4=node(4,[6,5,8])
node5=node(5,[4,7,3])

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




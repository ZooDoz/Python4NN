import board
import time
import copy
from math import log
from random import choice
from math import *

"""
Rapid Action Value Estimation
rave
快速行动价值评估
amaf值 
对于棋类来说，所有的子节点是平等的
all_moves_as_first 
选择节点，模拟，更新选择和模拟的节点
(模拟的节点构成一棵树，
如果更新到某个模拟的节点，这个节点如果和第一个节点颜色一致且发现是一个树，
那么把这棵树当作新的更新)

mc值 访问某节点次数
amaf值 访问某节点的次数+访问别的节点的时候，后续访问到该节点的次数
"""
class amaf(object):
    """
    完全随机模拟
    """
    def simulation(self,board,play_turn):
        node=[]
        for _ in range(1, len(board.availables) + 1):
            move=choice(board.availables)
            player=board.get_player(play_turn)
            board.update(player,move)
            node.append(move)
            #胜利
            win,winner = board.has_a_winner(board)
            if win:
                return win,winner,node
        #如果没有结果也算失败
        return False,-1,node
    
    '''
    进行uct算法
    '''
    def get_action(self,board,play_turn):

        # 棋盘只剩最后一个落子位置，直接返回
        if(len(board.availables)==1):
            return board.availables[0]

        simulations=0
        begin=time.time()
        #节点树信息
        node={}
        c_p=play_turn[0]


        while time.time()-begin<float(10) and simulations<10000:
             # 模拟会修改board的参数，所以必须进行深拷贝，与原board进行隔离
            board_copy=copy.deepcopy(board)
            # 每次模拟都必须按照固定的顺序进行，所以进行深拷贝防止顺序被修改
            play_turn_copy=copy.deepcopy(play_turn)
            # 进行UCT
            #决策树判断一组数据
            win,winner,n,sn=self.simTree(board_copy,play_turn_copy,node,len(board.availables),c_p)
            #反向更新节点
            self.update(node,n,sn,win,winner,c_p)
            #记录次数
            simulations+=1
            print("模拟次数：",simulations,win,winner)
      

        #获取ucb最大的节点
        bonus,move=max(
            (self.eval(value),key) for key,value in node.items())
        print("模拟次数：", simulations)
        location=board.move_to_location(move)
        print("Ai move: %d,%d\n" % (location[0],location[1]))
        return move

    def eval(self,node):
        return (node[1]+node[3])/(node[0]+node[2])
    '''

    模拟树
    '''
    def simTree(self,board,play_turn,node,l,c_p):
        #每次决策树都是在剩余的子里选
        #记录每次选择出来的节点树
        # print(len(node),l)
        #树上找到的节点
        n=[]
        #模拟出来的节点
        sn=[]

        ns=list(node.keys())
        #当前剩余可走位置
        #提出已经有信息的节点
        availables=list(filter(lambda x: x not in node or node[x][0]==0,board.availables))
        # print(availables)
        # print(len(availables))
        for _ in range(1, len(board.availables) + 1):
            #因为围棋比较特殊，所有剩余位置均为子节点,
            #所以需要所有位置均有信息才可能进行uct
            #即经过模拟后
            if len(availables)==0:
                #获取当前出手玩家
                player=board.get_player(play_turn)
                #遍历剩余节点
                #如果是当前玩家取胜率最大
                if c_p==player:
                    #ubc1公式
                    bonus,move=max(
                        (self.eval(node[key]),key) for key in board.availables)
                    # print(c_p,player,"win",move)
                else:
                    bonus,move=min(
                        (self.eval(node[key]),key) for key in board.availables)
                    # print(c_p,player,"win",move)
                #记录选出来的模拟节点
                n.append(move)
                #消除记录里的点
                ns.remove(move)
                #更新棋盘
                board.update(player,move)
                #胜利
                win,winner = board.has_a_winner(board)
                if win:
                    return win,winner,n,sn
            else:
                #需要扩展的节点
                move=choice(availables)
                player=board.get_player(play_turn)
                board.update(player,move)
                #记录选出来的模拟节点
                n.append(move)
                #该节点无数据
                win,winner,sn=self.simulation(board,play_turn)
                return win,winner,n,sn
        return False,-1,n,sn

    def update(self,node,n,sn,win,winer,c_p):
        if win and winer==c_p:
            w=1
        else:
            w=-1
        
        #寻找到的节点
        alln = copy.deepcopy(n)
        #随机模拟的节点
        alln.extend(copy.deepcopy(sn))
        # print(alln)
        #更新所有搜索到的节点
        for t in range(len(alln)):
            if node.get(alln[t]) is None:
                node[alln[t]]=[0,0,0,0]
            node.get(alln[t],[0,0,0,0])[0]+=1
            node.get(alln[t],[0,0,0,0])[1]+=w
            if t>0:
                node.get(alln[t],[0,0,0,0])[2]+=1
                node.get(alln[t],[0,0,0,0])[3]+=w


        
    


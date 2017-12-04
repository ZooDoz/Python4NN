import board
import time
import copy
from math import log
from random import choice
from math import *

"""
算法设计是为了解决棋类问题的双人全信息博弈问题
这里的默认策略是随机策略
这种办法是先对所有点进行随机产生节点的胜利数据
然后每一步都根据胜利数据进行ucb1
我最开始想的是先对所有点进行随机产生节点胜利数据
然后第一步的节点利用ucb1，然后在随机
仅更新了第一步的节点的数据
这样的算法很笨

"""
class uct(object):

    """
    随机模拟，用于基础信息的产生
    """
    def simulation(self,board,play_turn):
        for _ in range(1, len(board.availables) + 1):
            move=choice(board.availables)
            player=board.get_player(play_turn)
            board.update(player,move)
            #胜利
            win,winner = board.has_a_winner(board)
            if win:
                return win,winner
        #如果没有结果也算失败
        return False,-1


    '''
    进行uct算法
    '''
    def get_action(self,board,play_turn):
        # 棋盘只剩最后一个落子位置，直接返回
        if(len(board.availables)==1):
            return board.availables[0]

        simulations=0
        calculation_time = float(10)
        begin=time.time()
        # key选择的节点  key节点后续某个玩家，玩家走的位置 value访问的次数，获胜的次数
        node={}
        c_p=play_turn[0]
        while time.time()-begin<calculation_time and simulations<10000:
             # 模拟会修改board的参数，所以必须进行深拷贝，与原board进行隔离
            board_copy=copy.deepcopy(board)
            # 每次模拟都必须按照固定的顺序进行，所以进行深拷贝防止顺序被修改
            play_turn_copy=copy.deepcopy(play_turn)
            # 进行UCT
            #决策树进行决策
            win,winer,c_node=self.simTree(board_copy,play_turn_copy,node,len(board.availables),c_p)
            #反向更新树
            self.update(node,c_node,win,winer,c_p)
            #记录次数
            simulations+=1
            print("模拟次数：",simulations,win,winer)

        log_total=log(sum(node[(m)][0] for m in board.availables))
        bonus,move=max(
                        (node[(m)][1]+sqrt(log_total/node[(m)][0])
                        ,m)
                        for m in board.availables)

        print("模拟次数：", simulations)
        location=board.move_to_location(move)
        print("Ai move: %d,%d\n" % (location[0],location[1]))
        return move

    '''
    选择一步最好棋
    棋盘状态，子节点状态
    '''
    def simTree(self,board,play_turn,node,l,c_p):
        #每次决策树都是在剩余的子里选
        #记录每次选择出来的节点树
        # print(len(node),l)
        n=[]
        availables=list(filter(lambda x: x not in node,board.availables))
        for _ in range(1, len(board.availables) + 1):
            #因为围棋比较特殊，所有剩余位置均为子节点,
            #所以需要所有位置均有信息才可能进行uct
            #即经过模拟后
            #获取当前出手玩家
            player=board.get_player(play_turn)
            #当前剩余没有记录位置
            if len(availables)==0:   
                #遍历剩余节点
                #对剩余节点访问次数求和然后取对数
                #即当前节点访问次数 sum(剩余节点的访问次数)=当前节点的访问次数
                #因此total(v) = sum(total(v’),for v’ in childs(v))
                log_total=log(sum(node[m][0] for m in board.availables))
                #如果是当前玩家取胜率最大
                if c_p==player:
                    #ubc1公式
                    bonus,move=max(
                        (node[m][1]+sqrt(log_total/node[m][0])
                        ,m)
                        for m in board.availables)
                    # print(c_p,player,"win",move)
                else:
                    bonus,move=min(
                        (node[m][1]-sqrt(log_total/node[m][0])
                        ,m)
                        for m in board.availables)
                    # print(c_p,player,"win",move)
                #记录选出来的模拟节点
                n.append(move)
                #更新棋盘
                board.update(player,move)
                #胜利
                win,winner = board.has_a_winner(board)
                if win:
                    return win,winner,n
            else:
                # print(len(availables),len(board.availables))
                #需要扩展的节点
                move=choice(availables)
                #更新棋盘
                board.update(player,move)
                #记录选出来的模拟节点
                n.append(move)
                #该节点无数据，需要模拟
                win,winner=self.simulation(board,play_turn)
                return win,winner,n
        return False,-1,n

    def update(self,node,c_node,win,winer,c_p):
        print(c_p,winer,c_p==winer)
        if win and c_p==winer:
            w=1
        else:
            w=-1

        for c_move in c_node:
            self.updateNode(node,c_move,w)

    def updateNode(self,node,move,w):
        if move not in node:
            node[move]=[1,w]
        else:
            node[move][0]+=1
            node[move][1]+=(w-node[move][1])/node[move][0]
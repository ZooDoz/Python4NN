import board
import time
import copy
from math import log
from random import choice
from math import *

"""

"""


class uct(object):

    #随机模拟算法
    def defaulPolicy(board):
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
    
    """
    完全随机模拟
    """
    def simDefault(self,board,play_turn,move):
        node=[]
        player=board.get_player(play_turn)
        board.update(player,move.id)
        #对当前节点进行模拟
        #采用随机算法进行模拟
    

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
        #节点树信息
        node={}
        #计算10s或者100次
        while time.time()-begin<calculation_tim:
             # 模拟会修改board的参数，所以必须进行深拷贝，与原board进行隔离
            board_copy=copy.deepcopy(board)
            # 每次模拟都必须按照固定的顺序进行，所以进行深拷贝防止顺序被修改
            play_turn_copy=copy.deepcopy(play_turn)
            # 进行UCT
            #寻找一个点
            move=self.simTree(board_copy,play_turn_copy,node)
            #模拟当前决策结果
            win,winer=self.simDefault(board_copy,play_turn_copy,move)
            #反向更新节点
            self.update(node,move,win,winer)
            #记录次数
            simulations+=1
            print("模拟次数：", move , win , winer)
      
        #对已经计算的节点进行选择
        log_total = log(sum(value[0] for key,value in node.items()))
        #获取ucb最大的节点
        bonus,move=max(
            #
            (value[1]/value[0]+sqrt(2*log_total / value[0])
            ,key) 
                for key,value in node.items())
        print("模拟次数：", simulations)
        location=board.move_to_location(move)
        print("Ai move: %d,%d\n" % (location[0],location[1]))
        return move

    '''
    模拟树
    '''
    def simTree(self,board,play_turn,node):
        #当前剩余可走位置
        availables=board.availables
        #selection
        # 如果所有着法都有统计信息，则获取UCB最大的节点
        if len(availables)==0:
            #遍历剩余节点
            #对剩余节点访问次数求和然后取对数
            #即当前节点访问次数 sum(剩余节点的访问次数)=当前节点的访问次数
            #注意：对节点的模拟同时也包括了子节点回溯上来的模拟， 
            #因此total(v) = sum(total(v’),for v’ in childs(v))
            log_total = log(sum(value[0] for key,value in node.items()))
            #获取ucb最大的节点
            bonus,move=max(
                #
                (value[1]/value[0]+sqrt(2*log_total / value[0])
                ,key)
                 for key,value in node.items())
        else:
            #需要扩展的节点
            move=choice(availables)
        return move

    def update(self,node,move,win,winer):
        if win and winer==node.player:
            w=1
        else:
            w=-1
        if move not in node:
            node[move]=[1,1]
        else:
            node[move][0]+=1
            node[move][1]+=w

        
    


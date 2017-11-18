import board
import time
import copy
from math import log
from random import choice
from math import *

"""
这是一个模仿base来实现的算法，
在理解上存在偏差，
base因为是全是叶子节点的特殊树，
这个是一个有深度的树，模拟的时候有操作别的节点
但是这个实现里面没有对模拟的时候操作的节点进行记录
例如有1 2 3 4 5 6 7 8 9个点
1已经走过了，剩余2 3 4 5 6 7 8 9
分别对剩余8个点进行随机模拟
2 - 3 4 5 6 7 8 9 - 只模拟了，没有存储子节点信息
3 - 2 4 5 6 7 8 9 - 只模拟了，没有存储子节点信息
...
算法没有记录更深层的子节点
mcts算法实现需要：模拟的时候存储和记录到更深的节点，生成一颗深度的树
2 - 3 4 5 6
7 - 5 6 4 3
8 - 9 6 3 4
应该是这样的树
"""
class mc4ucb(object):

    """
    模拟
    """
    def run_simulation(self,board,play_turn):
        #对当前节点进行模拟
        #采用随机算法进行模拟
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
        node={}
        c_p=play_turn[0]
        while time.time()-begin<calculation_time:
             # 模拟会修改board的参数，所以必须进行深拷贝，与原board进行隔离
            board_copy=copy.deepcopy(board)
            # 每次模拟都必须按照固定的顺序进行，所以进行深拷贝防止顺序被修改
            play_turn_copy=copy.deepcopy(play_turn)
            # 进行UCT
            #决策树进行决策
            move=self.select_one_move(board_copy,play_turn_copy,node)
            #模拟当前决策结果
            win,winer=self.run_simulation(board_copy,play_turn_copy)
            #反向更新节点
            self.update(node,move,win,winer,c_p)
            #记录次数
            simulations+=1
            print("模拟次数：", move , win , winer)
      
        confident=1.96
        #对已经计算的节点进行选择
        log_total = log(sum(value[0] for key,value in node.items()))
        #获取ucb最大的节点
        bonus,move=max(
            #
            (value[1]/value[0]+sqrt(confident*log_total / value[0])
            ,key) 
                for key,value in node.items())
        print("模拟次数：", simulations)
        location=board.move_to_location(move)
        print("Ai move: %d,%d\n" % (location[0],location[1]))
        return move

    '''
    选择一步最好棋
    棋盘状态，子节点状态
    '''
    def select_one_move(self,board,play_turn,node):
        #当前剩余可走位置
        availables=board.availables
        confident=1.96
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
                (value[1]/value[0]+confident*sqrt(log_total / value[0])
                ,key)
                 for key,value in node.items())
        else:
            #需要扩展的节点
            move=choice(availables)
            #从出手列表中获取出手玩家
            #把当前节点放置在棋盘上
            player=board.get_player(play_turn)
            board.update(player,move)
        return move

    def update(self,node,move,win,winer,c_p):
        if win and winer==c_p:
            w=1
        else:
            w=-1
        if move not in node:
            node[move]=[1,1]
        else:
            node[move][0]+=1
            node[move][1]+=w

        
    


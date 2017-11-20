import board
import time
import copy
from math import log
from random import choice
from math import *

"""
这是纵向扩张方法
例如有1 2 3 4 5 6 7 8 9个点
1已经走过了，剩余2 3 4 5 6 7 8 9
注意处理的是一个树上的所有节点，对深度进行了加权
第一次开始走 2 3 4 5 6 7 8 获得结果后对这颗树上的节点进行ucb处理
第二次找到 9 还没有处理从9开始 3 6 8 然后对这颗树上节点进行ucb处理
所有节点都处理过了，就可以根据ucb公式进行处理了
这应该是一个标准的mcst_uct树了
mcst+ucb
这是阅读文档后的改进版
算法设计是为了解决棋类问题的双人全信息博弈问题
这里的默认策略是随机策略
"""
class uct(object):

    """
    模拟
    """
    def run_simulation(self,board,play_turn,move):
        #对当前节点进行模拟
        #采用随机算法进行模拟
        #返回当前术的节点结构
        #从出手列表中获取出手玩家
        #把当前节点放置在棋盘上
        player=board.get_player(play_turn)
        board.update(player,move)
        node=[]
        node.append(move)
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
            move=self.select_one_move(board_copy,play_turn_copy,node,len(board.availables))
            #模拟当前决策结果
            win,winer,c_node=self.run_simulation(board_copy,play_turn_copy,move)
            #反向更新树
            self.update(node,c_node,move,win,winer,c_p)
            #记录次数
            simulations+=1
            print("模拟次数：", move , win , winer)
      
        confident=1.96
        #对已经计算的节点进行选择
        log_total = log(sum(value[0] for key,value in node.items()))
        #获取ucb最大的节点
        bonus,move=max(
            #
            (value[1]/value[0]+confident*sqrt(log_total / value[0])
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
    def select_one_move(self,board,play_turn,node,l):
        #当前剩余可走位置
        availables=board.availables
        confident=1.96
        #selection
        #因为围棋比较特殊，所有剩余位置均为子节点,
        #所以需要所有位置均有信息才可能进行uct
        #即经过模拟后
        if len(node)==l:
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
        return move

    def update(self,node,c_node,move,win,winer,c_p):
        if win and winer==c_p:
            w=1
        else:
            w=-1
        self.updateNode(node,move,2)
        #这里的反向更新有问题，因为路径是两个人的，所以胜利要区分先后
        for c_move in c_node:
            self.updateNode(node,c_move,w)

    def updateNode(self,node,move,w):
        if move not in node:
            node[move]=[1,1]
        else:
            node[move][0]+=1
            node[move][1]+=w




        
    


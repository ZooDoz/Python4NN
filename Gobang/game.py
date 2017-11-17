from human import Human
from random import shuffle
from random import *
from board import Board

class Game(object):
    """
    game server
    """

    def start(self):
        board=Board()
        board.init_board()

        if randint(1,2)==1:
            p1=1
            p2=2
        else:
            p1=2
            p2=1


        ai = Human("ai" , p1)
        human = Human("human" , p2)

        players = {}
        players[p1] = ai
        players[p2] = human

        play_turn = [p1, p2]
 
        while(1):
            player=board.get_player(play_turn);
            move = players[player].get_action(board,play_turn)
            board.update(player,move)
            self.graphic(board,human,ai)
            end, winner = self.game_end(board)
            if end:
                if winner != -1:
                    print("Game end. Winner is", players[winner])
                break



    """
    检查游戏是否结束
    """
    def game_end(self,board):

        win, winner = board.has_a_winner(board)
        if win:
            return True, winner
        elif not len(board.availables):
            print("Game end. Tie")
            return True, -1
        return False, -1

    def graphic(self, board, human, ai):
        """
        在终端绘制棋盘，显示棋局的状态
        """
        width = board.width
        height = board.height

        print("Human Player", human.type, "with X".rjust(3))
        print("AI    Player", ai.type, "with O".rjust(3))
        print()
        for x in range(width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                if board.states[loc] == human.player:
                    print('X'.center(8), end='')
                elif board.states[loc] == ai.player:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')

game=Game()
game.start()

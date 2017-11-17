from mcts4UCT import mcts4uct as MCTS

class Human(object):
    """
    human player
    """
    def __init__(self,type,player):
        self.type=type
        self.player=player

    def get_action(self,board,play_turn):
        
        print(self.type)
        if self.type=="human":
            try:
                location = [int(n, 10) for n in input("Your move: ").split(",")]
                move = board.location_to_move(location)
            except Exception as e:
                move = -1
            if move == -1 or move not in board.availables:
                print("invalid move")
                move = self.get_action(board,play_turn)
            return move
        else:
            ai=MCTS()
            move=ai.get_action(board,play_turn)
            return move

'''这是一张棋盘'''
class Board(object):
    '''
    board for game
    '''
    '''构造函数'''
    def __init__(self,width=6,height=6,n_in_row=4):
        self.width=width
        self.height=height
        # 记录当前棋盘的状态，键是位置，值是棋子，这里用玩家来表示棋子类型
        self.states={}
        self.n_in_row=n_in_row

    '''初始化棋盘'''
    def init_board(self):
        # 表示棋盘上所有合法的位置，这里简单的认为空的位置即合法
        self.availables=list(range(self.width * self.height))
        for m in self.availables:
            # -1表示当前位置为空
            self.states[m]=-1;

    '''move 一维长度转换为二维坐标'''
    def move_to_location(self,move):
        #除数为行
        h=move//self.width
        #余数为列
        w=move%self.width
        #坐标
        return [h,w]

    '''将二维位置转换为一维move'''
    def location_to_move(self,location):
        if(len(location)!=2):
            return -1
        h=location[0]
        w=location[1]
        move=h*self.width+w
        if(move >= self.width*self.height):
            return -1
        return move

    '''
    更新坐标点的玩家，
    同时在空白列表中清除该点
    '''
    def update(self,player,move):
        self.states[move]=player
        self.availables.remove(move)

    '''
    获取当前棋手
    队列方式，
    执行完后放在队尾
    '''
    def get_player(self, players):
        #推出当前player
        p = players.pop(0)
        #把玩家放在队尾
        players.append(p)
        return p

    '''
    判断是否获胜
    返回获胜者
    '''
    def has_a_winner(self, board):
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        if(len(moved) < self.n_in_row + 2):
            return False, -1

        width = board.width
        height = board.height
        states = board.states
        n = self.n_in_row
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            #仅从第一列开始判断到获胜最小的列
            #例如总共8列，只用判断1234列就可以得到结果
            if (w in range(width - n + 1) and
                len(set(states[i] for i in range(m, m + n))) == 1): # 横向连成一线
                return True, player
            #仅从第一行开始判断到获胜最小的行
            #例如总共8行，只用判断1234行就可以得到结果
            if (h in range(height - n + 1) and
                len(set(states[i] for i in range(m, m + n * width, width))) == 1): # 竖向连成一线
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                len(set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1): # 右斜向上连成一线
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                len(set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1): # 左斜向下连成一线
                return True, player

        return False, -1
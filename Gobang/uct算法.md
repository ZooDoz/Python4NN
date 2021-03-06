一、建模

1. 玩家：

用1和2表示。

2. 状态集S：

合法棋局的集合，两个棋局相等当且仅当： 
a)两个棋局盘面完全一致。 
b)两个棋局的下一落子者相同。 
状态集的元素用s表示。

3. 后继关系：

设s, s’∈S，(s’,s)在后继关系中，当且仅当s’经过某一步合法落子可以达到s，简称为s为s’的后继。

4. 完全博弈树T和映射m：

T = (V,E)， m: V→S。T和S利用归纳定义构造： 
a)构建v0，令m(v0)为S的初始状态，令v0∈V，令v0的父节点为空 
b)设v∈V，对m(v)所有的后继s’，构建节点v’，令m(v’) = s’，令v’∈T，令v’的父节点为v。根据先手，可构造出两棵不同的完全博弈树T1和T2，分别对应玩家1先手和玩家2先手。 
显然： 
a)叶节点代表分出胜负或和的状态，一条从根节点到叶节点的路径代表一个合法的落子过程。 
b)m不是单射，但m为满射。

5. 博弈树：

如果完全博弈树的某个子图T’也为一棵树，则称T’为博弈树。显然，完全博弈树为博弈树。

6. 主路径：

博弈树T’的一条从根节点到叶节点的路径P。P代表棋局的进程。

7. 终结点：

若v∈T，且m(V)已分出胜负或和，则称v为终结点。显然v为终结点等价于v为T中的叶节点。

8. 全拓展节点：

若v∈T’，并且v在T’中的所有子节点与v在T中的所有子节点一致，则称v为全拓展节点。

9. 拓展：

若v∈T’，并且v非全拓展节点，则向v加入子节点v’的过程称为拓展。对v经过若干次拓展，v会变成全拓展节点。

10. 节点参数：

根据完全博弈树的定义，每个节点都有参数m，m(v)返回的是节点对应的棋盘状态。 
其他的参数有： 
parent，记录节点的父亲。 
childs，记录节点的孩子。 
total，记录节点总的模拟次数。 
win、lose，记录节点模拟中胜利次数、失败的次数。 
注意：对节点的模拟同时也包括了子节点回溯上来的模拟， 
因此total(v) = sum(total(v’),for v’ in childs(v))。对win和lose参数也有类似关系。

二、算法

采用UCT算法。 
由于T规模很大，不可能直接构建完全博弈树T，因此构建T的子树T’（博弈树）。 
T’在算法的过程中会逐渐拓展，T’的主路径P代表棋局进程。 
算法做的只有两件事：a)记录博弈的过程；b)UCT。 
除此之外，还有一件事需要注意，那便是c)选取子节点的策略，这个策略在a)和b)中都要用到，这个策略best_child()表示。 
在a)和b)的伪代码中，选取v的最佳节点v’用语句v’ = best_child(v)表示。在讨论了a)和b)之后，再讨论这个策略。

a) 记录博弈的过程

记录博弈的过程可分为两个部分。第一个部分为当对手落子后，AI更新博弈树和主路径。第二个部分为当自己落子后，AI更新博弈树和主路径。AI通过博弈树和主路径来记录博弈的过程，因此更新博弈树和主路径和主路径是等价的。伪代码如下：

algorithm record_part1： 
s = get_state(); //获取对手落子后的状态
v = P.tail(); //取主路径P的末尾节点v
for vc in childs(v): 
    if m(vc)== s: //如果存在v的子节点vc对应的状态为s 
        P.append(vc); //将vc加入路径尾部
        break; 
if not exists(m(vc) == s,for vc in childs(v)): //如果不存在v的子节点vc对应的状态为s
    vc = construct_node(); //构建新的节点vc
    m(vc) = s; //使得vc的状态为s
    parent(vc) = v; //vc的父亲为v
    P.append(vc); //将vc加入路径尾部

algorithm record_part2: 
v = P.tail(); //取主路径P的末尾节点v
vc = best_child(v); //选择v的最佳子节点，以得到最佳落子
P.append(vc); //将vc加入路径尾部
return (从m(v)到m(vc)的落子点); 

b) UCT算法

UCT算法的执行位置介于record_part1和record_part2之间。因此，总算法的执行顺序为record_part1→ UCT → record_part2。 
UCT算法需要传入一个节点v∈T’做参数。 
1. 首先算法从v开始向T’的深处探索，直到遇见终节点v’或非全拓展节点。如果遇到的是非全拓展节点，还要对节点进行向下拓展一步才得到v’。 
2. 接下来对v’进行模拟，得到一个得分mark。 
3. 最后进行回溯，按探索路径回溯至根节点，并且更新路中所有节点的total、win和lose参数。 
在我的算法中，得分mark指v’节点模拟的胜负情况： 
设状态m(v’)的当前玩家为i，经过一次模拟， 
若i胜利，则mark=1；若i失败，则mark=-1；若平局，则mark=0。 
伪代码如下：

for i in range(k): //执行k轮UCT
UCT(P.tail()); 

algorithm UCT(v): 
    while(v不是终结点): 
        if(v不是全拓展节点): v = expand(v); //v记录为v拓展后得到的子节点
        else: v = best_child(v); //探索
mark = simulate(v); //模拟
while(v非空): //回溯，T'中只有根节点v的parent(v)为空
    total(v) += 1; 
    if(mark == 1): win(v)=win(v)+1; 
    else if(mark == -1): lose(v)=lose(v)+1; 
    v = parent(v); 
    mark = -mark; 

c)选取v的子节点策略best_child(v)

在两种地方会用到这个策略：

1. record_part2

此时要选择v的子节点以确定落子点。 
显然只要选取一个落子点，能给对手造成最不利的局面即可。因此只要选择lose / total大，win / total小的子节点，综合两者，选择出(lose – win) / total最大的子节点即可。

2. UCT

此时要确定探索时选择的子节点。 
第二种场景相比第一种场景，同时还要考虑子节点的总模拟次数total，因为total越少，利用win、lose、total来评估节点局面的好坏则越不精确。从而，如果不考虑子节点的总模拟次数，可能会让算法错过一些有利的局面。 
综合第一种场景和第二种场景，利用多臂老虎机算法中的信心上界公式I来评估各个子节点：

I(vc) = (lose(vc) - win(vc)) / total(vc) + c * sqrt(2 * ln(total(parent(vc))) / total(vc))
1
其中c为一个参数。对于record_part2，c=0；对UCT，c可以根据实验结果不断调整。

best_child(v)的伪代码如下：

algorithm best_child(v): 
return argmax(I(vc), for vc in childs(v)) //选取拥有最大信心上界的子节点
1
2
三、优点

1. 没有任何人工评估的干预。

UCT的循环执行类似一个自然选择的过程，自动评估出每个节点v对应状态m(v)的好坏。

2. 探索与利用。

算法兼顾局面模拟的充分程度（探索）和局面的好坏（利用），避免遗漏了一些潜在的有利局面。

3. 减小探索分支。

由于子节点的选取不是随机的，因此对于一个节点v，选取往往会集中在v的几个子节点当中，从而算法对于这几个子节点会拓展更深。如果将best_child(v)改为随机选取v的一个子节点，那么博弈树T’的深度会大大减少。

4. 博弈树T’的不对称增长。

这也是由于子节点选取的非随机策略引起的。 
如下图，树中有探索较深的部分和探索较浅的部分： 
对于探索较深的部分，算法认为这些部分对应的博弈过程更有可能出现，因此对这部分做了充分的模拟，即如果棋局进入了这些部分，根据算法充分掌握的信息，算法具有较大的胜率。 
对于探索较浅的部分，算法认为这些部分对应的博弈过程出现概率少，因为如果进入了这些部分，算法就会认为对手采取了对它有利的落子（即对手选中了一个(lose – win) / total比较小的节点），尽管对于这部分没有进行充足的探索，但是对手采取了对算法有利的落子，因此算法仍然具有较大的胜率。 
因此无论棋局进入了博弈树的哪个部分，都是对算法有利的。 
import random
import math

'''
最简单的一个蒙特卡洛算法实现
蒙特卡洛的核心在于尝试的越多，越可能得到最优结果
在计算pi的设计中，尝试通过面积比例中的点数比例来求取结果
理论上所有的点的比例就是pi值，但是点是无穷的
所以采用蒙特卡洛算法
随机的点越多，这些点就越可能符合
正方形中的点和圆中的点的比例
'''
def main():
    print("请输入迭代次数：")
    n = int(input())
    total = 0
    for i in range(n):
        x=random.random()
        y=random.random()
        if math.sqrt(x**2+y**2)<1.0:
            total+=1
    mypi=4.0*total/n
    print("迭代次数是：",n,"pi的值是：",mypi)
main()

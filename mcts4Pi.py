import random
import math

'''
最简单的一个蒙特卡洛算法实现
通过迭代计算pi的值
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

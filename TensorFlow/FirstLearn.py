import tensorflow as tf
import numpy as np
# 没有使用gpu，所以设置忽略cpu错误
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 使用 NumPy 生成假数据(phony data), 总共 100 个点.
# 生成一个2x100的数组
x_data = np.float32(np.random.rand(2,100));
# print(x_data);
# 1x2*2x100=1x100数组
y_data = np.dot([0.100,0.200], x_data) + 0.300
# print(y_data);
# j代表了虚部
# j_data = np.dot([2j,3j],[2j,3j]);
# print(j_data);
# 构造一个线性模型
#
b = tf.Variable(tf.zeros([1]));
W = tf.Variable(tf.random_uniform([1,2],-1.0,1.0));
y = tf.matmul(W, x_data) + b;

# 定义回归的值，当这个值最小的时候，则达到最佳情况
loss = tf.reduce_mean(tf.square(y - y_data))
# 定义梯度下降算法
optimizer = tf.train.GradientDescentOptimizer(0.5)
# 使用梯度下降算法来进行回归
# 调整b和W来达到loss最佳
train = optimizer.minimize(loss)

# 初始化变量
init = tf.global_variables_initializer();
sess = tf.Session();
sess.run(init);

# 拟合平面
for step in range(0, 2001):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(W), sess.run(b));
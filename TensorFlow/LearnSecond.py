import tensorflow as tf

# 没有使用gpu，所以设置忽略cpu错误
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# 占位数据，是将来的输入训练的数据
x = tf.placeholder("float", [None, 784])
# 784x10的数组
W = tf.Variable(tf.zeros([784,10]))
# 训练数据和w进行线性回归后的偏移量
b = tf.Variable(tf.zeros([10]))
# 对输入结果进行tf.matmul(x,W) + b回归，线性回归
# 后在进行softmax回归逻辑回归，保证值回归到0-1
y = tf.nn.softmax(tf.matmul(x,W) + b)
# 正确结果
y_ = tf.placeholder("float", [None,10])
# 计算正确结果的交叉熵
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
# 使用梯度下降算法，通过损失函数cross_entropy进行反向传播
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

for i in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
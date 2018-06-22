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
# 对输入结果线性回归tf.matmul(x,W) + b
# 后在进行softmax回归
y = tf.nn.softmax(tf.matmul(x,W) + b)
# 正确结果
y_ = tf.placeholder("float", [None,10])
# 计算正确结果的交叉熵
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
loss = tf.reduce_mean(tf.square(y - y_))

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
train_step_loss = tf.train.GradientDescentOptimizer(0.5).minimize(loss)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

for i in range(100000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  # 使用梯度下降算法，通过损失函数cross_entropy进行反向传播
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
  # 使用梯度下降算法，通过损失函数loss进行反向传播
  # sess.run(train_step_loss, feed_dict={x: batch_xs, y_: batch_ys})
  if(i>=70000 and i%100==0):
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print(str(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))+' '+str(i/1000))

# cross_entropy法初期表现很好，但是当训练次数过大时，会产生过度拟合现象。当训练次数大于70000时会出现结果下降的情况
# loss前期表现较差，但是随着训练的加深，表现会趋近变好(好像极限就是0.93左右)
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
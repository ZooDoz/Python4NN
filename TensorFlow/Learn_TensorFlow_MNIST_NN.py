import tensorflow as tf

# 没有使用gpu，所以设置忽略cpu错误
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

'''
完整的卷积网络的训练过程可以总结如下：

第一步：我们初始化所有的滤波器，使用随机值设置参数/权重
第二步：网络接收一张训练图像作为输入，通过前向传播过程（卷积、ReLU 和池化操作，以及全连接层的前向传播），找到各个类的输出概率
我们假设船这张图像的输出概率是 [0.2, 0.4, 0.1, 0.3]
因为对于第一张训练样本的权重是随机分配的，输出的概率也是随机的
第三步：在输出层计算总误差（计算 4 类的和）
Total Error = ∑  ½ (target probability – output probability) ²
第四步：使用反向传播算法，根据网络的权重计算误差的梯度，并使用梯度下降算法更新所有滤波器的值/权重以及参数的值，使输出误差最小化
权重的更新与它们对总误差的占比有关
当同样的图像再次作为输入，这时的输出概率可能会是 [0.1, 0.1, 0.7, 0.1]，这就与目标矢量 [0, 0, 1, 0] 更接近了
这表明网络已经通过调节权重/滤波器，可以正确对这张特定图像的分类，这样输出的误差就减小了
像滤波器数量、滤波器大小、网络结构等这样的参数，在第一步前都是固定的，在训练过程中保持不变——仅仅是滤波器矩阵的值和连接权重在更新
第五步：对训练数据中所有的图像重复步骤 1 ~ 4
'''

'''
truncated_normal
shape表示生成张量的维度
mean是均值
stddev是标准差
'''
def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)
'''
构造一个常量矩阵
'''
def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)
'''
tf.nn.conv2d(input, w, strides, padding)
input 为输入，格式为[batch, height, width, channels], 分别为【输入的批次数量、图像的高（行数）、宽（列数）、通道（彩色为3，灰色为1）】
w 为卷积矩阵，[卷积核高度，卷积核宽度， 图像通道数， 卷积核个数]
strides 为滑动窗口尺寸，分别为[1, height, width, 1]，因为我们不想在batch和channels上做卷积，所以这两个维度设为了1
padding 为扩展方式，有两种 vaild 和 same
卷积使用
滤波器会反向传播
'''
def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')
'''
tf.nn.max_pool(value, ksize, strides, padding, name=None)
value：需要池化的输入，一般池化层接在卷积层后面，所以输入通常是feature map，依然是[batch, height, width, channels]这样的shape
ksize：池化窗口的大小，取一个四维向量，一般是[1, height, width, 1]，因为我们不想在batch和channels上做池化，所以这两个维度设为了1
strides：和卷积类似，窗口在每一个维度上滑动的步长，一般也是[1, stride,stride, 1]
padding：和卷积类似，可以取'VALID' 或者'SAME'
图片特征降维使用，不会反向传播
'''
def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# 占位数据，是将来的输入训练的数据
x = tf.placeholder("float", [None, 784])
# 占位数据，时将来的结果数据
y_ = tf.placeholder("float", shape=[None, 10])
# 将图片转换为四维数组
# batch, height, width, channels
x_image = tf.reshape(x, [-1,28,28,1])

'''第一层'''
# 生成卷积层
# [卷积核高度，卷积核宽度， 图像通道数， 卷积核个数]
# [5,5,1,32]
# 特征提取
# 对 28x28x1的数据在5x5x1的32个卷积核进行卷积
# 矩阵维度可以相互组合 4不同个维度 可以拆分成 1维+3维 = 1维+1维+2维：
W_conv1 = weight_variable([5, 5, 1, 32])
# 标准矩阵，用于计算偏移
b_conv1 = bias_variable([32])
# 卷积+偏移后进行激活
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
# 对激活结果进行池化
h_pool1 = max_pool_2x2(h_conv1)
'''第二层'''
# 生成卷积层
# [卷积核高度，卷积核宽度， 图像通道数， 卷积核个数]
# [5,5,32,64]
# 对前一层卷积产生的特征进行二次特征提取
W_conv2 = weight_variable([5, 5, 32, 64])
# 标准矩阵，用于计算偏移
b_conv2 = bias_variable([64])
# 卷积+偏移后进行激活
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
# 对激活结果进行池化
h_pool2 = max_pool_2x2(h_conv2)
'''密集层(全连接层)'''
# 生成卷积层
# [卷积核高度，卷积核宽度， 图像通道数， 卷积核个数]
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
# 将池化加过转换为二位输入数组
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
# 再次提取特征
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# 随机地删除隐藏层的部分单元
# 防止过度拟合
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
# 对计算出的特征值进行线性回归
y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# 设置反向传播机制
cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
# 梯度下降算法进行反向传播
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
# 比较训练后的值与真实值的差距
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

for i in range(20000):
  batch = mnist.train.next_batch(50)
  if i%100 == 0:
    train_accuracy = accuracy.eval(session=sess,feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
    print("step %d, training accuracy %g"%(i, train_accuracy))
  train_step.run(session=sess,feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print ("test accuracy %g"%accuracy.eval(session=sess,feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))





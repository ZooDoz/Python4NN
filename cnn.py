import os
import numpy as np
import scipy
import cv2
import keras

from keras.models import Sequential
from keras.utils.np_utils import to_categorical

# Defining the File Path

cat = os.listdir("/mnt/hdd/datasets/dogs_cats/train/cat")
dog = os.listdir("/mnt/hdd/datasets/dogs_cats/train/dog")
# Loading the Images
filepath = "/mnt/hdd/datasets/dogs_cats/train/cat/"
filepath2 = "/mnt/hdd/datasets/dogs_cats/train/dog/"

images = []
label = []
for i in cat:
    image = scipy.misc.imread(filepath + i)
    images.append(image)
    label.append(0)  
    # for cat imagesfor i in dog:
    image = scipy.misc.imread(filepath2 + i)
    images.append(image)
    label.append(1)  
    # for dog images
    # resizing all the imagesfor i in range(0,23000):
    images[i] = cv2.resize(images[i], (300, 300) , interpolation=cv2.INTER_AREA)

# converting images to arrays

images = np.array(images)
label = np.array(label)

# Defining the hyperparameters

filters = 10
filtersize = (5, 5)

epochs = 5
batchsize = 128
input_shape = (300, 300, 3)

# Converting the target variable to the required sizefrom keras.utils.np_utils import to_categorical
label = to_categorical(label)

# Defining the model

model = Sequential()

model.add(keras.layers.InputLayer(input_shape=input_shape))

model.add(keras.layers.convolutional.Conv2D(filters, filtersize, strides=(
    1, 1), padding='valid', data_format="channels_last", activation='relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(keras.layers.Flatten())

model.add(keras.layers.Dense(units=2, input_dim=50, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
model.fit(images, label, epochs=epochs,
          batch_size=batchsize, validation_split=0.3)

model.summary()

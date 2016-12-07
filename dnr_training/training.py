
# coding: utf-8

# In[1]:

import os
import sys
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense


# In[2]:

img_width, img_height = 500, 500

train_data_dir = sys.argv[1]
validation_data_dir = sys.argv[2]

tr0DIR = sys.argv[3]
tr1DIR = sys.argv[4]
vl0DIR = sys.argv[5]
vl1DIR = sys.argv[6]

nb_train_samples = len([name for name in os.listdir(tr0DIR) if os.path.isfile(os.path.join(tr0DIR, name))]) + len([name for name in os.listdir(tr1DIR) if os.path.isfile(os.path.join(tr1DIR, name))])
nb_validation_samples = len([name for name in os.listdir(vl0DIR) if os.path.isfile(os.path.join(vl0DIR, name))]) + len([name for name in os.listdir(vl1DIR) if os.path.isfile(os.path.join(vl1DIR, name))])


nb_epoch = 50


# In[ ]:

model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(3, img_width, img_height)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))


# In[ ]:

model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))


# In[ ]:

model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))


# In[ ]:

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))


# In[ ]:

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])


# In[ ]:

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        #zca_whitening=True
        )


# In[ ]:

test_datagen = ImageDataGenerator(rescale=1./255)


# In[ ]:

train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=32,
        class_mode='binary')


# In[ ]:

validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=32,
        class_mode='binary')


# In[ ]:

model.fit_generator(
        train_generator,
        samples_per_epoch=2000,
        nb_epoch=nb_epoch,
        validation_data=validation_generator,
        nb_val_samples=800)


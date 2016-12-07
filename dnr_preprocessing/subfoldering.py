
# coding: utf-8

# In[1]:

import numpy as np
import sys
import os
from scipy import misc
from os import listdir
from os.path import isfile, join


# In[2]:

# In[3]:

imagesdir = sys.argv[1]

path_train0 = sys.argv[3]
path_train1 = sys.argv[4]
path_val0 = sys.argv[5]
path_val1 = sys.argv[6]


# In[4]:

image_labels = sys.argv[2]

import csv

reader = csv.reader(open(image_labels),delimiter="\n")

data = []

for row in reader:
    for col in row:
        dt = col.split("\t")
        data += [[x for x in dt]]
npdata = np.array(data)
print(npdata.shape[0]) 


# In[6]:

ntrain = round(4./5*npdata.shape[0])
nval = len(npdata) - ntrain
train0 = []
train1 = []
val0 = []
val1 = []

for i in range(0,ntrain):   
    if npdata[i,1] == '0':
        train0.insert(i, npdata[i,0])
    else:
        train1.insert(i, npdata[i,0])
print(len(train0))
print(len(train1))

for i in range(ntrain,npdata.shape[0]):
    if npdata[i,1] == '0':
        val0.insert(i, npdata[i,0])
    else:
        val1.insert(i, npdata[i,0])
print(len(val0))
print(len(val1))        


# In[7]:

for i in train0:
    os.rename(imagesdir + i, path_train0 + i)
for i in train1:
    os.rename(imagesdir + i, path_train1 + i)
for i in val0:
    os.rename(imagesdir + i, path_val0 + i)
for i in val1:
    os.rename(imagesdir + i, path_val1 + i)
print("Images are now in the right subdirectories.")






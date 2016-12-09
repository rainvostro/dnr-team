"""
Testing Phase

"""

import os
import sys
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.models import model_from_json
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from sklearn.preprocessing import OneHotEncoder

# load dataset


# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
 
# evaluate loaded model on test data
loaded_model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
score = loaded_model.evaluate(X_test, y_test, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

y_pred_f = np.round(loaded_model.predict(X_test),0)

enc = OneHotEncoder()
enc.fit(y_pred_f)
OneHotEncoder(categorical_features='all', dtype='numpy.float64',
       handle_unknown='error', n_values='auto', sparse=True)
y_pred = enc.n_values_ - 1

print(y_pred.shape)

confusion_mat = confusion_matrix(y_test, y_pred)
print(confusion_mat.shape)
tp = confusion_mat[0,0]
tn = confusion_mat[0,1]
fp = confusion_mat[1,0]
fn = confusion_mat[1,1]
print("True Positive: ", tp,"\nTrue Negative: ", tn,"\nFalse Positive: ", fp,"\nFalse Negative: ", fn)

acc = accuracy_score(y_test, y_pred)
rocauc = roc_auc_score(y_test, y_pred)
prec, rec, fms, sup = precision_recall_fscore_support(y_test, y_pred)

print("Accuracy: {}".format(acc))
print("ROC AUC: {}".format(rocauc))
print("F1-Score: {}".format(fms))

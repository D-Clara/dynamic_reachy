from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, GlobalAveragePooling1D, Dropout, Conv1D, MaxPooling1D
from tensorflow.keras.utils import to_categorical

from random import shuffle
import numpy as np
import matplotlib.pyplot as plt

X, Y = np.array([]), np.array([])


def split_data(data, ratio=0.8):
    shuffle(data)
    return data[:int(len(data) * ratio)], data[int(len(data) * ratio):]


X_train, X_test = split_data(X, ratio=0.8)
y_train, y_test = split_data(Y, ratio=0.8)
input_dim = X_train.shape

# One hot encoding
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)


###############################################################################
# MODEL DEFINITION
model = Sequential()
model.add(Conv1D(64, 3, activation='relu', input_shape=input_dim))
model.add(Conv1D(64, 3, activation='relu'))
model.add(MaxPooling1D(3))
model.add(Conv1D(128, 3, activation='relu'))
model.add(Conv1D(128, 3, activation='relu'))
model.add(GlobalAveragePooling1D())
model.add(Dropout(0.5))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(6, activation='linear'))  # 6 coordinates to predict (x, y, z, vx, vy, vz)

###############################################################################
# MODEL COMPILATION and TRAINING
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()
model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test))

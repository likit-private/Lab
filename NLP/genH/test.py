from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM
import numpy

model = Sequential()

N = 1000
d = 50

model.add(LSTM(output_dim=128, input_shape=(d,1), activation='sigmoid', inner_activation='hard_sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])



X = numpy.random.random((N, d)).reshape((N,d,1))
y = numpy.random.random((N, 1))
model.fit(X, y, batch_size=16, nb_epoch=10)
#score = model.evaluate(X_test, Y_test, batch_size=16)


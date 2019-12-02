# -*- coding: utf-8 -*-
import  BasicModel
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Flatten, Dropout
from tensorflow.keras import utils
import numpy as np

class RecurrentModel (BasicModel.BasicModel):
    def __init__(self, params):

        model = Sequential()
        model.add(Embedding(params["maxWords"], 2, input_length=params["maxLength"]))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))

        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        self.model = model

    def fitModel(self, x, y, epochs=3):
        x = np.array(x)
        y = np.array(y)
        result = self.model.fit(x, y, epochs=epochs)

    def testModel(self,x,y):
        x = np.array(x)
        y = np.array(y)
        loss, acc = self.model.evaluate(x, y, verbose=True)

    def predict(self, x):
        return self.model.predict(np.array([x]))


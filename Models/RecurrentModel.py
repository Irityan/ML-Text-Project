# -*- coding: utf-8 -*-
from Models.BasicModel import BasicModel
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, SimpleRNN
import numpy as np

from DatasetContainer import OutputFormat


class RecurrentModel (BasicModel):
    def __init__(self, params):
        model = Sequential()
        model.add(Embedding(params["maxWords"], 2, input_length=params["maxLength"]))
        model.add(SimpleRNN(7))

        outputFormat = params["outputFormat"]
        if outputFormat == OutputFormat.vector3:
            model.add(Dense(3, activation='sigmoid'))
        elif outputFormat == OutputFormat.vector2:
            model.add(Dense(2, activation='sigmoid'))
        elif outputFormat == OutputFormat.numeric:
            model.add(Dense(1, activation='sigmoid'))
        else:
            raise Exception("Не предоставлен корректный формат выходных данных!")

        model.compile(optimizer='rmsprop',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        self.model = model

    def fitModel(self, x, y, epochs=3):
        x = np.array(x)
        y = np.array(y)
        result = self.model.fit(x, y, epochs=epochs, batch_size=128)
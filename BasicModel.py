# -*- coding: utf-8 -*-
import tensorflow as tf


class BasicModel:

    def __init__(self, params):
        self.model = None
        raise NotImplementedError

    def fitModel(self, x, y, epochs):
        raise NotImplementedError

    def testModel(self, x, y):
        raise NotImplementedError

    def saveModel(self, path):
        self.model.save(path)

    def loadModel(self, path):
        self.model = tf.keras.models.load_model(path)
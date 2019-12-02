# -*- coding: utf-8 -*-
import  tensorflow as tf

class BasicModel:

    def __init__(self):
        self.model = None

    def fitModel(self):
        raise NotImplementedError

    def testModel(self):
        raise  NotImplementedError

    def saveModel(self, path):
        self.model.save(path)

    def loadModel(self, path):
        self.model = tf.keras.models.load_model(path)
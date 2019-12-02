# -*- coding: utf-8 -*-

from RecurrentModel import RecurrentModel
from FeedforwardModel import FeedforwardModel
import DatasetGenerator
from DatasetContainer import InputFormat, OutputFormat
import numpy as np
import os

maxWords = 10000
maxLength = 250
jsonPath = "..\\ML-Text-Project DATA\\allReviews.json"

dataset = DatasetGenerator.getDatasetFromJSON(jsonPath, maxlength=maxLength, maxWordLength=maxWords, wordListPath="words.txt", wordListCached=True)
#x_train, y_train, x_test, y_test = dataset.getData(InputFormat.numeric, OutputFormat.numeric, testingPercentage=0.1)
x_train, y_train, x_test, y_test = dataset.getData(InputFormat.numeric, OutputFormat.vector3, testingPercentage=0.05)

currentModel = RecurrentModel({"maxWords": maxWords, "maxLength": maxLength})
#currentModel = FeedforwardModel({"maxWords": maxWords, "maxLength": maxLength})

if not os.path.exists("testModel"):
    currentModel.fitModel(x_train, y_train, epochs=50)
    currentModel.saveModel("testModel")
    print("\nTESTING...\n")
    currentModel.testModel(x_test, y_test)
else:
    currentModel.loadModel("testModel")
    print("Загружена модель")


print("\n")
print("{:>28}: [[{:^9} | {:^8} | {:^9}]]".format("Оценки", "m1", "zero", "p1"))
#print("{:>28}: [[{:^9} | {:^9}]]".format("Оценки", "m1", "p1"))
testText = open("negativeTest.txt", 'r').read()
encodedText = dataset._dataEncoder.encodeText(testText, maxLength)
result = currentModel.predict(encodedText)
print("Оценка отрицательного текста: {}".format(result))

testText =  open("positiveTest.txt", 'r').read()
#testText =  open("chto-obeshchayut-i-vypolnyayut.txt", 'r').read()
encodedText = dataset._dataEncoder.encodeText(testText, maxLength)
result = currentModel.predict(encodedText)
print("Оценка положительного текста: {}".format(result))
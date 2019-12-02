# -*- coding: utf-8 -*-

from RecurrentModel import  RecurrentModel
import  DatasetGenerator
from DatasetContainer import  InputFormat, OutputFormat
import  numpy as np
import os

maxWords = 10000
maxLength = 300
jsonPath = "..\\ML-Text-Project DATA\\allReviews.json"

dataset = DatasetGenerator.getDatasetFromJSON(jsonPath, maxlength=maxLength, maxWordLength=maxWords, wordListPath="words.txt", wordListCached=True)
x_train, y_train, x_test, y_test = dataset.getData(InputFormat.numeric, OutputFormat.numeric, testingPercentage=0.2)

currentModel = RecurrentModel({"maxWords": maxWords, "maxLength": maxLength})

if not os.path.exists("testModel"):
    currentModel.fitModel(x_train, y_train, epochs=20)
    currentModel.saveModel("testModel")
    print("TESTING...")
    currentModel.testModel(x_test, y_test)
else:
    currentModel.loadModel("testModel")
    print("Загружена модель")

testText = "Ужасный отель, совершенно непонятно, как он ещё до сих пор существует. Обслуживание плохое, а в отеле невозможно жить. Недостатков куча, а вот плюсов почти нет. Никому не советуем."
encodedText = dataset._dataEncoder.encodeText(testText, maxLength)

result = currentModel.predict(encodedText)

print(result)
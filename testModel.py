# -*- coding: utf-8 -*-

from Models.FeedforwardModel import FeedforwardModel
import DatasetGenerator
from DatasetContainer import InputFormat, OutputFormat
import os
import numpy as np

maxWords = 10000
maxLength = 250
#jsonPath = "..\\ML-Text-Project DATA\\allReviews.json"
jsonPath = "reviewsParsed\\data_file.json"
tweeterPaths = ["tweetsData\\positive.csv", "tweetsData\\negative.csv"]

#dataset = DatasetGenerator.getDatasetFromJSON(jsonPath, maxlength=maxLength, maxWordLength=maxWords, wordListPath="words.txt", wordListCached=True)
#dataset = DatasetGenerator.getDatasetFromTweetsCsv(tweeterPaths, maxlength=maxLength, maxWordLength=maxWords, wordListPath="tweeterWords.txt", wordListCached=True)

dataset = DatasetGenerator.getDatasetFromJSON(jsonPath, maxlength=maxLength, maxWordLength=maxWords, wordListPath="words.txt", wordListCached=True)

#x_train, y_train, x_test, y_test = dataset.getData(InputFormat.numeric, OutputFormat.numeric, testingPercentage=0.1)
#x_train, y_train, x_test, y_test = dataset.getData(InputFormat.numeric, OutputFormat.vector3, testingPercentage=0.05)
x_train, y_train, x_test, y_test = dataset.getData(InputFormat.numeric, OutputFormat.vector2, testingPercentage=0.2)

#reviewsDataset = DatasetGenerator.getDatasetFromJSON(jsonPath, maxlength=maxLength, maxWordLength=maxWords, wordListPath="tweeterWords.txt", wordListCached=True)
#x_test_reviews, y_test_reviews, _, _ = reviewsDataset.getData(InputFormat.numeric, OutputFormat.vector2, testingPercentage= 0.01)


#currentModel = RecurrentModel({"maxWords": maxWords, "maxLength": maxLength, "outputFormat": OutputFormat.vector2})
currentModel = FeedforwardModel({"maxWords": maxWords, "maxLength": maxLength, "dropout": 0.25, "outputFormat": OutputFormat.vector2})

if not os.path.exists("testModel"):
    currentModel.fitModel(x_train, y_train, epochs=30)
    currentModel.saveModel("testModel")
    #print("\nTESTING...\n")
    #currentModel.testModel(x_test, y_test)
else:
    currentModel.loadModel("testModel")
    print("Загружена модель")

#currentModel.testModel(x_test, y_test)
#print("\nTESTING...\n")
#currentModel.testModel(x_test_reviews, y_test_reviews)

print("\n")
#print("{:>28}: [[{:^9} | {:^8} | {:^9}]]".format("Оценки", "m1", "zero", "p1"))
print("{:>28}: [[{:^9} | {:^9}]]".format("Оценки", "m1", "p1"))

testText = open("negativeTest.txt", 'r').read()
#testText = input("Отрицательный отзыв:\n")

encodedText = dataset._dataEncoder.encodeText(testText, maxLength)
result = currentModel.predict(encodedText)
print("Оценка отрицательного текста: {}".format(np.round(result, 2)))

testText =  open("positiveTest.txt", 'r').read()
#testText = input("Положительный отзыв:\n")
#testText =  open("chto-obeshchayut-i-vypolnyayut.txt", 'r').read()

encodedText = dataset._dataEncoder.encodeText(testText, maxLength)
result = currentModel.predict(encodedText)
print("Оценка положительного текста: {}".format(np.round(result, 2)))


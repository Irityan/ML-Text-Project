import os
from enum import  Enum
import  DatasetGenerator
from DatasetContainer import InputFormat, OutputFormat
from Models.FeedforwardModel import FeedforwardModel
from Models.RecurrentModel import RecurrentModel


maxWords = 10000
maxLength = 250

tweetsPath = tweetsPaths = ["tweetsData\\positive.csv", "tweetsData\\negative.csv"]
jsonPath = "reviewsParsed\\data_file.json"
modelsFolder = "ModelsTrained"


class DataSource(Enum):
    tweeter = 1
    reviews = 2

class ModelType(Enum):
    recurrent = 1
    feedforward = 2


tweeterDataset = DatasetGenerator.getDatasetFromTweetsCsv(tweetsPaths, maxlength=maxLength, maxWordLength=maxWords, wordListPath="tweeterWords.txt", wordListCached=True)
reviewsDataset = DatasetGenerator.getDatasetFromJSON(jsonPath, maxlength=maxLength, maxWordLength=maxWords, wordListPath="words.txt", wordListCached=True)

def trainAndTestModel(dataSource, modelType, modelName, outputFormat):
    if dataSource == DataSource.tweeter:
        dataset = tweeterDataset
    elif dataSource == DataSource.reviews:
        dataset = reviewsDataset
    else:
        raise Exception("Неизвестный тип данных")

    x_train, y_train, x_test, y_test = dataset.getData(InputFormat.numeric, outputFormat, testingPercentage=0.1)

    if modelType == ModelType.feedforward:
        currentModel = FeedforwardModel({"maxWords": maxWords, "maxLength": maxLength, "dropout": 0.25, "outputFormat": outputFormat})
    elif modelType == ModelType.recurrent:
        currentModel = RecurrentModel({"maxWords": maxWords, "maxLength": maxLength, "outputFormat": outputFormat})
    else:
        raise Exception("Неизвестный тип модели")

    modelPath = os.path.join(modelsFolder, modelName)

    if not os.path.exists(modelPath):
        currentModel.fitModel(x_train, y_train, epochs=50)
        currentModel.saveModel(modelPath)
    else:
        currentModel.loadModel(modelPath)
        print(f"Загружена модель {modelName}")

    currentModel.testModel(x_test, y_test)


trainAndTestModel(DataSource.tweeter, ModelType.feedforward, "tweetsModel[Feedworward]", outputFormat =OutputFormat.vector2)
trainAndTestModel(DataSource.tweeter, ModelType.recurrent, "tweetsModel[Reccurrent]", outputFormat =OutputFormat.vector2)
trainAndTestModel(DataSource.reviews, ModelType.feedforward, "reviewsModel[Feedworward]", outputFormat =OutputFormat.vector3)
trainAndTestModel(DataSource.reviews, ModelType.recurrent, "reviewsModel[Reccurrent]", outputFormat =OutputFormat.vector3)
trainAndTestModel(DataSource.reviews, ModelType.recurrent, "reviewsModel[Feedworward,v2]", outputFormat =OutputFormat.vector2)

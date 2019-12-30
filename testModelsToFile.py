from enum import Enum
from Models.BasicModel import BasicModel
import DatasetGenerator
from DatasetContainer import  InputFormat, OutputFormat

testDataPath = "ModelsTrained\\tests.txt"
tweetsPath = tweetsPaths = ["tweetsData\\positive.csv", "tweetsData\\negative.csv"]
jsonPath = "reviewsParsed\\data_file.json"
maxLength = 250
maxWords = 10000

class DataSources(Enum):
    twitterData = 1
    reviewsData = 2

class ModelType(Enum):
    recurrent = 1
    feedforward = 2

modelFullNames = {(DataSources.twitterData, ModelType.recurrent): "Корпус твитов, Рекуррентная  модель",
                  (DataSources.twitterData, ModelType.feedforward): "Корпус твитов, Модель прямого распр.",
                  (DataSources.reviewsData, ModelType.recurrent): "Отзывы с сайта, Рекуррентная  модель",
                  (DataSources.reviewsData, ModelType.feedforward): "Отзывы с сайта, Модель прямого распр."}

tweeterDataset = DatasetGenerator.getDatasetFromTweetsCsv(tweetsPaths, maxlength=maxLength, maxWordLength=maxWords, wordListPath="tweeterWords.txt", wordListCached=True)
reviewsDataset = DatasetGenerator.getDatasetFromJSON(jsonPath, maxlength=maxLength, maxWordLength=maxWords, wordListPath="words.txt", wordListCached=True)

modelPaths = {(DataSources.twitterData, ModelType.recurrent): "ModelsTrained/tweetsModel[Reccurrent]",
              (DataSources.twitterData, ModelType.feedforward): "ModelsTrained/tweetsModel[Feedworward]",
              (DataSources.reviewsData, ModelType.recurrent): "ModelsTrained/reviewsModel[Reccurrent]",
              (DataSources.reviewsData, ModelType.feedforward): "ModelsTrained/reviewsModel[Feedworward]"}

models = {key: BasicModel(None) for key in modelPaths}
for key in models:
    models[key].loadModel(modelPaths[key])

open(testDataPath, "w").close()

for key in models:
    outputFormat = OutputFormat.vector3 if key[0] == DataSources.reviewsData else OutputFormat.vector2
    x, y, _, _ = tweeterDataset.getData(InputFormat.numeric, outputFormat, testingPercentage=0)
    loss, acc = models[key].testModel(x, y)

    with open(testDataPath, "a+") as f:
        f.write(f"Тест для модели (по твитам) {modelFullNames[key]}\n")
        f.write(f"Аккуратность = {acc}, Потеря = {loss}\n\n")
        f.close()

for key in models:
    outputFormat = OutputFormat.vector3 if key[0] == DataSources.reviewsData else OutputFormat.vector2
    x, y, _, _ = reviewsDataset.getData(InputFormat.numeric, outputFormat, testingPercentage=0)
    loss, acc = models[key].testModel(x, y)

    with open(testDataPath, "a+") as f:
        f.write(f"Тест для модели (по отзывам) {modelFullNames[key]}\n")
        f.write(f"Аккуратность = {acc}, Потеря = {loss}\n\n")
        f.close()
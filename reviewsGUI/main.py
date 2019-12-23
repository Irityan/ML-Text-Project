# -*- coding: utf-8 -*-

import sys

sys.path.append("..")

from PyQt5 import  QtWidgets
from enum import Enum
import  tensorflow as tf
import  numpy as np

import categorizeReviewsGUI as design
from FileHelper import readFile
from DataEncoder import  DataEncoder
import WordListGenerator
from DatasetContainer import  OutputFormat

class DataSources(Enum):
    twitterData = 1
    reviewsData = 2

class ModelType(Enum):
    recurrent = 1
    feedforward = 2


modelDescriptions = {
    DataSources.twitterData: "Корпус твитов",
    DataSources.reviewsData: "Отзывы с сайта"
}

descToModel = {value: key for key, value in modelDescriptions.items()}

wordListsPaths = {
    DataSources.twitterData: "Wordlists/tweeterWords.txt",
    DataSources.reviewsData: "Wordlists/words.txt"
}

#wordListTexts = {key: readFile(wordListsPaths[key]) for key in DataSources}
#wordLists = {key: fromString(wordListTexts[key]) for key in DataSources}
wordLists = {key: WordListGenerator.load(wordListsPaths[key]) for key in DataSources}

modelPaths = {(DataSources.twitterData, ModelType.recurrent): "ModelsTrained/tweetsModel[Reccurrent]",
              (DataSources.twitterData, ModelType.feedforward): "ModelsTrained/tweetsModel[Feedworward]",
              (DataSources.reviewsData, ModelType.recurrent): "ModelsTrained/reviewsModel[Reccurrent]",
              (DataSources.reviewsData, ModelType.feedforward): "ModelsTrained/reviewsModel[Feedworward]"}

models = {key: tf.keras.models.load_model(value) for key, value in modelPaths.items()}

modelFullNames = {(DataSources.twitterData, ModelType.recurrent): "Корпус твитов, Рекуррентная  модель",
                  (DataSources.twitterData, ModelType.feedforward): "Корпус твитов, Модель прямого распр.",
                  (DataSources.reviewsData, ModelType.recurrent): "Отзывы с сайта, Рекуррентная  модель",
                  (DataSources.reviewsData, ModelType.feedforward): "Отзывы с сайта, Модель прямого распр."}

modelNameToData = {value: key for key, value in modelFullNames.items()}

outputFormats = { DataSources.reviewsData: OutputFormat.vector3,
                  DataSources.twitterData: OutputFormat.vector2}


answersV2 = {0: "m1", 1: "p1"}
answersV3 = {0: "m1", 1: "zero", 2: "p1"}

class ReviewsGUI(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.currentModel = ModelType.feedforward
        self.currentData = DataSources.reviewsData
        self.currentWordList = None
        self.dataEncoder = DataEncoder()

        self.initUI()

    def initUI(self):
        self.modelBox.addItems([modelFullNames[x, y] for x in DataSources for y in ModelType])
        self.modelBox.activated[str].connect(self.onModelSelected)

        default = modelFullNames[self.currentData, self.currentModel]
        self.modelBox.setCurrentIndex(3)
        self.onModelSelected(default)

        self.pushButton.clicked.connect(self.analyzeReview)

    def onModelSelected(self, text):
        self.currentData, self.currentModel = modelNameToData[text]
        print(f"Выбрана модель {modelFullNames[self.currentData, self.currentModel]}")
        self.currentWordList = wordLists[self.currentData]
        self.dataEncoder.setWordList(self.currentWordList, maxListLength=10000)

    def analyzeReview(self):
        reviewText = str(self.reviewInput.toPlainText())
        print(self.dataEncoder.wordList)
        encodedText = self.dataEncoder.encodeText(reviewText, maxLength=250)
        print(encodedText)

        currentModel = models[self.currentData, self.currentModel]
        result = currentModel.predict(np.array([encodedText]))
        result = result[0]
        print(result)

        if outputFormats[self.currentData] == OutputFormat.vector3:
            self.negativeBar.setValue(result[0] * 100)
            self.neutralBar.setValue(result[1] * 100)
            self.positiveBar.setValue(result[2] * 100)
            answerIndex = np.where(result == max(result))[0][0]
            answer = answersV3[answerIndex]
            print(answer)

        elif outputFormats[self.currentData] == OutputFormat.vector2:
            self.negativeBar.setValue(result[0] * 100)
            self.positiveBar.setValue(result[1] * 100)
            self.neutralBar.setValue(0)

            if abs(result[0] - result[1]) < 0.2:
                answerIndex = 1
            else:
                answerIndex = np.where(result == max(result))[0][0]
                print(answerIndex)
                if answerIndex == 1:
                    answerIndex = 2
            answer = answersV3[answerIndex]
            print(answer)


        if answer == "p1":
            self.finalAnswer.setText("Положительный")
            self.finalAnswer.setStyleSheet("color: green")
        elif answer == "m1":
            self.finalAnswer.setText("Отрицательный")
            self.finalAnswer.setStyleSheet("color: red")
        else:
            self.finalAnswer.setText("Нейтральный")
            self.finalAnswer.setStyleSheet("color: gray")





def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ReviewsGUI()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
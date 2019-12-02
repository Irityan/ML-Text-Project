# -*- coding: utf-8 -*-
from enum import Enum
from DataEncoder import DataEncoder
import  random

class InputFormat(Enum):
    numeric = 1
    text = 2
    oneHotEncoding = 3

class OutputFormat(Enum):
    text = 1
    numeric = 2
    vector = 3

class DatasetContainer:
    numericCategories = {"m1": -1, "p1": 1, "zero": 0}
    vectorCategories = {"m1": [1.0, 0, 0], "p1": [0, 0, 1.0], "zero": [0, 1.0, 0]}

    def __init__(self, x: list, y: list, encoder: DataEncoder):
        self._x_numeric = x
        self._y_categories = y
        self._dataEncoder = encoder

    def _getX(self, inputFormat):
        if inputFormat == InputFormat.numeric:
            return self._x_numeric
        elif inputFormat == InputFormat.text:
            return [self._dataEncoder.decodeTextAsString(i) for i in self._x_numeric]
        elif inputFormat == InputFormat.oneHotEncoding:
            wordLength = len(self._dataEncoder.invertedWordList)
            onehot = []
            for review in self._x_numeric:
                reviewEncoded = []
                for word in review:
                    wordEncoded = [0 for _ in range(wordLength)]
                    wordEncoded[word] = 1
                    reviewEncoded.append(wordEncoded)
                onehot.append(reviewEncoded)
            return onehot
        else:
            raise Exception("Неизвестный тип входного значения")

    def _getY(self, outputFormat):
        if outputFormat == OutputFormat.text:
            return self._y_categories
        elif outputFormat == OutputFormat.numeric:
            return [self.numericCategories[i] for i in self._y_categories]
        elif outputFormat == OutputFormat.vector:
            return [self.vectorCategories[i] for i in self._y_categories]
        else:
            raise Exception("Неизвестный тип выходного значения")

    def getData(self, inputFormat: InputFormat, outputFormat: OutputFormat, testingPercentage: float = 0.1) -> (list, list):
        x = self._getX(inputFormat)
        y = self._getY(outputFormat)

        combined = list(zip(x, y))
        random.shuffle(combined)
        x[:], y[:] = zip(*combined)

        testingLength = int(len(x) * testingPercentage)

        return  x[testingLength:], y[testingLength:], x[:testingLength], y[:testingLength]

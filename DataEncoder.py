# -*- coding: utf-8 -*-

from WordListGenerator import load
from TextHelper import splitWords
import operator
from tensorflow.keras.preprocessing.sequence import pad_sequences
import  numpy as np

class DataEncoder:

    paddingCode = 0
    startCode = 1
    unknownCode = 2

    specialCodes = {paddingCode: '', startCode: '', unknownCode: '?'}

    def __init__(self):
        self.wordList = dict()
        self.invertedWordList = dict()

    def setWordList(self, wordList: dict, maxListLength: int = 0):
        if 0 < maxListLength < len(wordList) + len(self.specialCodes):
            if maxListLength <= len(DataEncoder.specialCodes):
                raise Exception("Длина списка слов слишком мала, необхдоимо как минимум более {} слов".format(len(DataEncoder.specialCodes)))
            sortedWords = sorted(wordList.items(), key=operator.itemgetter(1))
            sortedWords = sortedWords[:(maxListLength - len(DataEncoder.specialCodes))]
            self.wordList = {i[0]: i[1] for i in sortedWords}
        else:
            self.wordList = wordList

        inverted = {value: key for key, value in self.wordList.items()}
        self.invertedWordList = DataEncoder.specialCodes.copy()
        self.invertedWordList.update({int(key) + len(DataEncoder.specialCodes) - 1: value for key, value in inverted.items()})

    def setWordListFromFile(self, filepath, maxListLength: int = 0):
        wordList = load(filepath)
        self.setWordList(wordList, maxListLength=maxListLength)

    def encodeText(self, text: str, maxLength: int = -1) -> list:

        words = splitWords(text)

        encodedText = [DataEncoder.startCode]
        for word in words:
            if word in self.wordList.keys():
                encodedText.append(self.wordList[word] + len(DataEncoder.specialCodes) - 1)
            else:
                encodedText.append(DataEncoder.unknownCode)

        encodedText = np.array(encodedText)
        if maxLength > 0:
            encodedText = pad_sequences([encodedText],
                                        maxlen=maxLength,
                                        padding='post',
                                        truncating='post',
                                        value=self.paddingCode)[0]

        return encodedText

    def decodeText(self, text: list) -> list:
        decodedText = []
        for code in text:
            if code >= len(self.invertedWordList):
                decodedText.append(DataEncoder.specialCodes[DataEncoder.unknownCode])
            else:
                decodedText.append(self.invertedWordList[code])

        return decodedText

    def decodeTextAsString(self, text: list) -> str:
        return " ".join(self.decodeText(text)).strip()
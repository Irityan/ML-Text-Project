# -*- coding: utf-8 -*-

from WordListGenerator import load
from TextHelper import  splitWords
from FileHelper import  readFile
import os
import sys
import operator


class DataEncoder:

    paddingCode = 0
    startCode = 1
    unknownCode = 2

    specialCodes = {paddingCode: '', startCode: '', unknownCode: '?'}

    def __init__(self):
        self.wordList = dict()
        self._invertedWordList = dict()

    def setWordList(self, wordList: dict, maxListLength: int = 0):
        if maxListLength > 0 and maxListLength < len(wordList):
            sortedWords = sorted(wordList.items(), key=operator.itemgetter(1))[:maxListLength]
            self.wordList = {i[0]: i[1] for i in sortedWords}
        else:
            self.wordList = wordList

        inverted = {value: key for key, value in self.wordList.items()}
        self._invertedWordList = DataEncoder.specialCodes.copy()
        self._invertedWordList.update({int(key) + len(DataEncoder.specialCodes) - 1: value for key, value in inverted.items()})

    def setWordListFromFile(self, filepath, maxListLength: int = 0):
        wordList = load(filepath)
        self.setWordList(wordList, maxListLength=maxListLength)

    def encodeText(self, text: str, maxLength: int = -1) -> list:
        words = splitWords(text)

        # Убираем лишние слова
        if 0 < maxLength < len(words):
            words = words[:maxLength - 1]

        encodedText = [DataEncoder.startCode]
        for word in words:
            if word in self.wordList.keys():
                encodedText.append(self.wordList[word] + len(DataEncoder.specialCodes) - 1)
            else:
                encodedText.append(DataEncoder.unknownCode)

        if maxLength > 0 and len(encodedText) < maxLength:
            encodedText[:0] = [DataEncoder.paddingCode]*(maxLength - len(encodedText))

        return encodedText

    def decodeText(self, text: list) -> list:
        decodedText = []
        for code in text:
            if code >= len(self._invertedWordList):
                decodedText.append(DataEncoder.specialCodes[DataEncoder.unknownCode])
            else:
                decodedText.append(self._invertedWordList[code])

        return decodedText

    def decodeTextAsString(self, text: list) -> str:
        return " ".join(self.decodeText(text)).strip()

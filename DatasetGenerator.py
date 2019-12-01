# -*- coding: utf-8 -*-
import JSONHelper
import FileHelper
import DataEncoder
import WordListGenerator
import os
from DatasetContainer import  DatasetContainer

from DatasetContainer import  InputFormat, OutputFormat

def getDatasetFromJSON(jsonFile, maxlength=0, maxWordLength=0, wordListPath=None, wordListCached: bool = False, verbose: bool = True) -> (list, list):
    if wordListCached and wordListPath == None:
        raise Exception("Установлено сохранение списка слов, но желаемый путь к списку не указан.")

    metadata = JSONHelper.getData(jsonFile)

    filepaths = [i[JSONHelper.JSONFields.filename] for i in metadata]
    reviewTexts = FileHelper.readFiles(filepaths)

    if wordListCached:
        if os.path.isfile(wordListPath):
            if verbose: print("Кеширование включено, найден файл '{}'. Читаю список слов из файла...".format(wordListPath))
            wordList = WordListGenerator.load(wordListPath)
        else:
            if verbose: print("Кеширование включено, не найден файл '{}'. Список слов будет создан и сохранён по данному пути...".format(wordListPath))
            wordList = WordListGenerator.fromStrings(reviewTexts)
            WordListGenerator.save(wordList, wordListPath)
    else:
        wordList = WordListGenerator.fromStrings(reviewTexts)
        if wordListPath != None:
            WordListGenerator.save(wordList, wordListPath)

    encoder = DataEncoder.DataEncoder()
    encoder.setWordList(wordList, maxListLength=maxWordLength)
    encodedTexts = [encoder.encodeText(i, maxLength=maxlength) for i in reviewTexts]

    categories = [i[JSONHelper.JSONFields.tonality] for i in metadata]

    container = DatasetContainer(encodedTexts, categories, encoder)

    return container

#dataset = getDatasetFromJSON("..\\ML-Text-Project DATA\\allReviews.json", maxlength=200, maxWordLength=0, wordListPath="words.txt", wordListCached=True)
#print(dataset.getData(InputFormat.text, OutputFormat.text))

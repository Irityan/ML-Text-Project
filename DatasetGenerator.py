# -*- coding: utf-8 -*-
import JSONHelper
import FileHelper
import DataEncoder
import WordListGenerator
import os
from DatasetContainer import  DatasetContainer
import csv
import sys

from DatasetContainer import  InputFormat, OutputFormat

def getWordList(wordListCached, wordListPath, reviewTexts, verbose):
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

    return wordList

def getDatasetFromJSON(jsonFile, maxlength=0, maxWordLength=0, wordListPath=None, wordListCached: bool = False, verbose: bool = True) -> (list, list):
    if wordListCached and wordListPath == None:
        raise Exception("Установлено сохранение списка слов, но желаемый путь к списку не указан.")

    metadata = JSONHelper.getData(jsonFile, skipIncorrect=True)

    filepaths = [i[JSONHelper.JSONFields.filename] for i in metadata]
    reviewTexts = FileHelper.readFiles(filepaths)

    wordList = getWordList(wordListCached, wordListPath, reviewTexts, verbose)

    encoder = DataEncoder.DataEncoder()
    encoder.setWordList(wordList, maxListLength=maxWordLength)
    encodedTexts = [encoder.encodeText(i, maxLength=maxlength) for i in reviewTexts]

    categories = [i[JSONHelper.JSONFields.tonality] for i in metadata]
    for i in range(len(categories)):
        if categories[i] in (1, "1"):
            categories[i] = "p1"
        elif categories[i] in (-1, "-1"):
            categories[i] = "m1"
        else:
            categories[i] = "zero"

    container = DatasetContainer(encodedTexts, categories, encoder)

    return container

def getDatasetFromTweetsCsv(csvPaths, maxlength=0, maxWordLength=0, wordListPath=None, wordListCached: bool = False, verbose: bool = True) -> (list, list):
    for i in csvPaths:
        if not os.path.isfile(i):
            raise Exception(f"Файл '{i} не найден!'")

    reviewTexts = []
    categories = []

    catTranslator = {"1" : "p1", "-1" : "m1"}
    
    for file in csvPaths:
        with open(file, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader([x.replace('\0', '') for x in csvfile], delimiter=';', quotechar='"')
            for row in reader:
                if row != None:
                    reviewTexts.append(row[3])
                    categories.append(catTranslator[row[4]])
                    
    wordList = getWordList(wordListCached, wordListPath, reviewTexts, verbose)

    encoder = DataEncoder.DataEncoder()
    encoder.setWordList(wordList, maxListLength=maxWordLength)
    encodedTexts = [encoder.encodeText(i, maxLength=maxlength) for i in reviewTexts]

    container = DatasetContainer(encodedTexts, categories, encoder)

    return container

# -*- coding: utf-8 -*-

'''
Преобразует исходные текстовые данные в список вида 
wordList[<слово>] = <место по частоте> (то есть, 1 - самое испоьзуемое слово и т.д.)
Например, для английского датасета IMDB wordList["the"] = 1.

Использование:
WordListGenerator.py -s <строка> //обработка строки
WordListGenerator.py -f <имя файла> //обработка файла
WordListGenerator.py -F <путь 1> <путь 2> ... <путь N> //обработка списка путей (как файлы, так и директории)
WordListGenerator.py -F . //Обработка всех файлов в каталоге (с проходом по директориям)

По умолчанию список слов выводится в консоль (выходной поток).
Можно добавить аргумент -o, чтобы вывести список в файл:
WordListGenerator.py <Входные данные, см. выше> -o <путь к выходному файлу>

Конкретные примеры:
WordListGenerator.py -f Aelita.txt -o words.txt // обработать файл Aelita.txt и вывести результат в файл words.txt
WordListGenerator.py -F m1 p1 zero -o wordList.txt // обработать папки m1, p1, zero и вывести результат в файл wordList.txt
'''

import sys
import os
import re
import argparse
from collections import Counter
import TextHelper
import FileHelper

_SUPPORTED_EXTENSIONS = ["txt"]

def _countWords(text : str, appendTo : dict = None) -> dict:
    if appendTo == None:
        wordCount = dict()
    else:
        wordCount = appendTo

    text = text.lower()
    lines = text.split('\n')
    for l in lines:
        words = TextHelper.splitWords(l)
        for w in words:
            if w in wordCount.keys():
                wordCount[w] += 1
            else:
                wordCount[w] = 1

    return wordCount

def _wordCountToDict(wordCount : dict) -> dict:
    sortedWords = sorted(wordCount.items(), key=lambda x: (-x[1], x[0]), reverse=False)
    wordList = {sortedWords[i][0]: i + 1 for i in range(len(sortedWords))}

    return wordList

def makePretty(wordList : dict) -> list:
    if wordList == None:
        return ""
    return "\n".join(["{} - {}".format(key, wordList[key]) for key in wordList])

def fromString(text : str) -> dict:
    wordCount = _countWords(text)
    wordList = _wordCountToDict(wordCount)
    
    return wordList


def fromStrings(textList: list) -> dict:
    wordCount = dict()

    for text in textList:
        _countWords(text, wordCount)

    wordList = _wordCountToDict(wordCount)

    return wordList


def fromFile(filepath) -> dict:
    if not ("." in filepath and filepath.split(".")[-1].lower() in _SUPPORTED_EXTENSIONS):
        print("Неподдерживаемый тип файла")
        return None
    
    text = FileHelper.readFile(filepath)
    lines = " ".join(text.split("\n"))
    
    return fromString(lines)

def fromFiles(pathList) -> dict:
    
    fileList = FileHelper.getFilePaths(pathList, extensions=_SUPPORTED_EXTENSIONS)    
    
    #Теперь fileList содержит список путей к файлам с поддерживаемым расширением
    wordCount = dict()
    for file in fileList:
        text = FileHelper.readFile(file)
        _countWords(text, wordCount)

    wordList = _wordCountToDict(wordCount)
    
    return wordList

def save(wordList : dict, filepath):
    try:
        with open(filepath, 'w') as file:
            file.write(makePretty(wordList))
    except PermissionError:
        print("У вас нет доступа для записи этого файла.")
    except Exception as e:
        print("Неизвестная ошибка")
        print(repr(e))

def load(filepath) -> dict:
    try:
        with open(filepath, 'r') as file:
            text = file.read()
            lines = text.split("\n")
            wordList = {i.split(" - ")[0] : int(i.split(" - ")[1]) for i in lines}
            
            return wordList
    except PermissionError:
        print("У вас нет доступа для чтения из этого файла")
    except Exception as e:
        print("Неизвестная ошибка")
        print(repr(e))

def _makeParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    
    inputGroup = parser.add_mutually_exclusive_group(required=True)
    inputGroup.add_argument('-f', '--file', help='Формирует список слов по текстовому файлу')
    inputGroup.add_argument('-F', '--files', help='Формирует список слов по списку файлов и директорий', nargs='+')
    inputGroup.add_argument('-s', '--string', help='Формирует список слов по входной строке', nargs='+')
    
    parser.add_argument('-o', '--output', help="Выводит список слов в указанный файл")
    
    return parser

#MAIN
if __name__ == "__main__":
    parser = _makeParser()    
    args = parser.parse_args()
    
    wordList = dict()
    
    if args.files != None:
        fileList = args.files
        wordList = fromFiles(fileList)
        
    elif args.file != None:
        wordList = fromFile(args.file)
        
    elif args.string !=None:
        inputString = " ".join(args.string)
        wordList = fromString(inputString)
    '''
    Выше отсутствует else, ибо argparse сам обработает случай, когда ни одного входного файла не предоставлено.
    (Благодаря параметру required)
    '''
    
    #Вывод списка слов. Либо в консоль (выходной поток), либо в файл.
    if wordList != None and len(wordList) > 0:
        if args.output != None:
            save(wordList, args.output)
        else:
            print(makePretty(wordList))
    else:
        print("Не удалось сформировать список слов.")   


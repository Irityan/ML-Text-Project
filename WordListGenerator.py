# -*- coding: utf-8 -*-

'''
Преобразует исходные текстовые данные в список вида 
wordList[<слово>] = <место по частоте> (то есть, 1 - самое испоьзуемое слово и т.д.)
Например, для английского датасета IMDB wordList["the"] = 1.
'''

import sys
import os
import re
import argparse
from collections import Counter
import TextHelper

_SUPPORTED_EXTENSIONS = ["txt"]

def makePretty(wordList : dict) -> list:
    if wordList == None:
        return ""
    return "\n".join(["{} - {}".format(key, wordList[key]) for key in wordList])

def fromString(text : str) -> dict:
    words = TextHelper.splitWords(text)
    wordsByOccurence = Counter(words).most_common()
    sortedWords = {wordsByOccurence[i][0] : i + 1 for i in range(len(wordsByOccurence))}
    
    return sortedWords

def fromFile(filepath) -> dict:
    if not ("." in filepath and filepath.split(".")[-1].lower() in _SUPPORTED_EXTENSIONS):
        print("Неподдерживаемый тип файла")
        return None
    try:
        with open(filepath, 'r') as file:
            text = file.read()
            lines = " ".join(text.split("\n"))
            
            return fromString(lines)
    except FileNotFoundError:
        print("Ошибка: Входной файл не найден.")
    except Exception as e:
        print("Неизвестная ошибка!")
        print(repr(e))

def fromFiles(pathList) -> dict:
    '''
    Разворачиваем список путей (в котором могут быть как файлы, так и папки) в список
    путей к файлам. (берутся только файлы с расширением .txt)
    '''
    fileList = []
    while len(pathList) > 0:
        path = pathList.pop()
        if os.path.isdir(path):
            pathList.extend([os.path.join(path, f) for f in os.listdir(path)])
        elif os.path.isfile(path):
            fileName = os.path.basename(path)
            if fileName.split(".")[-1].lower() in _SUPPORTED_EXTENSIONS:
                fileList.append(path)
        else:
            print("couldn't find {}".format(path))  
    
    
    #Теперь fileList содержит список путей к файлам с поддерживаемым расширением
    wordCount = dict()
    for file in fileList:
        try:
            with open(file, 'r') as f:
                lines = f.read().split('\n')
                for l in lines:
                    words = TextHelper.splitWords(l)
                    for w in words:
                        if w in wordCount.keys():
                            wordCount[w] += 1
                        else:
                            wordCount[w] = 1
        except Exception as e:
            print('Ошибка при обработке файла "{}"'.format(file))
    
    sortedWords = sorted(wordCount.items(), key=lambda x:x[1], reverse=True)
    wordList = { sortedWords[i][0] : i + 1 for i in range(len(sortedWords))}
    
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
            wordList = {i.split(" - ")[0] : i.split(" - ")[1] for i in lines}
            
            return wordList
    except PermissionError:
        print("У вас нет доступа для чтения из этого файла")
    except Exception as e:
        print("Неизвестная ошибка")
        print(repr(e))

def _makeParser():
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

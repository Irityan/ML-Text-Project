# -*- coding: utf-8 -*-

'''
Преобразует исходные текстовые данные в список вида 
wordList[<слово>] = <место по частоте> (то есть, 1 - самое испоьзуемое слово и т.д.)
Например, для английского датасета IMDB wordList["the"] = 1.
'''

import sys
import getopt
from collections import Counter
import TextHelper
    
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

def fromFiles(filepaths) -> dict:
    raise NotImplementedError

def fromFolder(folderpath) -> dict:
    raise NotImplementedError

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


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:o:")
        arglist = {}
        for arg, val in opts:
            arglist[arg] = val
        
        if "-f" in arglist.keys():
            filename = arglist["-f"]
            wordList = fromFile(filename)
            if "-o" in arglist.keys():
                save(wordList, arglist["-o"])
            else:
                print(makePretty(wordList))
        
    except getopt.GetoptError:
        print("Ошибка в списке аргументов.")
        sys.exit(2)
        

# -*- coding: utf-8 -*-

from chardet import detect as _d
import os

def readFile(filepath) -> str:
    if not os.path.isfile(filepath):
        return None
    
    try:
        encoding = None
        with open(filepath, 'rb') as binfile:
            encoding = _d(binfile.read())['encoding']
        
        if encoding != None:
            with open(filepath, 'r', encoding=encoding) as file:
                text = file.read()
                return text
            
    except FileNotFoundError:
        print("Ошибка: Входной файл не найден.")
    except PermissionError:
        print("У вас нет доступа для записи этого файла.")

#По списку файлов и директорий возвращает список полных путей ко всем найденным файлам
def getFilePaths(paths : list, extensions  : list =["txt"]) -> list:
    fileList = []
    
    while len(paths) > 0:
        path = paths.pop()
        if os.path.isdir(path):
            paths.extend([os.path.join(path, f) for f in os.listdir(path)])
        elif os.path.isfile(path):
            fileName = os.path.basename(path)
            if fileName.split(".")[-1].lower() in extensions:
                fileList.append(path)
        else:
            print("couldn't find {}".format(path))
    
    return fileList
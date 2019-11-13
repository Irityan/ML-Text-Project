# -*- coding: utf-8 -*-

from chardet import detect as _d
import os

def readFile(filepath):
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
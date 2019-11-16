# -*- coding: utf-8 -*-
import FileHelper
import json
import os

class _JSONFields:
    studentName = "student_name"
    studentGroup = "student_group"
    studentNumber = "student_number"
    date = "date"
    dataSource = "Data source"
    tonality = "tonality"
    filename = "filename"

    relevantFields = (tonality, filename)

    def isRelevant(field):
        return field in _JSONFields.relevantFields


def getData(inputFile, relevant: bool = False) -> list:
    textData = FileHelper.readFile(inputFile)
    jsonData = json.loads(textData)

    '''
    Обработка относительных путей. Если путь указан относительно файла JSON, а тот
    в свою очередь находится в другой директории, пути к файлам изменяются соответственно.
    Например, если файлы лежат в одной папке с JSON, то к путям каждого файла добавляется
    эта папка.
    '''
    localPath = os.path.dirname(inputFile)
    for i in range(len(jsonData)):
        filename = jsonData[i][_JSONFields.filename]
        if not os.path.isabs(filename):
            jsonData[i][_JSONFields.filename] = os.path.join(localPath, filename)

    #Если нужно, убираем не используемые значения
    if relevant:
        for i in range(len(jsonData)):
            jsonData[i] = {k : v for k, v in jsonData[i].items() if _JSONFields.isRelevant(k)}

    return jsonData


def mergeFiles(fileList, relevant : bool = False, outputFile = None) -> list:
    filePaths = FileHelper.getFilePaths(fileList, extensions=["json"])
    if len(filePaths) == 0:
        return []
    elif len(filePaths) == 1:
        return getData(filePaths[0], relevant=relevant)

    jsonData = []
    for i in filePaths:
        jsonData.extend(getData(i,relevant=relevant))

    return  jsonData


def _printOutReviews(data : list):
    for i in range(len(data)):
        reviewText = FileHelper.readFile(data[i][_JSONFields.filename])
        print("{} - {}:\n{}".format(i+1,
                                    data[i][_JSONFields.tonality],
                                 reviewText))
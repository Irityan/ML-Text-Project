# -*- coding: utf-8 -*-
import FileHelper
import json
import os

class JSONFields:
    studentName = "student_name"
    studentGroup = "student_group"
    studentNumber = "student_number"
    date = "date"
    dataSource = "Data source"
    tonality = "tonality"
    filename = "filename"

    relevantFields = (tonality, filename)

    def isRelevant(field):
        return field in JSONFields.relevantFields


def getData(inputFile) -> list:
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
        filename = jsonData[i][JSONFields.filename]
        if not os.path.isabs(filename):
            jsonData[i][JSONFields.filename] = os.path.join(localPath, filename)

    return jsonData


def mergeFiles(fileList, outputFile = None) -> list:
    filePaths = FileHelper.getFilePaths(fileList, extensions=["json"])
    if len(filePaths) == 0:
        return []
    elif len(filePaths) == 1:
        return getData(filePaths[0])

    jsonData = []
    for i in filePaths:
        jsonData.extend(getData(i))

    if outputFile != None:
        with open(outputFile, 'w', encoding='utf-8') as fp:
            data = json.dump(jsonData, fp, ensure_ascii=False, indent=3)

    return jsonData

def _printOutReviews(data : list):
    for i in range(len(data)):
        reviewText = FileHelper.readFile(data[i][JSONFields.filename])
        print("{} - {}:\n{}".format(i + 1,
                                    data[i][JSONFields.tonality],
                                    reviewText))
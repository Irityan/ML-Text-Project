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


def getData(inputFile, skipIncorrect:bool = False) -> list:
    textData = FileHelper.readFile(inputFile)
    jsonData = json.loads(textData)

    incorrectElements = [False] * len(jsonData)

    for i in range(len(jsonData)):
        try:
            _checkFields(inputFile, jsonData[i])
        except Exception as e:
            if skipIncorrect:
                print(e)
                incorrectElements[i] = True
            else:
                raise e


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

    for i in range(len(jsonData)):
        try:
            _checkElement(inputFile, jsonData[i])
        except Exception as e:
            if skipIncorrect:
                print(e)
                incorrectElements[i] = True
            else:
                raise e

    print(incorrectElements)

    print(f"Длина списка элементов: {len(jsonData)}")

    if skipIncorrect:
        jsonData = [jsonData[i] for i in range(len(jsonData)) if not incorrectElements[i]]
        print(f"Длина списка после удаления неверных элементов: {len(jsonData)}")

    return jsonData


def mergeFiles(fileList, outputFile=None) -> list:
    filePaths = FileHelper.getFilePaths(fileList, extensions=["json"])
    if len(filePaths) == 0:
        return []
    elif len(filePaths) == 1:
        return getData(filePaths[0])

    jsonData = []
    for i in filePaths:
        jsonFile = getData(i)
        for element in jsonFile:
            _checkFields(i, element)
            _checkElement(i, element)
            jsonData.append(element)
        # if not os.path.exists(jsonElement["filename"]):
        #   raise Exception("{}\nФайл по данному пути не существует!".format(jsonElement["filename"]))

    if outputFile != None:
        with open(outputFile, 'w', encoding='utf-8') as fp:
            data = json.dump(jsonData, fp, ensure_ascii=False, indent=3)

    return jsonData



def _checkFields(filepath, element):
    for field in JSONFields.relevantFields:
        if field not in element.keys():
            raise Exception("{}\n{}\nОтсутствует поле {}!".format(filepath, element, field))

def _checkElement(filepath, element):
    if not os.path.exists(element["filename"]):
        raise Exception("{}\n{}\n Файл по данному пути не существует!".format(filepath, element["filename"]))
    elif FileHelper.readFile(element["filename"]) in (None, ""):
        raise Exception("{}\n{}\nНе удалось прочитать файл".format(filepath, element["filename"]))


def _printOutReviews(data: list, emptyOnly: bool = False):
    for i in range(len(data)):
        reviewText = FileHelper.readFile(data[i][JSONFields.filename])
        isEmpty = False
        if reviewText == None:
            isEmpty = True
            reviewText = "<ФАЙЛ НЕ НАЙДЕН>"
        if not emptyOnly or (emptyOnly and isEmpty):
            print("{} - {}, '{}':\n{}".format(i + 1,
                                              data[i][JSONFields.tonality],
                                              data[i][JSONFields.filename],
                                              reviewText))

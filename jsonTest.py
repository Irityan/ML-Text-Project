import JSONHelper
import FileHelper
import os

#path = "C:\\Programming Projects\\ML-Text-Project DATA\\allReviews.json"
path = "C:\\Programming Projects\\ML Text Project\\reviewsParsed\\data_file.json"

data =JSONHelper.getData(path, skipIncorrect=True)

#print(data[0])

'''
for i in range(len(data)):
    print("{} - {}".format(i + 1, data[i]["filename"]))
'''

JSONHelper._printOutReviews(data, emptyOnly=False)

#print(data[516])

#print(FileHelper.readFile(data[515]["filename"]))

'''
for i in data:
    if not os.path.exists(i["filename"]):
        print(i["filename"])
'''
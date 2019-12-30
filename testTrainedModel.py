import os
import  numpy as np

from DatasetContainer import OutputFormat
from Models.FeedforwardModel import FeedforwardModel
from WordListGenerator import  load
from DataEncoder import DataEncoder

import pydot
import tensorflow
from tensorflow.keras.utils import plot_model

modelsFolder = "ModelsTrained"
modelName = "reviewsModel[Feedworward]"
modelPath = os.path.join(modelsFolder, modelName)

wordListPath = "words.txt"

maxWords = 10000
maxLength = 250
dropout = 0.2

currentModel = FeedforwardModel({"maxWords": maxWords, "maxLength": maxLength, "dropout": dropout, "outputFormat": OutputFormat.vector3})
currentModel.loadModel(modelPath)

encoder = DataEncoder()
encoder.setWordListFromFile(wordListPath, maxWords)

text =  open("negativeTest.txt", 'r').read()
encodedText = encoder.encodeText(text, maxLength)
#print(encodedText)

print(np.size(encodedText))
result = currentModel.predict(encodedText)
result = result[0]
print (result)
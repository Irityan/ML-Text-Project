# -*- coding: utf-8 -*-

from Models.BasicModel import BasicModel
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, SimpleRNN
import numpy as np
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.text import  Tokenizer
from tensorflow.keras.models import  Model
from tensorflow.keras.layers import  Input, Activation, concatenate, Dropout, Conv1D, GlobalMaxPooling1D
from gensim.models import Word2Vec

from DatasetContainer import OutputFormat


class ConvolutionalModel (BasicModel):

    def __init__(self, params):

        if "x" not in params.keys():
            raise Exception("Для создания модели требуется предоставить текстовые входные данные")

        w2v_model = Word2Vec.load('ConvData/tweets_model.w2v')

        SENTENCE_LENGTH = 26
        NUM = 100000
        DIM = w2v_model.vector_size

        embedding_matrix = np.zeros((NUM, DIM))

        x = params["x"]
        self._tokenizer = Tokenizer(num_words=10000)
        self._tokenizer.fit_on_texts(x)

        for word, i in self._tokenizer.word_index.items():
            if i >= NUM:
                break
            if word in w2v_model.wv.vocab.keys():
                embedding_matrix[i] = w2v_model.wv[word]

        tweet_input = Input(shape=(SENTENCE_LENGTH,), dtype='int32')

        tweet_encoder = Embedding(NUM, DIM, input_length=SENTENCE_LENGTH,
                                  weights=[embedding_matrix], trainable=False)(tweet_input)

        branches = []
        x = Dropout(0.2)(tweet_encoder)

        for size, filters_count in [(2, 10), (3, 10), (4, 10), (5, 10)]:
            for i in range(filters_count):
                branch = Conv1D(filters=1, kernel_size=size, padding='valid', activation='relu')(x)
                branch = GlobalMaxPooling1D()(branch)
                branches.append(branch)

        x = concatenate(branches, axis=1)
        x = Dropout(0.2)(x)
        x = Dense(30, activation='relu')(x)
        x = Dense(1)(x)

        output = Activation('sigmoid')(x)

        def precision(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
            precision = true_positives / (predicted_positives + K.epsilon())
            return precision

        def recall(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
            recall = true_positives / (possible_positives + K.epsilon())
            return recall

        def f1(y_true, y_pred):
            def recall(y_true, y_pred):
                true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
                possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
                recall = true_positives / (possible_positives + K.epsilon())
                return recall

            def precision(y_true, y_pred):
                true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
                predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
                precision = true_positives / (predicted_positives + K.epsilon())
                return precision

            precision = precision(y_true, y_pred)
            recall = recall(y_true, y_pred)
            return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

        self.model = Model(inputs=[tweet_input], outputs=[output])
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[precision, recall, f1])


    def fitModel(self, x, y, epochs=3):
        x = np.array(x)
        y = np.array(y)
        result = self.model.fit(x, y, epochs=epochs, batch_size=128)

    def testModel(self, x, y):
        x = np.array(x)
        y = np.array(y)
        loss, acc = self.model.evaluate(x, y, verbose=True)

    def predict(self, x):
        x = self._tokenizer.texts_to_sequences([x])
        return self.model.predict(x)

    def loadModel(self, path):
        self.model.load_weights(path)


# -*- coding: utf-8 -*-
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from keras import backend as K
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from gensim.models import Word2Vec
from keras.layers import Input
from keras.layers.embeddings import Embedding
from keras.layers import Dense, concatenate, Activation, Dropout
from keras.models import Model
from keras.layers.convolutional import Conv1D
from keras.layers.pooling import GlobalMaxPooling1D
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from keras import optimizers

class GetModelCNN:

    # Считываем данные
    n = ['id', 'date', 'name', 'text', 'typr', 'rep', 'rtw', 'faw', 'stcount', 'foll', 'frien', 'listcount']
    data_positive = pd.read_csv('positive.csv', sep=';', error_bad_lines=False, names=n, usecols=['text'])
    data_negative = pd.read_csv('negative.csv', sep=';', error_bad_lines=False, names=n, usecols=['text'])
    # Формируем сбалансированный датасет
    sample_size = min(data_positive.shape[0], data_negative.shape[0])
    raw_data = np.concatenate((data_positive['text'].values[:sample_size],
                               data_negative['text'].values[:sample_size]), axis=0)
    labels = [1] * sample_size + [0] * sample_size

    # Перед началом обучения тексты прошли процедуру предварительной обработки:
    # приведение к нижнему регистру;
    # замена «ё» на «е»;
    # замена ссылок на токен «URL»;
    # замена упоминания пользователя на токен «USER»;
    # удаление знаков пунктуации.
    #МЕТОД ДЛЯ ПРЕДВАРИТЕЛЬНОЙ ОБРАБОТКИ ТЕКСТОВ
    def preprocess_text(text):
        text = text.lower().replace("ё", "е")
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
        text = re.sub('@[^\s]+', 'USER', text)
        text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
        text = re.sub(' +', ' ', text)
        return text.strip()
    data = [preprocess_text(t) for t in raw_data]

    #разбили набор данных на обучающую и тестовую выборку в соотношении 4:1.
    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=2)
#------------------------------------------------------------------------
    # Defining metrics (Определение метрик) - понадобятся для оценки качества работы для оценки качества моделей и
    # сравнения различных алгоритмов (классификатора)
    def precision(y_true, y_pred):
        # Метрическая точность.
        #Вычисляет только среднее значение точности по пакетам.
        #Вычисляет точность, метрику для классификации мульти-ярлыка
        #сколько выбранных элементов являются релевантными.

        #Precision можно интерпретировать как долю объектов,
        # названных классификатором положительными и при этом действительно являющимися положительными,
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    def recall(y_true, y_pred):
        # Вычисляет только среднее значение отзыва по пакетам.
        #Вычисляет отзыв, метрику для классификации нескольких меток
        #сколько релевантных элементов выбрано.

        #recall показывает, какую долю объектов положительного класса из всех объектов положительного
        # класса нашел алгоритм. Именно введение precision не позволяет нам записывать все объекты в один класс,
        # так как в этом случае мы получаем рост уровня False Positive.
        # Recall демонстрирует способность алгоритма обнаруживать данный класс вообще,
        # а precision — способность отличать этот класс от других классов.Precision и recall не зависят,
        # в отличие от accuracy, от соотношения классов и потому применимы в условиях несбалансированных выборок.
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def f1(y_true, y_pred):
        #Вычисляет только среднее значение отзыва по пакетам.
        #Вычисляет отзыв, метрику для классификации нескольких меток
        #сколько релевантных элементов выбрано.
        def recall(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
            recall = true_positives / (possible_positives + K.epsilon())
            return recall

        #Вычисляет только среднее значение точности по пакетам.
        #Вычисляет точность, метрику для классификации мульти-ярлыка
        #сколько выбранных элементов являются релевантными
        def precision(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
            precision = true_positives / (predicted_positives + K.epsilon())
            return precision
        precision = precision(y_true, y_pred)
        recall = recall(y_true, y_pred)
        return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

    # Preparing weights for the embedding layer(хранит вектора всех слов в словаре)
    SENTENCE_LENGTH = 26
    NUM = 100000  # Размер словарного запаса
    def get_sequences(tokenizer, x):
        sequences = tokenizer.texts_to_sequences(x)
        return pad_sequences(sequences, maxlen=26)

    #Keras содержит в себе инструменты для удобного препроцессинга текстов, картинок и временных рядов,
    # иными словами, самых распространенных типов данных. Сегодня мы работаем с текстами, поэтому нам нужно
    # разбить их на токены и привести в матричную форму.
    tokenizer = Tokenizer(num_words=NUM)
    tokenizer.fit_on_texts(x_train)## теперь токенизатор знает словарь для этого корпуса текстов

    x_train_seq = get_sequences(tokenizer, x_train)
    x_test_seq = get_sequences(tokenizer, x_test)
#-------------------------------------------------------------------------------------------------
    # Загружаем обученную модель
    w2v_model = Word2Vec.load('data/madel/tweets_model.w2v')
    DIM = w2v_model.vector_size #длина вектора вложения.
    # Инициализируем матрицу embedding слоя нулями
    embedding_matrix = np.zeros((NUM, DIM))
    # Добавляем NUM=100000 наиболее часто встречающихся слов из обучающей выборки в embedding слой
    for word, i in tokenizer.word_index.items():
        if i >= NUM:
            break
        if word in w2v_model.wv.vocab.keys():
            embedding_matrix[i] = w2v_model.wv[word]

    # Building the CNN(Свёрточная нейронная сеть)
    tweet_input = Input(shape=(SENTENCE_LENGTH,), dtype='int32')
    # embedding-слой был инициирован весами, полученными при обучении Word2Vec
    tweet_encoder = Embedding(NUM, DIM, input_length=SENTENCE_LENGTH,
                              weights=[embedding_matrix], trainable=False)(tweet_input)

    branches = []
    # Добавляем dropout-регуляризацию(метод исключения)
    x = Dropout(0.2)(tweet_encoder)

    # В разработанной архитектуре использованы фильтры с высотой h=(2, 3, 4, 5),
    # которые предназначены для параллельной обработки биграмм, триграмм, 4-грамм и 5-грамм соответственно.
    # Добавили в нейронную сеть по 10 свёрточных слоев для каждой высоты фильтра, функция активации — ReLU
    for size, filters_count in [(2, 10), (3, 10), (4, 10), (5, 10)]:
        for i in range(filters_count):
            # Добавляем слой свертки
            branch = Conv1D(filters=1, kernel_size=size, padding='valid', activation='relu')(x)
            # Добавляем слой субдискретизации
            branch = GlobalMaxPooling1D()(branch)#Уровень GlobalMaxPooling1D  берет максимальное значение любого вектора признаков из каждого из 256 объектов.
            branches.append(branch)
    # На следующем этапе происходило объединение в общий вектор признаков (слой объединения),
    # который подавался в скрытый полносвязный слой с 30 нейронами.
    # На последнем этапе итоговая карта признаков подавалась на выходной слой нейронной сети с
    # сигмоидальной функцией активации.
    # Конкатенируем карты признаков
    x = concatenate(branches, axis=1)
    # Добавляем dropout-регуляризацию
    x = Dropout(0.2)(x)
    x = Dense(30, activation='relu')(x)
    x = Dense(1)(x)
    output = Activation('sigmoid')(x)
    model = Model(inputs=[tweet_input], outputs=[output])
    # Итоговую модель сконфигурировали с функцией оптимизации Adam (Adaptive Moment Estimation) и
    # binary_crossentropy в качестве функции ошибок. Качество работы классификатора оценивали
    # в критериях precision, recall, f1.
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[precision, recall, f1])
    model.summary()

    # Training and evaluating the CNN
    # На первом этапе обучения заморозил embedding-слой, все остальные слои обучались в течение 1 эпохи:
    # Размер группы примеров, используемых для обучения: 32.
    # Размер валидационной выборки: 25%.
    checkpoint = ModelCheckpoint("models/cnn/cnn-frozen-embeddings-{epoch:02d}-{val_f1:.2f}.hdf5",
                                 monitor='val_f1', save_best_only=True, mode='max', period=1)
    history = model.fit(x_train_seq, y_train, batch_size=32, epochs=1, validation_split=0.25, callbacks = [checkpoint])
    plt.style.use('ggplot')

    def plot_metrix(ax, x1, x2, title):
        ax.plot(range(1, len(x1) + 1), x1, label='train')
        ax.plot(range(1, len(x2) + 1), x2, label='val')
        ax.set_ylabel(title)
        ax.set_xlabel('Epoch')
        ax.legend()
        ax.margins(0)

    def plot_history(history):
        fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(16, 9))
        ax1, ax2, ax3, ax4 = axes.ravel()

        plot_metrix(ax1, history.history['precision'], history.history['val_precision'], 'Precision')
        plot_metrix(ax2, history.history['recall'], history.history['val_recall'], 'Recall')
        plot_metrix(ax3, history.history['f1'], history.history['val_f1'], "$F_1$")
        plot_metrix(ax4, history.history['loss'], history.history['val_loss'], 'Loss')

        plt.show()

    plot_history(history)


    #выбрал модель с наивысшими показателями F-меры на валидационном наборе данных,
    # т.е. модель, полученную на восьмой эпохе обучения (F1=0.7791).
    # У модели разморозил embedding-слой, после чего запустил еще пять эпох обучения.
    # Загружаем веса модели
    model.load_weights('models/cnn/cnn-frozen-embeddings-01-0.74.hdf5')

    predicted = np.round(model.predict(x_test_seq))
    print(classification_report(y_test, predicted, digits=5))

    # Делаем embedding слой способным к обучению
    model.layers[1].trainable = True
    # Уменьшаем learning rate(Коэффициент скорости обучения)
    adam = optimizers.Adam(lr=0.0001)
    model.compile(loss='binary_crossentropy', optimizer=adam, metrics=[precision, recall, f1])
    model.summary()

    checkpoint = ModelCheckpoint("cnn-trainable-{epoch:02d}-{val_f1:.2f}.hdf5",
                                 monitor='val_f1', save_best_only=True, mode='max', period=1)

    history_trainable = model.fit(x_train_seq, y_train, batch_size=32, epochs=1, validation_split=0.25, callbacks = [checkpoint])

    plot_history(history_trainable)#какие-то графики

    model.load_weights('cnn-trainable-01-0.74.hdf5')

    predicted = np.round(model.predict(x_test_seq))
    print(classification_report(y_test, predicted, digits=5))
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'categorizeReviews.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(982, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setFrameShadow(QtWidgets.QFrame.Plain)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(15)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.reviewInput = QtWidgets.QPlainTextEdit(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reviewInput.sizePolicy().hasHeightForWidth())
        self.reviewInput.setSizePolicy(sizePolicy)
        self.reviewInput.setMinimumSize(QtCore.QSize(300, 0))
        self.reviewInput.setObjectName("reviewInput")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.modelSelector = QtWidgets.QHBoxLayout()
        self.modelSelector.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.modelSelector.setSpacing(15)
        self.modelSelector.setObjectName("modelSelector")
        self.modelLabel = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modelLabel.sizePolicy().hasHeightForWidth())
        self.modelLabel.setSizePolicy(sizePolicy)
        self.modelLabel.setObjectName("modelLabel")
        self.modelSelector.addWidget(self.modelLabel)
        self.modelBox = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modelBox.sizePolicy().hasHeightForWidth())
        self.modelBox.setSizePolicy(sizePolicy)
        self.modelBox.setObjectName("modelBox")
        self.modelSelector.addWidget(self.modelBox)
        self.verticalLayout.addLayout(self.modelSelector)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.resultBox = QtWidgets.QVBoxLayout()
        self.resultBox.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.resultBox.setObjectName("resultBox")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.resultBox.addWidget(self.label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(120, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.positiveBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.positiveBar.setStyleSheet("QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 255, 0);\n"
"    width: 20px;\n"
"}")
        self.positiveBar.setMaximum(100)
        self.positiveBar.setProperty("value", 0)
        self.positiveBar.setObjectName("positiveBar")
        self.horizontalLayout_4.addWidget(self.positiveBar)
        self.resultBox.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(120, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.negativeBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.negativeBar.setStyleSheet("QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: red;\n"
"    width: 20px;\n"
"}")
        self.negativeBar.setMaximum(100)
        self.negativeBar.setProperty("value", 0)
        self.negativeBar.setObjectName("negativeBar")
        self.horizontalLayout_3.addWidget(self.negativeBar)
        self.resultBox.addLayout(self.horizontalLayout_3)
        self.neutralBarLayout = QtWidgets.QHBoxLayout()
        self.neutralBarLayout.setObjectName("neutralBarLayout")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(120, 0))
        self.label_4.setObjectName("label_4")
        self.neutralBarLayout.addWidget(self.label_4)
        self.neutralBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.neutralBar.setStyleSheet("QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: gray;\n"
"    width: 20px;\n"
"}")
        self.neutralBar.setMaximum(100)
        self.neutralBar.setProperty("value", 0)
        self.neutralBar.setObjectName("neutralBar")
        self.neutralBarLayout.addWidget(self.neutralBar)
        self.resultBox.addLayout(self.neutralBarLayout)
        self.resultBox.setStretch(0, 10)
        self.verticalLayout.addLayout(self.resultBox)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.finalAnswer = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.finalAnswer.setFont(font)
        self.finalAnswer.setStyleSheet("")
        self.finalAnswer.setText("")
        self.finalAnswer.setAlignment(QtCore.Qt.AlignCenter)
        self.finalAnswer.setObjectName("finalAnswer")
        self.verticalLayout.addWidget(self.finalAnswer)
        self.widget = QtWidgets.QWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Категоризация отзыва"))
        self.modelLabel.setText(_translate("MainWindow", "Модель:"))
        self.pushButton.setText(_translate("MainWindow", "Анализ текста"))
        self.label.setText(_translate("MainWindow", "Результат"))
        self.label_2.setText(_translate("MainWindow", "Положительность"))
        self.label_3.setText(_translate("MainWindow", "Отрицательность"))
        self.label_4.setText(_translate("MainWindow", "Нейтральность"))
        self.label_5.setText(_translate("MainWindow", "Скорее всего этот отзыв:"))

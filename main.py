import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QHBoxLayout, QComboBox, QCheckBox
from PyQt5 import QtGui
from Calcul_conso_elec import Prediction
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt
import numpy as np
import catboost
import datetime

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setUI()
    def setUI(self):
        
        # création du champ de texte
        self.ChampDiam = QLineEdit('90' )   #order : Diameter, thickness, steel_type, weight, length, numbers, month
        self.ChampThick = QLineEdit('1.4')
        self.ChampSteel = QLineEdit('K60')
        self.ChampWeight = QLineEdit('0.06')
        self.ChampLen = QLineEdit('12')
        self.ChampNum = QLineEdit('1')
        self.ChampMonth = QLineEdit('1')

        # Création des boutons
        self.BoutonSubmit = QPushButton("Submit")
        self.BoutonExit = QPushButton("Quit")
        
        # on connecte pour le bouton Submit le "clique" à la méthode "CalculPrediction"
        # et le bouton "Exit" est connecte à la méthode .exit
        self.BoutonSubmit.clicked.connect(self.CalculPrediction)
        self.BoutonExit.clicked.connect(app.exit)
        
        # Création des nom des champ de saisie via des label
        # Création des nom des champ de saisie via des label
        Lmin=['86', '1.2', '0.01', '9.5', '0']
        Lmax=['245', '8', '0.15', '12.5', '16']
        self.welcome = QLabel('This program gives an idea of the consumption of the plant.\nUse these results with a critical look.\nThe min/max values are indicative, the predictions should be accurate in this range.\nYou can put whatever values you want, even negative, even if it should not be possible.\n')
        self.LabelDiam = QLabel("Diameter (cm), min : " + Lmin[0] + " | max : " + Lmax[0])
        self.LabelThick = QLabel("Thickness (cm), min : " + Lmin[1] + " | max : " + Lmax[1])
        self.LabelSteel = QLabel("Steel type")
        self.combo = QComboBox(self)
        self.comboMonth = QComboBox(self)
        self.LabelWeight = QLabel("Weight (tons), min : " + Lmin[2] + " | max : " + Lmax[2])
        self.LabelLen = QLabel("Length (m), min : " + Lmin[3] + " | max : " + Lmax[3])
        self.LabelNum = QLabel("Numbers, min : " + Lmin[4] + " | max : " + Lmax[4])
        self.LabelMonth = QLabel("Month")
        self.cb = QCheckBox("Export predictions to a CSV file ? (predictions.csv is saved in the program folder)")
        self.credits = QLabel("Program made by Clément Seguin, Michaël Soissons, Henri Prevost and Alexis Mourlon for the exclusive use of Chelpipe Group.")

        Lsteel = ['17Г1С-У', 'DNV SAWL 485 FD', 'X70ME', 'K52', 'K60', 'K65']
        Lmonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

        for steel in Lsteel:
            self.combo.addItem(steel)

        for month in Lmonths:
            self.comboMonth.addItem(month)

            # Mise en forme des widgets (alignement horizontal = QVBoxLayout, alignement horizontal = QHBoxLayout)
        layout = QVBoxLayout()
        hbox = QHBoxLayout()

        layout.addWidget(self.welcome)

        layout.addWidget(self.LabelDiam)
        layout.addWidget(self.ChampDiam)

        layout.addWidget(self.LabelThick)
        layout.addWidget(self.ChampThick)

        layout.addWidget(self.LabelSteel)
        layout.addWidget(self.combo)

        layout.addWidget(self.LabelWeight)
        layout.addWidget(self.ChampWeight)

        layout.addWidget(self.LabelLen)
        layout.addWidget(self.ChampLen)

        layout.addWidget(self.LabelNum)
        layout.addWidget(self.ChampNum)

        layout.addWidget(self.LabelMonth)
        layout.addWidget(self.comboMonth)

        layout.addWidget(self.cb)

        hbox.addWidget(self.BoutonExit)

        hbox.addStretch(1)

        hbox.addWidget(self.BoutonSubmit)

        layout.addWidget(self.credits)

        layout.addStretch(1)
        layout.addLayout(hbox)

        self.setLayout(layout)
        self.setWindowTitle('Chelpipe Group - Electrical Consumption Forecaster - Release 1.0 - August 2019')

    def MessageError(self):
        message = QMessageBox()
        message.setText("<b>Invalid value entered</b>")
        message.setInformativeText("Please enter a value with the correct type expected")
        message.setWindowTitle("Alert message")
        message.setStandardButtons(QMessageBox.Ok)
        message.exec()
        
    def CalculPrediction(self):
        # Zone de récup des var de saisies
        self.ValDiam = self.ChampDiam.text()
        self.ValThick = self.ChampThick.text()
        self.ValSteel = self.combo.currentText()
        self.ValWeight = self.ChampWeight.text()
        self.ValLen = self.ChampLen.text()
        self.ValNum = self.ChampNum.text()
        self.ValMonth = self.comboMonth.currentIndex() + 1

        # Test de verification des var de saisies
        try:
            self.ValDiam = float(self.ValDiam)
        except:
            self.MessageError()
            self.ValDiam = "LOLO <3"
            return app.exec_()

        try:
            self.ValThick = float(self.ValThick)
        except:
            self.MessageError()
            self.ValThick = "LOLO <3"
            return app.exec_()

        try:
            self.ValSteel = str(self.ValSteel)
        except:
            self.MessageError()
            self.ValSteel = "LOLO <3"
            return app.exec_()

        try:
            self.ValWeight = float(self.ValWeight)
        except:
            self.MessageError()
            self.ValWeight = "LOLO <3"
            return app.exec_()

        try:
            self.ValLen = float(self.ValLen)
        except:
            self.MessageError()
            self.ValLen = "LOLO <3"
            return app.exec_()

        try:
            self.ValNum = float(self.ValNum)
        except:
            self.MessageError()
            self.ValNum = "LOLO <3"
            return app.exec_()

        try:
            self.ValMonth = float(self.ValMonth)
        except:
            self.MessageError()
            self.ValMonth = "LOLO <3"
            return app.exec_()

        # Appel de la class calcul
        ElecConsoInput = Prediction.DD(self, self.ValDiam, self.ValThick, self.ValSteel, self.ValWeight, self.ValLen, self.ValNum, self.ValMonth)

# Création de la fenetre et de l'app
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

fen = Fenetre()
fen.show()
fen.setGeometry(300, 300, 570, 250)
fen.setWindowIcon(QtGui.QIcon("89001_big.ico"))
app.exec_()
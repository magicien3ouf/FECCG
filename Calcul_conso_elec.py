import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt
import catboost
from datetime import datetime
import pickle
from forecasting import *

class Prediction:
  """ Ici on récup les feat de l'user pour determiner avec les models des machines des diff point de prod de l'usine
   la valeur de conso elec de chacune des machine """

  def __init__(self): # Notre méthode constructeur qui appel la méthode DD
      self.DD()
  def DD(self, ValDiam, ValThick, ValSteel, ValWeight, ValLen, ValNum, ValMonth):
      self.ValDiam = ValDiam
      self.ValThick = ValThick
      self.ValSteel = ValSteel
      self.ValWeight = ValWeight
      self.ValLen = ValLen
      self.ValNum = ValNum
      self.ValMonth = ValMonth

      Lvalues = [ValDiam, ValThick, ValSteel, ValWeight, ValLen, ValNum, ValMonth]

      # Creation d'un dataframe a partir des val saisi par user
      Lcol = ['diameter', 'thickness', 'steel_type', 'weight', 'length', 'numbers', 'month']  # 7 features
      dfpipe = pd.DataFrame([[ValDiam, ValThick, ValSteel, ValWeight, ValLen, ValNum, ValMonth]], columns=Lcol)
      dfpipe.info()

      # Import du doc d'analyse des donnees portant sur les diff machine
      data = pd.read_csv('featuresToDrop-resultOfPredictionsV3.csv')
      data.info()

      # Recup les diff feat a supp par rapport au diff machines
      LLdropAnalized = []
      for i, elm in enumerate(data['LdropAnalized']):
          LLdropAnalized.append(elm.split(','))

      # Recup les diff dataframe avec les feat adapter en fonction des feat supp
      LpipeFiltered = []
      for LuselessFeatures in LLdropAnalized:
          LpipeFiltered.append( dfpipe.drop(LuselessFeatures, axis=1))

      Lmodels = []

      f = open('FILES_TXT/models.txt', 'r')
      for l in f:
          Lmodels.append(l.strip('\n'))
      f.close()

      Lconsprocess = forecasting( Lmodels, LpipeFiltered )

      LConso = [62.243757431629, 63.7526753864447, 56.2687277051129, 48.0142687277051, 45.602853745541, 46.1771700356718, 45.2140309155767, 46.4696789536266, 51.0107015457788, 55.1914387633769, 61.3448275862069]
      ConsProcess0 = LConso[int(ValMonth) - 1]

      Lconsprocess.insert(0, np.array([ConsProcess0]))

      ConsTot = sum([sum(process) for process in Lconsprocess])

      Lpercentprocess = RelPercentList(Lconsprocess, ConsTot)

      Lprocess = readlinesFile('FILES_TXT/processEN.txt')

      Lprocess.insert(0, '0-Ventilation, Heating, etc...')

      dfPrediction = pd.DataFrame(columns = ['Process', 'Consumption(%)', 'Consumption(kWh)', '', 'Feature','Values'])

      dfPrediction['Process'] = Lprocess
      dfPrediction['Consumption(%)'] = Lpercentprocess*ConsTot/ConsTot
      dfPrediction['Consumption(kWh)'] = Lpercentprocess*ConsTot/100
      dfPrediction['Feature'] = ['Diameter', 'Thickness', 'steel_type', 'Weight', 'Length', 'Numbers', 'Month'] + ['']*5
      dfPrediction['Values'] = Lvalues + ['']*5

      dfPrediction = dfPrediction.append(pd.DataFrame({'Process':['Total'],
                         'Consumption(%)':[100],
                         'Consumption(kWh)':[float(ConsTot)],
                         '': [' '],
                         'Feature': ['Predictions date'],
                         'Values': [datetime.now().strftime('%d.%m.%Y %H:%M:%S')]
                        }), ignore_index=True)

      if self.cb.isChecked() == True:
          dfPrediction.to_csv('prediction.csv', encoding='utf-8-sig')
      for i,process in enumerate(Lprocess):
          Lprocess[i] += ' ' + str(round(float(sum(Lconsprocess[i])),2)) + ' kWh'

      labels = Lprocess
      sizes = Lpercentprocess

      colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
      explode = (0.1, 0, 0, 0, 0.05, 0, 0, 0, 0, 0, 0, 0)

      plt.pie(sizes, explode=explode, labels=labels, colors=colors,
              autopct='%1.1f%%', shadow=True, startangle=140, labeldistance=1.05, center=(0,-8))

      plt.axis('equal')
      plt.title('Pie chart of all relative consumptions\nof the 11 industrial processes\nTotal consumption : ' + str(round(float(ConsTot), 4)) + ' kWh')
      plt.show()
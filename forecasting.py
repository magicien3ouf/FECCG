import pickle
from catboost import CatBoostRegressor
def forecasting(Lmodels, LpipeFiltered):
    path = 'MODELS/'
    Lprocess = [3, 2, 2, 12, 1, 4, 2, 11, 7, 2, 3]
    LconsProcess = []
    Lpred = []
    index = Lprocess[0] - 1
    nb = 0

    for i, model in enumerate(Lmodels):
        if i > index:
            if not nb >= 10:
                index += Lprocess[nb + 1]
            LconsProcess.append(Lpred)
            nb += 1
            Lpred = []

        if i == len(LpipeFiltered) - 1:
            LconsProcess.append(Lpred)

        if 'LR' in model:
            load_lr_model = pickle.load(open(path + model, 'rb'))
            y_load_predict = load_lr_model.predict(LpipeFiltered[i].drop('steel_type', axis=1))

        else:
            regressor = CatBoostRegressor()
            regressor.load_model(path + model, format='cbm')
            y_load_predict = regressor.predict(LpipeFiltered[i])

        Lpred.append(y_load_predict)

    return LconsProcess

def RelPercentList(L, sumToCompare):
    LrelPercent=[]
    for elt in L:
        LrelPercent.append(100 * sum(elt) / sumToCompare)
    return LrelPercent

def readlinesFile(relPath):
    L=[]
    f = open(relPath, 'r', encoding='utf-8-sig')
    for l in f:
        L.append(l.strip('\n'))
    f.close()
    return L
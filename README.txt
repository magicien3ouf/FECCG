This README will guide you through the setup of the program.

1) Install all the required libraries to run the program:
	- pandas		(deals with dataframes)
	- CatBoost 		(to load the CB models)
	- pickle		(to load the Linear Regressions models)
	- PyQt5 		(Gui)
	- numpy
	- datetime
	- matplotlib.pyplot

using the script 'install.bat' or manually with 'pip install XXX' for all missing modules.

2) Run 'main.py' using python 3.XX

3) Input the features of the pipe and the month and click submit to make predictions.

4) Output :
	- a pie chart showing the consumption of the 11 processes of the plant
	- prediction.csv, a file showing the results and the features in input, in this folder. (only if checkbox checked)

REQUIRED FILES :
	- MODELS, contains the 49 models, one per machine, 13 catboost, 36 linear regression models
	- FILES_TXT, contains two .txt files, one listing model name, one listing process name
	- featuresToDrop-resultOfPredictionsV3.csv, where we analyzed the features to drop. I think this file can be very useful for you.

Without these files, this program cannot run.

Written the Monday 12th August 2019 by Alexis Mourlon exclusively for Chelpipe Group.
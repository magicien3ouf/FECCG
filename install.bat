@echo off

echo This little script install all the modules you need to run the program.
echo Python need of course to be intalled.
echo Here is the list of the modules required :
echo.
echo  -pandas		(deals with dataframes)
echo  -CatBoost 		(to load the CB models)
echo  -pickle		(to load the Linear Regressions models)
echo  -PyQt5 		(Gui)
echo  -numpy
echo  -datetime
echo  -matplotlib.pyplot 
echo.

SET /P _inputname= Do you have pip installed on your computer ? (y/n)

IF "%_inputname%"=="n" GOTO:pipinstall
GOTO:end
:PIPINSTALL
echo Installing pip
python get-pip.py

:END
echo Installing all the modules
pip install matplotlib.pyplot
pip install datetime
pip install CatBoost
pip install pandas
pip install pickle
pip install numpy
pip install PyQt5
echo Modules hopefully sucessfully installed !
pause
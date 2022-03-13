from numpy import linspace
from UltraClass import UltraClass
import matplotlib.pyplot as pyplot
import os
import numpy as np
 
# Eingaben: Dateiname, Anzahl Windows, Treshold
filename = r'Probedaten/Hirnet_subsample/Hirnet4_S4.subsample.csv'  # Probedaten/Beispiesamples/Mail_lutz_3/verschobeneDatensätze/verschoben_0.2_5000_4.0_0.0,0.0_pos.csv' #Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_.20000,.40000_pos.csv #Probedaten/Beispiesamples/Mail_lutz_3/verschobeneDatensätze/verschoben_0.2_5000_4.0_0.0,0.0_pos.csv #Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_.20000,.40000_pos.csv
readsPerWindow = 100  # Wieviele Reads in einem Window erwartet werden sollen, Windowanzahl passt sich der Datensatzgröße dynamisch an.
start = 0
end = 1
thresholdLuecke = 1
thresholdUeberschuss = 1
wachstumsdiagramme = True  # True-> Wachstumsdiagramme werden angezeigt
createFiles = False  # Ob BetterDataset/AnalyseReads -Dateien erstellt werden sollen
windowQuality = False  # Ob die Windowqualität ermittelt werden soll
legende = False # Ob die Legende bei jedem Graphen angezeigt werden soll

# Erstellung der Wachstumsdiagramme
folderPosFiles = os.listdir("./Probedaten/Beispiesamples/Mail_lutz_3/5000")  # ./Probedaten/Beispiesamples/Mail_lutz_3/testdateienLücken || ./Probedaten/Beispiesamples/Mail_lutz_3/5000
folderPosFiles.sort()
regressionList = []
vectorsList = []
filledGapsList = []
filledEllipseList = []
steigungList = []
xValuesList = []
yValuesList = []
wachstumsratenList = []
relEaListWachstum = []
xListWachstum=[]
for file in folderPosFiles:
    ultraClass = UltraClass("Probedaten/Beispiesamples/Mail_lutz_3/5000/"+str(file), 10, -1, readsPerWindow)
    if len(folderPosFiles) == 3:
        wachstumsratenList.append(str(file[6]))
    elif len(folderPosFiles) == 7:
        wachstumsratenList.append(str(file[5]))
    else:
        print('[WARNING] anderen Ordner für die Wachstumsdiagramme verwenden!')

    datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage = ultraClass.readFile()
    degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcDegreeDifferences(datasetList)
    gapBereiche = ultraClass.determineGapsThresholdFunktion(relEaList, xList)[0]
    linReg1, linReg2, filledGaps, predictedValues, steigung, modelLinReg = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
    windowAbwDict = ultraClass.createOutputFiles(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict)
    regressionList.append([linReg1, linReg2])
    filledGapsList.append(filledGaps)
    # liste2.append([xVectors, yVectors])
    xValuesRegression, yValuesRegression = ultraClass.calcDataFromRegression(linReg1[1])
    xValuesList.append(xValuesRegression)  # gute Bezeichner!
    yValuesList.append(yValuesRegression)
    steigungList.append(steigung)
    relEaListWachstum.append(relEaList)
    xListWachstum.append(xList)
    # filledEllipseListe.append(filledEllipse)


# Beginn der eigentlichen Datenbehandlung
# Erstellung des Haupt-UltraClass-Objekts
ultraClass = UltraClass(filename, thresholdLuecke, -thresholdUeberschuss, readsPerWindow)

# Erste Ermittlung aller wichtigen Daten nach Auslesen des Datensatzes
datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage = ultraClass.readFile()

degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcDegreeDifferences(datasetList)
gapBereiche = ultraClass.determineGapsThresholdFunktion(relEaList, xList)[0]
linReg1, linReg2, filledGaps, predictedValues, steigung, modelLinReg = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram, start, end)
readAbweichungProWindow = ultraClass.windowQualität(readsPerSectionDict)
windowAbwDict, betterDataFileName = ultraClass.createOutputFiles(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, createFiles)
growthVector0 = ultraClass.calcGrowthVector(xVectors, yVectors, [0, 0.1])
rNormalisiert, theta = ultraClass.calcVectorplotPolar(readAmountPerSection, steigung)
fehlerVariableSteigung = (abs(steigung[0])-abs(steigung[1]))
print("FehlerVariableSteigung: " + str(fehlerVariableSteigung))

if wachstumsdiagramme:
    # Die entstandene Form wird an den Wachstumsdiagrammen angepasst
    xVectors, yVectors, linReg1, linReg2, predictedValues, steigung = ultraClass.kalibrieren(xVectors, yVectors, list(linReg1), list(linReg2), modelLinReg, predictedValues) 
    #wachstumsrateDiff = ultraClass.calcGrowthStreuungGraphen(xVectors, yVectors, xValuesList, yValuesList)
    #print("Wachstumrate Differenz: " + str(wachstumsrateDiff))

assumedGrowth = round(ultraClass.calcGrowthSteigung(steigung)[0])
for i in range(1):
    finalFileName = ultraClass.iterativGapFilling(filename, relEaListWachstum, xListWachstum, thresholdLuecke, thresholdUeberschuss, 1, ultraClass, assumedGrowth)


# Wachstumsrate wird über Standardabweichung bestimmt, zur Verfeinerung des Ergebnisses
# wird der ausgebesserte Datensatz ein zweites mal analysiert.
if createFiles:
    reAnalyse = UltraClass(betterDataFileName, thresholdLuecke, -thresholdUeberschuss, readsPerWindow)
    reDatasetList = reAnalyse.readFile()
    reDegreeDiffList, reXList, reAvg, reStandardAbw, reRelEaList = reAnalyse.calcDegreeDifferences(reDatasetList[0])
    # print(f"Zweite Standardardabweichung: {reStandardAbw}")
    growth = reAnalyse.calcGrowthStabw(datasetList, reStandardAbw)
    print(f"Wachstumsrate Stabw: {growth}")


print(f"Wachstumsrate Steigung: {ultraClass.calcGrowthSteigung(steigung)}")
print(f"Wachstumsrate V0: {growthVector0}")

# --------------------Plotting--------------------

# #####################################################################
# # Readamount per Section, mit eingezeichneten linearen Regressionen #
# #####################################################################
pyplot.figure(num='Readamount pro Window')
if wachstumsdiagramme:
    i = 0
    # Lineare Regressionen der jeweiligen Wachstumsraten
    for item in regressionList:
        pyplot.plot(item[0][0], item[0][1], color='black', label=steigungList[i][0])
        pyplot.plot(item[1][0], item[1][1], color='black', label=steigungList[i][1])
        i += 1

# Daten der Readamount per Section
pyplot.plot(xAxisDiagram, readAmountPerSection, color='blue', label='gemessener readAmountPerSection')
# Gefüllte Lücken
pyplot.plot(filledGaps[0], filledGaps[1], ".", color='red', label='vermuteter ReadAmountPerSection')
# Lineare Regressionen
pyplot.plot(linReg1[0], linReg1[1], color='green', label=('linReg 1 ' + str(int(steigung[0]))))
pyplot.plot(linReg2[0], linReg2[1], color='green', label=('linReg 2 ' + str(int(steigung[1]))))
# ggf. Windowqualität
if windowQuality:
    pyplot.plot(xAxisDiagram, readAbweichungProWindow, color='purple', label='Windowqualität')
if legende:
    pyplot.legend()
pyplot.xlabel("Position")
pyplot.ylabel("Anzahl pro Ausschnitt")

# #################################################
# # Readamount per Section, mit Relativer Y-Skala #
# #################################################
"""
pyplot.figure(num='Relative Reads pro Abschnitt')
pyplot.plot(xAxisDiagram, readAmountPerSectionPercentage, color='blue', label='gemessener readAmountPerSection')
pyplot.xlabel("Position")
pyplot.ylabel("Prozent an Reads")
"""

# ##########################
# # Winkeldifferenzengraph #
# ##########################
pyplot.figure(num='Winkeldifferenzengraph')
# Winkeldifferenzen
pyplot.plot(xList, degreeDiffList, label='Winkeldifferenz in Grad')
# Relative Einzelabweichung
pyplot.plot(xList, relEaList, label='Relativer Abstand einer Differenz vom\nDurchschnitt (Relative Einzelabweichung)')
# Durchschnitt
pyplot.plot(xList, [avg] * len(xList), label='Durschnittswert')
# Schwellenwert Lücke (Threshold)
pyplot.plot(xList, [thresholdLuecke] * len(xList), label='Lücke')
# Schwellenwert Überschuss (Threshold)
pyplot.plot(xList, [thresholdUeberschuss] * len(xList), label='Überschuss')
"""fn1 = thresholdFunktion[0](np.linspace(0, 0.5, 50))
fn2 = thresholdFunktion[1](np.linspace(0.5, 1, 50))
thresholdFunktion = np.concatenate((fn1, fn2), axis=0)
pyplot.plot(np.linspace(0, 1, 100), thresholdFunktion)"""

pyplot.title(f"Messabstand: {ultraClass.getReadsPerWindow()}; Standardabw: {standardAbw} Durchschn: {avg};")
pyplot.xlabel("Position")
pyplot.ylabel("Differenz der Winkel")
if legende:
    pyplot.legend()

#print(' '.join(str(i)+" " for i in relEaList[:len(relEaList)//2]))

#print(' '.join(str(i)+" " for i in xList[:len(xList)//2]))

#print(xList[:len(xList)//2])
#print(relEaList[:len(relEaList)//2])
# #########################################
# # Vektorengraph inkl. Wachstumsdigramme #
# #########################################
pyplot.figure(num='Vektorengraph')
# ggf. Wachstumsdigramme
if wachstumsdiagramme:
    for i in range(len(xValuesList)):
        pyplot.plot(xValuesList[i], yValuesList[i], label='Wachstumsrate: '+str(wachstumsratenList[i]))
if legende:
    pyplot.legend()

# Vektorenpunkte
pyplot.plot(xVectors, yVectors, '.', color='blue')
# Verbesserte Vektorenpunkte
pyplot.plot(predictedValues[0], predictedValues[1], '.', color='red')

pyplot.plot([0], [0], 's', color='black')
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(True, which='both')
pyplot.axhline(y=0, color='k')
pyplot.axvline(x=0, color='k')

# #############
# # Gaußkurve #
# #############
"""if wachstumsdiagramme:
    pyplot.figure(num='Gaußkurve')
    pyplot.hist(gaußList[wachstumsrateDiff-2], bins=10)
"""
pyplot.show()

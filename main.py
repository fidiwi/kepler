from UltraClass import UltraClass
import matplotlib.pyplot as pyplot
import os

# Eingaben: Dateiname, Abzahl Windows, Treshold
filename= 'Output/BackMovedDataset/backMovedDataset_0.2_verschoben_0.2_5000_4.0_0.0,0.0_pos.csv' #Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_.20000,.40000_pos.csv #Probedaten/Beispiesamples/Mail_lutz_3/verschobeneDatensätze/verschoben_0.2_5000_4.0_0.0,0.0_pos.csv
readsPerWindow = 100 # Wieviele Reads in einem Window erwartet werden sollen, Windowanzahl passt sich der Datensatzgröße dynamisch an. 
thresholdLuecke = 1
thresholdUeberschuss = -1
wachstumsdiagramme = True # True-> Wachstumsdiagramme werden angezeigt
createFiles = True

# Wachstumsdiagramme!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if wachstumsdiagramme:
    folderPosFiles = os.listdir("./Probedaten/Beispiesamples/Mail_lutz_3/testdateienLücken") # ./Probedaten/Beispiesamples/Mail_lutz_3/testdateienLücken || ./Probedaten/Beispiesamples/Mail_lutz_3/5000 Achtung: int(anzahlWindows/2)
    liste = []
    liste2 = []
    filledGapsListe = []
    filledEllipseListe = []
    xValuesList = []
    yValuesList = []
    for file in folderPosFiles:
        ultraClass = UltraClass("Probedaten/Beispiesamples/Mail_lutz_3/testdateienLücken/"+str(file), thresholdLuecke, thresholdUeberschuss, readsPerWindow)
        datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage = ultraClass.readFile()
        degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList)
        gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
        linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
        windowAbwDict = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict)
        liste.append([linReg1, linReg2])
        filledGapsListe.append(filledGaps)
        #liste2.append([xVectors, yVectors])
        xValuesL, yValuesL = ultraClass.idealeEllipse(linReg1[1])
        xValuesList.append(xValuesL)
        yValuesList.append(yValuesL)
        #filledEllipseListe.append(filledEllipse)

"Main!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
ultraClass = UltraClass(filename, thresholdLuecke, thresholdUeberschuss, readsPerWindow)

# für die originale Datei werden die Daten für die Diagramme bestimmt
datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage = ultraClass.readFile()
degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList)
gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
windowAbwDict, betterDataFileName = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, createFiles)
#--------------------Wachstumsrate Enno--------------------
ultraClass.calcGrowthVector(2, linReg1[1])
#readAbweichungProWindow = ultraClass.windowQualität(readsPerSectionDict)


# die Standardabweichung wird von der neue erstellte Datei bestimmt 
if createFiles:
    reAnalyse = UltraClass(betterDataFileName, thresholdLuecke, thresholdUeberschuss, readsPerWindow)
    reDatasetList = reAnalyse.readFile()
    reDegreeDiffList, reXList, reAvg, reStandardAbw, reRelEaList = reAnalyse.calcWinkel(reDatasetList[0])
    print(f"Zweite Standardardabweichung: {reStandardAbw}")
    growth = reAnalyse.calcGrowth(datasetList, reStandardAbw)
    print(f"Wachstumsrate: {growth}")


#print (windowAbwDict)
#print (gapBereiche)

#--------------------Plotting--------------------
#Readamount pro Window, mit LinRegs
pyplot.figure(num='Readamount pro Window')
if wachstumsdiagramme:
    for item in liste:
        pyplot.plot(item[0][0], item[0][1], color='black')
        pyplot.plot(item[1][0], item[1][1], color='black')

pyplot.plot(xAxisDiagram, readAmountPerSection, color='blue', label='gemessener readAmountPerSection')
pyplot.plot(filledGaps[0], filledGaps[1], ".", color='red', label='vermuteter ReadAmountPerSection')
pyplot.plot(linReg1[0], linReg1[1], color='green', label='linReg 1')
pyplot.plot(linReg2[0], linReg2[1], color='green', label='linReg 2')

#    pyplot.plot(xAxisDiagram, readAbweichungProWindow, color='purple', label='Windowqualität')
pyplot.legend()
pyplot.xlabel("Position")
pyplot.ylabel("Anzahl pro Ausschnitt")

pyplot.figure()
pyplot.plot(xAxisDiagram, readAmountPerSectionPercentage, color='blue', label='gemessener readAmountPerSection')
pyplot.title("Relative Reads pro Abschnitt")
pyplot.xlabel("Position")
pyplot.ylabel("Prozent an Reads")

#Winkeldifferenzgraph
pyplot.figure(num='Winkeldifferenzengraph')
pyplot.plot(xList, degreeDiffList, label='Winkeldifferenz in Grad')
pyplot.plot(xList, relEaList, label='Relative Einzelabweichung der Ausschnitte vom Durchschnittswert')
pyplot.plot(xList, [avg] * len(xList), label='Durschnittswert')
pyplot.plot(xList, [standardAbw] * len(xList), label='Standartabweichung')
pyplot.title(f"Abstand = {degreeDiffList[1] - degreeDiffList[0]}; Standardabw: {standardAbw} Durchschn: {avg};")
pyplot.xlabel(f"Reads (sortiert)")
pyplot.ylabel("Differenz der Winkel")
pyplot.legend()

#Vektorengraph
pyplot.figure(num='Vektorengraph')
if wachstumsdiagramme:
    for i in range(len(xValuesList)):
        pyplot.plot(xValuesList[i], yValuesList[i])

pyplot.plot(xVectors, yVectors, '.', color='blue')
pyplot.plot(filledEllipse[0], filledEllipse[1], '.', color='orange')
pyplot.plot([0], [0], 's', color='r')
#pyplot.plot([m[0]], [m[1]], 'v', color='green')
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)

pyplot.show()
from UltraClass import UltraClass
import matplotlib.pyplot as pyplot
import os

# Eingaben: Dateiname, Abzahl Windows, Treshold
filename = 'Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_0,.10000_.90000,1_pos.csv'
anzahlWindows = 250 #250 bei den Code weiter unten l.38
thresholdLuecke = 1
thresholdUeberschuss = -1

ultraClass = UltraClass(filename, thresholdLuecke, thresholdUeberschuss)

# für die originale Datei werden die Daten für die Diagramme bestimmt
datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClass.readFile(anzahlWindows)
degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList, anzahlWindows)
gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
windowAbwDict, betterDataFileName = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, anzahlWindows)

# die Standardabweichung wird von der neue erstellte Datei bestimmt 
reAnalyse = UltraClass(betterDataFileName, thresholdLuecke, thresholdUeberschuss)
reDatasetList = reAnalyse.readFile(anzahlWindows)
reDegreeDiffList, reXList, reAvg, reStandardAbw, reRelEaList = reAnalyse.calcWinkel(reDatasetList[0], anzahlWindows)
print(f"Zweite Standardardabweichung: {reStandardAbw}")

"""
# alle Daten in den Output-Ordner werden gelöscht
folderPosFiles = os.listdir("./Output/AnalyseReads") #alle erstellten Dateien werden gelöscht
for file in folderPosFiles:
    os.remove("./Output/AnalyseReads/"+str(file))

folderPosFiles = os.listdir("./Output/BetterDataset")
for file in folderPosFiles:
    os.remove("./Output/BetterDataset/"+str(file))
"""
"""
# die Daten mit den Lücken werden untersucht und werden in den AnalyseReads gespeichert
folderPosFiles = os.listdir("./Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent")
for file in folderPosFiles:
    ultraClass = UltraClass("Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/"+str(file), thresholdLuecke, thresholdUeberschuss)
    datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClass.readFile(anzahlWindows)
    degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList, anzahlWindows)
    gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
    linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
    windowAbwDict = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, anzahlWindows)

# die Daten mit den Überschuss werden untersucht und werden in den AnalyseReads gespeichert
thresholdLuecke = 100
thresholdUeberschuss = -0.2 # sonst funktioniert es nicht!!!
folderNegFiles = os.listdir("./Probedaten/Beispiesamples/Mail_lutz_3/neg_samples/20_percent")
for file in folderNegFiles:
    ultraClass = UltraClass("Probedaten/Beispiesamples/Mail_lutz_3/neg_samples/20_percent/"+str(file), thresholdLuecke, thresholdUeberschuss)
    datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClass.readFile(anzahlWindows)
    degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList, anzahlWindows)
    gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
    linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
    windowAbwDict = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, anzahlWindows)

# eine Liste mit den AnalyseReads wird erstellt
folderAnalyseReads = os.listdir("./Output/AnalyseReads")
ultraReadsList = []
for file in folderAnalyseReads:
    ultraClass = UltraClass("Output/AnalyseReads/"+str(file), thresholdLuecke, thresholdUeberschuss)
    ultraReadsList.append(ultraClass.calcMatchingReads())

# für die letze Datei werden die fehlende Reads gesucht 
foundFiles = []
readList = []
for searchedWindows in ultraReadsList[-1]:
    temp = searchedWindows[1]
    posListReads =[]
    for i in range(len(ultraReadsList)):
        for reads in ultraReadsList[i]:
            if searchedWindows[0] == reads[0] and reads[1] > 0:
                posListReads.append(i)
                temp += reads[1]
    
    if len(posListReads) > 0:
        foundFiles.append(posListReads)
    i+=1

    readList.append(temp)
    if temp > 0:
        print("Read gefunden!")
    else:
        print("Read nicht gefunden!")

print(foundFiles) # in welche Dateien welche Reads gefunden wurden
print(readList) # wie viel insgesamt gefunden wurde
print(ultraReadsList[-1])
"""

#print (windowAbwDict)
#print (gapBereiche)

#Readamount pro Window, mit LinRegs
pyplot.figure(num='Readamount pro Window')
pyplot.plot(xAxisDiagram, readAmountPerSection)
pyplot.plot(linReg1[0], linReg1[1])
pyplot.plot(linReg2[0], linReg2[1])
pyplot.plot(filledGaps[0], filledGaps[1], ".")
pyplot.xlabel("Position")
pyplot.ylabel("Anzahl pro Ausschnitt")

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
pyplot.plot(xVectors, yVectors, '.')
pyplot.plot(filledEllipse[0], filledEllipse[1], '.', color='orange')
pyplot.plot([0], [0], 's', color='r')
#pyplot.plot([m[0]], [m[1]], 'v', color='green')
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)

pyplot.show()
from UltraClass import UltraClass
import matplotlib.pyplot as pyplot
import os
import math

# Eingaben: Dateiname, Abzahl Windows, Treshold
filename= 'Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_4.0_20_.20000,.40000_pos.csv' #Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_.20000,.40000_pos.csv
readsPerWindow = 50 # Wieviele Reads in einem Window erwartet werden sollen, Windowanzahl passt sich der Datensatzgröße dynamisch an.
thresholdLuecke = 1
thresholdUeberschuss = -1
wachstumsdiagramme = False # True-> Wachstumsdiagramme werden angezeigt
windowsSuche = False # True-> Windowssuche wird durchgeführt
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
        datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClass.readFile(readsPerWindow)
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
datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClass.readFile()
degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList)
gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
windowAbwDict, betterDataFileName = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, createFiles)
#readAbweichungProWindow = ultraClass.windowQualität(readsPerSectionDict)


# die Standardabweichung wird von der neue erstellte Datei bestimmt 
if createFiles:
    reAnalyse = UltraClass(betterDataFileName, thresholdLuecke, thresholdUeberschuss, readsPerWindow)
    reDatasetList = reAnalyse.readFile()
    reDegreeDiffList, reXList, reAvg, reStandardAbw, reRelEaList = reAnalyse.calcWinkel(reDatasetList[0])
    print(f"Zweite Standardardabweichung: {reStandardAbw}")
    growth = reAnalyse.calcGrowth(datasetList, reStandardAbw)
    print(f"Wachstumsrate: {growth}")


if windowsSuche:
    windowsSucheEineDatei = False # True -> nur für eine spezielle Datei!

    # alle Daten in den Output-Ordner werden gelöscht
    folderPosFiles = os.listdir("./Output/AnalyseReads") #alle erstellten Dateien werden gelöscht
    for file in folderPosFiles:
        os.remove("./Output/AnalyseReads/"+str(file))

    folderPosFiles = os.listdir("./Output/BetterDataset")
    for file in folderPosFiles:
        os.remove("./Output/BetterDataset/"+str(file))

    # die Daten mit den Lücken werden untersucht und werden in den AnalyseReads gespeichert
    folderPosFiles = os.listdir("./Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent")
    for file in folderPosFiles:
        ultraClass = UltraClass("Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/"+str(file), thresholdLuecke, thresholdUeberschuss, readsPerWindow)
        datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClass.readFile()
        degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList)
        gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
        linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
        windowAbwDict = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict)

    # die Daten mit den Überschuss werden untersucht und werden in den AnalyseReads gespeichert
    thresholdLuecke = 100
    thresholdUeberschuss = -0.2 # sonst funktioniert es nicht!!!
    folderNegFiles = os.listdir("./Probedaten/Beispiesamples/Mail_lutz_3/neg_samples/20_percent")
    for file in folderNegFiles:
        ultraClass = UltraClass("Probedaten/Beispiesamples/Mail_lutz_3/neg_samples/20_percent/"+str(file), thresholdLuecke, thresholdUeberschuss, readsPerWindow)
        datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClass.readFile()
        degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList)
        gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
        linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
        windowAbwDict = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict)

    # eine Liste mit den AnalyseReads wird erstellt
    folderAnalyseReads = os.listdir("./Output/AnalyseReads")
    ultraReadsList = []
    for file in folderAnalyseReads:
        ultraClass = UltraClass("Output/AnalyseReads/"+str(file), thresholdLuecke, thresholdUeberschuss, readsPerWindow)
        ultraReadsList.append(ultraClass.windowsSucheOpenFile())
    if windowsSucheEineDatei:
        # für die letze Datei werden die fehlende Reads gesucht
        fileNumber = -1
        foundFiles = []
        readList = []
        for searchedWindows in ultraReadsList[fileNumber]:
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
        print(ultraReadsList[fileNumber])

    else:
        # für alle Datei werden die fehlende Reads gesucht 
        #**************************************************************************************
        # !!! Sollte hier eventuell anzahlWindows durch readsPerWindow ersetzt werden?  !!!
        #**************************************************************************************
        anzahlWindows = ultraClass.getAnzahlWindows()
        fileNameWindowsSuche ="WindowsSucheTestDatei_"+str(anzahlWindows)+".csv"
        ultraClass.calcMatchingReads(ultraReadsList, folderAnalyseReads, fileNameWindowsSuche)


#print (windowAbwDict)
#print (gapBereiche)

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
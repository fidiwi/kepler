from UltraClass import UltraClass
import os

windowsSucheEineDatei = False # True -> nur für eine spezielle Datei!
readsPerWindow = 100 # Wieviele Reads in einem Window erwartet werden sollen, Windowanzahl passt sich der Datensatzgröße dynamisch an.
thresholdLuecke = 1
thresholdUeberschuss = -1


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
    ultraClassUeberschuss = UltraClass("Probedaten/Beispiesamples/Mail_lutz_3/neg_samples/20_percent/"+str(file), thresholdLuecke, thresholdUeberschuss, readsPerWindow)
    datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClassUeberschuss.readFile()
    degreeDiffList, xList, avg, standardAbw, relEaList = ultraClassUeberschuss.calcWinkel(datasetList)
    gapBereiche = ultraClassUeberschuss.determineGaps(relEaList, datasetList)
    linReg1, linReg2, filledGaps, filledEllipse = ultraClassUeberschuss.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
    windowAbwDict = ultraClassUeberschuss.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict)

# eine Liste mit den AnalyseReads wird erstellt
folderAnalyseReads = os.listdir("./Output/AnalyseReads")
ultraReadsList = []
for file in folderAnalyseReads:
    ultraClassAnalyse = UltraClass("Output/AnalyseReads/"+str(file), thresholdLuecke, thresholdUeberschuss, readsPerWindow)
    ultraReadsList.append(ultraClassAnalyse.windowsSucheOpenFile())
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
    print(anzahlWindows)
    fileNameWindowsSuche ="WindowsSucheTestDateiNeu_"+str(anzahlWindows)+".csv"
    ultraClass.calcMatchingReads(ultraReadsList, folderAnalyseReads, fileNameWindowsSuche)
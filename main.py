from UltraClass import UltraClass
import matplotlib.pyplot as pyplot
import os
import math

# Eingaben: Dateiname, Abzahl Windows, Treshold
filename= 'Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_.40000,.60000_pos.csv' #Probedaten/Beispiesamples/Mail_lutz_3/verschobeneDatensätze/verschoben_0.2_5000_4.0_0.0,0.0_pos.csv' #Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_.20000,.40000_pos.csv #Probedaten/Beispiesamples/Mail_lutz_3/verschobeneDatensätze/verschoben_0.2_5000_4.0_0.0,0.0_pos.csv #Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_.20000,.40000_pos.csv
readsPerWindow = 50 # Wieviele Reads in einem Window erwartet werden sollen, Windowanzahl passt sich der Datensatzgröße dynamisch an. 
thresholdLuecke = 1
thresholdUeberschuss = 1
wachstumsdiagramme = True # True-> Wachstumsdiagramme werden angezeigt
createFiles = True
windowQualität = False

# Wachstumsdiagramme!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if wachstumsdiagramme:
    folderPosFiles = os.listdir("./Probedaten/Beispiesamples/Mail_lutz_3/5000") # ./Probedaten/Beispiesamples/Mail_lutz_3/testdateienLücken || ./Probedaten/Beispiesamples/Mail_lutz_3/5000
    folderPosFiles.sort()
    liste = []
    liste2 = []
    filledGapsListe = []
    filledEllipseListe = []
    steigungList = []
    xValuesList = []
    yValuesList = []
    wachstumsratenList = []
    for file in folderPosFiles:
        ultraClass = UltraClass("Probedaten/Beispiesamples/Mail_lutz_3/5000/"+str(file), 10, -1, readsPerWindow)
        if len(folderPosFiles) == 3:
            wachstumsratenList.append(str(file[6]))
        elif len(folderPosFiles) == 7:
            wachstumsratenList.append(str(file[5]))
        else:
            print('[WARNING] anderen Ordner für die Wachstumsdiagramme verwenden!')

        datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage = ultraClass.readFile()
        degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList)
        gapBereiche = ultraClass.determineGaps(relEaList, xList)
        linReg1, linReg2, filledGaps, filledEllipse, steigung = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
        windowAbwDict = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict)
        liste.append([linReg1, linReg2])
        filledGapsListe.append(filledGaps)
        #liste2.append([xVectors, yVectors])
        xValuesL, yValuesL = ultraClass.idealeEllipse(linReg1[1])
        xValuesList.append(xValuesL) #gute Bezeichner!
        yValuesList.append(yValuesL)
        steigungList.append(steigung)
        #filledEllipseListe.append(filledEllipse)

"Main!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
ultraClass = UltraClass(filename, thresholdLuecke, -thresholdUeberschuss, readsPerWindow)

# für die originale Datei werden die Daten für die Diagramme bestimmt
datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage = ultraClass.readFile()

degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList)
gapBereiche = ultraClass.determineGaps(relEaList, xList)
linReg1, linReg2, filledGaps, filledEllipse, steigung = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
readAbweichungProWindow = ultraClass.windowQualität(readsPerSectionDict)
windowAbwDict, betterDataFileName = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, createFiles)
ultraClass.calcGrowthVector(xVectors, yVectors,[0, 0.1])
fehlerVariabelSteigung = (abs(steigung[0])-abs(steigung[1]))
print("FehlerVariabelSteigung: " + str(fehlerVariabelSteigung))

for i in range(len(xValuesList)):
    xValuesList[i], yValuesList[i]= ultraClass.kalibrieren(xValuesList[i], yValuesList[i], xVectors, yVectors)

#--------------------Wachstumsrate Enno--------------------
#ultraClass.calcGrowthVector(xVectors, yVectors)



# die Standardabweichung wird von der neue erstellte Datei bestimmt 
if createFiles:
    reAnalyse = UltraClass(betterDataFileName, thresholdLuecke, -thresholdUeberschuss, readsPerWindow)
    reDatasetList = reAnalyse.readFile()
    reDegreeDiffList, reXList, reAvg, reStandardAbw, reRelEaList = reAnalyse.calcWinkel(reDatasetList[0])
    print(f"Zweite Standardardabweichung: {reStandardAbw}")
    growth = reAnalyse.calcGrowthStabw(datasetList, reStandardAbw)
    print(f"Wachstumsrate: {growth}")


#print (windowAbwDict)
print (gapBereiche)

#--------------------Plotting--------------------
#Readamount pro Window, mit LinRegs
pyplot.figure(num='Readamount pro Window')
if wachstumsdiagramme:
    for item in liste:
        pyplot.plot(item[0][0], item[0][1], color='black')
        pyplot.plot(item[1][0], item[1][1], color='black')

pyplot.plot(xAxisDiagram, readAmountPerSection, color='blue', label='gemessener readAmountPerSection')
pyplot.plot(filledGaps[0], filledGaps[1], ".", color='red', label='vermuteter ReadAmountPerSection')
pyplot.plot(linReg1[0], linReg1[1], color='green', label=('linReg 1 ' + str(int(steigung[0]))))
pyplot.plot(linReg2[0], linReg2[1], color='green', label=('linReg 2 ' + str(int(steigung[1]))))
if windowQualität:
    pyplot.plot(xAxisDiagram, readAbweichungProWindow, color='purple', label='Windowqualität')
pyplot.legend()
pyplot.xlabel("Position")
pyplot.ylabel("Anzahl pro Ausschnitt")

pyplot.figure(num='Relative Reads pro Abschnitt')
pyplot.plot(xAxisDiagram, readAmountPerSectionPercentage, color='blue', label='gemessener readAmountPerSection')
pyplot.xlabel("Position")
pyplot.ylabel("Prozent an Reads")

#Winkeldifferenzgraph
pyplot.figure(num='Winkeldifferenzengraph')
pyplot.plot(xList, degreeDiffList, label='Winkeldifferenz in Grad')
pyplot.plot(xList, relEaList, label='Relativer Abstand einer Differenz vom\nDurchschnitt (Relative Einzelabweichung)')
pyplot.plot(xList, [avg] * len(xList), label='Durschnittswert')
pyplot.plot(xList, [thresholdLuecke] * len(xList), label='Lücke')
pyplot.plot(xList, [thresholdUeberschuss] * len(xList), label='Überschuss')
pyplot.title(f"Messabstand: {ultraClass.getReadsPerWindow()}; Standardabw: {standardAbw} Durchschn: {avg};")
pyplot.xlabel(f"Position")
pyplot.ylabel("Differenz der Winkel")
pyplot.legend()

#Vektorengraph
pyplot.figure(num='Vektorengraph')
if wachstumsdiagramme:
    for i in range(len(xValuesList)):
        pyplot.plot(xValuesList[i], yValuesList[i], label='Wachstumsrate: '+str(wachstumsratenList[i]))
    pyplot.legend()

pyplot.plot(xVectors, yVectors, '.', color='blue')
pyplot.plot(filledEllipse[0], filledEllipse[1], '.', color='red')
pyplot.plot([0], [0], 's', color='black')
#pyplot.plot([m[0]], [m[1]], 'v', color='green')
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(True, which='both')
pyplot.axhline(y=0, color='k')
pyplot.axvline(x=0, color='k')
#pyplot.grid(color='blue', linestyle='-', linewidth=1)

pyplot.show()
import os
from UltraClass import UltraClass
import matplotlib.pyplot as pyplot
import numpy as np

anzahlWindows = 50
thresholdLuecke = 1
thresholdUeberschuss = -1
winList = [50, 75, 100, 150, 200, 250]

for anzahlWindows in winList:
    for threshold in np.arange(1.5,0.01,-0.1):
        
        thresholdLuecke = threshold
        thresholdLuecke = -1 * threshold

        folderPosFiles = os.listdir("./Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent")
        for file in folderPosFiles:
            ultraClass = UltraClass("Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/"+str(file), thresholdLuecke, thresholdUeberschuss)
            datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClass.readFile(anzahlWindows)
            degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList, anzahlWindows)
            gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
            linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
            windowAbwDict = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, anzahlWindows)


#-----Plotting-----
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
pyplot.plot(xList, degreeDiffList)
pyplot.plot(xList, relEaList)
pyplot.plot(xList, [avg] * len(xList))
pyplot.plot(xList, [standardAbw] * len(xList))
pyplot.title(f"Abstand = {degreeDiffList[1] - degreeDiffList[0]}; Standardabw: {standardAbw} Durchschn: {avg};")
pyplot.xlabel(f"""blau: Winkeldifferenz in Grad\n
                    orange: Relative Einzelabweichung der Ausschnitte vom Durchschnittswert\n
                    grün: Durchschnittswert\n
                    rot: Standardabweichung""")
pyplot.ylabel("Differenz der Winkel")

#Vektorengraph
pyplot.figure(num='Vektorengraph')
pyplot.plot(xVectors, yVectors, '.')
pyplot.plot(filledEllipse[0], filledEllipse[1], '.', color='orange')
pyplot.plot([0], [0], 's', color='r')
#pyplot.plot([m[0]], [m[1]], 'v', color='green')
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)

pyplot.show()
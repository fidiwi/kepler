from UltraClass import UltraClass
import matplotlib.pyplot as pyplot

filename = 'Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_.20000,.40000_pos.csv'
anzahlWindows = 50

ultraClass = UltraClass(filename, 1, -1)

datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram = ultraClass.readFile(anzahlWindows)
degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList, anzahlWindows)
gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
windowAbwDict = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, anzahlWindows)

print (windowAbwDict)
print (gapBereiche)
# Anzahl pro Window, mit LinRegs
pyplot.plot(xAxisDiagram, readAmountPerSection)
pyplot.plot(linReg1[0], linReg1[1])
pyplot.plot(linReg2[0], linReg2[1])
pyplot.plot(filledGaps[0], filledGaps[1], ".")
pyplot.xlabel("Position")
pyplot.ylabel("Anzahl pro Ausschnitt")

#Winkeldifferenzgraph
pyplot.figure()
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

#Vektorplot erstellen
pyplot.figure()
pyplot.plot(xVectors, yVectors, '.')
pyplot.plot(filledEllipse[0], filledEllipse[1], '.', color='orange')
pyplot.plot([0], [0], 's', color='r')
#pyplot.plot([m[0]], [m[1]], 'v', color='green')
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)


pyplot.show()
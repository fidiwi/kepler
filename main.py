from UltraClass import UltraClass
import matplotlib.pyplot as pyplot

filename = 'Probedaten/Beispiesamples/Mail_lutz_3/neg_samples/5_percent/10000_3.0_95_0,.57500_.62500,1_pos.csv'
anzahlWindows = 100

ultraClass = UltraClass(filename)

datasetList, readAmountPerSection, xVectors, yVectors, xAxisDiagram = ultraClass.readFile(anzahlWindows)
degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList, anzahlWindows)
gapBereiche = ultraClass.determineGaps(relEaList, datasetList)
linReg1, linReg2, filledGaps, filledEllipse = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
# Anzahl pro Window, mit LinRegs
pyplot.plot(xAxisDiagram, readAmountPerSection)
pyplot.plot(linReg1[0], linReg1[1])
pyplot.plot(linReg2[0], linReg2[1])
pyplot.plot(filledGaps[0], filledGaps[1])
pyplot.xlabel("Position")
pyplot.ylabel("Anzahl pro Ausschnitt")

#Winkeldifferenzgraph
pyplot.figure()
pyplot.plot(xList, degreeDiffList)
pyplot.plot(xList, relEaList)
pyplot.plot(xList, [avg] * len(xList))
pyplot.plot(xList, [standardAbw] * len(xList))
pyplot.title(f"Abstand = {degreeDiffList[1] - degreeDiffList[0]}; Standardabw: {standardAbw} Durchschn: {avg};")
pyplot.xlabel(f"Abstand = {degreeDiffList[1] - degreeDiffList[0]}")
pyplot.ylabel("Differenz der Winkel")

#Vektorplot erstellen
pyplot.figure()
pyplot.plot(xVectors, yVectors, '.')
#pyplot.plot(filledEllipse[0], filledEllipse[1], '.', color='orange')
pyplot.plot([0], [0], 's', color='r')
#pyplot.plot([m[0]], [m[1]], 'v', color='green')
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)


pyplot.show()
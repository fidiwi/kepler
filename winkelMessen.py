import csv
import math
import numpy as np
import matplotlib.pyplot as pyplot

def defineMittlepunkt(xValues, yValues):
    
    totalX = 0
    for x in xValues:
        totalX += x

    totalY = 0
    for y in yValues:
        totalY += y
    
    avgX = totalX / len(xValues)
    avgY = totalY / len(yValues)

    return [avgX, avgY]

def calcWinkel(mittelpunkt, p1, p2, ): #p1, p2 im Format [x, y]
    pass

def calcWinkel2(sortedData, messabstand):
    degreeDiffList = []
    xList = []
    totalSum = 0
    for i in range(0, len(sortedData)-messabstand, messabstand):
        degree1 = sortedData[i]*360
        degree2 = sortedData[i+messabstand]*360
        degreeDiff = degree2 - degree1
        degreeDiffList.append(degreeDiff)
        xList.append(i)
        totalSum += degreeDiff
    
    avg = totalSum/len(degreeDiffList)
    varianz = 0
    for degreeDiff in degreeDiffList:
        varianz += (degreeDiff - avg)**2
    varianz = varianz/len(degreeDiffList)
    standardAbw = math.sqrt(varianz)

    return [degreeDiffList, xList, avg, standardAbw]



anzahlWindows = 100

file = open('Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_8.0_0.0,0.0_pos.csv') #Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv
csvreader = csv.reader(file)
xAxisDiagram = np.arange(0, 1, 1/anzahlWindows)
readsPerSection = [[] for _ in range(anzahlWindows)] 

#Daten für den Vektorenplot
xPosSection = [[] for _ in range(anzahlWindows)]
yPosSection = [[] for _ in range(anzahlWindows)]

datasetLength = 0
datasetList = []
#Daten auslesen und einordnen
for row in csvreader:
    value = float(row[0])
    datasetList.append(value)
    index = int(value*anzahlWindows)
    if value == 1:
        index = 0
    readsPerSection[index].append(value)
    degree = value * 360
    x = math.cos(math.radians(degree)) 
    y = math.sin(math.radians(degree)) 

    xPosSection[index].append(x)
    yPosSection[index].append(y)

    datasetLength+=1
#Daten umwandeln Graph
readAmountPerSection = [0] * (anzahlWindows)

datasetList.sort()

degreeDiff = calcWinkel2(datasetList, 100)
#Positionen addieren Vektorplot
xVectors = []
yVectors = []
abstand = []
vergleich1 = [1] * anzahlWindows

for window in range(anzahlWindows):
    readAmountPerSection[window] = len(readsPerSection[window])

    vectorX = 0
    for x in xPosSection[window]:
        vectorX+=x
    
    vectorY = 0
    for y in yPosSection[window]:
        vectorY+=y

    xVectors.append(vectorX/(datasetLength/anzahlWindows))
    yVectors.append(vectorY/(datasetLength/anzahlWindows))
    abstand.append(math.sqrt(xVectors[window]**2 + yVectors[window]**2))


pyplot.plot(xAxisDiagram, abstand)
pyplot.plot(xAxisDiagram, vergleich1, color='red')
pyplot.xlabel("Position")
pyplot.ylabel("Abstand zum Zentrum")

#Winkeldifferenzgraph
pyplot.figure()
pyplot.plot(degreeDiff[1], degreeDiff[0])
pyplot.title(f"Abstand = {degreeDiff[1][1] - degreeDiff[1][0]}; Standardabw: {degreeDiff[3]} Durchschn: {degreeDiff[2]};")
pyplot.xlabel(f"Abstand = {degreeDiff[1][1] - degreeDiff[1][0]}")
pyplot.ylabel("Differenz der Winkel")

#Vektorplot erstellen
pyplot.figure()
pyplot.plot(xVectors, yVectors, '.')
pyplot.plot([0], [0], 's', color='r')
#pyplot.plot([m[0]], [m[1]], 'v', color='green')
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)


pyplot.show()

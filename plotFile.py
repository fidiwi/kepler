import csv
import math
import numpy as np
import matplotlib.pyplot as pyplot

def abstandZwPunkten(x1, y1, x2, y2):
    diffX = abs(x1-x2)
    diffY = abs(y1-y2)

    return(math.sqrt(diffX**2 + diffY**2))


anzahlWindows = 100

file = open('Probedaten/Beispiesamples/Mail_lutz_3/LБcken/20_percent/10000_2.0_20_.10000,.30000_pos.csv') #Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv
csvreader = csv.reader(file)
xAxisDiagram = np.arange(0, 1, 1/anzahlWindows)
readsPerSection = [[] for _ in range(anzahlWindows)] #Das +1 ist für den Fall des Wertes 1, der dann nicht mehr der größten Sektion zugeordnet werden kann

#Daten für den Vektorenplot
xPosSection = [[] for _ in range(anzahlWindows)]
yPosSection = [[] for _ in range(anzahlWindows)]

#Daten für den Kreisplot
xList = [0]
yList = [0]

datasetLength = 0
#Daten auslesen und einordnen
for row in csvreader:
    value = float(row[0])
    index = int(value*anzahlWindows)
    if value == 1:
        index = 0
    readsPerSection[index].append(value)
    degree = value * 360
    x = math.cos(math.radians(degree)) # *1 weil r=1 bzw Betrag von Vektoren = 1
    y = math.sin(math.radians(degree)) 

    xPosSection[index].append(x)
    yPosSection[index].append(y)

    xList.append(x)
    yList.append(y)

    datasetLength+=1
#Daten umwandeln Graph
readAmountPerSection = [0] * (anzahlWindows)

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


ketteY = [yVectors.pop(0)]
ketteX = [xVectors.pop(0)]

for yVector in ketteY:
    minAbstand = None
    pointWithMinAbstand = None
    for nextPossibleVector in yVectors:
        if yVector == nextPossibleVector:
            continue
        x1 = ketteX[-1]
        y1 = yVector

        x2 = xVectors[yVectors.index(nextPossibleVector)]
        y2 = nextPossibleVector

        abstandP = abstandZwPunkten(x1, y1, x2, y2)

        if not minAbstand or minAbstand > abstandP:
            minAbstand = abstandP
            pointWithMinAbstand = yVectors.index(nextPossibleVector)
    if not pointWithMinAbstand:
        continue
    ketteY.append(yVectors[pointWithMinAbstand])
    ketteX.append(xVectors[pointWithMinAbstand])
    del xVectors[pointWithMinAbstand]
    del yVectors[pointWithMinAbstand]

print(ketteX)
print(ketteY)


pyplot.plot(xAxisDiagram, readAmountPerSection)
pyplot.xlabel("Position")
pyplot.ylabel("reads/section")

pyplot.figure()
pyplot.plot(xAxisDiagram, abstand)
pyplot.plot(xAxisDiagram, vergleich1, color='red')
pyplot.xlabel("Position")
pyplot.ylabel("Abstand zum Zentrum")

#Kreisplot erstellen
pyplot.figure()
pyplot.plot(xList, yList, '.', color='black')
pyplot.gca().set_aspect('equal', adjustable='box')

#Vektorplot erstellen
pyplot.figure()
pyplot.plot(ketteX, ketteY, '.', color='black')
pyplot.plot(xVectors, yVectors, '.', color='red')
pyplot.plot([0], [0], 's', color='r')
#pyplot.ylim(-0.05,0.05)
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)

pyplot.show()

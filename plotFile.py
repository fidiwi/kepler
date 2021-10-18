import csv
import math
import numpy as np
import matplotlib.pyplot as pyplot

windows = 100

file = open('Probedaten/Hirnet_subsample/Hirnet4_S4.subsample.csv') #Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv
csvreader = csv.reader(file)
xAxisDiagram = np.arange(0, 1, 1/windows)
readsPerSection = [[] for _ in range(windows+1)] #Das +1 ist für den Fall des Wertes 1, der dann nicht mehr der größten Sektion zugeordnet werden kann.
datasetLength = 0

#Daten für den Vektorenplot
xPosSection = [[] for _ in range(windows+1)]
yPosSection = [[] for _ in range(windows+1)]

#Daten für den Kreisplot
xList = [0]
yList = [0]

#Daten auslesen und einordnen
for row in csvreader:
    value = float(row[0])
    index = int(value*windows)
    readsPerSection[index].append(value)
    degree = value * 360
    x = math.cos(math.radians(degree))
    y = math.sin(math.radians(degree))

    xPosSection[index].append(x)
    yPosSection[index].append(y)

    xList.append(x)
    yList.append(y)

    datasetLength+=1
#Daten umwandeln Graph
readAmountPerSection = [0] * (windows)

#Positionen addieren Vektorplot
xVectors = []
yVectors = []
abstand = []
vergleich1 = [1] * windows

for section in range(windows):
    readAmountPerSection[section] = len(readsPerSection[section])

    vectorX = 0
    for x in xPosSection[section]:
        vectorX+=x
    
    vectorY = 0
    for y in yPosSection[section]:
        vectorY+=y

    erwartetX = math.cos((section/windows-(windows/2))*360)
    erwartetY = math.sin((section/windows-(windows/2))*360)
    xVectors.append(vectorX/(datasetLength/windows))
    yVectors.append(vectorY/(datasetLength/windows))
    abstand.append(math.sqrt(xVectors[section]**2 + yVectors[section]**2))


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

        diffX = abs(x1-x2)
        diffY = abs(y1-y2)

        abstandP = math.sqrt(diffX**2 + diffY**2)
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

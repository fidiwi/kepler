import csv
import math
import numpy as np
import matplotlib.pyplot as pyplot

def abstandZwPunkten(x1, y1, x2, y2):
    diffX = abs(x1-x2)
    diffY = abs(y1-y2)

    return(math.sqrt(diffX**2 + diffY**2))


anzahlWindows = 100

file = open('kepler/Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv') #Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv
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



"""
Die Regression der Ellipse wird berechnet
Quelle: http://nadirpoint.de/Regression_2D.pdf
Beispiel auf S.19 wird kopiert:
"""
produktXY = 0
for i in range(len(xVectors)):
    produktXY += (xVectors[i] * yVectors[i])

produktXX = 0
for i in range(len(xVectors)):
    produktXX += (xVectors[i]**2)


a = (produktXY * window - sum(xVectors) * sum(yVectors)) / (produktXX * window - sum(xVectors)**2)
b = (produktXX * sum(yVectors) - produktXY * sum(xVectors)) - (produktXX * window - sum(xVectors)**2)
c = -(1/a)
d = (sum(yVectors) / window) - c *(sum(xVectors) / window) 
xMit = sum(xVectors) / window
yMit = sum(yVectors) / window

xTemp = 0
for xValue in xVectors:
    xTemp += (xValue - xMit)**2 

f = (xTemp / window)**0.5

yTemp = 0
for yValue in yVectors:
    yTemp += (yValue - yMit)**2 

e = (yTemp / window)**0.5

print(a)
print(b)
print(c)
print(d)
print(xMit)
print(yMit)
print(f)
print(e)



"""
xMin = 0
xMax = 0
for xValue in xVectors:
    if xMin > xValue:
        xMin = xValue

    if xMax < xValue:
        xMax = xValue
f = xMax - xMin

yMin = 0
yMax = 0
for yValue in yVectors:
    if yMin > yValue:
        yMin = yValue

    if yMax < yValue:
        yMax = yValue
e = yMax - yMin

xRegression = np.linspace(-1,2,100)
yRegression =  (yAchsenLaenge/xAchsenLaenge) * (xAchsenLaenge**2 - (xRegression - 0.4))**0.5
yNegativRegression = -(yAchsenLaenge/xAchsenLaenge) * (xAchsenLaenge**2 - (xRegression - 0.4))**0.5

print(xAchsenLaenge)
print(yAchsenLaenge)
"""




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

#print(ketteX)
#print(ketteY)


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
#pyplot.plot(xRegression, yRegression, color='black')
#pyplot.plot(xRegression, yNegativRegression, color='red')
#pyplot.ylim(-0.05,0.05)
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)


pyplot.show()

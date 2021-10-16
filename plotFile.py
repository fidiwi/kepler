import csv
import math
import numpy as np
import matplotlib.pyplot as pyplot

windows = 50

file = open('Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv') #Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv
csvreader = csv.reader(file)
xAxisDiagram = np.arange(0, 1, 1/windows)
readsPerSection = [[] for _ in range(windows)]
datasetLength = 0

#Daten für den Vektorenplot
xPosSection = [[] for _ in range(windows)]
yPosSection = [[] for _ in range(windows)]

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
print(readsPerSection)
print (xPosSection)
#Daten umwandeln Graph
readAmountPerSection = [0] * (windows)

#Positionen addieren Vektorplot
xVectors = []
yVectors = []

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

    print(vectorX)
print(xVectors)
    
pyplot.plot(xAxisDiagram, readAmountPerSection)
pyplot.xlabel("Position")
pyplot.ylabel("reads/section")

#Kreisplot erstellen
pyplot.figure()
pyplot.plot(xList, yList, '.', color='black')
pyplot.gca().set_aspect('equal', adjustable='box')

#Vektorplot erstellen
pyplot.figure()
pyplot.plot(xVectors, yVectors, '.', color='black')
pyplot.plot([0], [0], 's', color='r')
#pyplot.ylim(-0.05,0.05)
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)

pyplot.show()

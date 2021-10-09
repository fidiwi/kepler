import csv
import math
import numpy as np
import matplotlib.pyplot as pyplot

windows = 50

file = open('Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv')
csvreader = csv.reader(file)
xAxisDiagram = np.arange(0, 1+1/windows, 1/windows)
readsPerSection = [[] for _ in range(windows+1)]
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
    index = int(round(value*windows, 0))
    readsPerSection[index].append(value)
    degree = value * 360
    x = math.cos(degree)
    y = math.sin(degree)

    xPosSection[index].append(x)
    yPosSection[index].append(y)

    xList.append(x)
    yList.append(y)

    datasetLength+=1

#Daten umwandeln Graph
numberPerSection = [0] * (windows+1)

#Positionen addieren Vektorplot
xVectors = []
yVectors = []

for section in range(windows+1):
    numberPerSection[section] = len(readsPerSection[section])

    vectorX = 0
    for x in xPosSection[section]:
        vectorX+=x
    
    vectorY = 0
    for y in yPosSection[section]:
        vectorY=y

    erwartetX = math.cos((1/windows-1/(windows*2))*360)
    erwartetY = math.sin((1/windows-1/(windows*2))*360)
    xVectors.append(vectorX/((datasetLength/windows)*erwartetX))
    yVectors.append(vectorY/((datasetLength/windows)*erwartetY))

print(numberPerSection)
pyplot.plot(xAxisDiagram, numberPerSection)
pyplot.xlabel("Position")
pyplot.ylabel("reads/section")

#Kreisplot erstellen
#pyplot.figure()
#pyplot.plot(xList, yList, '.', color='black')
#pyplot.gca().set_aspect('equal', adjustable='box')

#Vektorplot erstellen
pyplot.figure()
pyplot.plot(xVectors, yVectors, '.', color='black')
pyplot.plot([0], [0],  's', color='r')
#pyplot.ylim(-0.05,0.05)
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(color='blue', linestyle='-', linewidth=1)

pyplot.show()
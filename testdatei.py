import csv
import math
import numpy as np



def vectorenBerechnen(fileName, anzahlWindows):
    fileName = fileName
    anzahlWindows = anzahlWindows
    file = open(fileName)
    print(file)
    csvreader = csv.reader(file)
    xAxisDiagram = np.arange(0, 1, 1/anzahlWindows)
    readsPerSection = [[] for _ in range(anzahlWindows)]
    #Daten für den Vektorenplot
    xPosSection = [[] for _ in range(anzahlWindows)]
    yPosSection = [[] for _ in range(anzahlWindows)]

    #Daten für den Kreisplot
    xList = [0]
    yList = [0]

    datasetLength = 0

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

    return [xVectors, yVectors]
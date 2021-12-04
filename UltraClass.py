import csv
import math
import numpy as np
import matplotlib.pyplot as pyplot
from sklearn.linear_model import LinearRegression


class UltraClass:

    def __init__(self, filename):
        self.filename = filename


    def readFile(self, anzahlWindows):
        file = open(self.filename) #Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv
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

        xVectors = []
        yVectors = []
        abstand = []
        readAmountPerSection = [0] * (anzahlWindows)
        
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

        datasetList.sort()

        self.datasetLength = datasetLength

        readAmountPerSectionDict = {}
        for i in range(len(list(xAxisDiagram))):
            readAmountPerSectionDict[xAxisDiagram[i]] = readAmountPerSection[i]

        return [datasetList, readAmountPerSection, readAmountPerSectionDict, xVectors, yVectors, xAxisDiagram]


    def calcWinkel(self, sortedData, anzahlWindows):

        messabstand = int(len(sortedData)/anzahlWindows)
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

        #Einzelabweichung = ea
        relEaList = [] # Relative Abweichung von Durchschnitt
        for degreeDiff in degreeDiffList:
            relEaList.append((degreeDiff-avg) / avg)

        return [degreeDiffList, xList, avg, standardAbw, relEaList]


    def determineGaps(self, relEaList, datasetList, thresholdLuecke = 1, thresholdUeberschuss = -1): # thresholdLuecke von 1 = 100% Abweichung
        gapBereiche = []
        gapUeberschuss = []
        for relEaIndex in range(len(relEaList)):
            if relEaList[relEaIndex] >= thresholdLuecke:
                gap = relEaIndex
                x = len(datasetList)/len(relEaList) #len relEaList ist wahrscheinlich = anzahlWindows
                anfang = datasetList[int(gap*x)]
                if gap*x >= len(datasetList)-x:
                    ende = anfang
                else:
                    ende = datasetList[int((gap+1)*x)]
                gapBereiche.append([anfang, ende])
            if relEaList[relEaIndex] <= thresholdUeberschuss:
                gap = relEaIndex
                x = len(datasetList)/len(relEaList) #len relEaList ist wahrscheinlich = anzahlWindows
                anfang = datasetList[int(gap*x)]
                if gap*x >= len(datasetList)-x:
                    ende = anfang
                else:
                    ende = datasetList[int((gap+1)*x)]
                gapBereiche.append([anfang, ende])
        return gapBereiche


    def fillGaps(self, gapBereiche, readAmountPerSection, xAxisDiagram):
        xAxisDiagram = list(xAxisDiagram) # Weil es vorher ein np.arange()-Objekt ist
        
        readAmount1 = readAmountPerSection[:len(readAmountPerSection)//2]
        readAmount2 = readAmountPerSection[len(readAmountPerSection)//2:]
        xAxis1 = xAxisDiagram[:len(xAxisDiagram)//2]
        xAxis2 = xAxisDiagram[len(xAxisDiagram)//2:]
        print(gapBereiche)
        #print(xAxis2)
        anzahlWindows = len(readAmountPerSection)        
        foundWindows = []
        for gap in gapBereiche:
            if gap[1] < 0.5:
                deletedWindows = []
                for i in range(len(xAxis1)):
                    if gap[0] <= xAxis1[i] and gap[1] >= xAxis1[i]:
                        deletedWindows.append(i)
                deletedWindows = sorted(deletedWindows, reverse=True)
                for delWindow in deletedWindows:
                    del readAmount1[delWindow]
                    foundWindows.append(xAxis1.pop(delWindow))
            elif gap[0] > 0.5:
                deletedWindows = []
                for i in range(len(xAxis2)):
                    if gap[0] <= xAxis2[i] and gap[1] >= xAxis2[i]:
                        deletedWindows.append(i)
                deletedWindows = sorted(deletedWindows, reverse=True)
                for delWindow in deletedWindows:
                    del readAmount2[delWindow]
                    foundWindows.append(xAxis2.pop(delWindow))
            else: # Für den Fall dass es um 0.5 herum ist.
                pass
            
        model1 = LinearRegression()
        model1.fit(np.array(xAxis1).reshape((-1, 1)), readAmount1)
        linReg1 = model1.predict(np.array(xAxis1).reshape((-1, 1)))

        model2 = LinearRegression()
        model2.fit(np.array(xAxis2).reshape((-1, 1)), readAmount2)
        linReg2 = model2.predict(np.array(xAxis2).reshape((-1, 1)))

        filledValues = []
        xValuesEllipse = []
        yValuesEllipse = []
        for w in foundWindows:
            if w > 0.5:
                filledValue = model2.predict(np.array([w]).reshape((-1, 1)))
            elif w < 0.5:
                filledValue = model1.predict(np.array([w]).reshape((-1, 1)))[0]

            filledValues.append(filledValue)

            x = math.cos(math.radians(w*360))
            y = math.sin(math.radians(w*360))

            xValuesEllipse.append(x*filledValue/(self.datasetLength/anzahlWindows))
            yValuesEllipse.append(y*filledValue/(self.datasetLength/anzahlWindows))

        return[[xAxis1, linReg1], [xAxis2, linReg2], [foundWindows, filledValues], [xValuesEllipse, yValuesEllipse]]


    def getWindowAbweichung(self, foundWindows, filledValues, readAmountPerSectionDict):
        windowAbwDict = {}
        for i in range(len(foundWindows)):
            fw = foundWindows[i]
            fv = filledValues[i]
            originalValue = readAmountPerSectionDict[fw]
            diff = originalValue - fv
            relDiff = originalValue / fv

            windowAbwDict[fw] = [diff, relDiff]
        return windowAbwDict


    

    

    





    
    #Daten umwandeln Graph
"""
    datasetList.sort()

    degreeDiff = calcWinkel(datasetList, 100)
    determineGaps(getEinzelAbweichung(degreeDiff[0], degreeDiff[2])[1], datasetList)
    #Positionen addieren Vektorplot
    vergleich1 = [1] * anzahlWindows

    


    linReg1, linReg2 = fillGaps(determineGaps(getEinzelAbweichung(degreeDiff[0], degreeDiff[2])[1], datasetList), readAmountPerSection, xAxisDiagram)

    pyplot.plot(xAxisDiagram, readAmountPerSection)
    pyplot.plot(linReg1[0], linReg1[1])
    pyplot.plot(linReg2[0], linReg2[1])
    #pyplot.plot(xAxisDiagram, vergleich1, color='red')
    pyplot.xlabel("Position")
    pyplot.ylabel("Anzahl pro Ausschnitt")

    #Winkeldifferenzgraph
    pyplot.figure()
    pyplot.plot(degreeDiff[1], degreeDiff[0])
    pyplot.plot(degreeDiff[1], getEinzelAbweichung(degreeDiff[0], degreeDiff[2])[0])
    pyplot.plot(degreeDiff[1], getEinzelAbweichung(degreeDiff[0], degreeDiff[2])[1])
    pyplot.plot(degreeDiff[1], [degreeDiff[2]] * len(degreeDiff[1]))
    pyplot.plot(degreeDiff[1], [degreeDiff[3]] * len(degreeDiff[1]))
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
"""
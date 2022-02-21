import os
import csv
import math
from re import S
import numpy as np
from sklearn.linear_model import LinearRegression


class UltraClass:

    # Initialisierung der Klasse, Übergabe der Attribute
    def __init__(self, filename, thresholdLuecke, thresholdUeberschuss, readsPerWindow):
        self.filename = filename
        self.thresholdLuecke = thresholdLuecke
        self.thresholdUeberschuss = thresholdUeberschuss
        file = open(self.filename)
        csvreader = csv.reader(file)
        csvreaderlist = list(csvreader)
        datasetLength = len(csvreaderlist)
        self.anzahlWindows = datasetLength//readsPerWindow
        self.readsPerWindow = int(datasetLength/self.anzahlWindows)

    # Funktion zum Einlesen des Datensatzes und Ermitteln einiger Größen
    def readFile(self):
        file = open(self.filename)
        csvreader = csv.reader(file)
        csvreaderlist = list(csvreader)
        datasetLength = len(csvreaderlist)
        xAxisDiagram = list(np.arange(0, 1, 1/self.anzahlWindows))
        if(len(xAxisDiagram) > self.anzahlWindows):
            del xAxisDiagram[-1]
        readsPerSection = [[] for _ in range(self.anzahlWindows)]

        # Daten für den Vektorenplot
        xPosSection = [[] for _ in range(self.anzahlWindows)]
        yPosSection = [[] for _ in range(self.anzahlWindows)]

        datasetList = []

        # Daten auslesen und einordnen
        for row in csvreaderlist:
            value = float(row[0])
            if value >= 1:
                value -= 1

            datasetList.append(value)
            index = int(value*self.anzahlWindows)
            """if value >= 1:
                index = 0"""
            # Werte werden dem jeweiligen Window zugeordnet
            readsPerSection[index].append(value)
            degree = value * 360 + 90
            if degree > 360:
                degree -= 360
            # x- und y-Position werden bestimmt
            x = math.cos(math.radians(degree))
            y = math.sin(math.radians(degree))

            xPosSection[index].append(x)
            yPosSection[index].append(y)

        xVectors = []
        yVectors = []
        abstand = []
        readAmountPerSection = [0] * (self.anzahlWindows)

        # Windows werden erstellt
        for window in range(self.anzahlWindows):
            readAmountPerSection[window] = len(readsPerSection[window])
            vectorX = 0
            for x in xPosSection[window]:
                vectorX += x

            vectorY = 0
            for y in yPosSection[window]:
                vectorY += y

            xVectors.append(vectorX/(datasetLength/self.anzahlWindows))
            yVectors.append(vectorY/(datasetLength/self.anzahlWindows))
            abstand.append(math.sqrt(xVectors[window]**2 + yVectors[window]**2))

        datasetList.sort()

        self.datasetLength = datasetLength

        readAmountPerSectionDict = {}
        readsPerSectionDict = {}
        for i in range(len(xAxisDiagram)):
            readAmountPerSectionDict[xAxisDiagram[i]] = readAmountPerSection[i]
            readsPerSectionDict[xAxisDiagram[i]] = readsPerSection[i]

        readAmountPerSectionPercentage = []
        for readAmount in readAmountPerSection:
            readAmountPerSectionPercentage.append(readAmount/(self.datasetLength/self.anzahlWindows))

        return [datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage]

    # Verschiebung des Datensatzes, wenn der Terminus nicht genau bei 0,5 ist
    def datensatzVerschieben(self, datasetList, readAmountPerSection, gapBereiche, resetValue=0):
        max = 0
        maxPos = 0
        min = 1000
        minPos = 0
        if resetValue == 0:
            for windowIndex in range(len(readAmountPerSection)):
                flag = True
                for gap in gapBereiche:
                    if gap[1] >= windowIndex/self.anzahlWindows >= gap[0]:
                        flag = False
                if flag:
                    if max < readAmountPerSection[windowIndex]:
                        max = readAmountPerSection[windowIndex]
                        maxPos = windowIndex/self.anzahlWindows
                    if min > readAmountPerSection[windowIndex]:
                        min = readAmountPerSection[windowIndex]
                        minPos = windowIndex/self.anzahlWindows

            if minPos < 0.45 or minPos > 0.55:
                resetValue = minPos - 0.5
                resetValue = round(resetValue, 5)
            if abs(maxPos-minPos) > 0.45 and abs(maxPos-minPos) < 0.55:
                print("Verschiebung wahrscheinlich erfolgreich ausgeführt")

        nameFile = self.filename.rsplit('/', 1)[-1]
        cd = 'Output/BackMovedDataset/backMovedDataset_' + str(resetValue) + "_"+ nameFile
        with open(cd, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
            for row in datasetList:
                value = row - resetValue
                if value < 0:
                    value += 1
                if value > 1:
                    value += -1
                writer.writerow([value])
            csvfile.close()
        return cd

    # Ermittlung der Winkeldifferenzen, Intervall an "readsPerWindow" gebunden
    def calcDegreeDifferences(self, sortedData):
        degreeDiffList = []
        xList = []
        totalSum = 0
        # der Winkel wird berechnet und die Differenz angegeben
        for i in range(0, len(sortedData)-self.readsPerWindow, self.readsPerWindow):
            degree1 = sortedData[i]*360
            degree2 = sortedData[i+self.readsPerWindow]*360
            degreeDiff = degree2 - degree1
            degreeDiffList.append(degreeDiff)
            xList.append(sortedData[i])
            totalSum += degreeDiff

        # die Standardabweichung wird bestimmt
        avg = totalSum/len(degreeDiffList)
        varianz = 0
        for degreeDiff in degreeDiffList:
            varianz += (degreeDiff - avg)**2
        varianz = varianz/len(degreeDiffList)
        standardAbw = math.sqrt(varianz)

        # Einzelabweichung = ea
        relEaList = []  # Relative Abweichung von Durchschnitt
        for degreeDiff in degreeDiffList:
            relEaList.append((degreeDiff-avg) / avg)

        return [degreeDiffList, xList, avg, standardAbw, relEaList]

    # Funktion zu Erkennung von Lücken und Überschüssen anhand der relativen Einzelabweichung
    def determineGaps(self, relEaList, xList):  # thresholdLuecke von 1 = 100% Abweichung (Bezogen auf die Abweichung vom Durchschnittabstand[avg])
        gapBereiche = []

        for relEaIndex in range(len(relEaList)):
            if relEaList[relEaIndex] >= self.thresholdLuecke:  # wenn die Abweichung zu stark ist -> Lücke
                gap = relEaIndex
                anfang = xList[gap]
                if anfang < 0.005:
                    anfang = 0
                if gap >= len(xList) - 1:
                    ende = 1
                else:
                    ende = xList[gap+1]
                gapBereiche.append([anfang, ende])
            elif relEaList[relEaIndex] <= self.thresholdUeberschuss:  # -> Überschuss
                gap = relEaIndex
                anfang = xList[gap]
                if anfang < 0.005:
                    anfang = 0

                if gap >= len(xList) - 1:
                    ende = 1
                else:
                    ende = xList[gap+1]
                gapBereiche.append([anfang, ende])
        return gapBereiche

    # Funktion zur Ermittlung neuer Werte für Lücken/Überschüsse anhand 
    # Linearer Regressionen, die hier erstellt werden
    def fillGaps(self, gapBereiche, readAmountPerSection, xAxisDiagram, start=0, end=1):
        readAmount1 = readAmountPerSection[:len(readAmountPerSection)//2]  # Listen aufteilen: 0-0.5; 0.5-1
        readAmount2 = readAmountPerSection[len(readAmountPerSection)//2:]
        xAxis1 = xAxisDiagram[:len(xAxisDiagram)//2]
        xAxis2 = xAxisDiagram[len(xAxisDiagram)//2:]

        if start!=0 or end!=1:
            gapBereiche = [[0, start], [end, 1]]
        foundWindows = []
        halfWindow = (1/self.anzahlWindows)/2
        for gap in gapBereiche:
            deletedWindows = []  # bis 0.5 werden alle Windows, die Lücken/Überschüsse enthalten, gesucht
            for i in range(len(xAxis1)):
                if (gap[0] <= xAxis1[i] <= gap[1]) or (xAxis1[i]-halfWindow) <= gap[0] <= (xAxis1[i]+halfWindow) or (xAxis1[i]-halfWindow) <= gap[1] <= (xAxis1[i]+halfWindow):
                    deletedWindows.append(i)
            deletedWindows = sorted(deletedWindows, reverse=True)
            for delWindow in deletedWindows:
                del readAmount1[delWindow]
                foundWindows.append(xAxis1.pop(delWindow))
            deletedWindows = []  # ab 0.5 werden alle Windows, die Lücken/Überschüsse enthalten, gesucht
            for i in range(len(xAxis2)):
                if (gap[0] <= xAxis2[i] <= gap[1]) or (xAxis2[i]-halfWindow) <= gap[0] <= (xAxis2[i]+halfWindow) or (xAxis2[i]-halfWindow) <= gap[1] <= (xAxis2[i]+halfWindow):
                    deletedWindows.append(i)
            deletedWindows = sorted(deletedWindows, reverse=True)
            for delWindow in deletedWindows:
                del readAmount2[delWindow]
                foundWindows.append(xAxis2.pop(delWindow))

        
        # Ermittlung der linearen Regressionen
        if len(readAmount1) > 0: # >1?
            model1 = LinearRegression()
            model1.fit(np.array(xAxis1).reshape((-1, 1)), readAmount1)
            linReg1 = model1.predict(np.array(xAxis1).reshape((-1, 1)))
            # Die Randwert 0 und 0.5 werden ggf. zusätzlich berechnet, 
            # damit eine schöne lineare Regression entsteht
            
            if xAxis1[0] != 0:
                value = model1.predict(np.array([0]).reshape((-1, 1))).tolist()[0]
                xAxis1.insert(0, 0)
                linReg1 = np.insert(linReg1, 0, value)
                readAmount1.insert(0, value)

            if xAxis1[-1] != 0.5:
                value = model1.predict(np.array([0.5]).reshape((-1, 1))).tolist()[0]
                xAxis1.append(0.5)
                linReg1 = np.append(linReg1, value)
                readAmount1.append(value)
            model1.fit(np.array(xAxis1).reshape((-1, 1)), readAmount1)

        if len(readAmount2) > 0:
            model2 = LinearRegression()
            model2.fit(np.array(xAxis2).reshape((-1, 1)), readAmount2)
            linReg2 = model2.predict(np.array(xAxis2).reshape((-1, 1)))

            if xAxis2[0] != 0.5:
                value = model2.predict(np.array([0.5]).reshape((-1, 1))).tolist()[0]
                xAxis2.insert(0, 0.5)
                linReg2= np.insert(linReg2, 0, value)
                readAmount2.insert(0, value)
            if xAxis2[-1] != 1:
                value = model2.predict(np.array([1]).reshape((-1, 1))).tolist()[0]
                xAxis2.append(1)
                linReg2 = np.append(linReg2, value)
                readAmount2.append(value)
            model2.fit(np.array(xAxis2).reshape((-1, 1)), readAmount2)

        if len(readAmount1) == 0 and len(readAmount2) == 0:
            print("Regression konnte nicht gebildet werden. Datensatz oder Parameter sind fehlerhaft!")
        # Für den Fall, dass nur Daten einer der Hälften des Daten-
        # satzes enthalten sind, erstelle eine Regression für den
        # fehlenden Teil des Datensatzes als Spiegelung der Regression
        # des vorhandenen Datensatzes
        elif len(readAmount1) == 0 and len(readAmount2) > 0:
            for xPos in xAxis2:
                xAxis1.append(xPos - ((xPos-0.5)*2))
            readAmount1 = readAmount2
            model1 = LinearRegression()
            model1.fit(np.array(xAxis1).reshape((-1, 1)), readAmount1)
            linReg1 = model1.predict(np.array(xAxis1).reshape((-1, 1)))
        elif len(readAmount1) > 0 and len(readAmount2) == 0:
            for xPos in xAxis1:
                xAxis2.append(xPos + ((0.5-xPos)*2))
            readAmount2 = readAmount1
            model2 = LinearRegression()
            model2.fit(np.array(xAxis2).reshape((-1, 1)), readAmount2)
            linReg2 = model2.predict(np.array(xAxis2).reshape((-1, 1)))

        filledValues = []
        predictedXValues = []
        predictedYValues = []
        # filledValue gibt die prognostizierte Anzahl an Reads im jeweiligen Windows an
        for w in foundWindows:
            if w >= 0.5:
                filledValue = model2.predict(np.array([w]).reshape((-1, 1)))
            elif w < 0.5:
                filledValue = model1.predict(np.array([w]).reshape((-1, 1)))

            filledValues.append(filledValue)
            winkel = w*360 + 90
            if winkel > 360:
                winkel -= 360
            x = math.cos(math.radians(winkel))
            y = math.sin(math.radians(winkel))

            predictedXValues.append(x*filledValue/(self.datasetLength/self.anzahlWindows))
            predictedYValues.append(y*filledValue/(self.datasetLength/self.anzahlWindows))

        return[[xAxis1, linReg1], [xAxis2, linReg2], [foundWindows, filledValues], [predictedXValues, predictedYValues], [model1.coef_, model2.coef_], [model1, model2]]

    # Funktion zum Erstellen der Ausgabedateien
    def createOutputFiles(self, foundWindows, filledValues, readAmountPerSectionDict, readsPerSectionDict, createFiles = True, iteration = 1, originalFile = None):
        # Ermittlung der Abweichung verbesserter Werte zu den ursprünglichen
        # Werten für "AnalyseReads"
        windowAbwDict = {}
        betterDataFileName = ""
        for i in range(len(foundWindows)):
            fw = foundWindows[i]
            fv = filledValues[i]
            originalValue = readAmountPerSectionDict[fw]
            diff = float(originalValue - fv)  # wie viele Reads zu viel bzw. zu wenig sind
            relDiff = str(int((originalValue / fv)*10000)/100) + "%"  # realtiv zum erwartetem Wert

            # Alte Werte mit generierten Ersetzen
            # readsPerSectionDict[fw] = [fw]*int(fv) #Setze fv mal (prognostizierte Häufigkeit) den Wert des Windows ein
            # Alternative:
            newWindowData = []
            lowerBound = fw
            upperBound = fw + (self.anzahlWindows/self.datasetLength)
            stepSize = (upperBound-lowerBound) / int(fv)

            for v in np.arange(lowerBound, upperBound, stepSize):
                newWindowData.append(v.item())  # .item macht aus v ein float anstelle von numpy float
            readsPerSectionDict[fw] = newWindowData
            windowAbwDict[fw] = [diff, relDiff]

        if createFiles:
            # Daten in csv schreiben
            if not originalFile:
                nameFile = self.filename.rsplit('/', 1)[-1]
            else:
                nameFile = originalFile.rsplit('/', 1)[-1]

            # Better Dataset
            datasetInfo = str(self.anzahlWindows)+"_"+str(self.datasetLength)+"_"+str(self.thresholdLuecke)+"_"+str(self.thresholdUeberschuss)+"_$$_"
            if not os.path.isdir(f'Output/BetterDataset/{iteration}'):
                os.mkdir(f'Output/BetterDataset/{iteration}')
            betterDataFileName = f'Output/BetterDataset/{iteration}/NewData_{datasetInfo}{nameFile}'
            with open(betterDataFileName, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
                for key in readsPerSectionDict:
                    for value in readsPerSectionDict[key]:
                        writer.writerow([value])
                csvfile.close()

            # Analyse Reads
            nameFile = self.filename.rsplit('/', 1)[-1]
            infoDataset2 = str(self.anzahlWindows)+"_"+str(self.datasetLength)+"_"+str(self.thresholdLuecke)+"_"+str(self.thresholdUeberschuss)+"_$$_"
            cd = 'Output/AnalyseReads/Analyse_' + infoDataset2 + nameFile
            with open(cd, 'w', newline='') as csvfile2:
                writer2 = csv.writer(csvfile2, delimiter=' ', quotechar='|')
                # writer2.writerow(["Position"] + ["Read"] + ["Relative Abweichung"])
                for key in windowAbwDict:
                    writer2.writerow([key] + [windowAbwDict[key][0]] + [windowAbwDict[key][1]])
                csvfile2.close()
            
        return [windowAbwDict, betterDataFileName]

    # Erzeugt Daten, die ausschließlich aus der gegebenen Linearen Regression berechnet werden (originale Werte werden überschrieben)
    def calcDataFromRegression(self, linReg1):
        calcValue = (((self.datasetLength/self.anzahlWindows)/100)**2)*2
        xValuesList = []
        yValuesList = []
        linReg1List = np.array(linReg1).flatten().tolist()
        for i in range(len(linReg1List)):
            winkel = (i/self.anzahlWindows)*360 + 90
            if winkel > 360:
                winkel -= 360

            x = math.cos(math.radians(winkel))*(linReg1List[i]/self.anzahlWindows/calcValue)
            y = math.sin(math.radians(winkel))*(linReg1List[i]/self.anzahlWindows/calcValue)
            xValuesList.append(x)
            yValuesList.append(y)
        linReg1List.reverse()
        yValuesListNP = np.array(yValuesList)
        xValuesListNP = np.array(xValuesList)
        yValuesList = yValuesListNP.tolist()
        xValuesList = xValuesListNP.tolist()

        yValuesListNew = list(yValuesList)
        for i in range(len(yValuesList)):
            yValuesListNew.append(yValuesList[-(i+1)])

        xValuesListNew = list(xValuesList)
        for i in range(len(xValuesList)):
            xValuesListNew.append((xValuesList[-(i+1)])*-1)

        return [xValuesListNew, yValuesListNew]

    # Dient zur Auslesung eines Datensatzes durch andere Hilfsprogramme
    def windowsSucheOpenFile(self):
        # die AnalyseReads-Dateien werden ausgelesen und als Liste zurückgegeben 
        searchReads = []
        with open(self.filename, newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in file:
                value = [round(float(row[0]),3), round(float(row[1]))]
                searchReads.append(value)
            csvfile.close()

        return(searchReads)

    # Wachstumsbestimmung anhand der Abstände der Vektoren zu Wachstumsdiagrammen
    # mithilfe einer Gaußkurve
    def calcGrowthStreuungGraphenGauss(self, xValues, yValues, xValueGraphList, yValueGraphList):
        divList = []
        gaußList = [[] for _ in range(len(xValueGraphList))]
        for i in range(len(xValueGraphList)):
            print(f"W-D {i+2}:")
            div = 0
            for j in range(len(xValueGraphList[i])):
                value = math.sqrt(xValues[j]**2 + yValues[j]**2) / math.sqrt(xValueGraphList[i][j]**2 + yValueGraphList[i][j]**2)
                div += value
                gaußList[i].append(value)
                print(value)
            divList.append(abs(div/(len(xValues))-1))
        min = divList[0]
        print(divList)
        minPos = 0
        for i in range(len(divList)):
            if divList[i] < min:
                min = divList[i]
                minPos = i
        wachstumsrate = minPos + 2

        return [wachstumsrate, gaußList]

    # Wachstumsratenbestimmung über die Differenz zum nächsten Wachstumsdiagramm
    def calcGrowthStreuungGraphen(self, xValues, yValues, xValueGraphList, yValueGraphList):
        diffAvgList = []
        for i in range(len(xValueGraphList)):
            diff = 0
            for j in range(len(xValueGraphList[i])):
                value = math.sqrt(xValues[j]**2 + yValues[j]**2) - math.sqrt(xValueGraphList[i][j]**2 + yValueGraphList[i][j]**2)
                diff += abs(value)
            diffAvgList.append(abs(diff/(len(xValues))))
        min = diffAvgList[0]
        print(diffAvgList)
        minPos = 0
        for i in range(len(diffAvgList)):
            if diffAvgList[i] < min:
                min = diffAvgList[i]
                minPos = i
        wachstumsrate = minPos + 2

        return wachstumsrate

    # Funktion zur Zuordnung von Lücken/Überschüssen unter verschiedenen
    # Datensätzen, benötigt für AnalyseReads 
    def calcMatchingReads(self, ultraReadsList, folderAnalyseReads, filename):
        # Datei mit den gefundenen Reads wird erstellt
        cd = 'Output/WindowsSuche/' + filename
        with open(cd, 'w', newline='') as csvfile:
            windowsSucheCSV = csv.writer(csvfile, delimiter=';', quotechar='|')
            windowsSucheCSV.writerow(["Window"]+["Summe Reads"]+["Datensätze mit Lücken"]+["Tiefe der Lücken"]+["Datensätze mit Überschüssen"]+["Höhe der Überschüsse"])
            for window in range(self.anzahlWindows):
                ReadsInAllWindows = 0
                filesNeg = []
                valueNeg = []
                filesPos = []
                valuePos = []
                cd = 'Output/WindowsSuche_' + "test1.csv"

                for i in range(len(ultraReadsList)):
                    for j in range(len(ultraReadsList[i])):
                        if ultraReadsList[i][j][0] == window/self.anzahlWindows:
                            if ultraReadsList[i][j][1] > 0:
                                filesPos.append(folderAnalyseReads[i])
                                valuePos.append(ultraReadsList[i][j][1])
                            else:
                                filesNeg.append(folderAnalyseReads[i])
                                valueNeg.append(ultraReadsList[i][j][1])
                            ReadsInAllWindows += ultraReadsList[i][j][1]

                if len(filesNeg) == 0:
                    filesNeg.append("null")
                    valueNeg.append("0")
                if len(filesPos) == 0:
                    filesPos.append("null")
                    valuePos.append("0")

                windowsSucheCSV.writerow([window/self.anzahlWindows]+[ReadsInAllWindows]+[filesNeg]+[valueNeg]+[filesPos]+[valuePos])

    # Ermittelt die Streuung innerhalb eines Windows
    def windowQualität(self, readsPerSectionDict):
        readAbweichungProWindow = []
        for windowkey in readsPerSectionDict:
            window = readsPerSectionDict[windowkey]

        # Standardabweichung der Readabstände in einem Window:
            window.sort()
            abstandSumme = 0
            abstandListe = []
            for read in range(len(window)-1):
                abstandListe.append(window[read+1] - window[read])
                abstandSumme += (window[read+1] - window[read])  # Aktuell nur die "inneren Abstände" -> nur die Abstände zwischen den Reads, also nicht zu den Windowbounds

            varianz = 0
            if len(abstandListe) == 0:
                standardabweichung = 0
            else:
                avg = abstandSumme/len(abstandListe)
                for abstand in abstandListe:
                    varianz += (abstand-avg)**2
                varianz = varianz/len(abstandListe)
                standardabweichung = math.sqrt(varianz)
            readAbweichungProWindow.append(standardabweichung*100000)  # Um eine bessere Darstellung zu ermöglichen, werden die Werte hochskaliert

        return readAbweichungProWindow    

    # Sorgt dafür, dass Wachstumsdiagramme und der entstandene Vektorenplot
    # auf dieselbe Größe skaliert werden
    def kalibrieren2(self, xVectorsEllipse, yVectorsEllipse, linEins, linZwei, xVectors, yVectors):
        idealisierung = 0.9591384589301084 
        punkt1 = math.sqrt((xVectors[round(self.anzahlWindows* 0.23)])**2+(yVectors[round(self.anzahlWindows* 0.23)])**2)
        punkt2 = math.sqrt((xVectors[round(self.anzahlWindows* 0.77)])**2+(yVectors[round(self.anzahlWindows* 0.77)])**2)
        streckfaktor = (punkt1/idealisierung + abs(punkt2)/idealisierung)/2
        for i in range(len(xVectorsEllipse)):
            xVectorsEllipse[i] = xVectorsEllipse[i] * streckfaktor
            yVectorsEllipse[i] = yVectorsEllipse[i] * streckfaktor
        
        for i in range(len(linEins[1])):
            linEins[1][i] = linEins[1][i] * streckfaktor
            linZwei[1][i] = linZwei[1][i] * streckfaktor
        
        return [xVectorsEllipse, yVectorsEllipse, linEins, linZwei]


    def kalibrieren(self, xVectors, yVectors, linEins, linZwei, modelLinReg, predictedValues):
        punkt1 = modelLinReg[0].predict(np.array([0.23]).reshape((-1, 1))).tolist()[0]
        punkt2 = modelLinReg[1].predict(np.array([0.77]).reshape((-1, 1))).tolist()[0]
        streckfaktor = (self.readsPerWindow/punkt1 + self.readsPerWindow/punkt2)/2
        for i in range(len(xVectors)):
            xVectors[i] = xVectors[i] * streckfaktor
            yVectors[i] = yVectors[i] * streckfaktor
        for i in range(len(predictedValues[0])):
            predictedValues[0][i] = predictedValues[0][i] * streckfaktor
            predictedValues[1][i] = predictedValues[1][i] * streckfaktor
        
        for i in range(len(linEins[1])):
            linEins[1][i] = linEins[1][i] * streckfaktor
        for i in range(len(linZwei[1])):
            linZwei[1][i] = linZwei[1][i] * streckfaktor
        steigung1 = modelLinReg[0].coef_ * streckfaktor
        steigung2 = modelLinReg[1].coef_ * streckfaktor
        steigung = [steigung1, steigung2]    
        return [xVectors, yVectors, linEins, linZwei, predictedValues, steigung]

    # Berechnet die Wachstumsrate anhand der Standardabweichung der Winkeldifferenzen
    def calcGrowthStabw(self, datasetList, standardAbw):
        growth = 0.8*((1+len(datasetList)/(len(datasetList)*100))**self.anzahlWindows)**standardAbw
        return growth

    # Berechnet die Wachstumsrate anhand der Steigung der Linearen Regressionen
    def calcGrowthSteigung(self, steigungList):
        steigungMedian = 0
        steigung = [abs(steigungList[0]), abs(steigungList[1])]
        diff = abs(steigung[0] - steigung[1])
        if diff == 0:
            steigungMedian = steigung[0]
        elif steigung[0] > steigung[1]:
            steigungMedian = steigung[1] + diff
        else:
            steigungMedian = steigung[0] + diff
        growth = ((0.585+(7650/self.datasetLength))/self.readsPerWindow)*steigungMedian  # (1.35/self.readsPerWindow)*steigungMedian
        return growth

    # Berechnet die Wachstumsrate anhand des Vektorenbetrags
    def calcGrowthVector(self, xVectors, yVectors, relVposList):
        # Funktioniert aktuell nur bei einer Windowanzahl, die
        # glatt durch 100 teilbar ist, oder multipliziert mit einer natürlichen Zahl 100 ergibt, z.B. 50, 200, etc.
        # Vb: Vektorbetrag; Wr: Wachstumsrate; relVpos: relative Vektorposition
        vektorBeträge = []
        wRList = []
        for relVPos in relVposList:
            # relative Position in Vektor Index umrechnen
            v = int(relVPos*self.anzahlWindows)

            # Betrag berechnen
            vektorBetrag = math.sqrt(xVectors[v]**2 + yVectors[v]**2)
            vektorBeträge.append(vektorBetrag)

            # Wachstumsrate berechnen
            if relVPos == 0:
                # HyperbolicReg: Vb = 2.1618163138193 - (1.1637523144608/Wr)
                # => Wr = 1.1637523144608/(-Vb + 2.1618163138193)
                wrV0 = 1.1637523144608/(-vektorBetrag + 2.1618163138193)
                wRList.append(wrV0)
            elif relVPos == 0.1:
                # HyperbolicReg: Vb = 1.8101018100695 - (0.8022883449255/Wr)
                # => Wr = 0.8022883449255/(-Vb + 1.8101018100695)
                wRList.append(0.8022883449255/(-vektorBetrag + 1.8101018100695))
    
        return[wrV0]

    # Berechnet Vektorenplot für polares Koordinatensystem
    def calcVectorplotPolar(self, readAmountPerSection, steigung):
        # 0 bis 0.5, bzw. 0 bis pi
        theta1 = np.linspace(0, np.pi, int(0.5*(self.anzahlWindows)))
        r1 = steigung[0] * (theta1/(2*math.pi)) + readAmountPerSection[0]

        # 0.5 bis 1, bzw. pi bis 2pi
        theta2 = np.linspace(np.pi, 2*np.pi, int(0.5*(self.anzahlWindows)))
        yAchsenAbschnitt = -0.5*steigung[1] + readAmountPerSection[int(self.anzahlWindows/2)]
        r2 = steigung[1] * (theta2/(2*math.pi)) + yAchsenAbschnitt

        r = np.concatenate([r1, r2])
        theta = np.concatenate([theta1, theta2])
        rNormalisiert = r/(self.datasetLength/self.anzahlWindows)

        return [rNormalisiert, theta]

    # Get-Methoden
    def getAnzahlWindows(self):
        return self.anzahlWindows

    def getReadsPerWindow(self):
        return self.readsPerWindow

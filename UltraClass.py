import os
import csv
import math
import numpy as np
import matplotlib.pyplot as pyplot
from sklearn.linear_model import LinearRegression


class UltraClass:

    def __init__(self, filename, thresholdLuecke, thresholdUeberschuss, readsPerWindow):
        self.filename = filename
        self.thresholdLuecke = thresholdLuecke
        self.thresholdUeberschuss = thresholdUeberschuss
        file = open(self.filename)
        csvreader = csv.reader(file)
        csvreaderlist = list(csvreader)
        datasetLength = len(csvreaderlist)
        self.anzahlWindows = datasetLength//readsPerWindow
        #self.readsPerWindow = readsPerWindow Wird später erst in calcWinkel definiert, da
        #der Wert wegen unterschiedlicher Datensatzlängen abweichen kann


    def readFile(self):
        file = open(self.filename)
        csvreader = csv.reader(file)
        csvreaderlist = list(csvreader)
        datasetLength = len(csvreaderlist)
        xAxisDiagram = list(np.arange(0, 1, 1/self.anzahlWindows))
        if(len(xAxisDiagram) > self.anzahlWindows):
            del xAxisDiagram[-1]
        readsPerSection = [[] for _ in range(self.anzahlWindows)] 

        #Daten für den Vektorenplot
        xPosSection = [[] for _ in range(self.anzahlWindows)]
        yPosSection = [[] for _ in range(self.anzahlWindows)]

        datasetList = []

        #Daten auslesen und einordnen
        for row in csvreaderlist:
            value = float(row[0])
            datasetList.append(value)
            index = int(value*self.anzahlWindows)
            if value >= 1:
                index = 0
            readsPerSection[index].append(value) # dem jeweiligen Window zugeordnet
            degree = value * 360 + 90
            if degree > 360:
                degree -= 360
            x = math.cos(math.radians(degree)) # x- und y-Position werden bestimmt
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
                vectorX+=x
            
            vectorY = 0
            for y in yPosSection[window]:
                vectorY+=y

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


    def datensatzVerschieben(self, datasetList, readAmountPerSection, gapBereiche, resetValue = 0):
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


    def calcWinkel(self, sortedData):
        self.readsPerWindow = int(len(sortedData)/self.anzahlWindows)
        degreeDiffList = []
        xList = []
        totalSum = 0
        # ??? Könnten hier nicht theoretisch Daten ausgelassen werden wenn sich sortedData nicht durch messabsand teilen lässt?
        # der Winkel wird berechnet und die Differenz angegeben
        for i in range(0, len(sortedData)-self.readsPerWindow, self.readsPerWindow):
            degree1 = sortedData[i]*360
            degree2 = sortedData[i+self.readsPerWindow]*360
            degreeDiff = degree2 - degree1
            degreeDiffList.append(degreeDiff)
            xList.append(sortedData[i])
            totalSum += degreeDiff
        
        # die Standartabweichung wird bestimmt
        avg = totalSum/len(degreeDiffList)
        varianz = 0
        for degreeDiff in degreeDiffList:
            varianz += (degreeDiff - avg)**2
        varianz = varianz/len(degreeDiffList)
        standardAbw = math.sqrt(varianz)

        # Einzelabweichung = ea
        relEaList = [] # Relative Abweichung von Durchschnitt
        for degreeDiff in degreeDiffList:
            relEaList.append((degreeDiff-avg) / avg)

        #print(xList)

        return [degreeDiffList, xList, avg, standardAbw, relEaList]


    def determineGaps(self, relEaList, xList): # thresholdLuecke von 1 = 100% Abweichung (Bezogen auf die Abweichung vom Durchschnittabstand[avg])
        gapBereiche = []
        for relEaIndex in range(len(relEaList)):
            if relEaList[relEaIndex] >= self.thresholdLuecke: # wenn die Abweichung zu stark ist -> Lücke
                gap = relEaIndex

                anfang = xList[gap]
                if anfang < 0.005:
                    anfang = 0

                if gap/self.anzahlWindows >= xList[-1]:
                    ende = 1
                else:
                    ende = xList[gap+1]
                gapBereiche.append([anfang, ende])
            elif relEaList[relEaIndex] <= self.thresholdUeberschuss:
                gap = relEaIndex
                anfang = xList[gap]
                if anfang < 0.005:
                    anfang = 0
                
                if gap/self.anzahlWindows >= xList[-2]:
                    ende = 1  
                else:
                    ende = xList[gap+1]
                """print("G:",gap)
                print("X:",len(xList))"""
                gapBereiche.append([anfang, ende])
        return gapBereiche


    def fillGaps(self, gapBereiche, readAmountPerSection, xAxisDiagram):
        xAxisDiagram = list(xAxisDiagram) # Weil es vorher ein np.arange()-Objekt ist
        readAmount1 = readAmountPerSection[:len(readAmountPerSection)//2] # Listen aufteilen 0-0.5; 0.5-1
        readAmount2 = readAmountPerSection[len(readAmountPerSection)//2:]
        xAxis1 = xAxisDiagram[:len(xAxisDiagram)//2]
        xAxis2 = xAxisDiagram[len(xAxisDiagram)//2:]

        foundWindows = []
        halfWindow = (1/self.anzahlWindows)/2
        for gap in gapBereiche:
            deletedWindows = [] # bis 0.5 werden alle falschen Windows gesucht
            for i in range(len(xAxis1)):
                if (gap[0] <= xAxis1[i] <= gap[1]) or (xAxis1[i]-halfWindow)<=gap[0]<=(xAxis1[i]+halfWindow) or (xAxis1[i]-halfWindow)<=gap[1]<=(xAxis1[i]+halfWindow):
                    deletedWindows.append(i)
            deletedWindows = sorted(deletedWindows, reverse=True)
            for delWindow in deletedWindows:
                del readAmount1[delWindow]
                foundWindows.append(xAxis1.pop(delWindow))
            deletedWindows = [] # ab 0.5 werden alle falschen Windows gesucht
            for i in range(len(xAxis2)):
                if (gap[0] <= xAxis2[i] <= gap[1]) or (xAxis2[i]-halfWindow)<=gap[0]<=(xAxis2[i]+halfWindow) or (xAxis2[i]-halfWindow)<=gap[1]<=(xAxis2[i]+halfWindow):
                    deletedWindows.append(i)
            deletedWindows = sorted(deletedWindows, reverse=True)
            for delWindow in deletedWindows:
                del readAmount2[delWindow]
                foundWindows.append(xAxis2.pop(delWindow))

        # zeigt den allgemeinen Durchschnitt in einem Graph an 
        """readAmount1 = sorted(readAmount1)
        readAmount2 = sorted(readAmount2)
        xAxis1 = sorted(xAxis1)
        xAxis2 = sorted(xAxis2)"""
        if len(readAmount1) > 0:
            model1 = LinearRegression() 
            model1.fit(np.array(xAxis1).reshape((-1, 1)), readAmount1)
            linReg1 = model1.predict(np.array(xAxis1).reshape((-1, 1)))
        if len(readAmount2) > 0:
            model2 = LinearRegression()
            model2.fit(np.array(xAxis2).reshape((-1, 1)), readAmount2)
            linReg2 = model2.predict(np.array(xAxis2).reshape((-1, 1)))
        
        if len(readAmount1) == 0 and len(readAmount2) == 0:
            print("Regression konnte nicht gebildet werden. Datensatz oder die Parameter sind fehlerhaft!")
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
        xValuesEllipse = []
        yValuesEllipse = []
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

            xValuesEllipse.append(x*filledValue/(self.datasetLength/self.anzahlWindows))
            yValuesEllipse.append(y*filledValue/(self.datasetLength/self.anzahlWindows))

        return[[xAxis1, linReg1], [xAxis2, linReg2], [foundWindows, filledValues], [xValuesEllipse, yValuesEllipse], [model1.coef_, model2.coef_]]


    def getWindowAbweichung(self, foundWindows, filledValues, readAmountPerSectionDict, readsPerSectionDict, createFiles = True, iteration = 1, originalFile = None):
        windowAbwDict = {}
        betterDataFileName = ""
        for i in range(len(foundWindows)):
            fw = foundWindows[i]
            fv = filledValues[i]
            originalValue = readAmountPerSectionDict[fw]
            diff = float(originalValue - fv) # wie viele Reads zu viel bzw. zu wenig sind 
            relDiff = str(int((originalValue / fv)*10000)/100) +"%" # realtiv zum erwartetem Wert

            #Alte Werte mit generierten Ersetzen
            #readsPerSectionDict[fw] = [fw]*int(fv) #Setze fv mal (prognostizierte Häufigkeit) den Wert des Windows ein
            #Alternative:
            newWindowData = []
            lowerBound = fw 
            upperBound = fw + (self.anzahlWindows/self.datasetLength)
            stepSize = (upperBound-lowerBound) / int(fv)

            for v in np.arange(lowerBound, upperBound, stepSize):
                newWindowData.append(v.item()) #.item macht aus v ein float anstelle von numpy float
            readsPerSectionDict[fw] = newWindowData
            windowAbwDict[fw] = [diff, relDiff]
        
        if createFiles:
            #Daten in csv schreiben
            if not originalFile:
                nameFile = self.filename.rsplit('/', 1)[-1]
            else:
                nameFile = originalFile.rsplit('/', 1)[-1]
            infoDataset = str(self.anzahlWindows)+"_"+str(self.datasetLength)+"_"+str(self.thresholdLuecke)+"_"+str(self.thresholdUeberschuss)+"_$$_"
            if not os.path.isdir(f'Output/BetterDataset/{iteration}'):
                os.mkdir(f'Output/BetterDataset/{iteration}')
            betterDataFileName = f'Output/BetterDataset/{iteration}/NewData_{infoDataset}{nameFile}'
            with open(betterDataFileName, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ', quotechar='|')    
                for key in readsPerSectionDict:
                    for value in readsPerSectionDict[key]:
                        writer.writerow([value])
                csvfile.close()

            
            nameFile = self.filename.rsplit('/', 1)[-1]
            infoDataset2 = str(self.anzahlWindows)+"_"+str(self.datasetLength)+"_"+str(self.thresholdLuecke)+"_"+str(self.thresholdUeberschuss)+"_$$_"
            cd = 'Output/AnalyseReads/Analyse_' + infoDataset2 + nameFile
            with open(cd, 'w', newline='') as csvfile2:
                writer2 = csv.writer(csvfile2, delimiter=' ', quotechar='|')
                #writer2.writerow(["Position"] + ["Read"] + ["Relative Abweichung"])
                for key in windowAbwDict:
                    writer2.writerow([key] + [windowAbwDict[key][0]] + [windowAbwDict[key][1]])
                csvfile2.close()
            
        return [windowAbwDict, betterDataFileName]


    def idealeEllipse(self, linReg1):
        calcValue = (((self.datasetLength/self.anzahlWindows)/100)**2)*2
        xValuesList = []
        yValuesList = []
        linReg1List = np.array(linReg1)
        linReg1List = linReg1List.flatten().tolist()
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
            

    def windowQualität(self, readsPerSectionDict):
        #Aktuell wird nur die Qualität des angegebenen Windows berechnet und noch nicht für jedes Window.
        #das erste window (von 0 bis ...) hat hier den Index 0

        readAbweichungProWindow = []
        for windowkey in readsPerSectionDict:
            window = readsPerSectionDict[windowkey]
        
         #Standartabweichung der Readabstände in einem Window:
            window.sort()
            abstandSumme = 0
            abstandListe = []
            for read in range(len(window)-1):
                abstandListe.append(window[read+1] - window[read])
                abstandSumme += (window[read+1] - window[read]) #Aktuell nur die "inneren Abstände" -> nur die Abstände zwischen den Reads, also nicht zu den Windowbounds

            varianz = 0
            if len(abstandListe) == 0:
                standartabweichung = 0
            else:
                avg = abstandSumme/len(abstandListe)
                for abstand in abstandListe:
                    varianz += (abstand-avg)**2
                varianz = varianz/len(abstandListe)
                standartabweichung = math.sqrt(varianz)
            readAbweichungProWindow.append(standartabweichung*100000) #Um eine bessere Darstellung zu ermöglichen, werden die Werte hochskaliert

        
        return readAbweichungProWindow

        """
        winLowerBound = 1/anzahlWindows * windowIndex
        winUpperBound = 1/anzahlWindows * (windowIndex+1)
        winHaelfte =  (winLowerBound+winUpperBound)/2

        #avg berechnen:
        totalSum = 0
        anzahlReads = 0
        for read in readsPerSection[windowIndex]:
            totalSum += read
            anzahlReads +=1
        avg = totalSum/anzahlReads

        #Standartabweichung (von den Abständen zu winHaelfte):
        varianz = 0
        for read in window:
            varianz += read**2
        varianz = varianz/anzahlReads
        """
    

    def kalibrieren(self, xVectorsEllipse, yVectorsEllipse, xVectors, yVectors):
        #print("Wurzel: " + str(math.sqrt(((xVectors[23]+xVectors[24])/2)**2+((yVectors[23]+yVectors[24])/2)**2)))
        idealisierung = 0.9591384589301084 
        punkt1 = math.sqrt((xVectors[round(self.anzahlWindows* 0.24)])**2+(yVectors[round(self.anzahlWindows* 0.24)])**2)
        punkt2 = math.sqrt((xVectors[round(self.anzahlWindows* 0.74)])**2+(yVectors[round(self.anzahlWindows* 0.74)])**2)
        streckfaktor = (punkt1/idealisierung + abs(punkt2)/idealisierung)/2
        print("Streckfaktor: "+str(streckfaktor))
        for i in range(len(xVectorsEllipse)):
            xVectorsEllipse[i] = xVectorsEllipse[i] * streckfaktor
            yVectorsEllipse[i] = yVectorsEllipse[i] * streckfaktor
        
        return [xVectorsEllipse, yVectorsEllipse]

    def calcGrowthStabw(self, datasetList, standardAbw):
        growth = 0.8*((1+len(datasetList)/(len(datasetList)*100))**self.anzahlWindows)**standardAbw
        return growth

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
        growth = (1.35/self.readsPerWindow)*steigungMedian
        return growth

    def calcGrowthVector(self, xVectors, yVectors, relVposList):
        #MAN MUSS!!!!!! AnzahlWindows = 100 haben SONST FUNKTIONIERT ES NICHT
        #bzw. muss es glatt durch 100 teilbar sein, oder multipliziert mit einer natürlichen Zahl 100 ergeben, z.B. 50, 200, etc.
        #Vb: Vektorbetrag; Wr: Wachstumsrate; relVpos: relative Vektor Position

        vektorBeträge = []
        wRList = []
        for relVPos in relVposList:
            #relative Position in Vektor Index umrechnen
            v = int(relVPos*self.anzahlWindows)
            print('absoluter V: '+str(v))
            
            #Betrag berechnen
            vektorBetrag = math.sqrt(xVectors[v]**2 + yVectors[v]**2)
            print('BETRAG: '+str(vektorBetrag))
            vektorBeträge.append(vektorBetrag)

            #Wachstumsrate berechnen
            #Ich habe nicht für jeden Vektor eine Regression
            if relVPos == 0:
                #HyperbolicReg: Vb = 2.1618163138193 - (1.1637523144608/Wr)
                #=> Wr = 1.1637523144608/(-Vb + 2.1618163138193)
                wRList.append(1.1637523144608/(-vektorBetrag + 2.1618163138193))
            elif relVPos == 0.1:
                #HyperbolicReg: Vb = 1.8101018100695 - (0.8022883449255/Wr)
                #=> Wr = 0.8022883449255/(-Vb + 1.8101018100695)
                wRList.append(0.8022883449255/(-vektorBetrag + 1.8101018100695))
            elif relVPos == 0.2:
                #
                #
                wRList
        print('wRList: '+str(wRList))

        

        
        
        
        '''wachstumsrateV2 = 0
        wachstumsrateV49 = 0
        avg = 0

        #Vectorbeträge ausrechnen:
        vectorBeträge = []
        for vector in range(len(xVectors)):
            vectorBeträge.append(math.sqrt(xVectors[vector]**2 + yVectors[vector]**2))

        # X: Wachstumsrate, Y: Betrag vom Vektor
        #Vektor 2 linReg => Y1 = 26.776254501802 * X + 85.410780312125
        #==> X = (Y1-85.410780312125)/26.776254501802
        #Vektor 49 linReg => Y2 = -17.834588235294 * X + 120.08470588235
        #==> X = (Y2-120.08470588235)/-17.834588235294

        #Wachstumsrate über Vektor 2 bestimmen:
        wachstumsrateV2 = (vectorBeträge[2]-85.410780312125)/26.776254501802
        #Wachstumsrate über Vektor 49 bestimmen:
        wachstumsrateV49 = (vectorBeträge[49]-120.08470588235)/-17.834588235294
        #avg bestimmen
        avg = (wachstumsrateV2+wachstumsrateV49)/2

        print('wachstumsrateV2: ' + str(wachstumsrateV2))
        print('wachstumsrateV49: ' + str(wachstumsrateV49))
        print('avg: ' + str(avg))'''



    
    # Get-Methoden
    def getAnzahlWindows(self):
        return self.anzahlWindows

    
    def getReadsPerWindow(self):
        return self.readsPerWindow


import os
from UltraClass import UltraClass
import matplotlib.pyplot as pyplot
import csv

#User Input
folderRelPath = 'Probedaten/position_files'
startWithIndex = 0

readsPerWindow = 100
thresholdLuecke = 1
thresholdUeberschuss = 1
printLenDataset = True
searchMax = False
wachstumsdiagramme = True
createFiles = False
windowQualität = True

#Preperation
folderPosFiles = os.listdir("./"+folderRelPath)
folderPosFiles.sort()

#searchMax
#für Probedaten/position_files: maxlen=1724285 3011: Dundee106_S18_R1.ndp.trm.s.mm.dup.mq30.calmd.filt_1_AE004091_2_Pseudomonas_aeruginosa_PAO1__complete_genome_BAC_pos.csv
if searchMax == True:
    print('items in Folder: '+str(len(folderPosFiles)))
    maxlen = -1
    maxlenfile = ''
    i=0
    for filename in folderPosFiles:
        file = open(folderRelPath+"/"+str(filename))
        csvreader = csv.reader(file)
        csvreaderlist = list(csvreader)
        datasetLength = len(csvreaderlist)
        if datasetLength > maxlen:
            maxlen  = datasetLength
            maxlenfile = filename
            maxlenfileindex = i
        if i%100 == 0:
            print(str(i)+" curmaxlen: "+str(maxlen))
        i+=1
    print('maxlen='+str(maxlen)+' '+str(i)+': '+maxlenfile)



#Vektorplot Scanner
i=0
for filename in folderPosFiles:
    if i < startWithIndex:
        i+=1
        continue
    try:
        "Main!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        ultraClass = UltraClass(folderRelPath+"/"+filename, thresholdLuecke, -thresholdUeberschuss, readsPerWindow)

        # für die originale Datei werden die Daten für die Diagramme bestimmt
        datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage = ultraClass.readFile()
        if printLenDataset == True:
            print(str(len(datasetList)))
        degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList)
        gapBereiche = ultraClass.determineGaps(relEaList, xList)
        linReg1, linReg2, filledGaps, filledEllipse, steigung = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
        readAbweichungProWindow = ultraClass.windowQualität(readsPerSectionDict)
        windowAbwDict, betterDataFileName = ultraClass.getWindowAbweichung(filledGaps[0], filledGaps[1], readAmountPerSectionDict, readsPerSectionDict, createFiles)
        #ultraClass.calcGrowthVector(xVectors, yVectors,[0, 0.1])

        #Vektorenplot
        pyplot.figure(num=str(i)+": "+filename)
        pyplot.plot(xVectors, yVectors, '.', color='blue')
        pyplot.plot(filledEllipse[0], filledEllipse[1], '.', color='red')
        pyplot.plot([0], [0], 's', color='black')
        #pyplot.plot([m[0]], [m[1]], 'v', color='green')
        pyplot.gca().set_aspect('equal', adjustable='box')
        pyplot.grid(True, which='both')
        pyplot.axhline(y=0, color='k')
        pyplot.axvline(x=0, color='k')
        #pyplot.grid(color='blue', linestyle='-', linewidth=1)

        pyplot.show()
        print(str(i)+": "+filename)
    except KeyboardInterrupt:
        exit()
    except:
        print(str(i)+": [Error] "+filename)
    i+=1


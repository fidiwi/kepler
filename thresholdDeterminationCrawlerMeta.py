import csv
import os
import re
import winkelMessen

dir = "Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/"
degreeDiffParameter = 100

for filename in os.listdir(dir):
    file = open(dir+filename)
    csvreader = csv.reader(file)
    datasetList = []
    for row in csvreader:
        value = float(row[0])
        datasetList.append(value)
    datasetList.sort()
    degreeDiff = winkelMessen.calcWinkel2(datasetList, degreeDiffParameter)
    eaList, relEaList = winkelMessen.getEinzelAbweichung(degreeDiff[0], degreeDiff[2])
    


import csv
import numpy as np
import matplotlib.pyplot as pyplot

windows = 1000

file = open('data.subsample/Hirnet1_S1.subsample.csv')
csvreader = csv.reader(file)
xAxis = np.arange(0, 1+1/windows, 1/windows)
readsPerSection = [[] for _ in range(windows+1)]

#Daten auslesen und einordnen
for row in csvreader:
    value = float(row[0])
    index = int(value*windows)
    readsPerSection[index].append(value)

#Daten umwandeln
numberPerSection = [0] * (windows+1)
for section in range(windows+1):
    numberPerSection[section] = len(readsPerSection[section])
print(numberPerSection)
pyplot.plot(xAxis, numberPerSection)
pyplot.xlabel("Position")
pyplot.ylabel("reads/section")
pyplot.show()
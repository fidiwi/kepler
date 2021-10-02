import csv
import numpy as np
import matplotlib.pyplot as pyplot

file = open('data.subsample/Hirnet1_S1.subsample.csv')
csvreader = csv.reader(file)
xAxis = np.arange(0, 1.01, 0.01)
readsPerSection = [[] for _ in range(101)]

#Daten auslesen und einordnen
for row in csvreader:
    value = float(row[0])
    index = int(value/0.01)
    readsPerSection[index].append(value)

#Daten umwandeln
numberPerSection = [0] * 101
for section in range(101):
    numberPerSection[section] = len(readsPerSection[section])
print(numberPerSection)
pyplot.plot(xAxis, numberPerSection)
pyplot.xlabel("Position")
pyplot.ylabel("reads/section")
pyplot.show()
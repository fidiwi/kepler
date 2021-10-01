import csv
import matplotlib.pyplot as pyplot

file = open('data.subsample/differnces_10000_2.0_90_0,.45000_.55000,1_pos.csv')
csvreader = csv.reader(file)
rows = []
next(csvreader)
for row in csvreader:
    rows.append([float(row[0])])
print(rows)
pyplot.plot(rows)
pyplot.show()
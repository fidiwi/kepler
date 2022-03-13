import matplotlib.pyplot as pyplot
import numpy as np
from sklearn.linear_model import LinearRegression

readList = []
xValues = []
lenDataset = 100
for i in range(lenDataset):
    readList.append(1)
    xValues.append(i/lenDataset)

toXValue = 0.4
newPoly = 0.15
def calc(toXValue):
    if toXValue  > 0:
        for i in range(int(toXValue*len(readList))):
            readList[i] = readList[i] * 2
            xMirrow = int(i + (len(readList)/2-i)*2) -1
            readList[xMirrow] = readList[xMirrow] * 2

        calc(toXValue-newPoly)

calc(toXValue)

model = np.poly1d(np.polyfit(xValues, readList, 2))
polyline = np.linspace(0, 1, 50)

xList1 = xValues[:lenDataset//2]
xList2 = xValues[lenDataset//2:]
value1 = readList[:lenDataset//2]
value2 = readList[lenDataset//2:]
model1 = LinearRegression()
model1.fit(np.array(xList1).reshape((-1, 1)), value1)
linReg1 = model1.predict(np.array(xList1).reshape((-1, 1)))
model2 = LinearRegression()
model2.fit(np.array(xList2).reshape((-1, 1)), value2)
linReg2 = model2.predict(np.array(xList2).reshape((-1, 1)))

print(readList)
pyplot.figure(num='Readamount pro Window')
pyplot.plot(xValues, readList)
pyplot.plot(polyline, model(polyline))
#pyplot.plot(xList1, linReg1, color='green')
#pyplot.plot(xList2, linReg2, color='green')
pyplot.show()
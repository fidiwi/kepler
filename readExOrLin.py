import matplotlib.pyplot as pyplot
import numpy as np
from sklearn.linear_model import LinearRegression
import math

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
coef3 = np.polyfit(xValues[:len(xValues)//2], np.log(readList[:len(readList)//2]), 1, w=np.sqrt(readList[:len(readList)//2]))
coef4 = np.polyfit(xValues[len(xValues)//2:], np.log(readList[len(readList)//2:]), 1, w=np.sqrt(readList[len(readList)//2:]))
model3 = lambda x : np.exp(coef3[1]) * np.exp(coef3[0]*x)
model4 = lambda x : np.exp(coef4[1]) * np.exp(coef4[0]*x)
polyline1 = np.linspace(0, 0.5, 25)
polyline2 = np.linspace(0.5, 1, 25)

xList1 = xValues[:lenDataset//2]
xList2 = xValues[lenDataset//2:]
value1 = readList[:lenDataset//2]
value2 = readList[lenDataset//2:]
print(model)
print(coef3[1])
model1 = LinearRegression()
model1.fit(np.array(xList1).reshape((-1, 1)), value1)
linReg1 = model1.predict(np.array(xList1).reshape((-1, 1)))
model2 = LinearRegression()
model2.fit(np.array(xList2).reshape((-1, 1)), value2)
linReg2 = model2.predict(np.array(xList2).reshape((-1, 1)))

xVectorsQuad = []
yVectorsQuad = []
for i in range(len(xValues)):
    winkel = (i/len(xValues))*360 
    y=math.cos(math.radians(winkel)) * model(xValues)[i]
    x=math.sin(math.radians(winkel)) * model(xValues)[i]
    xVectorsQuad.append(x)
    yVectorsQuad.append(y)

xVectorsExp = []
yVectorsExp = []
for i in range(len(polyline1)):
    winkel = (i/(len(polyline1)*2))*360
    y=math.cos(math.radians(winkel)) * model3(polyline1)[i]
    x=math.sin(math.radians(winkel)) * model3(polyline1)[i]
    xVectorsExp.append(x)
    yVectorsExp.append(y) 
for i in range(len(polyline2)):
    winkel = (i/(len(polyline2)*2))*360 + 180
    y=math.cos(math.radians(winkel)) * model4(polyline2)[i]
    x=math.sin(math.radians(winkel)) * model4(polyline2)[i]
    xVectorsExp.append(x)
    yVectorsExp.append(y) 

xVectorsLin = []
yVectorsLin = []
for i in range(len(xList1)):
    winkel = (i/(len(linReg1)*2))*360
    y=math.cos(math.radians(winkel)) * linReg1[i]
    x=math.sin(math.radians(winkel)) * linReg1[i]
    xVectorsLin.append(x)
    yVectorsLin.append(y)
for i in range(len(xList2)):
    winkel = (i/(len(linReg2)*2))*360 + 180
    y=math.cos(math.radians(winkel)) * linReg2[i]
    x=math.sin(math.radians(winkel)) * linReg2[i]
    xVectorsLin.append(x)
    yVectorsLin.append(y)


print(readList)
pyplot.figure(num='Readamount pro Window')
# Datensatz
pyplot.plot(xValues, readList)
# Quadratische Regression
pyplot.plot(xValues, model(xValues), color='orange')
# Exponentielle Regression
pyplot.plot(polyline1, model3(polyline1), color='blue')
pyplot.plot(polyline2, model4(polyline2), color='blue')
# Lineare Regression
pyplot.plot(xList1, linReg1, color='green')
pyplot.plot(xList2, linReg2, color='green')

# Vektorengraph
pyplot.figure(num='Vektorengraph')
pyplot.plot(xVectorsQuad, yVectorsQuad, '.', color='orange')
pyplot.plot(xVectorsExp, yVectorsExp, '.', color='blue')
pyplot.plot(xVectorsLin, yVectorsLin, '.', color='green')
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.grid(True, which='both')
pyplot.show()
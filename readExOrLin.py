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

xValues = [8.16706211158591e-05, 0.010247729920939586, 0.020041122492911678, 0.03110658776351327, 0.04432649714699721, 0.05741120647745168, 0.06972913456243979, 0.08083459006337368, 0.09409901735534631, 0.10638763619339897, 0.12093227371737914, 0.13744218457365065, 0.15214909388973907, 0.16701650792769185, 0.18544440595722178, 0.20384740070143714, 0.21864415294703943, 0.23722857508129225, 0.25919358402499526, 0.2793771194941188, 0.30655076902435907, 0.33319394020282345, 0.3640970972384051, 0.40015194466976145, 0.43966580714331405]
readList = [3.6597813479365415, 3.5256213259099534, 3.9835674974165736, 4.759167378054219, 4.710495358963609, 4.43445411059572, 3.9979639803361984, 4.775193825110147, 4.423902781698956, 5.236069508632859, 5.943567908257748, 5.29448735379183, 5.352269053663001, 6.634043290630771, 6.625078107917531, 5.32683080841683, 6.690391968331014, 7.907403219733084, 7.26607276888447, 9.7825138308865, 9.59154162424717, 11.125136532809407, 12.979745075288292, 14.224990490478916, 26.47139675103739]


model = np.poly1d(np.polyfit(xValues, readList, 2))
coef3 = np.polyfit(xValues, np.log(readList), 1, w=np.sqrt(readList))
model3 = lambda x : np.exp(coef3[1]) * np.exp(coef3[0]*x)
polyline = np.linspace(0, 1, 25)

xList1 = xValues[:lenDataset//2]
xList2 = xValues[lenDataset//2:]
value1 = readList[:lenDataset//2]
value2 = readList[lenDataset//2:]
print(model)
print(coef3[1])
"""model1 = LinearRegression()
model1.fit(np.array(xList1).reshape((-1, 1)), value1)
linReg1 = model1.predict(np.array(xList1).reshape((-1, 1)))
model2 = LinearRegression()
model2.fit(np.array(xList2).reshape((-1, 1)), value2)
linReg2 = model2.predict(np.array(xList2).reshape((-1, 1)))
"""
print(readList)
pyplot.figure(num='Readamount pro Window')
pyplot.plot(xValues, readList)
pyplot.plot(xValues, model(xValues))
pyplot.plot(polyline, model3(polyline))
#pyplot.plot(xList1, linReg1, color='green')
#pyplot.plot(xList2, linReg2, color='green')
pyplot.show()
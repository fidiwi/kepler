from numpy.lib.nanfunctions import nanmax
import testdatei
import numpy as np
import matplotlib.pyplot as pyplot

xs = []
ys = []
zs = []


def berechnen(fileName, minWindows, maxWindows, stepSize):
    global xs
    global ys
    global zs

    #iterationen = (maxWindows - minWindows) / stepSize
    
    for i in range(minWindows, maxWindows, stepSize):
    
        for i in range(minWindows, maxWindows, stepSize):
            curWindows = minWindows + i*stepSize

            VectorenListe = testdatei.vectorenBerechnen(fileName, curWindows)
            xVektoren = VectorenListe[0]
            yVektoren = VectorenListe[1]

            xs.extend(xVektoren)
            ys.extend(yVektoren)
            zs.extend([curWindows]*curWindows)

            

            

            #print(VectorenListe)
            #print(xVektoren)
            #print(yVektoren)


fig = pyplot.figure()
ax = fig.add_subplot(projection='3d')


fileName = 'kepler/Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv'
minWindows = 100
maxWindows = 500
stepSize = 50
berechnen(fileName, minWindows, maxWindows, stepSize)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Anzahl Windows')

ax.scatter(xs, ys, zs)
pyplot.show()
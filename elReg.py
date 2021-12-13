import math

def fehlerEliminieren(xVectors, yVectors):
    xVectorsCopy = xVectors
    yVectorsCopy = yVectors

    ketteY = [yVectors[0]]
    ketteX = [xVectors[0]]
    for yVector in ketteY:
        minAbstand = None
        pointWithMinAbstand = None
        for nextPossibleVector in yVectors:
            if yVector == nextPossibleVector:
                continue
            x1 = xVectors[yVectors.index(yVector)]
            y1 = yVector

            x2 = xVectors[yVectors.index(nextPossibleVector)]
            y2 = nextPossibleVector

            diffX = abs(x1-x2)
            diffY = abs(y1-y2)

            abstand = math.sqrt(diffX**2 + diffY**2)
            if minAbstand > abstand:
                minAbstand = abstand
                pointWithMinAbstand = yVectors.index(nextPossibleVector)
        ketteY.append(yVectors[pointWithMinAbstand])
        ketteX.append(xVectors[pointWithMinAbstand])
        del xVectors[pointWithMinAbstand]
        del yVectors[pointWithMinAbstand]
    
    return 
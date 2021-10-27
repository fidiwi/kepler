import testdatei

anzahlWindows = 4
fileName = 'kepler/Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv'

VectorenListe = testdatei.__init__(fileName, anzahlWindows)
xVectors = VectorenListe[0]
yVectors = VectorenListe[1]

print(VectorenListe)
print(xVectors)
print(yVectors)

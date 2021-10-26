import testdatei

anzahlWindows = 100
fileName = 'kepler/Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv'

VextorenListe = testdatei.__init__(fileName, anzahlWindows)
print(VextorenListe)
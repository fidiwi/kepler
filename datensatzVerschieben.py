from UltraClass import UltraClass
import csv
filenameVerschoben = "Output/BackMovedDataset/backMovedDataset_0.19_verschoben_0.2_10000_4.0_20_.20000,.40000_pos.csv"

file = open(filenameVerschoben)
csvreader = csv.reader(file)
csvreaderlist = list(csvreader)
verschiebeFaktor = 0.2

nameFile = filenameVerschoben.rsplit('/', 1)[-1]
cd = 'Probedaten/Beispiesamples/Mail_lutz_3/verschobeneDatensätze/verschoben_' + str(verschiebeFaktor) + "_"+ nameFile
with open(cd, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
    #writer2.writerow(["Position"] + ["Read"] + ["Relative Abweichung"])
    for row in csvreaderlist:
        value = float(row[0]) + verschiebeFaktor
        if value > 1:
            value += -1
        writer.writerow([value])
    csvfile.close()

filename = 'Probedaten/Beispiesamples/Mail_lutz_3/verschobeneDatensätze/verschoben_0.2_10000_4.0_20_.20000,.40000_pos.csv' #Probedaten/Beispiesamples/Mail_lutz_3/Luecken/20_percent/10000_2.0_20_.20000,.40000_pos.csv
readsPerWindow = 100 # Wieviele Reads in einem Window erwartet werden sollen, Windowanzahl passt sich der Datensatzgröße dynamisch an. Probedaten/Beispiesamples/Mail_lutz_3/verschobeneDatensätze/verschoben_0.2_5000_4.0_0.0,0.0_pos.csv
thresholdLuecke = 1
thresholdUeberschuss = -1

ultraClass = UltraClass(filename, thresholdLuecke, thresholdUeberschuss, readsPerWindow)
# für die originale Datei werden die Daten für die Diagramme bestimmt

datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage = ultraClass.readFile()
degreeDiffList, xList, avg, standardAbw, relEaList = ultraClass.calcWinkel(datasetList)
gapBereiche = ultraClass.determineGaps(relEaList, xList)
newFileName = ultraClass.datensatzVerschieben(datasetList, readAmountPerSection, gapBereiche)
print(newFileName)

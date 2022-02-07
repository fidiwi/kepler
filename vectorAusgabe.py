from UltraClass import UltraClass
import xlsxwriter
import os
import math

# Eingaben: Dateiname, Abzahl Windows, Treshold
readsPerWindow = 100 # Wieviele Reads in einem Window erwartet werden sollen, Windowanzahl passt sich der Datensatzgröße dynamisch an. 
thresholdLuecke = 1
thresholdUeberschuss = 1


#--------------------AUSGABE--------------------
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('./Output/VektorAusgabe/5000_VektorAusgabe.xlsx')
worksheet = workbook.add_worksheet()

folderPosFiles = os.listdir("./Probedaten/Beispiesamples/Mail_lutz_3/testdateienLücken") # z.B. Probedaten/Beispiesamples/Mail_lutz_3/5000/5000_3.0_0.0,0.0_pos.csv
folderPosFiles.sort()

#Preperation
worksheet.write(0, 0, 'Datei')
worksheet.write(0, 1, 'Wachstumsrate')
worksheet.write(0, 2, 'AnzahlWindows')
worksheet.write(0, 3, 'ReadsPerWindow')    

row=1
for file in folderPosFiles:
    #Werte Generieren
    ultraClass = UltraClass('Probedaten/Beispiesamples/Mail_lutz_3/testdateienLücken/'+file, thresholdLuecke, -thresholdUeberschuss, readsPerWindow)
    datasetList, readAmountPerSection, readAmountPerSectionDict, readsPerSectionDict, xVectors, yVectors, xAxisDiagram, readAmountPerSectionPercentage = ultraClass.readFile()
    gapBereiche = []
    linReg1, linReg2, filledGaps, filledEllipse, steigung = ultraClass.fillGaps(gapBereiche, readAmountPerSection, xAxisDiagram)
    xValuesL, yValuesL = ultraClass.calcDataFromRegression(linReg1[1])

    if row == 1:
        for j in range(len(xValuesL)):
            worksheet.write(0, j+4, 'Vektor'+str(j))

    #Parameter eintragen
    worksheet.write(row, 0, file)
    if len(folderPosFiles) == 3:
        worksheet.write(row, 1, file[6])
    elif len(folderPosFiles) == 6:
        worksheet.write(row, 1, file[5])
    else:
        print('[WARNING] anderen Ordner für die Vektor Ausgabe verwenden!')
    worksheet.write(row, 2, ultraClass.getAnzahlWindows())
    worksheet.write(row, 3, readsPerWindow)

    #Vektorenbeträge berechnen und eintragen
    col=4
    for vector in range(len(xValuesL)):
        worksheet.write(row, col, math.sqrt(xValuesL[vector]**2 + yValuesL[vector]**2))
        col+=1

    row+=1


#Min/Max

workbook.close()
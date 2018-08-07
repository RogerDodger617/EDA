import xlrd
import openpyxl
import csv
import datetime

todayDate = datetime.datetime.now()
todayYear = todayDate.year
escalationPercentage = 2.36 / 100
feeDict = {}
cfdSummary = [('APN', 'Total APNs', 'Total Levied APNs', 'Old Levy', 'New Levy', 'Levy Sum', 'Escalation Year')]
cfdWorkBook = xlrd.open_workbook('D:\MillerSpatial\EDA\CFD Info\CFD parcels final 2 test.xlsx')
cfdBaseAndEscalationWB = xlrd.open_workbook('D:\MillerSpatial\EDA\CFD Info\CFD Base Fees & Escalation.xlsx')
cfdFinalWrite = openpyxl.load_workbook('D:\MillerSpatial\EDA\CFD Info\CFD parcels final 2 test.xlsx')

cfdSheets = cfdWorkBook.sheet_names()
cfdBaseAndEscalationSheets = cfdBaseAndEscalationWB.sheet_names()

cfdBaseSheet = cfdBaseAndEscalationWB.sheet_by_name(cfdBaseAndEscalationSheets[0])

for i2 in range(1, cfdBaseSheet.nrows):
    rowValues2 = cfdBaseSheet.row_values(i2)
    if rowValues2[0]:
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(rowValues2[3], cfdWorkBook.datemode)
        listValues = [rowValues2[1], year]
        feeDict["CFD " + rowValues2[0]] = listValues

for i in cfdSheets:
    cfdSheet = cfdWorkBook.sheet_by_name(i)
    workSheetWrite = cfdFinalWrite.get_sheet_by_name(i)

    levyInformation = feeDict.get(i, 0)

    escalationValue = levyInformation[0] * escalationPercentage
    if todayYear == levyInformation[1]:
        newLevyValue = levyInformation[0] + escalationValue
    else:
        newLevyValue = levyInformation[0]
    apnCount = 0
    levyEscalationCount = 0

    if 'Bella' in i:
        newLevyValue = 2928.10

    for iN in range(0, cfdSheet.nrows):
        rowValues = cfdSheet.row_values(iN)
        if rowValues[1] == 'District Name':
            apnCount = iN
        if rowValues[4] and 'BRS' in rowValues[4] and '19-20' not in rowValues[5]:
            cellRef = workSheetWrite.cell(row=iN + 1, column=7)
            cellRef.value = round(newLevyValue, 2)

            levyEscalationCount += 1

            print "Sheet {} done".format(i)

    apnTotalCount = cfdSheet.nrows - (apnCount + 1)
    if 'Bella' in i:
        finalLevy = round((levyEscalationCount * newLevyValue), 2)
        finalLevy = finalLevy - .16
        finalLevy = round(finalLevy, 2)
    else:
        finalLevy = round((levyEscalationCount * newLevyValue), 2)

    if int(finalLevy * 10) % 2 == 0:
        pass
    else:
        finalLevy = finalLevy + .01
    cfdSummary.append((i, apnTotalCount, levyEscalationCount, levyInformation[0], 
                       round(newLevyValue, 2),finalLevy, levyInformation[1]))

cfdFinalWrite.save("123test.xlsx")

with open(r'D:\MillerSpatial\EDA\cfdSummary_test.csv', "wb") as f:
    writer = csv.writer(f)
    writer.writerows(cfdSummary)

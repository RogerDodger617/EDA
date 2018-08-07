import re
import xlrd
import glob
import os
import csv
import traceback

ROOTDIR = r'D:\MillerSpatial\EDA\2017_18\Psomas\DataFiles'
wb_pattern = os.path.join(ROOTDIR, '*.xlsx')
workbooks = glob.glob(wb_pattern)
regex = re.compile(r'CSA No.')

minMax = r"D:\MillerSpatial\EDA\2017_18\ExportMaxChargesQuery.xlsx"
minMaxWB = xlrd.open_workbook(minMax)
minMaxSheet = minMaxWB.sheet_by_index(0)
minMaxDict = dict()

testList = [("APN", "District ID", "Elevator", "Levy", "Name", "MaxTax")]

for i4 in range(minMaxSheet.nrows):
    if i4 > 0:
        rowValues = minMaxSheet.row_values(i4)
        minMaxAPN = rowValues[1]
        minMaxTax = rowValues[3]

        if minMaxAPN in minMaxDict:
            minMaxDict[minMaxAPN].append(minMaxTax)
        else:
            minMaxDict[minMaxAPN] = [minMaxTax]

print minMaxDict.get("115210007-5")

for i in range(len(workbooks)):
    try:
        test = workbooks[i]
        workBook = xlrd.open_workbook(workbooks[i])
        sheet = workBook.sheet_by_index(0)
        print "Parsing {}...".format(test)
        for i2 in range(sheet.nrows):
            if i2 > 0:
                rowValuesList = sheet.row_values(i2)
                apnValue = rowValuesList[1]
                disID = rowValuesList[2]
                elevator = rowValuesList[4]
                levy = rowValuesList[7]
                name = rowValuesList[15]
                minMaxTaxGet = [None]

                if apnValue:
                    if type(elevator) is unicode:
                        elevator = 'N'
                    else:
                        elevator = 'Y'

                    if type(apnValue) is unicode:
                        if not regex.search(apnValue):
                            if not regex.search(name):
                                if disID == 681852:
                                    minMaxTaxGet = list(set(minMaxDict.get(apnValue, [0])))
                                    print minMaxTaxGet
                                nextRow = 1
                                while True:
                                    rowValuesListFix = sheet.row_values(i2 + nextRow)
                                    findValue = None
                                    for i3 in range(len(rowValuesListFix)):
                                        findValue = rowValuesListFix[i3]
                                        if type(findValue) is unicode:
                                            if regex.search(findValue):
                                                name = findValue
                                                testList.append((apnValue, disID, elevator, levy, name, minMaxTaxGet[0]))
                                                # print "Added {} to list...".format(test)
                                                break
                                    if not regex.search(findValue):
                                        nextRow += 1
                                    else:
                                        break
                            else:
                                if disID == 681852:
                                    minMaxTaxGet = list(set(minMaxDict.get(apnValue, [0])))
                                    print minMaxTaxGet
                                testList.append((apnValue, disID, elevator, levy, name, minMaxTaxGet[0]))
                                # print "Added {} to list...".format(test)

    except Exception, err:
        print traceback.print_exc()
        pass

print "Writing to excel..."
with open(r'D:\MillerSpatial\EDA\masterTest.csv', "wb") as f:
    writer = csv.writer(f)
    writer.writerows(testList)
print "done"

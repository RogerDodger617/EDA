import re
import xlrd
import glob
import os
import csv
import traceback
import arcpy


def getCheckDigit(apnString, check):
    apnString = int(float(apnString))
    apnString = "{:09}".format(apnString)
    checkDigitMathList = []
    for iSingle in range(len(apnString)):
        apnSingleValue = int(apnString[iSingle])
        checkDigitSingleValue = int(check[iSingle])
        checkDigitMath = apnSingleValue * checkDigitSingleValue
        checkDigitMathList.append(checkDigitMath)

    checkDigitSum = str(sum(checkDigitMathList))
    apn_checkDigit = '{}-{}'.format(apnString, checkDigitSum[-1])
    return apn_checkDigit


ROOTDIR = r'D:\MillerSpatial\EDA\CSA 152 Replacements'
wb_pattern = os.path.join(ROOTDIR, '*.xlsx')
workbooks = glob.glob(wb_pattern)

regex = r'68[^_.\s]+'
checkDigit = '137913791'

replacementDict = {}

# workpsace = r'C:\Users\MillerSpatial-AF\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\Connection to SQLRIAGD01.rivcoca.org.sde'
masterDB = r'GDB_EDA.EDA.csa_master_2018_2019_test'
# arcpy.env.workspace = workpsace
# edit = arcpy.da.Editor(workpsace)
# edit.startEditing()
# print "edit started"
# edit.startOperation()
# print "operation started"


insertFields = ['APN', 'District_ID', 'Elevator', 'Levy', 'Name']

distNameDict = {'681853': 'CSA No. 152 (City of Riverside)',
                '681859': 'CSA No. 152 (City of LaQuinta)',
                '681857': 'CSA No. 152 (City of Desert Hot Springs)',
                '681861': 'CSA No. 152 (City of Murrieta)',
                '681854': 'CSA No. 152 (City of Corona)',
                '681867': 'CSA No. 152 (City of Lake Elsinore)',
                '681864': 'CSA No. 152 (City of Palm Springs)',
                '681860': 'CSA No. 152 (City of Moreno Valley)',
                '681862': 'CSA No. 152 (City of Norco)',
                '681868': 'CSA No. 152 (City of San Jacinto)'}

for i in range(len(workbooks)):
    try:
        findDisID = re.search(regex, workbooks[i])
        findDisID = findDisID.group(0)
        workBook = xlrd.open_workbook(workbooks[i])
        sheet = workBook.sheet_by_index(0)
        headerRow = sheet.row_values(0)

        apnKeywords = ['apn', 'assessor', 'parcel']
        levyKeyWords = ['levy', 'charge']
        apnIndex = None
        levyIndex = None

        for iA in range(len(headerRow)):
            apnCellValue = str(headerRow[iA]).lower()
            for word in apnKeywords:
                if word in apnCellValue:
                    apnIndex = iA
                    break

        for iL in range(len(headerRow)):
            levyCellValue = str(headerRow[iL]).lower()
            for word in levyKeyWords:
                if word in levyCellValue:
                    levyIndex = iL
                    break
        if '-' in findDisID:
            findDisID = findDisID.replace('-', '')

        replacementList = []
        for nRows in range(sheet.nrows):
            if nRows > 0:
                apnValue = str(sheet.cell_value(nRows, apnIndex))
                levyValue = sheet.cell_value(nRows, levyIndex)

                if '-' in apnValue:
                    if len(apnValue) > 9:
                        apnValue = apnValue.replace('-', '')
                        if len(apnValue) > 9:
                            apnValue = apnValue[:-1]
                    finalApnValue = getCheckDigit(apnValue, checkDigit)
                else:
                    finalApnValue = getCheckDigit(apnValue, checkDigit)

                replacementList.append([finalApnValue, findDisID, 'N', levyValue, distNameDict.get(findDisID, None)])
        replacementDict[findDisID] = replacementList

        expression = '{} = {}'.format(arcpy.AddFieldDelimiters(masterDB, 'District_ID'), findDisID)

        with arcpy.da.UpdateCursor(masterDB, ['*'], where_clause=expression) as dCursor:
            for dRow in dCursor:
                dCursor.deleteRow()
        del dCursor

        insertCursor = arcpy.da.InsertCursor(masterDB, insertFields)

        for iRow in replacementList:
            insertCursor.insertRow(iRow)
        del insertCursor

    except Exception, err:
        traceback.print_exc()

# edit.stopOperation()
# print "operation stopped"
# edit.stopEditing(True)  ## Stop the edit session with True to save the changes
# print "edit stopped"
# print workbooks

"""
FUND xxxx
APN || Assessor || Parcel xxxxxxxxxx
LEVY || Charge xxxxxxxxxx

"""

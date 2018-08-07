import arcpy


def getCheckDigit(apnString, check):
    csaList = []

    for iCSA in apnString:
        # making sure apn has 9 digits
        iCSA = "{:09}".format(iCSA)

        checkDigitMathList = []
        # breaking down the APN so i can get the check digit
        for iSingle in range(len(iCSA)):
            apnSingleValue = int(iCSA[iSingle])
            checkDigitSingleValue = int(check[iSingle])
            checkDigitMath = apnSingleValue * checkDigitSingleValue
            checkDigitMathList.append(checkDigitMath)

        checkDigitSum = str(sum(checkDigitMathList))
        apn_checkDigit = '{}-{}'.format(iCSA, checkDigitSum[-1])
        csaList.append(apn_checkDigit)
    return csaList


csaTestTable = r'Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019'
# csaTestTable = r'Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019_updateCSA'

checkDigit = '137913791'
edaNote = None
insertFields = ['APN', 'District_ID', 'Elevator', 'Levy', 'Name', 'MaxTax', 'Parent_APN', 'notes']

parentAPNS = '480020051-6, 480020053-8, 480020054-9'

parentAPNS2 = '480040012-3, 480040059-6, 480040077-2'

parentAPNS3 = '480040053-0, 480040055-2, 480040057-4, 480040063-9, 480040064-0, 480040067-3, 480040069-5, 480040008-0'

parentAPNS4 = '290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4'

parentAPNS5 = [[480621001, 480621084], [480621088], [480621090, 480621091], [480622001, 480622024],
               [480622037, 480622046], [480622048, 480622049], [480622051], [480623001, 480623012],
               [480623015, 480623017], [480623019], [480624023]]

childrenLevy = {'681815': {'levy': 70.40, 'maxTax': None, 'name': 'CSA No. 103 (Lighting)'},
                '681869': {'levy': 174.68, 'maxTax': None, 'name': 'CSA No. 152 (Temescal Drainage Basin)'},
                '681852': {'levy': None, 'maxTax': 79.06, 'name': 'CSA No. 152 (Street Sweeping)'}}

childrenLevy2 = {'681815': {'levy': 118.40, 'maxTax': None, 'name': 'CSA No. 103 (Lighting)'},
                 '681852': {'levy': None, 'maxTax': 79.06, 'name': 'CSA No. 152 (Street Sweeping)'}}

childrenLevy3 = {'681815': {'levy': 60.24, 'maxTax': None, 'name': 'CSA No. 103 (Lighting)'},
                 '681852': {'levy': None, 'maxTax': 79.05, 'name': 'CSA No. 152 (Street Sweeping)'}}

childrenLevy4 = {
    '681822': {'levy': 488.60, 'maxTax': None, 'name': 'CSA No. 134 (Temescal Lighting, Landscaping, & Park)'},
    '681869': {'levy': 49.74, 'maxTax': None, 'name': 'CSA No. 152 (Temescal Drainage Basin)'}}

childrenLevy5 = {
    '681815': {'levy': 46.36, 'maxTax': None, 'name': 'CSA No. 103 (Lighting)'},
    '681852': {'levy': 40.00, 'maxTax': 40.00, 'name': 'CSA No. 152 (Street Sweeping)'}
}

updateCSA = [[480020055, 480020058], [480020059, 480020060], [480830001, 480830035], [480831001, 480831045],
             [480832001, 480832013], [480840001, 480840036], [480841001, 480841041], [480842001, 480842012],
             [480850001, 480850016], [480851001, 480851031]]

updateCSA2 = [[480040081], [480860001, 480860028], [480861001, 480861016], [480862001, 480862002]]

updateCSA3 = [[480820001, 480820013], [480821001, 480821029], [480822001, 480822011]]

updateCSA4 = [[290070052, 290070058], [290070067, 290070068], [290080044, 290080048], [290080050, 290080051],
              [290080053, 290080056], [290080058], [290080060, 290080062], [290770001, 290770072],
              [290780001, 290780068], [290790001, 290790033], [290800001, 290800029], [290810001, 290810052],
              [290820001, 290820058], [290830001, 290830061], [290840001, 290840051], [290850001, 290850056],
              [290860001, 290860071]]

updateCSA5 = [[480620013, 480620014], [480620026], [480623021, 480623081], [480624001, 480624010],
              [480624012, 480624022], [480624024, 480624066]]

parentRangeList = []

for iP in parentAPNS5:
    iPCounter = iP[0]
    try:
        while iPCounter <= iP[1]:
            parentRangeList.append(iPCounter)
            iPCounter += 1
    except IndexError:
        while iPCounter <= iP[0]:
            parentRangeList.append(iPCounter)
            iPCounter += 1

parentAPNS5 = getCheckDigit(parentRangeList, checkDigit)
stringParentAPN5 = ", ".join(str(x) for x in parentAPNS5)

for iCurrentParentCSA in range(len(parentAPNS5)):
    expression = "{} = '{}'".format(arcpy.AddFieldDelimiters(csaTestTable, 'APN'), parentAPNS5[iCurrentParentCSA])
    # deleting all children APNs from the range leni gave me
    with arcpy.da.UpdateCursor(csaTestTable, ['*'], where_clause=expression) as dCursor:
        for dRow in dCursor:
            dCursor.deleteRow()
        del dCursor
print 'deleting is done'

# looping through range that leni gave me
for iCSARange in updateCSA5:
    rangeList = []
    finalList = []
    iCounter = iCSARange[0]
    # creating a range
    try:
        while iCounter <= iCSARange[1]:
            rangeList.append(iCounter)
            iCounter += 1
    except IndexError:
        while iCounter <= iCSARange[0]:
            rangeList.append(iCounter)
            iCounter += 1
    print 'range has been created for {}'.format(iCSARange)
    csaRangeCheck = getCheckDigit(rangeList, checkDigit)
    print 'check digits have been added'
    # looping over newly created APNs w/ check digits and appending them to the final list with the correct information
    # for the dictionary leni created
    for iFinal in csaRangeCheck:
        for k, v in childrenLevy5.iteritems():
            finalList.append([iFinal, k, 'N', v.get('levy'), v.get('name'), v.get('maxTax'), stringParentAPN5, edaNote])
    print 'iFinal list has completed'

    for iCurrentCSA in range(len(csaRangeCheck)):
        expression = "{} = '{}'".format(arcpy.AddFieldDelimiters(csaTestTable, 'APN'), csaRangeCheck[iCurrentCSA])
        # deleting all children APNs from the range leni gave me
        with arcpy.da.UpdateCursor(csaTestTable, ['*'], where_clause=expression) as dCursor:
            for dRow in dCursor:
                dCursor.deleteRow()
            del dCursor
    print 'deleting is done'

    insertCursor = arcpy.da.InsertCursor(csaTestTable, insertFields)
    # re-inserting the children apns with the correct info
    for iRow in finalList:
        insertCursor.insertRow(iRow)
    del insertCursor
    print 'insert is done'

print 'DONE DONE'

# APN IN ('391480012-2', '391480023-2', '393140018-2', '393140020-2')
# # 391480012-2, 391480023-2, 393140003-7, 3931400034-8

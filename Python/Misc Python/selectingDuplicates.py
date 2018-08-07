import arcpy
import csv


def deleteAllDup(dupDict):
    for keyDisID, apnDict in dupDict.iteritems():
        for apnValue, apnValueList in apnDict.iteritems():
            for i in apnValueList:
                for deleteOID, deleteList in i.iteritems():
                    deleteExperession = '{} = {}'.format(arcpy.AddFieldDelimiters(master_18_19, 'OBJECTID'), deleteOID)

                    with arcpy.da.UpdateCursor(master_18_19, ['*'], where_clause=deleteExperession) as deleteRows:
                        for delete in deleteRows:
                            deleteRows.deleteRow()
                        del deleteRows
    print 'Done Deleting Items'


def insertCorrectValues(inDict):
    for keyDisID, insertList in inDict.iteritems():
        insertFields = ['APN', 'District_ID', 'Elevator', 'Levy', 'Name', 'MaxTax', 'Parent_APN', 'created_user',
                        'created_date', 'last_edited_user', 'last_edited_date', 'notes', 'designation', 'tract']
        insertCursor = arcpy.da.InsertCursor(master_18_19, insertFields)
        insertList = insertList[1:]

        insertCursor.insertRow(insertList)
        del insertCursor

    print 'Done Inserting Items'


def checkForWhiteSpace(db):
    whiteSpacesExp = "{} LIKE '{}'".format(arcpy.AddFieldDelimiters(db, 'APN'), '%')
    with arcpy.da.UpdateCursor(db, ['APN'], where_clause=whiteSpacesExp) as updateWhiteSpaces:
        for updateThis in updateWhiteSpaces:
            if ' ' in updateThis[0]:
                noSpaceAPN = updateThis[0].strip()
                updateThis[0] = noSpaceAPN

                updateWhiteSpaces.updateRow(updateThis)


master_18_19 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019"

checkForWhiteSpace(master_18_19)

disID = [681701, 681712, 681714, 681724, 681727, 681729, 681739, 681744, 681747, 681756, 681765, 681768, 681776, 681789,
         681793, 681794, 681796, 681799, 681802, 681805, 681808, 681815, 681816, 681817, 681820, 681822, 681823, 681825,
         681828, 681829, 681833, 681834, 681836, 681843, 681848, 681849, 681851, 681852, 681853, 681854, 681857, 681859,
         681860, 681861, 681862, 681864, 681865, 681867, 681868, 681869, 681870, 681883, 681885, 681886]

# count = 0
# notCorrect = 0
# select6882 = "{} = {}".format(arcpy.AddFieldDelimiters(master_18_19, 'District_ID'), 681852)
# with arcpy.da.SearchCursor(master_18_19, ['APN', 'levy'], where_clause=select6882) as cursor:
#     for iCursor in cursor:
#         if iCursor[1] <= 68.82:
#             count += 1
#         else:
#             print '{}: {}'.format(iCursor[0], iCursor[1])
#             notCorrect += 1
# print count

duplicateList = []
duplicateDict = {}
for iDisID in disID:
    newSelectionExp = "{} = {}".format(arcpy.AddFieldDelimiters(master_18_19, 'District_ID'), iDisID)
    duplicateDict[iDisID] = {}
    with arcpy.da.SearchCursor(master_18_19, ['*'], where_clause=newSelectionExp) as newSelectCursor:
        for newSelectRow in newSelectCursor:
            newSelectRow = list(newSelectRow)
            OID = newSelectRow[0]
            APN = str(newSelectRow[1])
            if APN in duplicateDict[iDisID]:
                duplicateDict[iDisID][APN].append({OID: newSelectRow})
            else:
                duplicateDict[iDisID][APN] = [{OID: newSelectRow}]
    for key, value in duplicateDict[iDisID].items():
        valueLen = len(value)
        if valueLen == 1:
            duplicateDict[iDisID].pop(key)

insertDict = {}
tractMaxTaxErr = {}

for disKey, apnKeys in duplicateDict.items():
    lenAPNKeys = len(apnKeys)
    if lenAPNKeys > 0:
        for apns, iList in apnKeys.iteritems():
            newOID = 0
            newLevyAMT = 0
            newParent = None
            newMaxTax = None
            newTract = None
            newUser = None
            for iDict in iList:
                for OIDKey, values in iDict.iteritems():
                    levyAMT = float(str(round(values[4], 2)))
                    maxTax = values[6]
                    parentAPN = values[7]
                    tract = values[14]
                    apn = values[1]
                    distID = values[2]
                    creatureUser = values[8]
                    getDistIDValues = tractMaxTaxErr.get(newOID)

                    if apn == '480010023-0 ':
                        print 'wtf man'

                    if creatureUser is not None or newUser is not None:
                        if newUser is None:
                            newLevyAMT = 0
                        if newUser is None or newUser is not None:
                            if levyAMT == newLevyAMT:
                                if tract is not None and maxTax is None and distID == 681852:
                                    if newOID in insertDict:
                                        insertDict.pop(newOID)
                                        newOID = OIDKey
                                        newTract = tract
                                        insertDict[newOID] = values
                                    # elif newOID in tractMaxTaxErr:
                                    #     tractMaxTaxErr.pop(newOID)
                                    # if newParent is None and parentAPN is not None or newParent is not None and parentAPN is None:
                                    #     if getDistIDValues is None:
                                    #         if newParent is not None:
                                    #             tractMaxTaxErr[newOID][7] = newParent
                                    #         else:
                                    #             tractMaxTaxErr[newOID][7] = parentAPN
                                    #     else:
                                    #         if newParent is not None:
                                    #             values[7] = newParent
                                    #         else:
                                    #             values[7] = parentAPN
                                else:
                                    if parentAPN is None:
                                        getPrevValues = insertDict.get(newOID)
                                        if getDistIDValues is not None:
                                            getPrevParent = getDistIDValues[7]
                                            if getPrevParent is None or getPrevParent == '':
                                                if newOID in insertDict:
                                                    insertDict.pop(newOID)
                                                newOID = OIDKey
                                                # if newParent is None and parentAPN is not None:
                                                #     newParent = parentAPN
                                                #     values[7] = newParent
                                                insertDict[newOID] = values
                                    elif newTract is not None and parentAPN is not None:
                                        break
                                    else:
                                        if newOID in insertDict:
                                            insertDict.pop(newOID)
                                        newOID = OIDKey
                                        # if newParent is None and parentAPN is not None:
                                        #     newParent = parentAPN
                                        #     values[7] = newParent
                                        insertDict[newOID] = values
                                    # else:
                                    #     if newParent is None and parentAPN is not None or newParent is not None and parentAPN is None:
                                    #         if getDistIDValues is not None:
                                    #             if newParent is not None:
                                    #                 tractMaxTaxErr[newOID][7] = newParent
                                    #             else:
                                    #                 tractMaxTaxErr[newOID][7] = parentAPN
                                    #         else:
                                    #             if newParent is not None:
                                    #                 tractMaxTaxErr[newOID][7] = newParent
                                    #             else:
                                    #                 tractMaxTaxErr[newOID][7] = parentAPN
                            elif levyAMT > newLevyAMT:
                                if tract is not None and maxTax is None and distID == 681852:
                                    if newOID in insertDict:
                                        insertDict.pop(newOID)
                                        newLevyAMT = levyAMT
                                        newOID = OIDKey
                                        newTract = tract
                                        insertDict[newOID] = values
                                    # elif newOID in tractMaxTaxErr:
                                    #     tractMaxTaxErr.pop(newOID)
                                    # if newParent is None and parentAPN is not None or newParent is not None and parentAPN is None:
                                    #     if getDistIDValues is not None:
                                    #         if newParent is not None:
                                    #             tractMaxTaxErr[newOID][7] = newParent
                                    #         else:
                                    #             tractMaxTaxErr[newOID][7] = parentAPN
                                    #     else:
                                    #         if newParent is not None:
                                    #             values[7] = newParent
                                    #         else:
                                    #             values[7] = parentAPN
                                else:
                                    if getDistIDValues is None:
                                        if newOID in insertDict:
                                            insertDict.pop(newOID)
                                        newLevyAMT = levyAMT
                                        newOID = OIDKey
                                        # if newParent is None and parentAPN is not None:
                                        #     newParent = parentAPN
                                        #     values[7] = newParent
                                        insertDict[newOID] = values
                                    # else:
                                    #     if newParent is None and parentAPN is not None or newParent is not None and parentAPN is None:
                                    #         if getDistIDValues is not None:
                                    #             if newParent is not None:
                                    #                 tractMaxTaxErr[newOID][7] = newParent
                                    #             else:
                                    #                 tractMaxTaxErr[newOID][7] = parentAPN
                                    #         else:
                                    #             if newParent is not None:
                                    #                 tractMaxTaxErr[newOID][7] = newParent
                                    #             else:
                                    #                 tractMaxTaxErr[newOID][7] = parentAPN
                            newUser = creatureUser
                        break
                    else:
                        if levyAMT == newLevyAMT:
                            if tract is not None and maxTax is None and distID == 681852:
                                if newOID in insertDict:
                                    insertDict.pop(newOID)
                                    newOID = OIDKey
                                    insertDict[newOID] = values
                                # elif newOID in tractMaxTaxErr:
                                #     tractMaxTaxErr.pop(newOID)
                                # if newParent is None and parentAPN is not None or newParent is not None and parentAPN is None:
                                #     if getDistIDValues is None:
                                #         if newParent is not None:
                                #             tractMaxTaxErr[newOID][7] = newParent
                                #         else:
                                #             tractMaxTaxErr[newOID][7] = parentAPN
                                #     else:
                                #         if newParent is not None:
                                #             values[7] = newParent
                                #         else:
                                #             values[7] = parentAPN
                            else:
                                if getDistIDValues is None:
                                    if newOID in insertDict:
                                        insertDict.pop(newOID)
                                    newOID = OIDKey
                                    # if newParent is None and parentAPN is not None:
                                    #     newParent = parentAPN
                                    #     values[7] = newParent
                                    insertDict[newOID] = values
                                # else:
                                #     if newParent is None and parentAPN is not None or newParent is not None and parentAPN is None:
                                #         if getDistIDValues is not None:
                                #             if newParent is not None:
                                #                 tractMaxTaxErr[newOID][7] = newParent
                                #             else:
                                #                 tractMaxTaxErr[newOID][7] = parentAPN
                                #         else:
                                #             if newParent is not None:
                                #                 tractMaxTaxErr[newOID][7] = newParent
                                #             else:
                                #                 tractMaxTaxErr[newOID][7] = parentAPN
                        elif levyAMT > newLevyAMT:
                            if tract is not None and maxTax is None and distID == 681852:
                                if newOID in insertDict:
                                    insertDict.pop(newOID)
                                    newLevyAMT = levyAMT
                                    newOID = OIDKey
                                    insertDict[newOID] = values
                                # elif newOID in tractMaxTaxErr:
                                #     tractMaxTaxErr.pop(newOID)
                                # if newParent is None and parentAPN is not None or newParent is not None and parentAPN is None:
                                #     if getDistIDValues is not None:
                                #         if newParent is not None:
                                #             tractMaxTaxErr[newOID][7] = newParent
                                #         else:
                                #             tractMaxTaxErr[newOID][7] = parentAPN
                                #     else:
                                #         if newParent is not None:
                                #             values[7] = newParent
                                #         else:
                                #             values[7] = parentAPN
                            else:
                                if getDistIDValues is None:
                                    if newOID in insertDict:
                                        insertDict.pop(newOID)
                                    newLevyAMT = levyAMT
                                    newOID = OIDKey
                                    if newParent is None and parentAPN is not None:
                                        newParent = parentAPN
                                        values[7] = newParent
                                    insertDict[newOID] = values
                                # else:
                                #     if newParent is None and parentAPN is not None or newParent is not None and parentAPN is None:
                                #         if getDistIDValues is not None:
                                #             if newParent is not None:
                                #                 tractMaxTaxErr[newOID][7] = newParent
                                #             else:
                                #                 tractMaxTaxErr[newOID][7] = parentAPN
                                #         else:
                                #             if newParent is not None:
                                #                 tractMaxTaxErr[newOID][7] = newParent
                                #             else:
                                #                 tractMaxTaxErr[newOID][7] = parentAPN
    else:
        duplicateDict.pop(disKey)

with open('insert.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.writer(f)
    for key2, value2 in insertDict.iteritems():
        w.writerow(value2)

deleteAllDup(duplicateDict)
insertCorrectValues(insertDict)
# with open('tractErr.csv', 'wb') as f:  # Just use 'w' mode in 3.x
#     w = csv.writer(f)
#     for key2, value2 in tractMaxTaxErr.iteritems():
#         w.writerow(value2)


print 'Done'

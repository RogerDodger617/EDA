import arcpy
import json
import ast


def deleteParentAPN(table, apn):
    # tempList = []
    for i in range(len(apn)):
        expression = "{}='{}'".format(arcpy.AddFieldDelimiters(master_18_19, 'APN'), apn[i])

        with arcpy.da.UpdateCursor(table, ["*"], where_clause=expression) as cursor:
            for delRow in cursor:
                # tempList.append(apn[1])
                print "Deleting:\n {}".format(delRow)
                cursor.deleteRow()

        del cursor


def insertNewAPN(table, newAPNData):
    jsonData = json.loads(newAPNData)

    for i in range(len(jsonData)):
        newAPN = jsonData[i]
        fieldList = []
        valueList = []
        for key, value in newAPN.iteritems():
            if key != 'OBJECTID':
                if key == 'Levy':
                    value = str(value)
                    value = float(value.strip() or 0)
                    fieldList.append(key)
                    valueList.append(value)
                elif key == 'District_ID':
                    value = str(value)
                    value = int(value.strip() or 0)
                    fieldList.append(key)
                    valueList.append(value)
                else:
                    fieldList.append(key)
                    valueList.append(value)

        insertChildAPN = arcpy.da.InsertCursor(table, fieldList)

        print "Inserting into table:\n {}".format(valueList)
        insertChildAPN.insertRow(valueList)

        del insertChildAPN


def updateChildrenApn(compareChildrenList, parentParcel):
    updateJsonDate = json.loads(compareChildrenList)
    insertUpdateDict = {'insert': [], 'updated': []}
    for i in range(len(updateJsonDate)):
        childrenDict = updateJsonDate[i]
        disID = childrenDict['District_ID']
        levy = childrenDict['Levy']
        childrenAPN = childrenDict['APN']
        # parentParcels = ''

        if disID == 681852:
            print 'hold up'

        # for iP in range(len(parentParcel)):
        #     parentParcels += ', {}'.format(parentParcel[iP])

        updateFields = ['Levy', 'Parent_APN']

        updateExpression = "{} = '{}' AND {} = {}".format(arcpy.AddFieldDelimiters(master_18_19, 'APN'), childrenAPN,
                                                          arcpy.AddFieldDelimiters(master_18_19, 'District_ID '), disID)

        with arcpy.da.UpdateCursor(master_18_19, updateFields, where_clause=updateExpression) as updateCursor:
            for updateRow in updateCursor:
                currentLevy = updateRow[0]
                currentParentApns = updateRow[1]
                if currentParentApns is None:
                    currentParentApns = []
                else:
                    currentParentApns = currentParentApns.split(',')

                if levy < currentLevy:
                    updateRow[0] = levy

                for newParent in parentParcel:
                    if newParent not in currentParentApns:
                        currentParentApns.append(newParent)
                updateRow[1] = ', '.join(currentParentApns)

                if [childrenAPN, disID] not in insertUpdateDict['updated']:
                    insertUpdateDict['updated'].append([childrenAPN, disID])

                updateCursor.updateRow(updateRow)

        del updateCursor

        if [childrenAPN, disID] not in insertUpdateDict['updated']:
            # if [childrenAPN, disID] not in insertUpdateDict['insert']:
            insertUpdateDict['insert'].append(childrenDict)

    return insertUpdateDict['insert']


master_17_18 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2017_2018"
master_18_19 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019"

userSearchedAPN = ast.literal_eval(arcpy.GetParameterAsText(0))
# ["273590011-8", "273590012-9"]
# ast.literal_eval(arcpy.GetParameterAsText(0))

arcpy.AddMessage(userSearchedAPN)

addNewAPNList = arcpy.GetParameterAsText(1)
# """[
#   {
#    "APN": "290080062-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290080062-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290080062-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810001-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810002-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810003-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810004-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810005-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810006-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810007-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810008-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810009-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810010-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810011-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810012-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810013-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810014-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810015-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810016-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810017-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810018-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810019-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810020-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810021-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810022-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810023-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810024-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810025-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810026-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810027-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810028-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810029-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810030-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810031-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810032-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810033-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810034-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810035-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810036-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810037-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810038-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810039-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810040-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810041-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810042-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810043-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810044-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810045-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810046-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810047-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810048-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810049-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810050-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810051-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810052-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810001-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810002-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810003-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810004-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810005-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810006-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810007-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810008-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810009-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810010-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810011-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810012-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810013-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810014-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810015-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810016-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810017-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810018-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810019-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810020-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810021-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810022-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810023-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810024-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810025-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810026-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810027-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810028-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810029-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810030-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810031-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810032-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810033-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810034-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810035-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810036-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810037-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810038-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810039-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810040-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810041-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810042-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810043-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810044-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810045-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810046-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810047-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810048-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810049-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810050-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810051-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810052-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810001-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810002-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810003-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810004-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810005-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810006-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810007-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810008-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810009-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810010-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810011-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810012-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810013-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810014-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810015-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810016-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810017-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810018-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810019-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810020-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810021-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810022-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810023-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810024-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810025-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810026-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810027-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810028-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810029-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810030-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810031-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810032-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810033-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810034-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810035-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810036-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810037-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810038-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810039-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810040-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810041-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810042-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810043-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810044-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810045-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810046-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810047-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810048-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810049-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810050-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810051-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290810052-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820001-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820002-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820003-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820004-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820005-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820006-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820007-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820008-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820009-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820010-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820011-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820012-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820013-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820014-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820015-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820016-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820017-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820018-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820019-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820020-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820021-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820022-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820023-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820024-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820025-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820026-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820027-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820028-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820029-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820030-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820031-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820032-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820033-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820034-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820035-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820036-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820037-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820038-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820039-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820040-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820041-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820042-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820043-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820044-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820045-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820046-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820047-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820048-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820049-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820050-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820051-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820052-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820053-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820054-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820055-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820056-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820057-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820058-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 310.84,
#    "MaxTax": null,
#    "Name": "CSA No. 152B (Temescal Regional Sports Facilities)",
#    "District_ID": 681870,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820001-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820002-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820003-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820004-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820005-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820006-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820007-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820008-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820009-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820010-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820011-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820012-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820013-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820014-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820015-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820016-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820017-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820018-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820019-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820020-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820021-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820022-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820023-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820024-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820025-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820026-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820027-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820028-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820029-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820030-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820031-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820032-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820033-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820034-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820035-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820036-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820037-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820038-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820039-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820040-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820041-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820042-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820043-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820044-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820045-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820046-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820047-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820048-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820049-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820050-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820051-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820052-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820053-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820054-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820055-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820056-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820057-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820058-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 556.43,
#    "MaxTax": null,
#    "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
#    "District_ID": 681822,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820001-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820002-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820003-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820004-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820005-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820006-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820007-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820008-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820009-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820010-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820011-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820012-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820013-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820014-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820015-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820016-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820017-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820018-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820019-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820020-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820021-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820022-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820023-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820024-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820025-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820026-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820027-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820028-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820029-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820030-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820031-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820032-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820033-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820034-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820035-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820036-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820037-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820038-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820039-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820040-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820041-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820042-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820043-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820044-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820045-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820046-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820047-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820048-7",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820049-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820050-8",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820051-9",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820052-0",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820053-1",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820054-2",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820055-3",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820056-4",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820057-5",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   },
#   {
#    "APN": "290820058-6",
#    "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4",
#    "Levy": 50.91,
#    "MaxTax": null,
#    "Name": "CSA No. 152 (Street Sweeping)",
#    "District_ID": 681852,
#    "Elevator": "Yes"
#   }
#  ]"""
# """[{"APN":"273590054-7", "Parent_APN":"273590011-8, 273590012-9","Levy":37.94,"MaxTax":null,"Name":"CSA No. 132 (The Orchards/Lake Mathews Lighting)","District_ID":681789,"Elevator":"Yes"},{"APN":"273590054-7","Parent_APN":"273590011-8, 273590012-9","Levy":68.82,"MaxTax":"77.26","Name":"CSA No. 152 (Street Sweeping)","District_ID":681852,"Elevator":"Yes"}]"""

updateChildrenTrueFalse = arcpy.GetParameterAsText(2)
# 'true'
# arcpy.GetParameterAsText(2)

arcpy.AddMessage(addNewAPNList)

if not userSearchedAPN:
    print 'Nope'
    arcpy.AddMessage('No APN searched')
else:
    if updateChildrenTrueFalse == 'true':
        insertNewChildren = updateChildrenApn(addNewAPNList, userSearchedAPN)

        deleteParentAPN(master_18_19, userSearchedAPN)

        if insertNewChildren:
            insertNewAPN(master_18_19, json.dumps(insertNewChildren))
    else:
        deleteParentAPN(master_18_19, userSearchedAPN)

        insertNewAPN(master_18_19, addNewAPNList)

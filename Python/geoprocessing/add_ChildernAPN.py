import arcpy
import json
import ast


def deleteParentAPN(table, apn):
    expression = "{}='{}'".format(arcpy.AddFieldDelimiters(table, 'APN'), apn)

    with arcpy.da.UpdateCursor(table, ["*"], where_clause=expression) as cursor:
        for delRow in cursor:
            print "Deleting:\n {}".format(delRow)
            cursor.deleteRow()
    del cursor


def insertNewAPN(table, newAPNData, parentAPN):
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


master_17_18 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2017_2018"
master_18_19 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019"

userSearchedAPN = arcpy.GetParameterAsText(0)
# '391352028-1'
# arcpy.GetParameterAsText(0)
arcpy.AddMessage(userSearchedAPN)

addNewAPNList = arcpy.GetParameterAsText(1)
# """[{"APN": "102092030-7", "District_ID": 681701, "Elevator": "N", "Levy": 0, "MaxTax": null, "Name": "CSA No. 1 (Coronita Lighting)", "Parent_APN": "102092001-1"}]"""
# arcpy.GetParameterAsText(1)
arcpy.AddMessage(addNewAPNList)

if not userSearchedAPN:
    print 'Nope'
    arcpy.AddMessage('No APN searched')
else:
    deleteParentAPN(master_18_19, userSearchedAPN)

insertNewAPN(master_18_19, addNewAPNList, userSearchedAPN)

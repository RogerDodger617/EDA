import arcpy
import json
import ast


def deleteParentAPN(table, apn):
    for i in range(len(apn)):
        expression = "{}='{}'".format(arcpy.AddFieldDelimiters(table, 'APN'), apn[i])

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
                    value = float(value.strip() or 0)
                    fieldList.append(key)
                    valueList.append(value)
                elif key == 'District_ID':
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

master_17_18 = r"Database Connections\Connection to gis01.sde\CLGEGIS.DBO.master_17_18_test"
master_18_19 = r"Database Connections\Connection to gis01.sde\CLGEGIS.DBO.master_18_19_test"

userSearchedAPN = ast.literal_eval(arcpy.GetParameterAsText(0))
arcpy.AddMessage(userSearchedAPN)
# "476040025-4"
addNewAPNList = arcpy.GetParameterAsText(1)
arcpy.AddMessage(addNewAPNList)
# """{"paramName": "Result", "dataType": "GPString", "value": "[{u'Levy': 0.0, u'MaxTax': None, u'Name': u'CSA No. 103 (Lighting)', u'OBJECTID': 1, u'Parent_APN': None, u'District_ID': 681815, u'Elevator': u'N', u'APN': u'476020011-9'}, {u'Levy': 0.0, u'MaxTax': None, u'Name': u'CSA No. 152', u'OBJECTID': 199, u'Parent_APN': None, u'District_ID': 681815, u'Elevator': u'N', u'APN': u'476020011-9'}]"}"""

if not userSearchedAPN:
    print 'Nope'
    arcpy.AddMessage('No APN searched')
else:
    deleteParentAPN(master_18_19, userSearchedAPN)
    
insertNewAPN(master_18_19, addNewAPNList, userSearchedAPN)


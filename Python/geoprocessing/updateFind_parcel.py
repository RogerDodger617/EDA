import arcpy
import json
import ast

master_17_18 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2017_2018"
master_18_19 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019"

fields = arcpy.ListFields(master_18_19)
fieldNames = []
APN_List = []
missingList = []
foundList = []

getAPNValue = ast.literal_eval(arcpy.GetParameterAsText(0))

# "476040025-4"

for i in range(len(getAPNValue)):
    expression = "{}='{}'".format(arcpy.AddFieldDelimiters(master_18_19, 'APN'), getAPNValue[i])

    for name in fields:
        fieldNames.append(name.name)

    with arcpy.da.SearchCursor(master_18_19, ['*'], where_clause=expression) as cursor:
        for row in cursor:
            result_Dict = {}
            foundList.append(getAPNValue[i])
            for i2 in range(len(row)):
                if fieldNames[i2] != u'created_user' and fieldNames[i2] != u'created_date' and fieldNames[i2] != u'last_edited_user' and fieldNames[i2] != u'last_edited_date':
                    result_Dict[fieldNames[i2]] = row[i2]

            jsonString = json.dumps(result_Dict)
            APN_List.append(jsonString)

    del cursor

for i2 in getAPNValue:
    if i2 not in foundList:
        missingList.append(i2)

arcpy.AddMessage(APN_List)
arcpy.SetParameterAsText(1, APN_List)
arcpy.SetParameterAsText(2, missingList)

print APN_List

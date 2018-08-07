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
                # cursor.deleteRow()

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
        # insertChildAPN.insertRow(valueList)

        del insertChildAPN


def updateChildrenApn(compareChildrenList, parentParcel):
    updateJsonDate = json.loads(compareChildrenList)
    insertUpdateDict = {'insert': [], 'updated': []}
    for i in range(len(updateJsonDate)):
        childrenDict = updateJsonDate[i]
        disID = childrenDict['District_ID']
        levy = childrenDict['Levy']
        childrenAPN = childrenDict['APN']
        parentParcels = ''

        for iP in range(len(parentParcel)):
            parentParcels = ', {}'.format(parentParcel[iP])

        updateFields = ['Levy', 'Parent_APN']

        updateExpression = "{} = '{}' AND {} = {}".format(arcpy.AddFieldDelimiters(master_18_19, 'APN'), childrenAPN,
                                                        arcpy.AddFieldDelimiters(master_18_19, 'District_ID '), disID)

        with arcpy.da.UpdateCursor(master_18_19, updateFields, where_clause=updateExpression) as updateCursor:
            for updateRow in updateCursor:
                currentLevy = updateRow[0]
                currentParentApns = updateRow[1]

                if levy < currentLevy:
                    updateRow[0] = levy
                if parentParcels not in currentParentApns:
                    updateRow[1] = updateRow[1] + parentParcels

                if childrenAPN not in insertUpdateDict['updated']:
                    insertUpdateDict['updated'].append(childrenAPN)

                # updateCursor.updateRow(updateRow)

        if childrenAPN not in insertUpdateDict['updated']:
            if childrenAPN not in insertUpdateDict['insert']:
                insertUpdateDict['insert'].append(childrenDict)

    return insertUpdateDict['insert']

master_17_18 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2017_2018"
master_18_19 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019_test"

userSearchedAPN = ["290820001-4"]
# ast.literal_eval(arcpy.GetParameterAsText(0))
# """["136110004-6", "136110005-6", "136110008-0", "136110021-1", "136110022-2"]"""
# arcpy.GetParameterAsText(0)
arcpy.AddMessage(userSearchedAPN)

addNewAPNList = """[
  {
   "APN": "290820001-4",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "290820002-5",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "290820003-6",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "290820004-7",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "290820005-8",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "290820001-4",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  },
  {
   "APN": "290820002-5",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  },
  {
   "APN": "290820003-6",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  },
  {
   "APN": "290820004-7",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  },
  {
   "APN": "290820005-8",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  },
  {
   "APN": "111111111-1",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "111111112-2",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "111111113-3",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "111111114-4",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "111111115-5",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 500.13,
   "MaxTax": null,
   "Name": "CSA No. 134 (Temescal Lighting, Landscaping, & Park)",
   "District_ID": 681822,
   "Elevator": "Y"
  },
  {
   "APN": "111111111-1",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  },
  {
   "APN": "111111112-2",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  },
  {
   "APN": "111111113-3",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  },
  {
   "APN": "111111114-4",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  },
  {
   "APN": "111111115-5",
   "Parent_APN": "290070049-1, 290070050-1, 290070051-2, 290080040-3, 290080041-4, 290080042-5, 290080043-6, 290080049-2, 290080052-4, 290820001-4",
   "Levy": 49.74,
   "MaxTax": null,
   "Name": "CSA No. 152 (Temescal Drainage Basin)",
   "District_ID": 681869,
   "Elevator": "Y"
  }
 ]
"""
# arcpy.GetParameterAsText(1)

# arcpy.GetParameterAsText(1)
arcpy.AddMessage(addNewAPNList)

updateChildrenTrueFalse = 'true'
# arcpy.GetParameterAsText(2)

if not userSearchedAPN:
    print 'Nope'
    arcpy.AddMessage('No APN searched')
else:
    if updateChildrenTrueFalse == 'true':
        insertNewChildren = updateChildrenApn(addNewAPNList, userSearchedAPN)

        if insertNewChildren:
            insertNewAPN(master_18_19, json.dumps(insertNewChildren))
    else:
        deleteParentAPN(master_18_19, userSearchedAPN)

        insertNewAPN(master_18_19, addNewAPNList)

print 'DONE'
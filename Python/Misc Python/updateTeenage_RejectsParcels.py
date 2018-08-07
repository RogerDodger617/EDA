import arcpy
import json
import ast


def searchForRejects(db, teenageAPNS):
    apnList = []
    for apn in teenageAPNS:
        teenageExp = "{} = '{}'".format(arcpy.AddFieldDelimiters(db, 'APN'), apn)

        with arcpy.da.SearchCursor(db, ['*'], where_clause=teenageExp) as teenageCursor:
            for iResults in teenageCursor:
                iResults = list(iResults)
                apnResults = iResults[1]
                parentAPNs = iResults[7]

                if parentAPNs is None or parentAPNs.isspace():
                    iResults[7] = apnResults
                    apnList.append(iResults)
                else:
                    apnList.append(iResults)
            del teenageCursor
    return apnList


masterDB = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019_rejectTest"

teenageAPNs = ['957780067-5', '269581012-0']
# ast.literal_eval(arcpy.GetParameterAsText(0))
addNewChildAPN = """[
{
    "APN": "111111111-1", 
    "District_ID": "681729", 
    "Elevator": "No", 
    "Levy": "", 
    "MaxTax": "", 
    "Name": "CSA No. 27 (Cherry Valley Lighting)", 
    "Parent_APN": "957780067-5
},
{
    "APN": "111111112-2",
    "District_ID": "681729",
    "Elevator": "No",
    "Levy": "",
    "MaxTax": "",
    "Name": "CSA No. 27 (Cherry Valley Lighting)",
    "Parent_APN": "957780067-5"
},
{   
    "APN": "111111113-3",
    "District_ID": "681729",
    "Elevator": "No",
    "Levy": "",
    "MaxTax": "", 
    "Name": "CSA No. 27 (Cherry Valley Lighting)",
    "Parent_APN": "957780067-5"}]"""
# ast.literal_eval(arcpy.GetParameter(1))

if not teenageAPNs:
    print 'No Teenage APNS searched'
else:
    searchForRejects(masterDB, teenageAPNs)

import arcpy
import datetime
import json
import ast


def genSummaryReport(masterTable, summaryTable):
    APN_List = []
    correctionList = []
    apnDict = dict()

    now = datetime.datetime.now()
    currentYear = now.year
    nextYear = currentYear + 1
    arcpy.Statistics_analysis(masterTable, summaryTable, [['Levy', 'SUM']], ['District_Name'])

    expression = "{} LIKE '{}'".format(arcpy.AddFieldDelimiters(summaryTable, 'District_Name'), '%')
    selectAllExpression = "{} LIKE '{}'".format(arcpy.AddFieldDelimiters(masterTable, 'APN'), '%')

    with arcpy.da.SearchCursor(summaryTable, ['District_Name', 'FREQUENCY', 'SUM_Levy'],
                               where_clause=expression) as cursor:
        for row in cursor:
            valueList = []
            for value in row:
                if type(value) is float:
                    roundNumber = '${0:,.2f}'.format(round(value, 2))
                    valueList.append(roundNumber)
                else:
                    valueList.append(str(value))
            APN_List.append(valueList)

    with arcpy.da.SearchCursor(masterTable, ['APN', 'District_ID', 'Levy'],
                               where_clause=selectAllExpression) as selectAllCursor:
        for selectRow in selectAllCursor:
            correctionString = []

            apn = str(selectRow[0])
            apn = apn.replace('-', '')
            apn = "{:0>10}".format(int(apn))

            disID = "{:0>6}".format(selectRow[1])

            if selectRow[2] is None:
                levy = "{:0>9}".format(0)
            else:
                levy = '{:.2f}'.format(float(selectRow[2]))
                levy = levy.replace('.', '')
                levy = "{:0>9}".format(int(levy))

            corrections = "      {} {}  {}<br>".format(apn, disID, levy)

            if disID not in apnDict:
                apnDict[disID] = []
                apnDict[disID].append(corrections)
            else:
                apnDict[disID].append(corrections)
    arcpy.AddMessage('Done with Function')
    return APN_List, apnDict


arcpy.env.overwriteOutput = True

workSpace = r"C:\Users\anfuentes\AppData\Roaming\Esri\Desktop10.3\ArcCatalog\Connection to SQLRIAGD01.rivcoca.org (2).sde"


master_18_19 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.CFDs_master_2018_2019"
# dateRangeTable = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_dateRange"

csa_SummaryTable = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.CFD_Summary"

# out_name = "csa_dateRange"
# template = master_18_19

# getGenerateValue = ast.literal_eval(arcpy.GetParameterAsText(0))
# arcpy.GetParameterAsText(0) '["2018-05-01", "2018-05-13"]'

# arcpy.AddMessage(len(getGenerateValue))

# if len(getGenerateValue) == 1:
apnList, apn_Dict = genSummaryReport(master_18_19, csa_SummaryTable)

arcpy.AddMessage('About to set the parameters')

arcpy.SetParameterAsText(1, apnList)
arcpy.SetParameterAsText(2, apn_Dict)

arcpy.AddMessage('Done setting parameters')

# elif len(getGenerateValue) == 2:
#     arcpy.DeleteRows_management(dateRangeTable)
#
#     created_date = arcpy.AddFieldDelimiters(master_18_19, 'created_date')
#     createExpression = "{} >= '{}' AND {} < '{}'".format(created_date, getGenerateValue[0], created_date,
#                                                          getGenerateValue[1])
#
#     insertCursor = arcpy.da.InsertCursor(dateRangeTable, ['*'])
#
#     with arcpy.da.SearchCursor(master_18_19, ['*'], where_clause=createExpression) as cursor:
#         for rows in cursor:
#             insertCursor.insertRow(rows)
#
#     del insertCursor
#
#     apnList, apn_Dict = genSummaryReport(dateRangeTable, csa_SummaryTable)
#
#     arcpy.SetParameterAsText(1, apnList)
#     arcpy.SetParameterAsText(2, apn_Dict)

print 'done'

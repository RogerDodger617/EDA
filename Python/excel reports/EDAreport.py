import arcpy

def searchForAPNs(table, field):
    setList = set()
    with arcpy.da.SearchCursor(table, field) as cursor:
        for row in cursor:
            setList.add(str(row[0]))
    return setList


def buildTableList(table, missingAPNs):
    field_names = [f.name for f in arcpy.ListFields(table)]
    fields = field_names[1:]
    tableList = []
    for missingValues in missingAPNs:
        with arcpy.da.SearchCursor(table, field_names=fields,
                                   where_clause="{} = '{}'".format(arcpy.AddFieldDelimiters(table, 'pl_csa_apn'),
                                                                   missingValues)) as cursor:
            for row in cursor:
                tableList.append(row)
    return tableList

# def createAndbuildTable(outPath)


outTable = arcpy.GetParameterAsText(0)
psomas_master = r'D:\MillerSpatial\EDA\EDA Test.gdb\psomas_master'
dataFiles_master = r'D:\MillerSpatial\EDA\EDA Test.gdb\dataFile_master'

psomas_set = searchForAPNs(psomas_master, 'APN')
dataFile_set = searchForAPNs(dataFiles_master, 'pl_csa_apn')

dataDifference = dataFile_set.difference(psomas_set)
outList = buildTableList(dataFiles_master, dataDifference)

print dataFile_set.difference(psomas_set)

# def findMissing(m, p):
#     foundAPNs = []
#     missingAPNList = []
#
#     for i in range(len(m)):
#         masterAPNValue = m[i].value
#         for i2 in range(len(p)):
#             psomasAPNValue = p[i2].value
#             if masterAPNValue == psomasAPNValue:
#                 foundAPNs.append(str(masterAPNValue))
#             else:
#                 if i2 + 1 == len(p):
#                     if masterAPNValue in foundAPNs:
#                         pass
#                     else:
#                         missingAPNList.append((i + 1, str(masterAPNValue)))
#
#     return missingAPNList
#
#
# def txtBuilder(missingList, header):
#     txtBuilderList = [header]
#
#     for i3 in range(len(missingList)):
#         row = masterSheet.row_values(missingList[i3][0])
#         txtBuilderList.append(row)
#
#     return txtBuilderList
#
#
# cfg = config.cfg
#
# master_data = cfg['dataFile']
# master_psomas = cfg['psomas']
#
# master_xls = xlrd.open_workbook(master_data)
# psomas_xls = xlrd.open_workbook(master_psomas)
#
# masterSheet = master_xls.sheet_by_index(0)
# psomasSheet = psomas_xls.sheet_by_index(0)
#
# headers = masterSheet.row_values(0)
#
# masterAPN = masterSheet.col(1)
# del masterAPN[0]
# psomasAPN = psomasSheet.col(0)
# del psomasAPN[0]
#
# missingAPNs = findMissing(masterAPN, psomasAPN)
# txtList = txtBuilder(missingAPNs, headers)
#
# with open(r'D:\MillerSpatial\EDA\test.csv', "wb") as f:
#     writer = csv.writer(f)
#     writer.writerows(txtList)

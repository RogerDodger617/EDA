import arcpy


def fixNMaxTax_Levy(db):
    expression = "{} = {} AND {} = '{}'".format(
        arcpy.AddFieldDelimiters(db, 'District_ID'), 681852,
        arcpy.AddFieldDelimiters(db, 'Elevator'), 'N'
    )
    i = 0
    with arcpy.da.UpdateCursor(masterDB, ['Levy', 'Elevator', 'MaxTax'], where_clause=expression) as uCursor:
        for updateRow in uCursor:
            if updateRow[0] > 68.82:
                updateRow[0] = 68.82
                # updateRow[2] = str(updateRow[0])
                #     uCursor.updateRow(updateRow)
                #  if levy is > 68.82. lower the levy to 68.82
                i += 1
    print '{} records updated'.format(i)


def findBetween68and100(db):
    expression = "{} = {}".format(arcpy.AddFieldDelimiters(db, 'District_ID'), 681852)
    levyCounter = 0
    with arcpy.da.UpdateCursor(db, ['APN', 'Levy', 'MaxTax', 'tract'], where_clause=expression) as levyCursor:
        for values in levyCursor:
            apn = values[0]
            levy = values[1]
            maxTax = values[2]
            tract = values[3]
            if 68.82 < levy < 100:
                levyCounter += 1
                print '{}:\n\t{}\t{}\t{}'.format(apn, levy, maxTax, tract)
    print levyCounter


masterDB = r'Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019'
test = """APN IN ('136110008-0', '255150012-7', '255180037-3', '255200045-1', '255180039-5', '255190017-6', '136110004-6', 
'136110005-7', '136110021-1', '136110022-2', '255150016-1', '255150017-2', '255180035-1', '255180036-2', '255180038-4', 
'136120016-8', '270070004-4', '270080017-7', '270090001-3', '270090002-4', '273174012-3', '273590011-8', '273590012-9', 
'273590013-0', '273590042-6', '273590043-7', '459030013-7', '461020025-4', '461020029-8', '461150007-0', '461150008-1', 
'461150009-2', '461150015-7', '461190041-4', '461190079-9', '476090002-8', '476090003-9', '476090004-0', '476090005-1', 
'476090006-2', '476090007-3', '476090008-4', '476090009-5', '476090010-5', '476090011-6', '480030049-6', '480040012-3', 
'480040077-2', '963060021-3', '963100003-0', '963100004-1', '964010001-7') AND District_ID = 681852"""
# fixNMaxTax_Levy(masterDB)
findBetween68and100(masterDB)
print 'done'

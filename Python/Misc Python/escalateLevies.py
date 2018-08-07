import arcpy


def escalateLevy(db, csaDict, levyAmount):
    distIDList = []
    distField = arcpy.AddFieldDelimiters(db, 'District_ID ')
    elevatorField = arcpy.AddFieldDelimiters(db, 'Elevator')
    for key in csaDict:
        distIDList.append(key)

    distIDTuples = tuple(distIDList)
    expression = "{} NOT IN {} AND {} LIKE 'Y%'".format(distField, distIDTuples, elevatorField)

    with arcpy.da.UpdateCursor(db, ['District_ID', 'Levy', 'MaxTax'], where_clause=expression) as upCursor:
        for upRow in upCursor:
            distID = upRow[0]
            levy = upRow[1]
            maxTax = upRow[2]

            if levy is None:
                levy = 0

            if distID == 681870 or distID == 681852:
                if maxTax is None:
                    levy = float(levy)
                    # maxTax = float(maxTax)
                    pDecimal = levyAmount / 100
                    levyIncreaseAmount = pDecimal * levy
                    # maxIncreaseAmount = pDecimal * maxTax
                    finalLevy = levyIncreaseAmount + levy
                    # finalMax = maxIncreaseAmount + maxTax

                    upRow[1] = round(finalLevy, 2)
                    # upRow[2] = round(finalMax, 2)
                else:
                    levy = float(levy)
                    maxTax = float(maxTax)
                    pDecimal = levyAmount / 100
                    levyIncreaseAmount = pDecimal * levy
                    maxIncreaseAmount = pDecimal * maxTax
                    finalLevy = levyIncreaseAmount + levy
                    finalMax = maxIncreaseAmount + maxTax

                    upRow[1] = round(finalLevy, 2)
                    upRow[2] = round(finalMax, 2)
            else:
                levy = float(levy)
                pDecimal = levyAmount / 100
                levyIncreaseAmount = pDecimal * levy
                finalLevy = levyIncreaseAmount + levy

                upRow[1] = round(finalLevy, 2)

            upCursor.updateRow(upRow)

    print 'done escalating levies and maxtaxes by {}'.format(levyAmount)


def levyVsMaxTax(db, levyRest):
    for key, val in levyRest.iteritems():
        distField = arcpy.AddFieldDelimiters(db, 'District_ID ')
        levyField = arcpy.AddFieldDelimiters(db, 'Levy ')
        limitExpression870 = "{} = {} AND {} > {}".format(distField, key, levyField, val)
        limitExpression852 = "{} = {} AND {} > {} AND {} < 100".format(distField, key, levyField, val, levyField)

        if key == 681870:
            with arcpy.da.UpdateCursor(db, ['District_ID', 'Levy', 'MaxTax'],
                                       where_clause=limitExpression870) as limitCursor:
                for limitRow in limitCursor:
                    if limitRow[1] > val:
                        limitRow[1] = val

                    limitCursor.updateRow(limitRow)
        else:
            with arcpy.da.UpdateCursor(db, ['District_ID', 'Levy', 'MaxTax'],
                                       where_clause=limitExpression852) as limitCursor:
                for limitRow in limitCursor:
                    if limitRow[1] > val:
                        limitRow[1] = val

                    limitCursor.updateRow(limitRow)
        print 'done reseting {} to {}'.format(key, val)


masterDB = r'Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019'
# masterDB = r'Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019_EscalateLevyTest'
notLevy = {681854: 'CSA No. 152 (City of Corona)',
           681857: 'CSA No. 152 (City of Desert Hot Springs)',
           681867: 'CSA No. 152 (City of Lake Elsinore)',
           681859: 'CSA No. 152 (City of LaQuinta)',
           681860: 'CSA No. 152 (City of Moreno Valley)',
           681861: 'CSA No. 152 (City of Murrieta)',
           681862: 'CSA No. 152 (City of Norco)',
           681864: 'CSA No. 152 (City of Palm Springs)',
           681865: 'CSA No. 152 (City of Rancho Mirage)',
           681853: 'CSA No. 152 (City of Riverside)',
           681868: 'CSA No. 152 (City of San Jacinto)',
           681869: 'CSA No. 152 (Temescal Drainage Basin)'
           }

levyLimits = {681870: 310.84, 681852: 68.82}

eMaxTax = 2.36

escalateLevy(masterDB, notLevy, eMaxTax)
levyVsMaxTax(masterDB, levyLimits)

# '681854', '681857', '681867', '681859', '681860', '681861', '681862', '681864', '681865', '681853', '681868',
# '681870', '681869', '681852'

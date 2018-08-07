import arcpy


def findOffLevies(db):
    oddNumberList = ['1', '3', '5', '7', '9']
    # findOddLevyExp = "{} LIKE '{}'".format(arcpy.AddFieldDelimiters(db, 'Levy'), '%')
    findOddLevyExp = "{} >= '{}'".format(arcpy.AddFieldDelimiters(db, 'last_edited_date'), '2018-08-1')
    with arcpy.da.UpdateCursor(db, ['APN', 'Levy'], where_clause=findOddLevyExp) as findLevyCursor:
        for values in findLevyCursor:
            apn = values[0]
            levy = values[1]
            levyNotFormatted = str(values[1])
            findDecimal = levyNotFormatted.find('.')
            decimalStr = levyNotFormatted[findDecimal:]

            levyFormatted = "{0:.2f}".format(round(values[1], 2))
            lastDecDigit = levyFormatted[-1:]

            if len(decimalStr) > 3:
                if lastDecDigit in oddNumberList:
                    levy = float(levyFormatted)
                    levy -= 0.01
                    values[1] = levy
                    print '{}:\t{}\t{}'.format(apn, levyFormatted, levy)

                    findLevyCursor.updateRow(values)
                else:
                    levy = float(levyFormatted)
                    values[1] = levy
                    print '{}:\t{}\t{}'.format(apn, levyFormatted, levy)

                    findLevyCursor.updateRow(values)
            elif lastDecDigit in oddNumberList:
                levy = float(levyFormatted)
                levy -= 0.01
                values[1] = levy
                print '{}:\t{}\t{}'.format(apn, levyFormatted, levy)

                findLevyCursor.updateRow(values)
        del findLevyCursor

        print 'Done'



master_18_19 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019"

findOffLevies(master_18_19)

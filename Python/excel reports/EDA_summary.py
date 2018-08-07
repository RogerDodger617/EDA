import re
import xlrd
import glob
import os
import csv


def sum_list(items):
    sum_numbers = 0
    for x in items:
        sum_numbers += x
    return round(sum_numbers, 2)


def removeStr(list1):
    removeIndices = []
    for i1 in range(len(list1)):
        if type(list1[i1]) is unicode:
            removeIndices.append(i1)
    distID = [i2 for j, i2 in enumerate(list1) if j not in removeIndices]
    return distID


ROOTDIR = r'D:\MillerSpatial\EDA\2017_18\Psomas\DataFiles'
wb_pattern = os.path.join(ROOTDIR, '*.xlsx')

workbooks = glob.glob(wb_pattern)

regex = re.compile(r'CSA#152')
regex152Street = re.compile(r'68-1852')

summaryList = [("Name", "District ID", "Total Records", "Levy Sum")]

for i in range(len(workbooks)):
    try:
        test = workbooks[i]
        # if regex.search(test):
        #     if regex152Street.search(test):
        #         workBook = xlrd.open_workbook(workbooks[i])
        #         sheet = workBook.sheet_by_index(0)
        #
        #         totalRows_disID = sheet.col_values(colx=2, start_rowx=1)
        #         totalRows_disID = filter(None, totalRows_disID)
        #         totalRows_disID = removeStr(totalRows_disID)
        #         totalRowsLen = len(totalRows_disID)
        #
        #         levySum = sheet.col_values(colx=7, start_rowx=1)
        #         levySum = filter(None, levySum)
        #         levySum = sum_list(levySum)
        #
        #         disID = list(set(totalRows_disID))
        #
        #         disNameList = set(sheet.col_values(colx=15, start_rowx=1))
        #         disNameList = filter(None, disNameList)
        #         disNameList = list(disNameList)
        #
        #         summaryList.append((disNameList[0], disID[0], totalRowsLen, levySum))
        # else:
        workBook = xlrd.open_workbook(workbooks[i])
        sheet = workBook.sheet_by_index(0)

        totalRows_disID = sheet.col_values(colx=2, start_rowx=1)
        totalRows_disID = filter(None, totalRows_disID)
        totalRows_disID = removeStr(totalRows_disID)
        totalRowsLen = len(totalRows_disID)

        levySum = sheet.col_values(colx=7, start_rowx=1)
        levySum = filter(None, levySum)
        levySum = sum_list(levySum)

        disID = list(set(totalRows_disID))

        disNameList = set(sheet.col_values(colx=15, start_rowx=1))
        disNameList = filter(None, disNameList)
        disNameList = list(disNameList)

        summaryList.append((disNameList[0], disID[0], totalRowsLen, levySum))

    except Exception, e:
        print str(e)
        pass

with open(r'D:\MillerSpatial\EDA\sumTest2.csv', "wb") as f:
    writer = csv.writer(f)
    writer.writerows(summaryList)
print 'done'

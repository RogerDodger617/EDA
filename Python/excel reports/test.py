# import pandas as pd
# import os
# print os.path.dirname(__file__)
# arr_xls = [os.path._getfullpathname(".\\2017_18\\Psomas\\DataFiles\\" + x) for x in os.listdir('../EDA/2017_18/Psomas/DataFiles') if x.endswith('.xlsx')]
#
# excels = [pd.ExcelFile(name) for name in arr_xls]
#
# # turn them into dataframes
# frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]
#
# # delete the first row for all frames except the first
# # i.e. remove the header row -- assumes it's the first
# frames[1:] = [df[1:] for df in frames[1:]]
#
# # concatenate them..
# combined = pd.concat(frames)
#
# # write it out
# combined.to_excel("c.xlsx", header=False, index=False)

import glob
import os
import xlrd
import csv

ROOTDIR = r'D:\MillerSpatial\EDA\2017_18\Psomas\DataFiles'
wb_pattern = os.path.join(ROOTDIR, '*.xlsx')

workbooks = glob.glob(wb_pattern)

with open(r'D:\MillerSpatial\EDA\master lists\out.csv', 'wb') as outcsv:
    writer = csv.writer(outcsv)
    for wb in workbooks:
        book_path = os.path.join(ROOTDIR, wb)
        print book_path
        book = xlrd.open_workbook(book_path)
        sheet = book.sheet_by_index(0)
        for row_num in xrange(1, sheet.nrows):
            row = sheet.row_values(row_num)
            try:
               writer.writerow(row)
            except:
                print row, row_num
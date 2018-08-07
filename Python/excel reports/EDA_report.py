import xlrd
import config
import csv


def findMissing(m, p):
    foundAPNs = []
    missingAPNList = []

    for i in range(len(m)):
        masterAPNValue = m[i].value
        for i2 in range(len(p)):
            psomasAPNValue = p[i2].value
            if masterAPNValue == psomasAPNValue:
                foundAPNs.append(str(masterAPNValue))
            else:
                if i2 + 1 == len(p):
                    if masterAPNValue in foundAPNs:
                        pass
                    else:
                        missingAPNList.append((i + 1, str(masterAPNValue)))

    return missingAPNList


def txtBuilder(missingList, header):
    txtBuilderList = [header]

    for i3 in range(len(missingList)):
        row = masterSheet.row_values(missingList[i3][0])
        txtBuilderList.append(row)

    return txtBuilderList


cfg = config.cfg

master_data = cfg['dataFile']
master_psomas = cfg['psomas']

master_xls = xlrd.open_workbook(master_data)
psomas_xls = xlrd.open_workbook(master_psomas)

masterSheet = master_xls.sheet_by_index(0)
psomasSheet = psomas_xls.sheet_by_index(0)

headers = masterSheet.row_values(0)

masterAPN = masterSheet.col(1)
del masterAPN[0]
psomasAPN = psomasSheet.col(1)
del psomasAPN[0]

missingAPNs = findMissing(masterAPN, psomasAPN)
txtList = txtBuilder(missingAPNs, headers)

with open(r'D:\MillerSpatial\EDA\test2.csv', "wb") as f:
    writer = csv.writer(f)
    writer.writerows(txtList)

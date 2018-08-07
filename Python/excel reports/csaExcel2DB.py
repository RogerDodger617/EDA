import xlrd
import arcpy


def excelToDict(excelSheet, headers):
    for nRows in range(excelSheet.nrows):
        getDisID = None
        if nRows > 3:
            rowValues = excelSheet.row_values(nRows)
            apnValues = rowValues[0]
            for findDisID in range(len(rowValues)):
                # skipping over blank lines
                if rowValues[findDisID] != '':
                    # only looking through certain cells to find the levies
                    if 0 < findDisID < 8:
                        listToDict = []
                        # getDisID refers back to the disHeader list to match up district id's in csaDict
                        getDisID = headers[findDisID]
                        levy = rowValues[findDisID]
                        # tract and elevator are hard coded
                        tract = rowValues[8]
                        elevator = rowValues[9]
                        listToDict.extend([apnValues, levy, tract, elevator])

                        # append to dict list on each levy find
                        csaDict[getDisID]['apnInfo'].append(listToDict)

excelPath = r'D:\MillerSpatial\EDA\2017_18'
docName = r'\FY 18-19 APNs cont.xlsx'
workBook = xlrd.open_workbook(excelPath + docName)
sheet = workBook.sheet_by_index(0)
tract_elevatorHeader = sheet.row_values(2)
disIDHeader = sheet.row_values(3)

csaDict = {681701: {'name': 'CSA No. 1 (Coronita Lighting)', 'apnInfo': []},
           681714: {'name': 'CSA No. 13 (North Palm Springs Lighting)', 'apnInfo': []},
           681724: {'name': 'CSA No. 22 (Lake Elsinore Lighting)', 'apnInfo': []},
           681729: {'name': 'CSA No. 27 (Cherry Valley Lighting)', 'apnInfo': []},
           681739: {'name': 'CSA No. 36 (Idyllwild Lighting,Park, & Rec.)', 'apnInfo': []},
           681747: {'name': 'CSA No. 43 (Homeland Lighting)', 'apnInfo': []},
           681756: {'name': 'CSA No. 51 (Desert Center/Lake Tamarisk Lighting, Water, Sewer)', 'apnInfo': []},
           681765: {'name': 'CSA No. 59 (Hemet Lighting)', 'apnInfo': []},
           681768: {'name': 'CSA No. 62 (Ripley Lighting, Water, Sewer)', 'apnInfo': []},
           681776: {'name': 'CSA No. 69 (Hemet Lighting)', 'apnInfo': []},
           681793: {'name': 'CSA No. 84 (Sun City Lighting)', 'apnInfo': []},
           681794: {'name': 'CSA No. 85 (Cabazon Lighting, Park & Rec.)', 'apnInfo': []},
           681796: {'name': 'CSA No. 87 (Woodcrest Lighting)', 'apnInfo': []},
           681799: {'name': 'CSA No. 89 (Perris Lighting)', 'apnInfo': []},
           681802: {'name': 'CSA No. 91 (Valle Vista Lighting)', 'apnInfo': []},
           681805: {'name': 'CSA No. 94 (SE Hemet Lighting)', 'apnInfo': []},
           681808: {'name': 'CSA No. 97 (Mecca Lighting)', 'apnInfo': []},
           681815: {'name': 'CSA No. 103 (Lighting)', 'apnInfo': []},
           681816: {'name': 'CSA No. 104 (Sky Valley Roads, Fire Protection)', 'apnInfo': []},
           681817: {'name': 'CSA No. 105 (Indio Hills Roads)', 'apnInfo': []},
           681820: {'name': 'CSA No. 108 (Minto Way Roads)', 'apnInfo': []},
           681825: {'name': 'CSA No. 113 (Woodcrest Lighting)', 'apnInfo': []},
           681712: {'name': 'CSA No. 115 (Desert Hot Springs Lighting)', 'apnInfo': []},
           681727: {'name': 'CSA No. 117 (Mead Valley Lighting)', 'apnInfo': []},
           681833: {'name': 'CSA No. 121 (Bermuda Dunes Lighting, Drainage Basin)', 'apnInfo': []},
           681834: {'name': 'CSA No. 122 (Mesa Verde Lighting, Water)', 'apnInfo': []},
           681836: {'name': 'CSA No. 124 (Warm Springs Valley Roads)', 'apnInfo': []},
           681883: {'name': 'CSA No. 126 (Highgrove Landscaping, Park & Rec.)', 'apnInfo': []},
           681885: {'name': 'CSA No. 128E (Lake Mathews Roads)', 'apnInfo': []},
           681886: {'name': 'CSA No. 128W (Lake Mathews Roads)', 'apnInfo': []},
           681789: {'name': 'CSA No. 132 (The Orchards/Lake Mathews Lighting)', 'apnInfo': []},
           681822: {'name': 'CSA No. 134 (Temescal Lighting, Landscaping, & Park)', 'apnInfo': []},
           681843: {'name': 'CSA No. 135 (Temescal Lighting)', 'apnInfo': []},
           681744: {'name': 'CSA No. 142 (Wildomar Lighting)', 'apnInfo': []},
           681823: {'name': 'CSA No. 143 (Lighting, Landscaping, Park & Rec.)', 'apnInfo': []},
           681828: {'name': 'CSA No. 143C (Silverhawk C Lighting, Park & Rec. Landscape)', 'apnInfo': []},
           681829: {'name': 'CSA No. 143D (Temecula Lighting, Park & Rec. Landscape)', 'apnInfo': []},
           681851: {'name': 'CSA No. 146 (Lakeview, Nuevo, Romoland, Homeland Street Lighting, Landscaping)', 'apnInfo': []},
           681849: {'name': 'CSA No. 149 (Wine Country Roads)', 'apnInfo': []},
           681848: {'name': 'CSA No. 149A (Wine Country Landscaping)', 'apnInfo': []},
           681870: {'name': 'CSA No. 152B (Temescal Regional Sports Facilities)', 'apnInfo': []},
           681854: {'name': 'CSA No. 152 (City of Corona)', 'apnInfo': []},
           681857: {'name': 'CSA No. 152 (City of Desert Hot Springs)', 'apnInfo': []},
           681869: {'name': 'CSA No. 152 (Temescal Drainage Basin)', 'apnInfo': []},
           681867: {'name': 'CSA No. 152 (City of Lake Elsinore)', 'apnInfo': []},
           681859: {'name': 'CSA No. 152 (City of LaQuinta)', 'apnInfo': []},
           691860: {'name': 'CSA No. 152 (City of Moreno Valley)', 'apnInfo': []},
           681861: {'name': 'CSA No. 152 (City of Murrieta)', 'apnInfo': []},
           681862: {'name': 'CSA No. 152 (City of Norco)', 'apnInfo': []},
           681864: {'name': 'CSA No. 152 (City of Palm Springs)', 'apnInfo': []},
           681865: {'name': 'CSA No. 152 (City of Rancho Mirage)', 'apnInfo': []},
           681853: {'name': 'CSA No. 152 (City of Riverside)', 'apnInfo': []},
           681868: {'name': 'CSA No. 152 (City of San Jacinto)', 'apnInfo': []},
           681852: {'name': 'CSA No. 152 (Street Sweeping)', 'apnInfo': []}
           }

# consolidating headers based on excel doc
for iFind in range(len(tract_elevatorHeader)):
    if tract_elevatorHeader[iFind] == 'Tract' or tract_elevatorHeader[iFind] == 'Escalator':
        disIDHeader[iFind] = tract_elevatorHeader[iFind]

excelToDict(sheet, disIDHeader)

for key, val in csaDict.iteritems():
    if val['apnInfo']:
        print val['apnInfo']

print workBook

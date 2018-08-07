import arcpy

arcpy.AddMessage("hi")

workSpace = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde"
walk = arcpy.da.Walk(workSpace, datatype="Table")

arcpy.AddMessage(walk)

tableList2 = None

for dirpath, dirnames, filenames in walk:
    # arcpy.AddMessage('im in the for loop :o')
    # arcpy.AddMessage(dirpath)
    # arcpy.AddMessage(dirnames)
    print (filenames)

    tableList2 = filenames

    arcpy.AddMessage(tableList2)
        
arcpy.AddMessage(tableList2)

arcpy.SetParameter(0, tableList2)

print tableList2

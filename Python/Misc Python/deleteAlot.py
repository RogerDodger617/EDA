import arcpy

master_18_19 = r"C:\Users\anfuentes\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\Connection to SQLRIAGD01.rivcoca.org (2).sde"
master_18_191 = r"Database Connections\Connection to SQLRIAGD01.rivcoca.org (2).sde\GDB_EDA.EDA.csa_master_2018_2019"
# arcpy.env.workspace = master_18_19
#
# edit = arcpy.da.Editor(master_18_19)
# edit.startEditing(False, True)
# edit.startOperation()


expression = "created_date >= '6/13/2018' AND APN In (SELECT APN FROM GDB_EDA.EDA.csa_master_2018_2019 GROUP BY APN HAVING Count(*)>3 )"

with arcpy.da.UpdateCursor(master_18_191, ["*"], where_clause=expression) as cursor:
    for delRow in cursor:
        print delRow
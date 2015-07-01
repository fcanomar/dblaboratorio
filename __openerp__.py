{
'name' : 'Bases de Datos Laboratorio',
'version' : '1.0',
'description' : """
Añade los campos necesarios para la base de datos de productos de laboratorio
""",
'author' : 'Francisco Cano Marchal',
'depends' : ['base','purchase'],
'data' : ['dblaboratorio_view.xml','laboratorio_view.xml','sequences.xml','caducidad_scheduler.xml','security/dblabo_security.xml','security/ir.model.access.csv','categories_data.xml','dblaboratorio_data.xml'],
'demo': [],
'installable' : True,
'auto_install' : False,
}




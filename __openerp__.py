{
'name' : 'Bases de Datos Laboratorio',
'version' : '1.0',
'description' : """
Añade los campos necesarios para la base de datos de productos de laboratorio
""",
'author' : 'Francisco Cano Marchal',
'depends' : ['base','purchase','administracioncm','product_expiry'],
'data' : ['security/dblabo_security.xml','security/ir.model.access.csv','dblaboratorio_view.xml','laboratorio_view.xml','sequences.xml','caducidad_scheduler.xml','categories_data.xml','dblaboratorio_data.xml'],
'demo': [],
'installable' : True,
'auto_install' : False,
}




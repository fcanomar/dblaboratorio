#!/usr/bin/env python
# -*- coding: utf-8 -*-


from openerp import models, fields, api
from datetime import date


class dblaboratorio_stock_production_lot(models.Model):
    _inherit = "stock.production.lot"
    
    x_riqueza = fields.Char("Riqueza")
    x_tipolabo = fields.Selection(related='product_id.product_tmpl_id.x_tipolabo')
    

class dblaboratorio_product_template (models.Model) :
    _inherit = "product.template"
        
    #reactivos y comunes
    default_code = fields.Char('Referencia Interna', compute='_get_nri', store=True, readonly=False)
    x_tipolabo = fields.Selection([('disolucion','Disolución'),('equipo','Equipo'),('generico','Genérico'),('materiallabo','Material de Laboratorio'),('materialref','Material de Referencia'),('patron','Patrón'),('reactivo','Reactivo')],'Clase de Producto',default='generico') 
    x_marca = fields.Many2one('dblaboratorio.marca','Fabricante', ondelete='cascade')
    x_formato = fields.Many2one('dblaboratorio.formato', 'Formato', ondelete='cascade')
    x_conservacion = fields.Many2one('dblaboratorio.conservacion', 'Conservación', ondelete='cascade',domain="[('name','=',x_espreact)]", related="x_espreact.x_conservacion", readonly=True)
    x_estado = fields.Selection([('solido','Solido'),('liquido','Liquido'),('gaseoso','Gaseoso')],'Estado', domain="[('name','=',x_espreact)]", related="x_espreact.x_estado", readonly=True)
    x_tipocodigo = fields.Selection([('ean13','EAN13'),('qweb','Qweb')],'Tipo de Codigo')
    x_qweb = fields.Char('Codigo Qweb')
    x_espreact = fields.Many2one('dblaboratorio.reactivoesp','Cumple Especificaciones',ondelete='cascade')
    
    #patrones
    x_patrongen = fields.Many2one('dblaboratorio.patrongen','Cumple Especificaciones',ondelete='cascade')
    x_estado_p = fields.Selection([('solido','Solido'),('liquido','Liquido'),('gaseoso','Gaseoso')],'Estado', related="x_patrongen.x_estado", readonly=True)
    x_conservacion_p = fields.Many2one('dblaboratorio.conservacion', 'Conservación', ondelete='cascade',domain="[('name','=',x_patrongen)]", related="x_patrongen.x_conservacion", readonly=True)
    #x_equiposcalibrar = fields.Char('Métodos a Calibrar --prueba')
    x_metodoscalibrar = fields.Many2many(related='x_patrongen.x_metodoscalibrar', string='Métodos a Calibrar',  readonly=True)
    x_equiposcalibrar = fields.Many2many(related='x_patrongen.x_equiposcalibrar', string='Equipos a Calibrar',  readonly=True)
    
    #material de laboratorio
    x_matlabogen = fields.Many2one('dblaboratorio.matlabogen','Cumple Especificaciones', ondelete='cascade')

    #disoluciones
    x_origen_tipo = fields.Selection([('disolucion','Disolución'),('patron','Patrón'),('reactivo','Reactivo')],'Tipo de Origen')
    x_origen_p = fields.Many2one('dblaboratorio.patrongen', 'Origen', ondelete='cascade')
    x_origen_r = fields.Many2one('dblaboratorio.reactivoesp', 'Origen', ondelete='cascade')
    x_origen_d = fields.Many2one('product.template', 'Origen', ondelete='cascade', domain="[('x_tipolabo','=','disolucion')]")
    x_origen = fields.Char('Origen (inicial)', compute='_get_origen_dis', readonly=True)
    
    #para equipos y material de referencia
    x_modelo = fields.Char('Modelo')
    x_nserie = fields.Char('Número de serie')
    x_ubicacion = fields.Many2one('dblaboratorio.ubicacion','Ubicación',ondelete='cascade')
    x_tipoequipo = fields.Many2one('dblaboratorio.tipoequipo','Tipo de Equipo', ondelete='cascade')
    x_responsable = fields.Many2one('res.users','Responsable',ondelete='cascade')
    x_inicioservicio = fields.Date('Inicio Servicio')
    x_serviciotecnico = fields.Many2many('res.partner',string='Servicio Técnico')
    x_calibracion = fields.Selection([('int','Interna'),('ext','Externa')],'Calibración')
    x_fcalibracion = fields.Many2one('dblaboratorio.frecuencia','Frecuencia de Calibración')
    x_verificacion = fields.Selection([('int','Interna'),('ext','Externa')], 'Verificación')
    x_fverificacion = fields.Many2one('dblaboratorio.frecuencia','Frecuencia de Verificación')
    x_mantenimiento = fields.Selection([('int','Interno'),('ext','Externo')],'Mantenimiento')
    x_fmantenimiento = fields.Many2one('dblaboratorio.frecuencia','Frecuencia de Mantenimiento')
    x_teccalibrar = fields.Char('Métodos a Calibrar')
    x_control = fields.Selection([('si','Sí'),('no','No')],'Sometido a Control')
    x_accesorios = fields.Char('Accesorios')
    x_magnitud = fields.Many2one('dblaboratorio.magnitud','Magnitud')
    x_rango = fields.Char('Rango')
    x_resolucion = fields.Char('Resolución')
    x_exactitud = fields.Char('Exactitud')
    x_nalicuotas = fields.Char('Número Alícuotas')
    x_valicuotas = fields.Char('Volumen Alícuotas')
    
    @api.multi
    def _get_origen_dis(self):
        
        for record in self:
            if (record.x_tipolabo=='disolucion'):
                
                if (record.x_origen_tipo == 'reactivo'):
                    record.x_origen = record.x_origen_r.name + " (" + record.x_origen_r.x_nri + ")"
                
                if (record.x_origen_tipo == 'patron'):
                    record.x_origen = record.x_origen_p.name + " (" + record.x_origen_p.x_nri + ")"
        
                if (record.x_origen_tipo == 'disolucion'):
                    record.x_origen = record.x_origen_d.x_origen
                    
    
    @api.onchange('x_tipolabo')
    def _set_categoria_producto(self):
        
        for record in self:
            if record.x_tipolabo == 'reactivo':
                record.categ_id = self.env['product.category'].search([('name','=','Reactivos')]);
                
            if record.x_tipolabo == 'patron':
                record.categ_id = self.env['product.category'].search([('name','=','Patrones')]);
          
            if record.x_tipolabo == 'materiallabo':
                record.categ_id = self.env['product.category'].search([('name','=','Material de Laboratorio')]);
             
            if record.x_tipolabo == 'disolucion':
                record.categ_id = self.env['product.category'].search([('name','=','Disoluciones')]);
                 
            if record.x_tipolabo == 'equipo':
                record.categ_id = self.env['product.category'].search([('name','=','Equipos')]);
                 
            if record.x_tipolabo == 'materialref':
                record.categ_id = self.env['product.category'].search([('name','=','Material de Referencia')]);
                
            if record.x_tipolabo == 'generico':
                record.categ_id = self.env['product.category'].search([('name','=','All')]);


    @api.depends('x_espreact', 'x_patrongen', 'x_matlabogen')
    def _get_nri(self):

        for record in self:
            if record.x_tipolabo == 'reactivo':
                record.default_code = record.x_espreact.x_nri;
                
            if record.x_tipolabo == 'patron':
                record.default_code = record.x_patrongen.x_nri
         
            if record.x_tipolabo == 'materiallabo':
                record.default_code = record.x_matlabogen.x_nri
            
    
    #CADUCIDADES
                         
    @api.multi
    def enviar_mensajes_caducidad_reactivos(self, dias):
        
        #Responsable tambien pertenece al grupo Usuario
        group = self.env['res.groups'].search([['full_name','=','Bases de Datos de Laboratorio / Usuario']])
        
        recordset = self.env['stock.quant'].search([['product_id.x_tipolabo','=','reactivo']])
        caducidades = recordset.mapped(lambda r : (False if r.lot_id.life_date==False else (fields.Date.from_string(r.lot_id.life_date)-date.today()).days))
        
        #solo los productos en ubicaciones internas
        i=0
        productos = []
        for item in caducidades:
            if item == dias:
                a = (recordset[i].product_id.product_tmpl_id.default_code, recordset[i].product_id.name, recordset[i].product_id.x_marca.name, recordset[i].product_id.x_formato.name , recordset[i].lot_id.name, recordset[i].location_id.name,  dias)
                if recordset[i].location_id.usage == 'internal':
                    productos.append(a)
            i = i + 1
            
        
        #only one message for each lot
        unique_productos = []
        for item in productos:
            if item not in unique_productos:
                unique_productos.append(item)
             

        for producto in unique_productos: 
            for user in group.users :   
                user.message_post(body="Las unidades del producto %s %s %s %s del lote %s almacenados en %s caducan en %s dias" % producto, subject="Caducidad Reactivo")

    
    @api.multi
    def enviar_mensajes_caducidad_patrones(self, dias):
        
        #Responsable tambien pertenece al grupo Usuario
        group = self.env['res.groups'].search([['full_name','=','Bases de Datos de Laboratorio / Usuario']])
        
        recordset = self.env['stock.quant'].search([['product_id.x_tipolabo','=','patron']])
        caducidades = recordset.mapped(lambda r : (False if r.lot_id.life_date==False else (fields.Date.from_string(r.lot_id.life_date)-date.today()).days))
        
        #solo los productos en ubicaciones internas
        i=0
        productos = []
        for item in caducidades:
            if item == dias:
                a = (recordset[i].product_id.product_tmpl_id.default_code,recordset[i].product_id.name, recordset[i].product_id.x_marca.name, recordset[i].product_id.x_formato.name , recordset[i].lot_id.name, recordset[i].location_id.name,  dias)
                if recordset[i].location_id.usage == 'internal':
                    productos.append(a)
            i = i + 1
            
        
        #only one message for each lot
        unique_productos = []
        for item in productos:
            if item not in unique_productos:
                unique_productos.append(item)
             

        for producto in unique_productos: 
            for user in group.users :   
                user.message_post(body="Las unidades del producto %s %s %s %s del lote %s almacenados en %s caducan en %s dias" % producto, subject="Caducidad Patrón")

    
    @api.multi
    def enviar_mensajes_caducidad_materialref(self, dias):
        
        #Responsable tambien pertenece al grupo Usuario
        group = self.env['res.groups'].search([['full_name','=','Bases de Datos de Laboratorio / Usuario']])
        
        recordset = self.env['stock.quant'].search([['product_id.x_tipolabo','=','materialref']])
        caducidades = recordset.mapped(lambda r : (False if r.lot_id.life_date==False else (fields.Date.from_string(r.lot_id.life_date)-date.today()).days))
        
        #solo los productos en ubicaciones internas
        i=0
        productos = []
        for item in caducidades:
            if item == dias:
                a = (recordset[i].product_id.product_tmpl_id.default_code,recordset[i].product_id.name, recordset[i].product_id.x_marca.name, recordset[i].product_id.x_formato.name , recordset[i].lot_id.name, recordset[i].location_id.name,  dias)
                if recordset[i].location_id.usage == 'internal':
                    productos.append(a)
            i = i + 1
            
        
        #only one message for each lot
        unique_productos = []
        for item in productos:
            if item not in unique_productos:
                unique_productos.append(item)
             

        for producto in unique_productos: 
            for user in group.users :   
                user.message_post(body="Las unidades del producto %s %s %s %s del lote %s almacenados en %s caducan en %s dias" % producto, subject="Caducidad Material de Referencia")

    
    @api.multi
    def enviar_mensajes_caducidad_disoluciones(self, dias):
        
        #Responsable tambien pertenece al grupo Usuario
        group = self.env['res.groups'].search([['full_name','=','Bases de Datos de Laboratorio / Usuario']])
        
        recordset = self.env['stock.quant'].search([['product_id.x_tipolabo','=','disolucion']])
        caducidades = recordset.mapped(lambda r : (False if r.lot_id.life_date==False else (fields.Date.from_string(r.lot_id.life_date)-date.today()).days))
        
        #solo los productos en ubicaciones internas
        i=0
        productos = []
        for item in caducidades:
            if item == dias:
                origen = (recordset[i].product_id.x_origen_p.name if recordset[i].product_id.x_origen_p.name else recordset[i].product_id.x_origen_p.name) 
                a = (recordset[i].product_id.product_tmpl_id.default_code,recordset[i].product_id.name, origen, dias)
                if recordset[i].location_id.usage == 'internal':
                    productos.append(a)
            i = i + 1
            
        
        #only one message for each lot
        unique_productos = []
        for item in productos:
            if item not in unique_productos:
                unique_productos.append(item)
             

        for producto in unique_productos: 
            for user in group.users :   
                user.message_post(body="La disolucion %s %s de origen %s caduca en %s dias" % producto, subject="Caducidad Disolución")
                
      
    #para testeo con boton 'Run Caducidad'        
    @api.multi
    def action_run_caducidad(self):
        self.enviar_mensajes_caducidad_reactivos(30)
        self.enviar_mensajes_caducidad_reactivos(7)
        self.enviar_mensajes_caducidad_reactivos(1)
        
        self.enviar_mensajes_caducidad_patrones(30)
        self.enviar_mensajes_caducidad_patrones(7)
        self.enviar_mensajes_caducidad_patrones(1)
        
        self.enviar_mensajes_caducidad_materialref(30)
        self.enviar_mensajes_caducidad_materialref(7)
        self.enviar_mensajes_caducidad_materialref(1)
        
        self.enviar_mensajes_caducidad_disoluciones(30)
        self.enviar_mensajes_caducidad_disoluciones(7)
        self.enviar_mensajes_caducidad_disoluciones(1)
              
    #aquí se puede cambiar cuándo se envían avisos de caducidades
    @api.model
    def run_caducidad_scheduler(self):
        self.enviar_mensajes_caducidad_reactivos(30)
        self.enviar_mensajes_caducidad_reactivos(7)
        self.enviar_mensajes_caducidad_reactivos(1)
        
        self.enviar_mensajes_caducidad_patrones(30)
        self.enviar_mensajes_caducidad_patrones(7)
        self.enviar_mensajes_caducidad_patrones(1)
        
        self.enviar_mensajes_caducidad_materialref(30)
        self.enviar_mensajes_caducidad_materialref(7)
        self.enviar_mensajes_caducidad_materialref(1)
        
        self.enviar_mensajes_caducidad_disoluciones(30)
        self.enviar_mensajes_caducidad_disoluciones(7)
        self.enviar_mensajes_caducidad_disoluciones(1)
           
   
#     @api.multi
#     def name_get(self):
#         #return_val = super(especificaciones_cm, self).name_get()
#         res = []
#  
#         for item in self:
#             name = self.name + ' %s %s' % (self['x_marca'], self['x_formato'])
#             res.append((item.id, (name)))
#              
#         return res

    @api.multi
    def name_get(self):
        
        res=[]
        
        for item in self:
            
            if (item.x_tipolabo == "disolucion"):
            
                name = item.name + ' de ' + item.x_origen
                res.append((item.id,(name)))
            
        return res
            


class dblaboratorio_product_product(models.Model) :
    _inherit = "product.product"

# Para rellenar NRI en las variantes de producto
#    
#     default_code = fields.Char('Referencia Interna', compute='_get_nri', store=True, readonly=False)
#     
#     @api.depends('product_tmpl_id')
#     def _get_nri(self):
# 
#         for record in self:
#             if record.product_tmpl_id.x_tipolabo == 'reactivo':
#                 record.default_code = record.product_tmpl_id.x_espreact.x_nri;
#                 
#             if record.product_tmpl_id.x_tipolabo == 'patron':
#                 record.default_code = record.product_tmpl_id.x_patrongen.x_nri
#          
#             if record.product_tmpl_id.x_tipolabo == 'materiallabo':
#                 record.default_code = record.product_tmpl_id.x_matlabogen.x_nri
    
    @api.multi
    def name_get(self):
 
        res = []
     
        for item in self:
            
            if item.default_code: 
                code = '[%s] ' %(item.default_code)
            else:
                code = ''
                
            if item.x_marca.name:
                marca = item.x_marca.name
            else:
                marca = ''
                
            if item.x_formato.name:
                formato = item.x_formato.name
            else:
                formato = ''
            
            
            
            name = '%s%s %s %s' % (code, item.name, marca, formato)
            res.append((item.id, (name)))
             
        return res

    
class marca_reactivo(models.Model) :
    _name = 'dblaboratorio.marca'

    name = fields.Char('Marca')
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', "El fabricante que pretende crear ya existe"),]
    

class formato_reactivo(models.Model) :
    _name = 'dblaboratorio.formato'

    name = fields.Char('Formato')
  
    
class conservacion_reactivo(models.Model) :
    _name = 'dblaboratorio.conservacion'

    name = fields.Char('Conservacion')
    

class ubicacion_equipos(models.Model) :
    _name = 'dblaboratorio.ubicacion'

    name = fields.Char('Ubicación')


class tipo_equipo(models.Model) :
    _name = 'dblaboratorio.tipoequipo'

    name = fields.Char('Tipo de Equipo')
    
    
class frecuencia_equipo(models.Model) :
    _name = 'dblaboratorio.frecuencia'

    name = fields.Char('Frecuencia')
    
    
class magnitud_equipo(models.Model) :
    _name = 'dblaboratorio.magnitud'

    name = fields.Char('Magnitud')
    
    
class metodos_calibrar(models.Model):
    _name = 'dblaboratorio.metodo'
    
    name = fields.Char('Nombre')
    #x_patron_ids = fields.Many2many("dblaboratorio.patrongen")
  
  
class especificaciones_cm(models.Model):
    _name = 'dblaboratorio.reactivoesp' 
    
    name = fields.Char('Reactivo')
    x_nri = fields.Char('NRI')
    x_conservacion = fields.Many2one('dblaboratorio.conservacion', 'Conservacion', ondelete='cascade')
    x_estado = fields.Selection([('solido','Solido'),('liquido','Liquido'),('gaseoso','Gaseoso')],'Estado')
    x_observaciones = fields.Text('Observaciones')
    
    _sql_constraints = [
        ('nri_unique', 'UNIQUE(x_nri)', "El NRI que pretende asignar ya existe."),]
    
    @api.multi
    def name_get(self):
        #return_val = super(especificaciones_cm, self).name_get()
        res = []

        for item in self:
            name = '[%s] ' % (item['x_nri'],) + item.name
            res.append((item.id, (name)))
            
        return res
    
    
class patrones_generica(models.Model):
    _name = 'dblaboratorio.patrongen'
    
    name = fields.Char('Patrón')
    x_nri = fields.Char('NRI')
    x_estado = fields.Selection([('solido','Solido'),('liquido','Liquido'),('gaseoso','Gaseoso')],'Estado')
    x_conservacion = fields.Many2one('dblaboratorio.conservacion', 'Conservación', ondelete='cascade')
    x_metodoscalibrar = fields.Many2many('dblaboratorio.metodo', 'patron_metodo_rel', 'patron_id','metodo_id', 'Métodos a Calibrar')
    x_equiposcalibrar = fields.Many2many('product.template', 'patron_equipo_rel', 'patron_id','equipo_id', 'Equipos a Calibrar')
    x_observaciones = fields.Text('Observaciones')
    
    _sql_constraints = [
    ('nri_unique', 'UNIQUE(x_nri)', "El NRI que pretende asignar ya existe."),]
    
    
    @api.multi
    def name_get(self):
        #return_val = super(especificaciones_cm, self).name_get()
        res = []

        for patrongen in self:
            name = '[%s] ' % (patrongen['x_nri'],) + patrongen.name
            res.append((patrongen.id, (name)))
            
        return res
    

class materiallaboratorio_generica(models.Model):
    _name = 'dblaboratorio.matlabogen'
    
    name = fields.Char('Patrón')
    x_nri = fields.Char('NRI')
    x_observaciones = fields.Text('Observaciones')
    
    _sql_constraints = [
    ('nri_unique', 'UNIQUE(x_nri)', "El NRI que pretende asignar ya existe."),]
    
    
    @api.multi
    def name_get(self):
        #return_val = super(especificaciones_cm, self).name_get()
        res = []

        for item in self:
            name = '[%s] ' % (item['x_nri'],) + item.name
            res.append((item.id, (name)))
            
        return res
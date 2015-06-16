#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import openerp
from openerp import models, fields, api
from datetime import date



class dblaboratorio_product_template (models.Model) :
    _inherit = "product.template"
    
 
    @api.multi
    def enviar_mensajes_caducidad_reactivos(self, dias):
        
        #Responsable tambien pertenece al grupo Usuario
        group = self.env['res.groups'].search([['full_name','=','Bases de Datos de Laboratorio / Usuario']])
        
        recordset = self.env['stock.quant'].search([['product_id.x_tipolabo','=','reactivo']])
        caducidades = recordset.mapped(lambda r : (fields.Date.from_string(r.lot_id.life_date)-date.today()).days)

        i=0
        productos = []
        for item in caducidades:
            if item == dias:
                a = (recordset[i].product_id.name, recordset[i].product_id.x_marca.name, recordset[i].product_id.x_formato.name , recordset[i].lot_id.name, recordset[i].location_id.name,  dias)
                productos.append(a)
            i = i + 1
            
        
        #only one message for each lot
        unique_productos = []
        for item in productos:
            if item not in unique_productos:
                unique_productos.append(item)
                

        for producto in unique_productos: 
            for user in group.users :   
                user.message_post(body="Los articulos del producto %s %s %s del lote %s almacenados en %s caducan en %s dias" % producto, subject="Caducidad Reactivo")

      
    #para testeo con boton 'Run Caducidad'        
    @api.multi
    def action_run_caducidad(self):
        self.enviar_mensajes_caducidad_reactivos(30)
        self.enviar_mensajes_caducidad_reactivos(7)
        self.enviar_mensajes_caducidad_reactivos(1)
              
    
    @api.model
    def run_caducidad_scheduler(self):
        self.enviar_mensajes_caducidad_reactivos(30)
        self.enviar_mensajes_caducidad_reactivos(7)
        self.enviar_mensajes_caducidad_reactivos(1)
        

    #reactivos y comunes
    default_code = fields.Char('Referencia Interna', compute='_get_nri', store=True)
    x_tipolabo = fields.Selection([('reactivo','Reactivo'),('patron','Patrón'),('materiallabo','Material de Laboratorio'),('disolucion','Disolución'),('equipo','Equipo'),('materialref','Material de Referencia'),('generico','Genérico')],'Clase de Producto',default='generico') 
    x_marca = fields.Many2one('dblaboratorio.marca','Fabricante', ondelete='cascade')
    x_formato = fields.Many2one('dblaboratorio.formato', 'Formato', ondelete='cascade')
    x_conservacion = fields.Many2one('dblaboratorio.conservacion', 'Conservación', ondelete='cascade',domain="[('name','=',x_espreact)]", related="x_espreact.x_conservacion", readonly=True)
    x_estado = fields.Selection([('solido','Solido'),('liquido','Liquido'),('gaseoso','Gaseoso')],'Estado', domain="[('name','=',x_espreact)]", related="x_espreact.x_estado", readonly=True)
    x_tipocodigo = fields.Selection([('ean13','EAN13'),('qweb','Qweb')],'Tipo de Codigo')
    x_qweb = fields.Char('Codigo Qweb')
    x_espreact = fields.Many2one('dblaboratorio.reactivoesp','Cumple Especificaciones',ondelete='cascade')

    x_estabilidad = fields.Many2one('dblaboratorio.estabilidad','Estabilidad',ondelete='cascade')
    x_origen = fields.Many2one('dblaboratorio.origen','Origen',ondelete='cascade')
    
    #patrones
    x_patrongen = fields.Many2one('dblaboratorio.patrongen','Cumple Especificaciones',ondelete='cascade')
    x_estado_p = fields.Selection([('solido','Solido'),('liquido','Liquido'),('gaseoso','Gaseoso')],'Estado', related="x_patrongen.x_estado", readonly=True)
    x_conservacion_p = fields.Many2one('dblaboratorio.conservacion', 'Conservación', ondelete='cascade',domain="[('name','=',x_patrongen)]", related="x_patrongen.x_conservacion", readonly=True)
    x_equiposcalibrar = fields.Char('Equipos/Técnicas a Calibrar', related='x_patrongen.x_equiposcalibrar', readonly=True)
    x_nri_p = fields.Char('NRI', related='x_patrongen.x_nri', readonly=True)
    
    #material de laboratorio
    x_matlabogen = fields.Many2one('dblaboratorio.matlabogen','Cumple Especificaciones', ondelete='cascade')

    
    
    #para equipos y material de referencia
    x_modelo = fields.Char('Modelo')
    x_nserie = fields.Char('Número de serie')
    x_ubicacion = fields.Many2one('dblaboratorio.ubicacion','Ubicación',ondelete='cascade')
    x_tipoequipo = fields.Char('Tipo de Equipo')
    x_responsable = fields.Many2one('res.users','Responsable',ondelete='cascade')
    x_inicioservicio = fields.Date('Inicio Servicio')
    x_serviciotecnico = fields.Char('Servicio Técnico')
    x_teccalibrar = fields.Char('Técnica a Calibrar')
    x_control = fields.Selection([('si','Sí'),('no','No')],'Sometido a Control')
    x_accesorios = fields.Char('Accesorios')
    x_datostecnicos = fields.Char('Datos Técnicos')
    x_alicuotas = fields.Char('Alícuotas')
    

    @api.depends('x_espreact', 'x_patrongen', 'x_matlabogen')
    def _get_nri(self):

        for record in self:
            if record.x_tipolabo == 'reactivo':
                record.default_code = self.x_espreact.x_nri;
                
            if record.x_tipolabo == 'patron':
                record.default_code = self.x_patrongen.x_nri
         
            if record.x_tipolabo == 'materiallabo':
                record.default_code = self.x_matlabogen.x_nri
         
 


class calidad_cm(models.Model) :
    _name = 'dblaboratorio.calidadcm'

    name = fields.Char('Calidad CM')
    x_eqespec = fields.One2many('dblaboratorio.calidadesmarca', 'x_calidadfab_id', string='Calidad Fabricante')
    x_marca = fields.Many2one(string='Fabricante', related='x_eqespec.x_marca')


    _sql_constraints = [
    ('name_unique', 'UNIQUE(name)', "La calidad que pretende crear ya existe"),]


class calidades_marca(models.Model) :
    _name = 'dblaboratorio.calidadesmarca'

    name = fields.Char('Calidad Fabricante')
    x_calidadfab_id = fields.Many2one('dblaboratorio.calidadcm','Calidad Fabricante ID', ondelete='cascade', copy=True)
    x_marca = fields.Many2one('dblaboratorio.marca','Fabricante', ondelete='cascade', copy=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name,x_marca)', "La calidad que pretende crear ya existe para dicho fabricante"),]
 
    
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
    

class variables_materiallabo(models.Model) :
    _name = 'dblaboratorio.variables'

    name = fields.Char('Variables')  
      

class estabilidad_disoluciones(models.Model) :
    _name = 'dblaboratorio.estabilidad'

    name = fields.Char('Estabilidad')  
    
 
class origen_disoluciones(models.Model) :
    _name = 'dblaboratorio.origen'

    name = fields.Char('Origen') 
     

class ubicacion_equipos(models.Model) :
    _name = 'dblaboratorio.ubicacion'

    name = fields.Char('Ubicación')   
        
    
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

        for reactivoesp in self:
            name = '[%s] ' % (self['x_nri'],) + self.name
            res.append((reactivoesp.id, (name)))
            
        return res
    
    
class patrones_generica(models.Model):
    _name = 'dblaboratorio.patrongen'
    
    name = fields.Char('Patrón')
    x_nri = fields.Char('NRI')
    x_estado = fields.Selection([('solido','Solido'),('liquido','Liquido'),('gaseoso','Gaseoso')],'Estado')
    x_conservacion = fields.Many2one('dblaboratorio.conservacion', 'Conservación', ondelete='cascade')
    x_equiposcalibrar = fields.Char('Equipos a Calibrar')
    x_observaciones = fields.Text('Observaciones')
    
    _sql_constraints = [
    ('nri_unique', 'UNIQUE(x_nri)', "El NRI que pretende asignar ya existe."),]
    
    
    @api.multi
    def name_get(self):
        #return_val = super(especificaciones_cm, self).name_get()
        res = []

        for patrongen in self:
            name = '[%s] ' % (self['x_nri'],) + self.name
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
            name = '[%s] ' % (self['x_nri'],) + self.name
            res.append((item.id, (name)))
            
        return res
    

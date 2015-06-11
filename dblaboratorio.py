#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import openerp
from openerp import models, fields, api
from datetime import date



class dblaboratorio_reactivo_quant (models.Model):
    _inherit = "stock.quant"
    
    x_caducidad = fields.Date('Fecha de Caducidad')
    
    

class dblaboratorio_product_template (models.Model) :
    _inherit = "product.template"
    
 
    @api.multi
    def enviar_mensajes_caducidad_reactivos(self, dias):
        
        #Responsable tambien pertenece al grupo Usuario
        group = self.env['res.groups'].search([['full_name','=','Bases de Datos de Laboratorio / Usuario']])
        recordset = self.env['stock.quant'].browse([['product_id.x_tipolabo','=','reactivo']])

#         for record in recordset:
#             if record.lot_id.life_date == dias:
#                 record.message_post(body="Alguna unidad de este producto caduca en %s dias" % dias,subject="Caducidad Reactivo")
#                 for user in group.users :
#                     user.message_post(body="Alguna unidad del producto %s %s caduca en %s dias" % (record.x_codigo, record.name, dias),subject="Caducidad Reactivo")
   
    @api.multi
    def action_run_caducidad(self):
        self.enviar_mensajes_caducidad_reactivos(30)
        self.enviar_mensajes_caducidad_reactivos(7)
        self.enviar_mensajes_caducidad_reactivos(1)
          
    @api.multi
    def action_get_codigo_reactivo(self):
        #self.enviar_mensajes_caducidad_reactivos()
        self.default_code = self._get_codigo()
    
    @api.multi
    def _get_codigo(self):
        #if self.x_tipolabo == 'reactivo':
            #print seq
            return self.env['ir.sequence'].next_by_code('react')
              
    
    @api.model
    def run_caducidad_scheduler(self):
        self.enviar_mensajes_caducidad_reactivos(30)
        self.enviar_mensajes_caducidad_reactivos(7)
        self.enviar_mensajes_caducidad_reactivos(1)
        

    
    x_tipolabo = fields.Selection([('reactivo','Reactivo'),('materiallabo','Material de Laboratorio'),('materialrefe','Material de Referencia'),('patron','Patron'),('equipo','Equipo'),('generico','Genérico')],'Clase de Producto',default='generico') 
    x_marca = fields.Many2one('dblaboratorio.marca','Marca', ondelete='cascade')
    x_calidadfabr = fields.Many2one('dblaboratorio.calidadesmarca','Calidad Fabricante', ondelete='cascade', domain="[('x_marca','=',x_marca)]")
    x_calidadcm = fields.Many2one('dblaboratorio.calidadcm','Cumple Especificaciones CM', ondelete='cascade', domain="[('x_eqespec','=',x_calidadfabr),('x_marca','=',x_marca)]") 
    x_formato = fields.Many2one('dblaboratorio.formato', 'Formato', ondelete='cascade')
    x_conservacion = fields.Many2one('dblaboratorio.conservacion', 'Conservacion', ondelete='cascade',domain="[('name','=',x_espreact)]", related="x_espreact.x_conservacion", readonly=True)
    x_caducidad = fields.Date('Fecha de Caducidad')
    x_today = fields.Date('Today', compute='_get_today')
    x_time = fields.Char('Time', compute='_get_time')
    x_trestante = fields.Integer('Caducidad en Meses', compute='_get_trestante')
    x_daysrestante = fields.Integer('Caducidad en Dias', compute='_get_daysrestante')
    x_estado = fields.Selection([('solido','Solido'),('liquido','Liquido'),('gaseoso','Gaseoso')],'Estado', domain="[('name','=',x_espreact)]", related="x_espreact.x_estado", readonly=True)
    x_tipocodigo = fields.Selection([('ean13','EAN13'),('qweb','Qweb')],'Tipo de Codigo')
    x_qweb = fields.Char('Codigo Qweb')
    x_espreact = fields.Many2one('dblaboratorio.reactivoesp','Cumple Especificaciones',ondelete='cascade')
    x_nri = fields.Char('NRI', related='x_espreact.x_nri', readonly=True)
    #x_secuenciaprod = fields.Many2one('ir.sequence','Secuencia producto', ondelete='cascade')
    #x_codigo = fields.Char('Referencia de Laboratorio')
    
    #material de referencia
    
   
   
    @api.one
    def _get_today(self):
        self.x_today = date.today()
    
    @api.one
    def _get_time(self):
        self.x_time = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')
        #print('hora!')
     
    @api.depends('x_caducidad','x_today')
    def _get_trestante(self):
        for record in self:
            days = record.x_caducidad and (fields.Date.from_string(record.x_caducidad) - fields.Date.from_string(fields.Date.today())).days
            record.x_trestante = days/30    
                  
    @api.depends('x_caducidad','x_today')
    def _get_daysrestante(self):
        for record in self:
            days = record.x_caducidad and (fields.Date.from_string(record.x_caducidad) - fields.Date.from_string(fields.Date.today())).days
            record.x_daysrestante = days 

    _sql_constraints = [
    ('codigo_unico','UNIQUE(x_codigo)',"La referencia que pretende utilizar pertenece a un producto ya existente."),]       


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
    

    

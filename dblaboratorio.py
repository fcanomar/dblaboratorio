import datetime

import openerp
from openerp import models, fields, api
from datetime import date

class dblaboratorio_product_template (models.Model) :
    _inherit = "product.template"
    
    
    @api.onchange('x_tipolabo')
    def _get_codigo(self):
        #if self.x_tipolabo == 'reactivo':
            #print seq
            return self.env['ir.sequence'].get('react')  
    
    
    x_tipolabo = fields.Selection([('reactivo','Reactivo'),('materiallabo','Material de Laboratorio'),('materialrefe','Material de Referencia'),('equipo','Equipo')],'Clase de Producto') 
    x_marca = fields.Many2one('dblaboratorio.marca','Marca', ondelete='cascade')
    x_calidadfabr = fields.Many2one('dblaboratorio.calidadesmarca','Calidad Fabricante', ondelete='cascade', domain="[('x_marca','=',x_marca)]")
    x_calidadcm = fields.Many2one('dblaboratorio.calidadcm','Cumple Especificaciones', ondelete='cascade', domain="[('x_eqespec','=',x_calidadfabr),('x_marca','=',x_marca)]") 
    x_formato = fields.Many2one('dblaboratorio.formato', 'Formato', ondelete='cascade')
    x_conservacion = fields.Many2one('dblaboratorio.conservacion', 'Conservacion', ondelete='cascade')
    x_caducidad = fields.Date('Fecha de Caducidad')
    x_today = fields.Date('Today', compute='_get_today')
    x_trestante = fields.Integer('Caducidad en Meses', compute='_get_trestante')
    x_daysrestante = fields.Integer('Caducidad en Dias', compute='_get_daysrestante')
    x_estado = fields.Selection([('solido','Solido'),('liquido','Liquido'),('gaseoso','Gaseoso')],'Estado')
    x_tipocodigo = fields.Selection([('ean13','EAN13'),('qweb','Qweb')],'Tipo de Codigo')
    x_qweb = fields.Char('Codigo Qweb')
    x_secuenciaprod = fields.Many2one('ir.sequence','Secuencia producto', ondelete='cascade')
    x_codigo = fields.Char('Referencia de Laboratorio', default=_get_codigo)
   
   
    #para asegurar que x_trestante esta actualizado segun vayamos avanzando en el tiempo
    @api.one
    def _get_today(self):
        self.x_today = date.today()
     
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

    @api.onchange('x_caducidad')
    def onchange_warning_caducidad(self):
    
        titulo = 'titulo de ejemplo'
        mensaje = 'mensaje de ejemplo'
        warning = {
                'title': titulo,
                'message': mensaje,
        }
        
        return {'value':{},'warning':warning}


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
    

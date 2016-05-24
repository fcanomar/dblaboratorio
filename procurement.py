#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openerp import models, api, fields

class dblaboratorio_procurement_order (models.Model) :
    _inherit = "procurement.order"
    
    @api.multi
    @api.depends('product_id.x_tipolabo')
    def _get_procurement_location(self):
        
        if self.product_id.x_tipolabo == 'disolucion':
            self.location_id = self.env['stock.location'].search([('name','=','Laboratorio')]);
        

    location_id = fields.Many2one('stock.location', 'Procurement Location', compute=_get_procurement_location)
#    product_id = fields.Many2one('product.product', 'Product', required=True, states={'confirmed': [('readonly', False)]}, readonly=True, default='_get_procurement_location'),
    

        
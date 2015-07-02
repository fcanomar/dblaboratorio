#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openerp import models, api, fields

class dblaboratorio_procurement_order (models.Model) :
    _inherit = "procurement.order"
    
    @api.onchange('product_qty')
    def _get_procurement_location(self):
        
        if self.product_id.x_tipolabo == 'disolucion':
            self.location_id = self.env['stock.location'].search([('name','=','Laboratorio')]);
        
    
#    product_id = fields.Many2one('product.product', 'Product', required=True, states={'confirmed': [('readonly', False)]}, readonly=True, default='_get_procurement_location'),
    

        
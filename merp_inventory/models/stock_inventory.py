# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models, _


class Inventory(models.Model):
    _inherit = "stock.inventory"
    _description = "Inventory"

    state = fields.Selection(selection_add=[
        ('ready', 'Waiting for Validation')
    ])

    @api.multi
    def finish_inventory(self):
        self.write({'state': 'ready'})
        return True

    @api.multi
    def return_inventory(self):
        self.write({'state': 'confirm'})
        return True

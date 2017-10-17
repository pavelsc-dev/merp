# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models, _


class Inventory(models.Model):
    _inherit = "stock.inventory"

    def __init__(self, pool, cr):
        init_res = super(Inventory, self).__init__(pool, cr)
        selection_add = ('ready', 'Waiting for Validation')
        if selection_add not in self.INVENTORY_STATE_SELECTION:
            # add new state 'ready' before 'done'
            type(self).INVENTORY_STATE_SELECTION.insert(-1, selection_add)
        return init_res

    @api.multi
    def finish_inventory(self):
        self.write({'state': 'ready'})
        return True

    @api.multi
    def return_inventory(self):
        self.write({'state': 'confirm'})
        return True

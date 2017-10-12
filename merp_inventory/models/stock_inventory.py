# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Inventory(models.Model):
    _inherit = "stock.inventory"
    _description = "Inventory"

    state = fields.Selection(selection_add=[
        ('ready', 'Waiting for Validation')
    ])

    validate_inventory_adjustments = fields.Boolean(
        compute='_compute_merp_permissions', store=False,
    )

    @api.multi
    def _compute_merp_permissions(self):
        self.validate_inventory_adjustments = \
            self.env.user.validate_inventory_adjustments

    @api.multi
    def finish_inventory(self):
        self.write({'state': 'ready'})
        return True

    @api.multi
    def return_inventory(self):
        self.write({'state': 'confirm'})
        return True

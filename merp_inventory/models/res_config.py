# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class StockConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_inventory_location = fields.Many2one(
        comodel_name='stock.location',
        related='company_id.default_inventory_location',
    )

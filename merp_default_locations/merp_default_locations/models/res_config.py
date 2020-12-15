# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models, fields


class StockConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    inventory_location = fields.Many2one('stock.location',
                                         string='Default Inventory Location',
                                         readonly=False,
                                         related='company_id.stock_inventory_location')

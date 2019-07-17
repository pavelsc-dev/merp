# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class StockChangeQtyMerp(models.TransientModel):
    _inherit = 'stock.change.product.qty'

    @api.model
    def default_get(self, fields):

        res = super(StockChangeQtyMerp, self).default_get(fields)
        if 'location_id' in fields:

            default_location_id = self.env.user.default_inventory_location.id \
                if self.env.user.default_inventory_location else False

            if not default_location_id:
                default_location_id = self.env.user.company_id.default_inventory_location.id \
                    if self.env.user.company_id.default_inventory_location.id else False

            if default_location_id:
                res['location_id'] = default_location_id

        return res

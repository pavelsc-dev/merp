# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductBarcodeMulti(models.Model):
    _name = 'product.barcode.multi'
    _description = 'Product Barcode Multi'

    name = fields.Char('Barcode')
    product_id = fields.Many2one(
        'product.product', 
        string='Product', 
        required=True,
        ondelete="cascade",
    )

    @api.constrains('name')
    def _check_empty_name(self):
        for rec in self:
            if not rec.name:
                raise ValidationError("Additional barcode can't be empty")

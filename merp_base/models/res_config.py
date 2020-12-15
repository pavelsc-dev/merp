# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models, fields, api
from odoo import http

import logging
_logger = logging.getLogger(__name__)


class StockConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_merp_outgoing_routing = fields.Boolean(
        string='Outgoing Routing'
    )

    module_merp_custom_access_rights = fields.Boolean(
        string='Custom Access Rights',
    )

    module_merp_picking_wave = fields.Boolean(
        string='Picking Wave',
    )

    module_merp_picking_products_skip = fields.Boolean(
        string='Smart Skip of Products',
    )

    module_merp_instant_move = fields.Boolean(
        string='Instant Move',
    )

    module_merp_custom_logotype = fields.Boolean(
        string='Use Custom Logo',
    )

    merp_version = fields.Char(
        string='Ventor/mERP Version',
        compute='_compute_merp_version',
        store=False,
    )

    module_merp_default_locations = fields.Boolean(
        string='Use Advanced Locations',
    )

    inventory_location = fields.Many2one(
        'stock.location',
        string='Default Inventory Location',
        readonly=False,
        related='company_id.stock_inventory_location'
    )

    @api.depends('company_id')
    def _compute_merp_version(self):
        manifest = http.addons_manifest.get('merp_base', None)
        version = manifest['version'].split('.')
        self.merp_version = '.'.join(version[-3:])

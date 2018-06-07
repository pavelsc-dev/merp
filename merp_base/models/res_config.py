from openerp import models, fields, api
from odoo import http


class StockConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    module_merp_outgoing_routing = fields.Boolean(
        'Add Outgoing Routing strategy options (sort locations)')

    module_merp_custom_access_rights = fields.Boolean(
        'Enable Custom Access Rights for Ventor App')

    module_merp_receiving_wave_access_rights = fields.Boolean(
        'Enable Receiving Wave Access Rights for Ventor App')
    module_merp_receiving_wave = fields.Boolean('Enable Receiving Wave')

    module_merp_picking_wave_access_rights = fields.Boolean(
        'Enable Picking Wave Rights for Ventor App')
    module_merp_picking_wave = fields.Boolean('Enable Picking Wave')

    module_merp_picking_products_skip = fields.Boolean(
        'Allow smart skip of products in pickings and picking waves')

    module_merp_instant_move = fields.Boolean(
        'Allow add more items automatically via Ventor App')

    module_merp_inventory = fields.Boolean(
        'Advanced Ventor/mERP Inventory Improvements')

    module_merp_custom_logotype = fields.Boolean(
        'Use Custom Logo')

    @api.depends('company_id')
    def _compute_merp_version(self):
        manifest = http.addons_manifest.get('merp_base', None)
        version = manifest['version'].split('.')
        return '.'.join(version[-3:])

    merp_version = fields.Char(string='Ventor/mERP Version',
        compute='_compute_merp_version', store=False,
        default=lambda self: self._compute_merp_version())

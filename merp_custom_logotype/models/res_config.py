from openerp import models, fields, api
from odoo import http


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    module_merp_custom_logotype = fields.Boolean(
        'Use Custom Logo')

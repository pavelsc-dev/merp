from openerp import models, fields, api, _
from openerp.exceptions import Warning
import base64
import struct
import logging

_logger = logging.getLogger(__name__)

LOGOTYPE_W = 500
LOGOTYPE_H = 500


class StockConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    merp_logotype_file = fields.Binary('mERP logotype file')
    merp_logotype_name = fields.Char('mERP logotype name')

    @api.model
    def get_default_merp_logotype(self, fields):
        conf = self.env['merp.config'].sudo()
        logo = conf.get_param('logo.file', default=None)
        name = conf.get_param('logo.name', default=None)
        return {'merp_logotype_file': logo or '',
                'merp_logotype_name': name or ''}

    @api.multi
    def set_merp_logotype(self):
        conf = self.env['merp.config'].sudo()
        for record in self:
            self._validate_merp_logotype(record)
            conf.set_param('logo.file', record.merp_logotype_file or '')
            conf.set_param('logo.name', record.merp_logotype_name or '')

    def _validate_merp_logotype(self, record):
        if not record.merp_logotype_file:
            return False

        dat = base64.decodestring(record.merp_logotype_file)
        png = (dat[:8] == '\211PNG\r\n\032\n' and (dat[12:16] == 'IHDR'))
        if not png:
            raise Warning(_('Apparently, the logotype is not a .png file.'))
        w, h = struct.unpack('>LL', dat[16:24])
        if int(w) < LOGOTYPE_W or int (h) < LOGOTYPE_H:
            raise Warning(_('The logotype can\'t be less than %sx%s px.') \
                % (LOGOTYPE_W, LOGOTYPE_H))

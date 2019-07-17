# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase


class TestCheckDefaultLocation(TransactionCase):

    def setUp(self):
        super(TestCheckDefaultLocation, self).setUp()
        self.location = self.env['stock.location'].create({
            'name': 'test_location'
        })
        self.user = self.env['res.users'].create({
            'name': 'test_user',
            'login': 'test_user',
            'email': 'test.user@email.com'
        })
        self.ventor_worker = self.env.ref('merp_custom_access_rights.ventor_role_wh_worker')
        self.ventor_worker.write({'users': [(4, self.user.id)]})
        self.inventory_manager = self.env.ref('stock.group_stock_manager')
        self.inventory_manager.write({'users': [(4, self.user.id)]})
        self.administration_settings = self.env.ref('base.group_system')
        self.administration_settings.write({'users': [(4, self.user.id)]})
        self.company = self.env['res.company'].create({
            'name': 'test_company',
            'default_inventory_location': self.location.id
        })
        self.product = self.env['product.template'].create({
            'name': 'new_product'
        })

    def test_check_default_inventory_location(self):
        self.user.write({
            'company_id': self.company.id,
            'company_ids': [(4, self.company.id)]
        })
        res = self.env['stock.change.product.qty'].sudo(self.user.id).default_get(['location_id'])
        self.assertEqual(self.location.id, res.get('location_id'))
